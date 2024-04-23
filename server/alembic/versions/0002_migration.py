"""0002_migration

Revision ID: d569340cf589
Revises: 1d2c242a10d7
Create Date: 2022-07-16 23:34:51.296749

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d569340cf589"
down_revision = "1d2c242a10d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("name_user_id_uc", "tags", ["name", "user_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("name_user_id_uc", "tags", type_="unique")
    # ### end Alembic commands ###
