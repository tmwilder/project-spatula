# project-spatula

# Possible Data Sources
## Card Data
We need access to updated information on what all cards exist along with attributes, art, etc.. for searching and display.

These folks have an open bulk export API
https://scryfall.com/docs/api/bulk-data

## Match data
mtgo_scraper.py contains a prototype capable of going and getting Mtgo results from wotc official
We can probably get user submissions by scraping Goldfish - maybe we set something up to accept them too?

## Price Data
https://docs.tcgplayer.com/docs - pretty good pricing data available

MKM prices
https://api.cardmarket.com/ws/documentation/API_2.0:PriceGuide

# Quickstart
0. Check out the project, install deps, turn on project virtualenv 
1. Install docker
2. Optionally - move docker to properly isolated user: https://docs.docker.com/engine/install/linux-postinstall/ 
3. Run `docker swarm init`
4. Start up MySQL mapped to local 3306 - `docker stack deploy -c stack.yml mysql`
5. Run migrations:
  * We use out of the box Alembic - https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment
  * To update schema - `alembic upgrade head`
  * For downgrading - `alembic downgrade -1`
  * See their project docs for adding new migrations 
6. Run the web service out of your editor with debugger control - TODO

# TODO
1. Set up DB access fwork / config
2. ETL in ScryFall Cards
3. ETL in MTGO results - populating w/cards
4. CRUD access API
5. Local UI consuming w/format and some light filtering
6. AWS-ify
7. Gloat
