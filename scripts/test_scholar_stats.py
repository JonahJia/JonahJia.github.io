"""Offline checks for citation parsing and failure-safe publication."""

import json
import unittest
from unittest.mock import Mock

from update_scholar_stats import AUTHOR_ID, parse_citations, resolve_stats, valid_saved_count


def table(all_count, recent_count="19"):
    return f'''<table id="other"><tr><td class="gsc_rsb_std">999</td></tr></table>
    <table id="gsc_rsb_st"><thead><tr><th></th><th>All</th><th>Since 2021</th></tr></thead>
    <tbody><tr><td>Citations</td><td class="gsc_rsb_std"><span>{all_count}</span></td>
    <td class="gsc_rsb_std">{recent_count}</td></tr><tr><td>h-index</td>
    <td class="gsc_rsb_std">7</td><td class="gsc_rsb_std">3</td></tr></tbody></table>'''


class CitationTests(unittest.TestCase):
    def test_uses_all_time_column_in_correct_table(self):
        self.assertEqual(parse_citations(table("1,234")), 1234)
        self.assertEqual(parse_citations(table("1&#8239;234")), 1234)

    def test_zero_is_a_real_count(self):
        self.assertEqual(parse_citations(table("0", "0")), 0)

    def test_invalid_citation_does_not_fall_through_to_h_index(self):
        with self.assertRaises(ValueError):
            parse_citations(table("—"))
        with self.assertRaises(ValueError):
            parse_citations("<html>Please verify you are human</html>")

    def test_cache_requires_matching_author_and_integer_count(self):
        for count in (-1, True, False, "12", 2.5, None):
            self.assertIsNone(valid_saved_count({"author_id": AUTHOR_ID, "citations": count}, AUTHOR_ID))
        self.assertIsNone(valid_saved_count({"author_id": "someone-else", "citations": 99}, AUTHOR_ID))
        self.assertEqual(valid_saved_count({"author_id": AUTHOR_ID, "citations": 0}, AUTHOR_ID), (0, None))

    def test_network_failure_preserves_published_count_and_date(self):
        profile = Mock(side_effect=OSError("HTTP 429"))
        cache = Mock(return_value=json.dumps({"author_id": AUTHOR_ID, "citations": 42, "checked_at": "earlier"}))
        result, warnings = resolve_stats(AUTHOR_ID, profile, cache, None, "today")
        self.assertEqual((result["message"], result["citations"], result["checked_at"]), ("42", 42, "earlier"))
        self.assertEqual(result["status"], "cached")
        self.assertEqual(result["last_attempt_at"], "today")
        self.assertTrue(warnings)
        profile.assert_called_once()
        cache.assert_called_once()

    def test_invalid_cache_falls_back_to_seed(self):
        result, _ = resolve_stats(AUTHOR_ID, Mock(side_effect=OSError()),
                                 Mock(return_value='{"author_id":"wrong", "citations":999}'),
                                 {"author_id": AUTHOR_ID, "citations": 12}, "today")
        self.assertEqual((result["citations"], result["status"]), (12, "seeded"))

    def test_newer_manual_seed_replaces_cache_with_timezone_normalization(self):
        cached = {"author_id": AUTHOR_ID, "citations": 42, "checked_at": "2026-11-17T00:00:00Z"}
        seed = {"author_id": AUTHOR_ID, "citations": 45, "checked_at": "2026-11-17T09:00:00+08:00"}
        result, _ = resolve_stats(AUTHOR_ID, Mock(side_effect=OSError()),
                                 Mock(return_value=json.dumps(cached)), seed, "today")
        self.assertEqual((result["citations"], result["status"], result["checked_at"]),
                         (45, "seeded", seed["checked_at"]))

    def test_older_or_undated_seed_cannot_replace_cache(self):
        cached = {"author_id": AUTHOR_ID, "citations": 42, "checked_at": "2026-11-17T00:00:00Z"}
        for date in ("2026-11-17T07:00:00+08:00", "2026-11-17T00:00:00Z", None, "invalid"):
            with self.subTest(date=date):
                seed = {"author_id": AUTHOR_ID, "citations": 45, "checked_at": date}
                result, _ = resolve_stats(AUTHOR_ID, Mock(side_effect=OSError()),
                                         Mock(return_value=json.dumps(cached)), seed, "today")
                self.assertEqual((result["citations"], result["status"]), (42, "cached"))

    def test_verified_zero_does_not_load_cache(self):
        cache = Mock(side_effect=AssertionError("Cache should not be requested"))
        result, warnings = resolve_stats(AUTHOR_ID, Mock(return_value=table("0")), cache, None, "today")
        self.assertEqual((result["citations"], result["status"], result["checked_at"]), (0, "current", "today"))
        self.assertEqual(warnings, [])
        cache.assert_not_called()

    def test_all_sources_unavailable_display_unknown_not_zero(self):
        result, _ = resolve_stats(AUTHOR_ID, Mock(side_effect=OSError()), Mock(side_effect=OSError()),
                                 {"author_id": AUTHOR_ID, "citations": None}, "today")
        self.assertIsNone(result["citations"])
        self.assertEqual(result["message"], "—")
        self.assertIsNone(result["checked_at"])


if __name__ == "__main__":
    unittest.main()
