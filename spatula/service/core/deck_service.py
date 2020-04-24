from spatula.scrapers.scryfall_client import ScryFallClient

class DeckService:
    scryfall_client = None
    db = None

    def __init__(self, db, scryfall_client: ScryFallClient):
        self.db = db
        self.scryfall_client = scryfall_client

