from datetime import datetime

from migrate import *
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Text,
    BigInteger,
    Numeric,
    Float
)

meta = MetaData()
homes = Table(
    'homes', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(500)),
    Column('url', Text(), unique=True),
    Column('description', Text()),
    Column('price_per_square_meter', Numeric(precision=20, scale=4)),
    Column('price', Numeric(precision=20, scale=4)),
    Column('rooms', Integer()),
    Column('baths', Float()),
    Column('square_meter', Float()),
    Column('building_square_meter', Float()),
    Column('parking_lots', Float()),
    Column(
        'created_at',
        DateTime(timezone=True),
        default=datetime.now
    ),
    Column(
        'extracted_at',
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    ),
    Column(
        'updated_at',
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    ),
    Column('country', String(500)),
    Column('state', String(500)),
    Column('city', String(500)),
    Column('neighborhood', String(500)),
    Column('latitude', Float()),
    Column('longitude', Float()),
    Column('extra_features', JSONB()),

)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    homes.create(migrate_engine, checkfirst=True)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    homes.drop(checkfirst=True)
