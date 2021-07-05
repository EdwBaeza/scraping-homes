from datetime import datetime

from sqlalchemy import Table, MetaData, Integer, Float, Column, DateTime


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    homes = Table('homes', meta, autoload=True)

    date_out = Column('date_out', DateTime(timezone=True))
    building_year = Column('building_year', Integer())
    total_rooms_column = Column('total_rooms', Float())

    date_out.create(homes)
    building_year.create(homes)
    total_rooms_column.create(homes)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    homes = Table('homes', meta, autoload=True)
    homes.c.building_year.drop()
    homes.c.total_rooms.drop()
    homes.c.date_out.drop()
