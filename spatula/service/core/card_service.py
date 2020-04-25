import os.path as op
import tarfile
from io import BytesIO


from spatula.scrapers.scryfall_client import ScryFallClient
from spatula.service.db.card_accessor import CardAccessor


class CardService:
    scryfall_client = None
    db = None
    card_accessor = None

    def __init__(self, db, scryfall_client: ScryFallClient):
        self.db = db
        self.card_accessor = CardAccessor(db)
        self.scryfall_client = scryfall_client

    def load_cards(self, local=False):
        if local:
            cards = self.get_cards_remote()
        else:
            cards = self.get_cards_local()

        self.card_accessor.insert_cards(cards)
        return len(self.card_accessor.get_cards())

    def get_cards_remote(self):
        return self.scryfall_client.get_card_data()

    def get_cards_local(self):
        path = op.join(
                op.realpath(op.dirname(op.dirname(op.dirname(op.dirname(__file__))))),
                "tests", "scrapers", "scryfall_api_data", "scryfall-default-cards.json.tar.gz")

        with open(path, "rb") as f:
            memfile = BytesIO(f.read())
            tar = tarfile.open(mode="r:gz", fileobj=memfile)
            extracted_data = tar.extractfile(tar.getmembers()[0]).read()
            client = ScryFallClient()
            return client._parse_card_data(extracted_data)
