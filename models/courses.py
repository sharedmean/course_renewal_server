import sqlalchemy as sa
from models import users

metadata = sa.MetaData()

# Courses table
courses_table = sa.Table(
    'courses',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(70), nullable=False),
    sa.Column('hours', sa.Integer, nullable=False),
    sa.Column('price', sa.Float, nullable=False),
    sa.Column('form', sa.String(20), nullable=False),
    sa.Column('start_date', sa.Date, nullable=False),
    sa.Column('end_date', sa.Date, nullable=False),
    sa.Column('program', sa.String(40)),
    sa.Column('tutor_id', sa.Integer ),
    sa.Column('schedule', sa.String(40)),
    sa.ForeignKeyConstraint(('tutor_id',), [users.users_table.columns.id], ),
)