import requests
import datetime
import json
import bs4
import re


class MtgoScraper:
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
    base_url = "https://magic.wizards.com/en/section-articles-see-more-ajax"
    wotc_date_fmt = "%m/%d/%Y"
    base_url_event_page = "https://magic.wizards.com/"

    def get_events_for_dates(self, start_date: datetime.datetime, end_date: datetime.datetime):
        raw_events_html = self._fetch_events(start_date, end_date)
        parsed_event_info = self._parse_events(raw_events_html)
        # TODO should probably rate limit/jitter this - but slow for testing
        event_pages_html = [self._fetch_event_page(p["link"]) for p in parsed_event_info]
        parsed_events = [self._parse_event_page(h, i) for (h, i) in zip(event_pages_html, parsed_event_info)]
        return parsed_events

    def _fetch_events(self, start_date: datetime.datetime, end_date: datetime.datetime):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "magic.wizards.com",
            "Referer": 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.ua,
            "X-Requested-With": "XMLHttpRequest"
        }

        query_params = {
            "dateoff": "",
            "l": "en",
            "f": "9041", # TODO what is this?
            "search-result-theme": "",
            "limit": 10,
            "fromDate": start_date.strftime(self.wotc_date_fmt),
            "toDate": end_date.strftime(self.wotc_date_fmt),
            "sort": "DESC",
            "word": "",
            "offset": 0
        }

        r = requests.get(self.base_url, headers=headers, params=query_params)
        # TODO validation stuff lol
        return r.content

    def _parse_events(self, raw_events_html):
        events_dict = json.loads(raw_events_html)
        events = events_dict['data']
        event_infos = [self._parse_one_event_link(link_html) for link_html in events]
        return event_infos

    def _parse_one_event_link(self, event_link_html):
        soup = bs4.BeautifulSoup(event_link_html, features="html.parser")
        event_tag = soup.find("a")

        link = event_tag.get("href")
        name = event_tag.find("div", attrs={"class": "title"}).find("h3").text

        date_tag = event_tag.find("span", attrs={"class": "date"})
        year = date_tag.find("span", attrs={"class": "year"}).text.strip()
        month = date_tag.find("span", attrs={"class": "month"}).text.strip()
        day = date_tag.find("span", attrs={"class": "day"}).text.strip()

        datetime_of_event = datetime.datetime.strptime("{}-{}-{}".format(year, month, day), "%Y-%B-%d")
        date_of_event = datetime.date(
            year=datetime_of_event.year,
            month=datetime_of_event.month,
            day=datetime_of_event.day)

        return {
            "link": link,
            "name": name,
            "date": date_of_event
        }

    def _fetch_event_page(self, event_path):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "magic.wizards.com",
            "Referer": 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        r = requests.get(self.base_url_event_page + event_path, headers=headers)
        # TODO validation stuff lol
        return r.content

    def _parse_player_and_placement(self, player_and_placement):
        expression = re.compile('([^)]*) \\((\d+).*')
        match = expression.match(player_and_placement)
        return match[1], int(match[2])

    def _parse_event_page_deck(self, deck_tag: bs4.Tag):
        # Get player info and placement
        # TODO - is placement here also lined up with post t8 results - or is it post-swiss?
        deck_meta_tag = deck_tag.find("span", attrs={"class": "deck-meta"})
        player_and_placement_tag = deck_meta_tag.find("h4")
        player, placement = self._parse_player_and_placement(player_and_placement_tag.text)

        # Get main and SB
        main_tag = deck_tag.find("div", attrs={"class": "sorted-by-overview-container"})
        sb_tag = deck_tag.find("div", attrs={"class": "sorted-by-sideboard-container"})

        md_card_names = main_tag.findAll("span", attrs={"class": "card-name"})
        md_card_counts = main_tag.findAll("span", attrs={"class": "card-count"})

        sb_cards_names = sb_tag.findAll("span", attrs={"class": "card-name"})
        sb_card_counts = sb_tag.findAll("span", attrs={"class": "card-count"})

        md = zip(md_card_names, md_card_counts)
        sb = zip(sb_cards_names, sb_card_counts)

        md_parsed = dict([(x.text, int(y.text)) for (x, y) in md])
        sb_parsed = dict([(x.text, int(y.text)) for (x, y) in sb])

        return {
            "player": player,
            "placement": placement,
            "md": md_parsed,
            "sb": sb_parsed
        }

    def _parse_event_page(self, event_page_html, event_info):
        soup = bs4.BeautifulSoup(event_page_html, features="html.parser")
        decks = soup.findAll("div", attrs={"class": "deck-group"})
        parsed_decks = [self._parse_event_page_deck(deck) for deck in decks]
        return {
            "decks": parsed_decks,
            "link": event_info["link"],
            "event_name": event_info["name"],
            "event_date": event_info["date"]
        }


if __name__ == "__main__":
    start = datetime.datetime.strptime("04/21/2020", MtgoScraper.wotc_date_fmt)
    end = datetime.datetime.strptime("04/22/2020", MtgoScraper.wotc_date_fmt)
    scraper = MtgoScraper()
    parsed_events = scraper.get_events_for_dates(start, end)
    print(len(parsed_events))
