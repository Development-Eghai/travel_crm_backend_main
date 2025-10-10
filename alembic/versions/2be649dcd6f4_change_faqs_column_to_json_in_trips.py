"""Change faqs column to JSON in trips

Revision ID: 2be649dcd6f4
Revises: <previous_revision_id>
Create Date: 2025-10-09 16:55:34.592387
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '2be649dcd6f4'
down_revision: Union[str, None] = None # replace with your actual previous migration id
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # Fix invalid data
    conn.execute(sa.text("""
        UPDATE trips
        SET faqs = NULL
        WHERE faqs IS NULL OR faqs = '' OR faqs = 'None';
    """))
    conn.execute(sa.text("""
        UPDATE trips
        SET faqs = JSON_QUOTE(faqs)
        WHERE faqs IS NOT NULL AND faqs != '' AND faqs != 'None' AND JSON_VALID(faqs) = 0;
    """))

    # Now alter column
    op.alter_column('trips', 'faqs', type_=sa.JSON, existing_nullable=True)



def downgrade() -> None:
    # Revert JSON back to TEXT
    op.alter_column('trips', 'faqs',
        existing_type=mysql.JSON(),
        type_=sa.Text(),
        existing_nullable=True
    )
