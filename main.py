from database import (Database, PurchaseStores, Categories, Products)
from openfoodfacts import Openfoodfacts

terms = ["aperitif", "biscuits", "chips"]

db = Database('localhost', 'student_p5', 'studentOC97', 'openfoodfacts')

datas = Openfoodfacts()
products_data = datas.search_product(terms)

purchase_stores = PurchaseStores(db)
purchase_stores.create_table()
purchase_stores.insert_into_table(products_data)

categories = Categories(db)
categories.create_table()
categories.insert_into_table(products_data)

products = Products(db)
products.create_table()
products.insert_into_table(products_data)

# favorites = Favorites()

# products_categories = ProductCategories()
