import os.path as op
import unittest
from io import BytesIO
import tarfile

from spatula.scrapers.scryfall_client import ScryFallClient


class TestScryFallClient(unittest.TestCase):
    def test_parse_events(self):
        with open(
                op.join(op.realpath(op.dirname(__file__)), "scryfall_api_data", "scryfall-default-cards.json.tar.gz"),
                "rb") as f:
            memfile = BytesIO(f.read())
            tar = tarfile.open(mode="r:gz", fileobj=memfile)
            extracted_data = tar.extractfile(tar.getmembers()[0]).read()
            client = ScryFallClient()
            parsed_cards = client._parse_card_data(extracted_data)
            self.assertEqual(len(parsed_cards), 52228)
