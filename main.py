# from database import (Database, PurchaseStores, Categories, Products,
#                         Favorites, ProductCategories, ProductStores)
from database import (Database, PurchaseStores, Categories)

from openfoodfacts import Openfoodfacts

terms = ["mayonnaise", "ketchup", "milk", "biscuits", "chips"]

db = Database('localhost', 'student_p5', 'studentOC97', 'openfoodfacts')

datas = Openfoodfacts()
products = datas.search_product(terms)

purchase_stores = PurchaseStores(db)
purchase_stores.create_table()
purchase_stores.insert_into_table(products)

categories = Categories(db)
categories.create_table()
categories.insert_into_table(products)

# products = Products(db)
# products.insert_into_table(products)

# favorites = Favorites()

# products_categories = ProductCategories()
