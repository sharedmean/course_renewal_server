import sqlalchemy as sa
from models import courses
from models import users

metadata = sa.MetaData()

# Listeners_Courses table
listeners_courses_table = sa.Table(
    'listeners_courses',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('percent', sa.Integer, nullable=False),
    sa.Column('score', sa.String(30)),
    sa.Column('certificate', sa.String(30)),
    sa.Column('status', sa.Integer),
    sa.Column('user_id', sa.Integer ),
    sa.Column('course_id', sa.Integer ),
    sa.ForeignKeyConstraint(('user_id',), [users.users_table.columns.id], ),
    sa.ForeignKeyConstraint(('course_id',), [courses.courses_table.columns.id], ),
)