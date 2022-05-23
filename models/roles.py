import sqlalchemy as sa

metadata = sa.MetaData()

# Roles table
roles_table = sa.Table(
    'roles',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('details', sa.String(10))
)