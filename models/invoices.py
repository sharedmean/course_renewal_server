import sqlalchemy as sa
from models import agreements

metadata = sa.MetaData()

# Invoices table
invoices_table = sa.Table(
    'invoices',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('create_date', sa.Date, nullable=False),
    sa.Column('end_date', sa.Date, nullable=False),
    sa.Column('amount', sa.Float ),
    sa.Column('status', sa.Integer ),
    sa.Column('link', sa.String(30)),
    sa.Column('agreement_id', sa.Integer ),
    sa.ForeignKeyConstraint(('agreement_id',), [agreements.agreements_table.columns.id], ),
)