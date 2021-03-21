from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()

class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    # these are supplied by the sqlalchemy2-stubs, so may be omitted
    # when they are installed
    registry = mapper_registry
    metadata = mapper_registry.metadata
