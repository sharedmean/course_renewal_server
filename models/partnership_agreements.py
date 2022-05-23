import sqlalchemy as sa
from models import organizations

metadata = sa.MetaData()

# Partnership agreements table
partnership_agreements_table = sa.Table(
    'partnership_agreements',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('start_date', sa.Date, nullable=False),
    sa.Column('end_date', sa.Date, nullable=False),
    sa.Column('sale', sa.Integer, nullable=False),
    sa.Column('link', sa.String(50), nullable=False),
    sa.Column('organization_id', sa.Integer ),
    sa.ForeignKeyConstraint(('organization_id',), [organizations.organizations_table.columns.id], ),
)