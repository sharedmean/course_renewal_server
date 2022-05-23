import sqlalchemy as sa
from models import users

metadata = sa.MetaData()

# Users table
documents_table = sa.Table(
    'documents',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('link', sa.String(50), nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('user_id', sa.Integer ),
    sa.ForeignKeyConstraint(('user_id',), [users.users_table.columns.id], ),
)