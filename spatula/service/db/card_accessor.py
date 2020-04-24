from functools import reduce
from typing import List, Dict, Callable, Tuple

import MySQLdb

from spatula.service.model.card import Card


class CardAccessor:
    db = None

    # TODO fuzzy match here or elsewhere - composite joins vs. other records
    get_cards_query = "SELECT * from cards"

    insert_cards_query = """
        INSERT INTO cards
            (name, card_type, image_url, image_url_flip_side)
        VALUES
            {value_format_chars}
        ON DUPLICATE KEY IGNORE
    """

    values_fragment = "(%s, %s, %s, %s)"

    def __init__(self, db: MySQLdb.Connection):
        self.db = db

    def get_cards(self) -> List[Card]:
        card_rows = self.db.execute(self.get_cards_query)
        return [self._row_to_model(row) for row in card_rows]

    def insert_cards(self, cards: List[Card]) -> Tuple[List[Card], int]:
        fragmentize: Callable[[Card], List] = lambda x: [x.name, x.card_type, x.image_url, x.image_url_flip_side]

        query = self.insert_cards_query.format(",".join([self.values_fragment for _ in cards]))
        flat_values_list = reduce(list.__add__, [fragmentize(card) for card in cards])

        rows_updated = self.db.execute(query, flat_values_list)

        return self.get_cards(), rows_updated

    def _row_to_model(self, row: Dict) -> Card:
        return Card(
            db_id=row["id"],
            name=row["name"],
            card_type=row["card_type"],
            image_url=row["image_url"],
            image_url_flip_side=row["image_url_flip_side"],
            changed_on=row["changed_on"])
