import requests
import json


class ScryFallClient:
    endpoint = "https://archive.scryfall.com/json/scryfall-oracle-cards.json"

    def get_card_data(self):
        card_data = self._fetch_card_data()
        return self._parse_card_data(card_data)

    def _fetch_card_data(self):
        r = requests.get(self.endpoint)
        return r.content

    def _parse_card_data(self, raw_data):
        return json.loads(raw_data)


if __name__ == "__main__":
    client = ScryFallClient()
    parsed_events = client.get_card_data()
    print(len(parsed_events))
