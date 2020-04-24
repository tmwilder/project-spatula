import json
import requests
from typing import List, Dict, Optional

from spatula.service.model.card import Card


class ScryFallClient:
    endpoint = "https://archive.scryfall.com/json/scryfall-oracle-cards.json"

    def get_card_data(self) -> List[Card]:
        card_data = self._fetch_card_data()
        return self._parse_card_data(card_data)

    def _fetch_card_data(self):
        r = requests.get(self.endpoint)
        return r.content

    def _parse_card_data(self, raw_data):
        return [self._convert_to_card(card) for card in json.loads(raw_data)]

    def _convert_to_card(self, scryfall_card: Dict) -> Optional[Card]:
        try:
            return Card(
                db_id=None,
                name=scryfall_card["name"],
                card_type=scryfall_card["type_line"],
                image_url=scryfall_card["image_uris"]["png"],
                image_url_flip_side=None,
                changed_on=None
            )
        except KeyError as e:
            return Card(
                db_id=None,
                name=scryfall_card["name"],
                card_type=scryfall_card["type_line"],
                image_url=scryfall_card["card_faces"][0]["image_uris"]["png"],
                image_url_flip_side=scryfall_card["card_faces"][1]["image_uris"]["png"],
                changed_on=None
            )



if __name__ == "__main__":
    client = ScryFallClient()
    parsed_events = client.get_card_data()
    print(len(parsed_events))
