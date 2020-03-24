from database import (Database, PurchaseStores, Categories, Products, ProductCategories,
                      ProductStores, Favorites)
from openfoodfacts import Openfoodfacts

terms = ["aperitif", "biscuits", "chips"]

db = Database('localhost', 'student_p5', 'studentOC97', 'openfoodfacts')

datas = Openfoodfacts()
products_data = datas.search_product(terms)
data_dict = datas.create_dict(products_data)

purchase_stores = PurchaseStores(db)
purchase_stores.create_table()
purchase_stores.insert_into_table(data_dict)

categories = Categories(db)
categories.create_table()
categories.insert_into_table(data_dict)

products = Products(db)
products.create_table()
products.insert_into_table(data_dict)

products_categories = ProductCategories(db)
products_categories.create_table()
products_categories.insert_into_table(data_dict)

products_stores = ProductStores(db)
products_stores.create_table()
products_stores.insert_into_table(data_dict)

favorites = Favorites(db)
favorites.create_table()


