import sqlalchemy as db

engine = db.create_engine('sqlite:///exampl-db.db')

connection = engine.connect()

metadata = db.MetaData()

products = db.Table('products', metadata,
                    db.Column('product_id', db.Integer, primary_key=True),
                    db.Column('product_name', db.Text),
                    db.Column('company_name', db.Text),
                    db.Column('price', db.Integer)
                    )
metadata.create_all(engine)

insertion_query = products.insert().values([
    {"product_name":"Apple", "company_name":"Fruits_Art", "price":4},
    {"product_name":"Banana", "company_name":"Monster", "price":6},
    {"product_name":"Chery", "company_name":"Eat", "price":7}
])

connection.execute(insertion_query)
