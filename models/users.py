from sqlalchemy.dialects.postgresql import UUID

import sqlalchemy as sa
from models import roles

metadata = sa.MetaData()

# Users table
users_table = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('first_name', sa.String(50), nullable=False),
    sa.Column('last_name', sa.String(50), nullable=False),
    sa.Column('patronymic', sa.String(50), nullable=False),
    sa.Column('phone', sa.String(11)),
    sa.Column('email', sa.String(30)),
    sa.Column('login', sa.String(20)),
    sa.Column('password', sa.String(120)),
    sa.Column('role_id', sa.Integer ),
    sa.ForeignKeyConstraint(('role_id',), [roles.roles_table.columns.id], ),
)

tokens_table = sa.Table(
    'tokens',
    metadata,
    sa.Column(
        'token',
        UUID(as_uuid=False),
        server_default=sa.text('uuid_generate_v4()'),
        unique=True,
        nullable=False,
        index=True
    ),
    sa.Column('expires', sa.DateTime()),
    sa.Column('user_id', sa.ForeignKey('users.id', ondelete='CASCADE'))
)