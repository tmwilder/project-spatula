import os.path as op
import tarfile
from io import BytesIO

from MySQLdb import Connection

from spatula.service.model.tournament import Tournament
from spatula.scrapers.mtgo_scraper import MtgoScraper
from spatula.service.db.card_accessor import CardAccessor
from spatula.service.db.tournament_accessor import TournamentAccessor


class TournamentService:
    scryfall_client = None
    db = None
    card_accessor = None

    def __init__(
            self,
            db: Connection,
            mtgo_scraper: MtgoScraper,
            card_accessor: CardAccessor,
            tournament_accessor: TournamentAccessor):
        self.db = db
        self.card_accessor = CardAccessor(db)

    def load_tournaments(self, local=False, date_start=None, date_end=None):
        if local:
            cards = self._get_tournaments_remote(date_start, date_end)
        else:
            cards = self._get_tournaments_local()

        self.card_accessor.insert_cards(cards)
        return len(self.card_accessor.get_cards())

    def _get_tournaments_remote(self, date_start, date_end):
        # Get from MTGO

        # Later maybe change to data source parameterized and run it all through here
        return

    def _get_tournaments_local(self):
        # Get from file system for local dev
        path = op.join(
                op.realpath(op.dirname(op.dirname(op.dirname(op.dirname(__file__))))),
                "tests", "scrapers", "scryfall_api_data", "scryfall-default-cards.json.tar.gz")

        with open(path, "rb") as f:
            memfile = BytesIO(f.read())
            tar = tarfile.open(mode="r:gz", fileobj=memfile)
            extracted_data = tar.extractfile(tar.getmembers()[0]).read()
            # client = ScryFallClient()
            return client._parse_card_data(extracted_data)

    def get_one_tournament(self, tournament_id: int) -> Tournament:
        # TODO add by id access
        return


    def get_tournaments_matching(self, format=None, start_date=None, end_date=None):
        # TODO add by open param access
        return
