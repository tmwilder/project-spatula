from datetime import datetime
from typing import Dict

from spatula.service.model.card import Card


class DeckResult:
    player_name: str
    date_on: str
    placement: int
    labeled_name: str
    classified_name: str
    maindeck: Dict[Card, int]
    sideboard: Dict[Card, int]
    changed_on: datetime

    def __init__(self, player_name, date_on, placement, labeled_name, classified_name, maindeck, sideboard, changed_on):
        self.player_name = player_name
        self.date_on = date_on
        self.placement = placement
        self.labeled_name = labeled_name
        self.classified_name = classified_name
        self.maindeck = maindeck
        self.sideboard = sideboard
        self.changed_on = changed_on
