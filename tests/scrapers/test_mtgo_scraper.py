import unittest
import os.path as op
from spatula.scrapers.mtgo_scraper import MtgoScraper


class TestMtgoScraper(unittest.TestCase):
    def test_parse_events(self):
        with open(op.join(op.realpath(op.dirname(__file__)), "mtgo_api_data", "events_response.json")) as f:
            raw_data = f.read()
            scraper = MtgoScraper()
            parsed_events = scraper._parse_events(raw_data)
            self.assertEqual(len(parsed_events), 9)

    def test_parse_event_page(self):
        with open(op.join(op.realpath(op.dirname(__file__)), "mtgo_api_data", "event_page_modern_20200421.html")) as f:
            raw_data = f.read()
            scraper = MtgoScraper()
            parsed_decks = scraper._parse_event_page(raw_data, "/test")
            self.assertEqual(len(parsed_decks["decks"]), 16)
            self.assertEqual(parsed_decks["link"], "/test")

    def test_parse_player_and_placement(self):
        scraper = MtgoScraper()
        player, placement = scraper._parse_player_and_placement("GR_DONKIN (1st Place)")
        self.assertEqual(player, "GR_DONKIN")
        self.assertEqual(placement, 1)
