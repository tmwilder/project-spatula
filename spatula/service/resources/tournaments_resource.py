from flask import (
    Blueprint, Response, request
)
from spatula.scrapers.mtgo_scraper import MtgoScraper
from spatula.service.db.connection_factory import get_db
from spatula.service.db.card_accessor import CardAccessor
from spatula.service.db.tournament_accessor import TournamentAccessor
from spatula.service.core.tournament_service import TournamentService

cr_bp = Blueprint('events', __name__, url_prefix='/events')

# TODO add id, name, date range, format filters to query params
# TODO register with main app
@cr_bp.route('', methods=['GET'])
def get_events():
    db = get_db()
    mtgo_scraper = MtgoScraper()
    card_accessor = CardAccessor(db)
    tournament_accessor = TournamentAccessor(db)
    tournament_service = TournamentService(db, mtgo_scraper, card_accessor, tournament_accessor)

    if request.args.get('tournament_id'):
        return tournament_service.get_one_tournament(request.args.get('tournament_id'))
    else:
        # TODO parse + validate dates and int here
        return tournament_service.get_tournaments_matching(
            format=request.args.get('tournament_id'),
            start_date=request.args.get('start_date'),
            end_date=request.args.get('end_date'),
        )


@cr_bp.route('', methods=['POST'])
def pull_latest():
    db = get_db()
    client = ScryFallClient()
    card_service = CardService(db, client)
    cards_added = card_service.load_cards(local=False)
    return Response({"current_card_count": cards_added})


@cr_bp.cli.command("load-cards")
def load_cards():
    db = get_db()
    client = ScryFallClient()
    card_service = CardService(db, client)
    cards_added = card_service.load_cards(local=True)
    return Response({"current_card_count": cards_added})
