#!/usr/bin/env python3
"""Compute account-local post metrics; does not mix raw performance across platforms."""
import argparse
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


def num(value):
    try:
        if value is None or isinstance(value, bool):
            return None
        result = float(value)
        return result if math.isfinite(result) and result >= 0 else None
    except (TypeError, ValueError):
        return None


def enrich(rows):
    by_author_views = defaultdict(list)
    by_author_likes = defaultdict(list)
    for row in rows:
        views = num(row.get("views"))
        likes = num(row.get("likes"))
        key = (row.get("platform"), row.get("author_id") or row.get("author_name"))
        if key[1]:
            if views is not None:
                by_author_views[key].append(views)
            if likes is not None:
                by_author_likes[key].append(likes)
    view_medians = {k: statistics.median(v) for k, v in by_author_views.items()}
    like_medians = {k: statistics.median(v) for k, v in by_author_likes.items()}

    output = []
    for row in rows:
        x = dict(row)
        views = num(row.get("views"))
        likes = num(row.get("likes"))
        comments = num(row.get("comments"))
        shares = num(row.get("shares"))
        followers = num(row.get("followers"))
        x["engagement_rate"] = None
        x["view_follower_ratio"] = None
        x["relative_performance"] = None
        x["relative_performance_basis"] = None
        if views is not None and views > 0 and all(v is not None for v in (likes, comments, shares)):
            x["engagement_rate"] = (likes + comments + shares) / views
        if views is not None and followers is not None and followers > 0:
            x["view_follower_ratio"] = views / followers
        key = (row.get("platform"), row.get("author_id") or row.get("author_name"))
        view_baseline = view_medians.get(key)
        like_baseline = like_medians.get(key)
        if views is not None and view_baseline is not None and view_baseline > 0:
            x["relative_performance"] = views / view_baseline
            x["relative_performance_basis"] = "views"
        elif views is None and likes is not None and like_baseline is not None and like_baseline > 0:
            x["relative_performance"] = likes / like_baseline
            x["relative_performance_basis"] = "likes"
        output.append(x)
    return output


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    rows = [json.loads(line) for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    output = enrich(rows)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in output), encoding="utf-8")
    print(f"wrote {len(output)} rows -> {out}")


if __name__ == "__main__":
    main()
