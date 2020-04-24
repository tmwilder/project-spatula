import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from spatula.scrapers.scryfall_client import ScryFallClient
from spatula.service.db.connection_factory import get_db
from spatula.service.db.card_accessor import CardAccessor

bp = Blueprint('auth', __name__, url_prefix='/cards')


@bp.route('/', method='POST')
def pull_latest():
    db = get_db()
    card_accessor = CardAccessor(db)
    error = None

    client = ScryFallClient()
    data = client.get_card_data()

    card_accessor.insert_cards(data)

    if error is None:
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return redirect(url_for('auth.login'))

    return Response({
        "cards_found": "",
        "cards_added": ""
    })
