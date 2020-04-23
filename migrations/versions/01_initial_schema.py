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
        create table test  (id int)     
    """
    op.get_bind().execute(statement)



def downgrade():
    statement = """
        drop table test        
    """
    op.get_bind().execute(statement)
