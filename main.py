from database import (Database, PurchaseStores, Categories, Products, 
                        Favorites, ProductCategories, ProductStores)

from openfoodfacts import Openfoodfacts

terms = ["mayonnaise", "ketchup", "milk", "biscuits", "chips"]

db = Database('localhost', 'student_P5', 'studentOC97', 'openfoodfacts_P5')

datas = Openfoodfacts()
datas.search_product(terms)

purchase_stores = PurchaseStores(db)
purchase_stores.insert_into_table(datas.products)

categories = Categories(db)
categories.insert_into_table(datas.products)

products = Products(db)
products.insert_into_table(datas.products)

favorites = Favorites()

products_categories = ProductCategories()

product_stores = ProductStores()
