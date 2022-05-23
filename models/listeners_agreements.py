import sqlalchemy as sa
from models import users
from models import agreements

metadata = sa.MetaData()

# Listeners agreementss table
listeners_agreements_table = sa.Table(
    'listeners_agreements',
    metadata,
    sa.Column('user_id', sa.Integer, primary_key=True),
    sa.Column('agreement_id', primary_key=True ),
    sa.ForeignKeyConstraint(('user_id',), [users.users_table.columns.id], ),
    sa.ForeignKeyConstraint(('agreement_id',), [agreements.agreements_table.columns.id], ),
)