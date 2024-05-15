from sqlalchemy import URL, create_engine

connection_string = URL.create(
    'postgresql',
    username='koyeb-adm',
    password='Ivcu0b8YqiVs',
    host='ep-frosty-cherry-a2w8eegd.eu-central-1.pg.koyeb.app',
    database='koyebdb',
)

engine = create_engine(connection_string)