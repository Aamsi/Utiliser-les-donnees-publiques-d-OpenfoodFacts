import database
import request

terms = ["mayonnaise", "ketchup", "milk", "biscuits", "chips"]

init_SQL = database.InitSQL('localhost', 'student_P5', 'studentOC97', 'openfoodfacts_P5')
datas = request.RequestDatas()
products = datas.search_product()

purchase_stores_table = database.TablePurchaseStores()
categories_table = database.TableCategories()
products_table = database.TableProducts()
favorites_table = database.TableFavorites()
product_categories_table = database.TableProductCategories()
product_store_table = database.TableProductStores()

tables = [purchase_stores_table, categories_table, products_table,
            favorites_table, product_categories_table, product_store_table]

execute_SQL_methods = database.Execute_SQL_methods(init_SQL.cursor, tables)
execute_SQL_methods.creating_tables()

#C'est juste pour tester les méthodes
products_table.insert_into_table(init_SQL.cnx, init_SQL.cursor, datas.products)
purchase_stores_table.insert_into_table(init_SQL.cnx, init_SQL.cursor, datas.products)
categories_table.insert_into_table(init_SQL.cnx, init_SQL.cursor, datas.products)
