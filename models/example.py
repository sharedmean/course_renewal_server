# В моделях прописывается таблица для миграции

import sqlalchemy as sa

metadata = sa.MetaData()

example_table = sa.Table(
    'example',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False),
    sa.Column('params', sa.String()),
    sa.Column('test', sa.Integer)
)