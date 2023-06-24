"""migrations

Revision ID: c4d65dfdac7f
Revises: 2c5b148d2f81
Create Date: 2023-06-24 18:43:51.067126

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c4d65dfdac7f"
down_revision = "2c5b148d2f81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "residents_residences",
        sa.Column("resident_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("residence_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["residence_id"],
            ["residence.id"],
        ),
        sa.ForeignKeyConstraint(
            ["resident_id"],
            ["resident.id"],
        ),
    )
    op.drop_constraint("residence_resident_id_fkey", "residence", type_="foreignkey")
    op.drop_column("residence", "resident_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "residence",
        sa.Column("resident_id", postgresql.UUID(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "residence_resident_id_fkey", "residence", "resident", ["resident_id"], ["id"]
    )
    op.drop_table("residents_residences")
    # ### end Alembic commands ###
