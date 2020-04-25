from functools import reduce
from typing import List, Dict, Callable, Tuple

import MySQLdb

from spatula.service.model.tournament import Tournament
from spatula.service.model.deck_result import DeckResult
from spatula.service.model.card import Card


class TournamentAccessor:
    db: MySQLdb.Connection

    # TODO fuzzy match here or elsewhere - composite joins vs. other records
    get_tournament_by_id_query = """
        SELECT * from tournament t
            inner join tournament_finish tf on t.id = tf.tournament_id
            inner join deck d on tf.deck_id = d.id
            inner join deck_cards dc on d.id = dc.deck_id
            inner join card c on dc.card_id = c.id
        where t.id = %d
    """

    # TODO correct fields and write actual queries
    # TODO move matching story to rlike on searchable fields
    # TODO support pagination
    get_tournaments_without_cards_query = """
        SELECT * from tournament t
            inner join tournament_finish tf on t.id = tf.tournament_id
            inner join deck d on tf.deck_id = d.id
        where 
            (%s is NULL or tf.player_name = %s) AND
            (%s is NULL or t.date_on <= %s) AND
            (%s is NULL or t.date_on >= %s)
        order by t.date_on desc limit 100
    """

    # TODO one update per entity then batch insert all
    # TODO then plug into API and local prepop fixture + CLI command and readme
    # TODO then start skinning access apis on top
    insert_tournament_query = """
        INSERT INTO card
            (name, card_type, image_url, image_url_flip_side)
        VALUES
            {value_format_chars}
        ON DUPLICATE KEY UPDATE
            card_type=VALUES(card_type),
            image_url=VALUES(image_url),
            image_url_flip_side=VALUES(image_url_flip_side)
    """

    insert_tournament_finish_query = """
        INSERT INTO card
            (name, card_type, image_url, image_url_flip_side)
        VALUES
            {value_format_chars}
        ON DUPLICATE KEY UPDATE
            card_type=VALUES(card_type),
            image_url=VALUES(image_url),
            image_url_flip_side=VALUES(image_url_flip_side)
    """

    insert_deck_query = """
        INSERT INTO card
            (name, card_type, image_url, image_url_flip_side)
        VALUES
            {value_format_chars}
        ON DUPLICATE KEY UPDATE
            card_type=VALUES(card_type),
            image_url=VALUES(image_url),
            image_url_flip_side=VALUES(image_url_flip_side)
    """

    insert_deck_cards = """
        INSERT INTO card
            (name, card_type, image_url, image_url_flip_side)
        VALUES
            {value_format_chars}
        ON DUPLICATE KEY UPDATE
            card_type=VALUES(card_type),
            image_url=VALUES(image_url),
            image_url_flip_side=VALUES(image_url_flip_side)
    """

    values_fragment = "(%s, %s, %s, %s)"

    def __init__(self, db: MySQLdb.Connection):
        self.db = db

    def get_tournaments(self) -> List[Tournament]:
        with self.db.cursor() as c:
            c.execute(self.get_cards_query)
            card_rows = c.fetchall()
            return [self._row_to_model(row) for row in card_rows]

    def insert_cards(self, cards: List[Card]) -> Tuple[List[Card], int]:
        fragmentize: Callable[[Card], List] = lambda x: [x.name, x.card_type, x.image_url, x.image_url_flip_side]

        query = self.insert_cards_query.format(value_format_chars=",".join([self.values_fragment for _ in cards]))
        flat_values_list = reduce(list.__add__, [fragmentize(card) for card in cards])

        rows_updated = self.db.cursor().execute(query, flat_values_list)
        self.db.commit()

        return self.get_cards(), rows_updated

    def _row_to_model(self, row: Dict) -> Card:
        return Card(
            db_id=row[0],
            name=row[1],
            card_type=row[2],
            image_url=row[3],
            image_url_flip_side=row[4],
            changed_on=row[5])
