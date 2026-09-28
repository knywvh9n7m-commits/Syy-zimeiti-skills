import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_script(name):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


mcp = load_script("tikhub_mcp.py")
estimate_cost = load_script("estimate_cost.py")
score_posts = load_script("score_posts.py")
normalize = load_script("normalize.py")


class TestMcpHelpers(unittest.TestCase):
    def test_tool_search(self):
        tools = [
            {"name": "douyin_search_video", "description": "search videos by keyword", "inputSchema": {}},
            {"name": "douyin_user_info", "description": "fetch profile", "inputSchema": {}},
        ]
        hits = mcp.tool_search(tools, "search video")
        self.assertEqual(hits[0]["name"], "douyin_search_video")

    def test_parse_sse(self):
        payload = b'event: message\ndata: {"jsonrpc":"2.0","id":2,"result":{"tools":[]}}\n\n'
        data = mcp._parse_sse_or_json(payload, "text/event-stream")
        self.assertIn("result", data)


class TestCost(unittest.TestCase):
    def test_estimate(self):
        self.assertEqual(estimate_cost.estimate(100, 0.001, 0.01), (0.1, 1.0))

    def test_no_assumptions_means_no_quote(self):
        self.assertIsNone(estimate_cost.estimate(100))

    def test_invalid_prices(self):
        for low, high in [(0.01, None), (-1, 1), (2, 1), (float("nan"), 1), (0, float("inf"))]:
            with self.subTest(low=low, high=high):
                with self.assertRaises(ValueError):
                    estimate_cost.estimate(100, low, high)


class TestScoring(unittest.TestCase):
    def test_missing_counts_are_not_zero(self):
        row = {"platform": "douyin", "author_id": "a", "views": 100, "likes": 10, "comments": None, "shares": 1}
        result = score_posts.enrich([row])[0]
        self.assertIsNone(result["engagement_rate"])
        self.assertIsNone(result["comments"])

    def test_observed_zero_counts_are_valid(self):
        row = {"views": 100, "likes": 0, "comments": 0, "shares": 0}
        self.assertEqual(score_posts.enrich([row])[0]["engagement_rate"], 0)

    def test_baseline_stays_within_platform(self):
        rows = [{"platform": "douyin", "author_id": "a", "views": 100}, {"platform": "youtube", "author_id": "a", "views": 10000}]
        self.assertEqual([row["relative_performance"] for row in score_posts.enrich(rows)], [1, 1])

    def test_invalid_counts_do_not_create_metrics(self):
        for invalid in [-1, float("nan"), float("inf"), True]:
            with self.subTest(invalid=invalid):
                row = {"views": invalid, "likes": 1, "comments": 1, "shares": 1, "followers": 10}
                self.assertIsNone(score_posts.enrich([row])[0]["engagement_rate"])

    def test_relative_performance(self):
        rows = [
            {"platform": "douyin", "author_id": "a", "views": 100, "likes": 10, "comments": 2, "shares": 1, "followers": 50},
            {"platform": "douyin", "author_id": "a", "views": 300, "likes": 30, "comments": 4, "shares": 2, "followers": 50},
        ]
        out = score_posts.enrich(rows)
        self.assertAlmostEqual(out[0]["relative_performance"], 0.5)
        self.assertAlmostEqual(out[1]["relative_performance"], 1.5)


class TestNormalize(unittest.TestCase):
    def test_map_record(self):
        raw = {"author": {"name": "P"}, "stats": {"views": 12}}
        mapped = normalize.map_record(raw, {"author_name": "author.name", "views": "stats.views"}, {"platform": "x"})
        self.assertEqual(mapped["author_name"], "P")
        self.assertEqual(mapped["views"], 12)
        self.assertEqual(mapped["platform"], "x")
        self.assertIsNone(mapped["likes"])


if __name__ == "__main__":
    unittest.main()
