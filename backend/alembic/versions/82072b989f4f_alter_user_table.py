"""alter user table

Revision ID: 82072b989f4f
Revises: 
Create Date: 2025-10-23 11:19:15.169887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82072b989f4f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE user
    ADD COLUMN userType varchar(100)
               """)
    
    pass


def downgrade() -> None:
    op.execute("""
    ALTER TABLE user
    DROP COLUMN userType
               """)
    pass
