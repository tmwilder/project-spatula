from datetime import datetime
from typing import Optional


class Card:
    db_id: int
    name: str
    card_type: str
    image_url: str
    image_url_flip_side: Optional[str]
    changed_on: datetime

    def __init__(self, db_id, name, card_type, image_url, image_url_flip_side, changed_on):
        self.db_id = db_id
        self.name = name
        self.card_type = card_type
        self.image_url = image_url
        self.image_url_flip_side = image_url_flip_side
        self.changed_on = changed_on

    def __iter__(self):
        yield 'name', self.name
        yield 'card_type', self.card_type
        yield 'image_url', self.image_url
        yield 'image_url_flip_side', self.image_url_flip_side

    def __hash__(self):
        return self.name
