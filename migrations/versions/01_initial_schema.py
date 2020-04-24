"""01_initial_schema

Revision ID: df81622653f6
Revises: 
Create Date: 2020-04-23 08:53:23.170022

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'df81622653f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    statement = """
        create table deck  (
                id INT PRIMARY KEY AUTO_INCREMENT,
                format VARCHAR(128),
                changed_on DATETIME DEFAULT now()
            )
    """
    op.get_bind().execute(statement)

    tournament_statement = """
        create table tournament  (
            id INT PRIMARY KEY AUTO_INCREMENT,
            tournament_name VARCHAR(64),
            date_on DATE NOT NULL,
            format VARCHAR(64),
            data_source VARCHAR(20),
            total_participants INT,
            changed_on DATETIME DEFAULT now()
        )     
    """
    op.get_bind().execute(tournament_statement)

    card_statement = """
        create table card  (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name varchar(64) UNIQUE NOT NULL,
            card_type varchar(64) NOT NULL,
            image_url varchar(300) NOT NULL,
            image_url_flip_side varchar(300),
            changed_on DATETIME DEFAULT now()
        )     
    """
    op.get_bind().execute(card_statement)

    deck_cards_statement = """
        create table deck_cards  (
            id INT PRIMARY KEY AUTO_INCREMENT,
            count_in_deck INT NOT NULL,
            is_sideboard BOOLEAN NOT NULL,
            deck_id INT,
            card_id INT,
            FOREIGN KEY (deck_id) REFERENCES deck(id),
            FOREIGN KEY (card_id) REFERENCES card(id)
        )     
    """
    op.get_bind().execute(deck_cards_statement)

    tournament_finish_statement = """
        create table tournament_finish  (
            id INT PRIMARY KEY AUTO_INCREMENT,
            player_name VARCHAR(128),
            date_on DATE NOT NULL,
            placement INT NOT NULL,
            tournament_id INT,
            deck_id INT,
            changed_on DATETIME DEFAULT now(),
            FOREIGN KEY (tournament_id) REFERENCES tournament(id),
            FOREIGN KEY (deck_id) REFERENCES deck(id)
        )
    """
    op.get_bind().execute(tournament_finish_statement)


def downgrade():
    statements = [
        "drop table deck_cards",
        "drop table tournament_finish",
        "drop table deck",
        "drop table tournament",
        "drop table card"
    ]

    [op.get_bind().execute(statement) for statement in statements]
