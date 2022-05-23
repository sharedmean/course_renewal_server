import sqlalchemy as sa

metadata = sa.MetaData()

# Organizations table
organizations_table = sa.Table(
    'organizations',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('director', sa.String(100), nullable=False),
    sa.Column('phone', sa.String(11)),
    sa.Column('email', sa.String(30)),
)