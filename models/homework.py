import sqlalchemy as sa
from models import courses
from models import users


metadata = sa.MetaData()

# homeworks table
homeworks_table = sa.Table(
    'homeworks',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(70), nullable=False),
    sa.Column('link', sa.String(30)),
    sa.Column('percent', sa.Integer),
    sa.Column('end_date', sa.Date, nullable=False),
    sa.Column('course_id', sa.Integer ),
    sa.ForeignKeyConstraint(('course_id',), [courses.courses_table.columns.id], ),
)

# listeners_homeworks table
listeners_homeworks_table = sa.Table(
    'listeners_homeworks',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('link', sa.String(30)),
    sa.Column('status', sa.Integer),
    sa.Column('homework_id', sa.Integer ),
    sa.Column('listener_id', sa.Integer ),
    sa.ForeignKeyConstraint(('homework_id',), [homeworks_table.columns.id], ),
    sa.ForeignKeyConstraint(('listener_id',), [users.users_table.columns.id], ),
)