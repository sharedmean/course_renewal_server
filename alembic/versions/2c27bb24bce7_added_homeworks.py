"""added homeworks

Revision ID: 2c27bb24bce7
Revises: 7edfe5b04c33
Create Date: 2022-05-27 09:28:39.728477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c27bb24bce7'
down_revision = '7edfe5b04c33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('homeworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('link', sa.String(length=30), nullable=True),
    sa.Column('percent', sa.Integer(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('listeners_homeworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(length=30), nullable=True),
    sa.Column('check', sa.Integer(), nullable=True),
    sa.Column('homework_id', sa.Integer(), nullable=True),
    sa.Column('listener_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homework_id'], ['homeworks.id'], ),
    sa.ForeignKeyConstraint(['listener_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listeners_homeworks')
    op.drop_table('homeworks')
    # ### end Alembic commands ###