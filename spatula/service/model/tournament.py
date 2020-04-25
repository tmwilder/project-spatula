from datetime import date
from typing import Optional, List

from spatula.service.model.deck_result import DeckResult


class Tournament:
    name: str
    date_on: date
    format: str
    player_count: Optional[int]
    data_source: str
    deck_results: List[DeckResult]

    def __init__(self, name, date_on, format, player_count, data_source, deck_results):
        self.name = name
        self.date_on = date_on
        self.format = format
        self.player_count = player_count
        self.data_source = data_source
        self.deck_results = deck_results
