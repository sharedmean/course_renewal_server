import sqlalchemy as sa
from models import courses
from models import organizations
from models import partnership_agreements

metadata = sa.MetaData()

# Agreements table
agreements_table = sa.Table(
    'agreements',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('link', sa.String(30)),
    sa.Column('status', sa.Integer),
    sa.Column('organization_id', sa.Integer ),
    sa.Column('course_id', sa.Integer ),
    sa.Column('partnership_agreement_id', sa.Integer ),
    sa.ForeignKeyConstraint(('organization_id',), [organizations.organizations_table.columns.id], ),
    sa.ForeignKeyConstraint(('course_id',), [courses.courses_table.columns.id], ),
    sa.ForeignKeyConstraint(('partnership_agreement_id',), [partnership_agreements.partnership_agreements_table.columns.id], ),
)