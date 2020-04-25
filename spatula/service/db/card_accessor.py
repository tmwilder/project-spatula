from functools import reduce
from typing import List, Dict, Callable, Tuple

import MySQLdb

from spatula.service.model.card import Card


class CardAccessor:
    db: MySQLdb.Connection

    # TODO fuzzy match here or elsewhere - composite joins vs. other records
    get_cards_query = "SELECT * from card"

    insert_cards_query = """
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

    def get_cards(self) -> List[Card]:
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
