# PyInstaller hook for SQLModel
# SQLModel depends on SQLAlchemy and Pydantic, which have their own hidden imports

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all SQLModel submodules
hiddenimports = collect_submodules('sqlmodel')

# SQLAlchemy hidden imports (database dialects and connectors)
hiddenimports += collect_submodules('sqlalchemy')

# Pydantic hidden imports
hiddenimports += collect_submodules('pydantic')
hiddenimports += collect_submodules('pydantic_core')

# Additional commonly needed imports
hiddenimports += [
    'sqlalchemy.sql.default_comparator',
    'sqlalchemy.ext.baked',
    'sqlalchemy.dialects.sqlite',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.dialects.mysql',
    'sqlalchemy.pool',
    'sqlalchemy.orm',
    'sqlalchemy.orm.properties',
    'sqlalchemy.orm.relationships',
    'sqlalchemy.orm.session',
    'sqlalchemy.orm.query',
    'sqlalchemy.orm.mapper',
    'sqlalchemy.orm.attributes',
    'sqlalchemy.orm.instrumentation',
    'sqlalchemy.orm.descriptor_props',
    'sqlalchemy.orm.strategies',
    'sqlalchemy.orm.collections',
    'sqlalchemy.orm.dependency',
    'sqlalchemy.orm.unitofwork',
    'sqlalchemy.orm.identity',
    'sqlalchemy.orm.path_registry',
    'sqlalchemy.orm.loading',
    'sqlalchemy.orm.persistence',
    'sqlalchemy.orm.util',
    'sqlalchemy.engine.default',
    'sqlalchemy.engine.reflection',
    'sqlalchemy.engine.interfaces',
    'sqlalchemy.engine.mock',
    'sqlalchemy.event',
    'sqlalchemy.events',
    'sqlalchemy.inspection',
    'sqlalchemy.schema',
    'sqlalchemy.types',
    'sqlalchemy.util.queue',
    'greenlet',  # Required by SQLAlchemy for async
    'typing_extensions',
    'annotated_types',
]

# Collect data files
datas = collect_data_files('sqlmodel')
datas += collect_data_files('pydantic')
datas += collect_data_files('pydantic_core')
