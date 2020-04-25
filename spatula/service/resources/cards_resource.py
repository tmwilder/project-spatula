from flask import (
    Blueprint, Response
)

from spatula.scrapers.scryfall_client import ScryFallClient
from spatula.service.db.connection_factory import get_db
from spatula.service.core.card_service import CardService

cr_bp = Blueprint('cards', __name__, url_prefix='/cards')


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
