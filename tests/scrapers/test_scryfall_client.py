import unittest

from spatula.scrapers.scryfall_client import ScryFallClient
from spatula.service.core.card_service import CardService


class TestScryFallClient(unittest.TestCase):
    def test_parse_events(self):
        card_service = CardService(None, scryfall_client=ScryFallClient())
        cards = card_service.get_cards_local()
        self.assertEqual(len(cards), 52228)
