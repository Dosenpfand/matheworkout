# NOTE: has to be executed from within "flask shell"

# pgloader \
#     --with "create tables" \
#     --with "create indexes" \
#     --with "reset sequences" \
#     ./app.db postgresql://mathesuper:n7lMzk6JovNo@localhost:5432/matheueben

from sqlalchemy import create_engine, select
from flask_appbuilder import Model


def migrate():
    engine_lite = create_engine('sqlite:///app.db')
    engine_cloud = create_engine(
        'postgresql://mathesuper:n7lMzk6JovNo@localhost:5432/matheueben')

    with engine_lite.connect() as conn_lite:
        with engine_cloud.connect() as conn_cloud:
            for table in reversed(Model.metadata.sorted_tables):
                print(f'deleting from table: {table.name}')
                conn_cloud.execute(f'DELETE FROM {table.name}')
            for table in Model.metadata.sorted_tables:
                print(f'migrating table: {table.name}')
                data = [dict(row)
                        for row in conn_lite.execute(select(table.c))]
                conn_cloud.execute(table.insert().values(data))
            for table in reversed(Model.metadata.sorted_tables):
                print(f'resetting sequence for table: {table.name}')
                conn_cloud.execute(f"SELECT setval('{table.name}_id_seq', max(id)) FROM {table.name};")
