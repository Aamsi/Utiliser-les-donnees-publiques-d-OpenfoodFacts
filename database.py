import mysql.connector
from mysql.connector import errorcode


class Database:

    def __init__(self, host, user, password, name_database):
        self.cnx = mysql.connector.connect(host=host,
                                           user=user,
                                           password=password,
                                           database=name_database)
        self.cursor = self.cnx.cursor()


class Table:

    def __init__(self, database):
        self.database = database

    def create_table(self):
        try:
            self.database.cursor.execute(self.__class__.SQL_QUERY_CREATE_TABLE)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)


class PurchaseStores(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE Purchase_stores (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        store_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB"""
    SQL_QUERY_INSERT_INTO = """INSERT INTO Purchase_stores
        (store_name)
        VALUES (%(store_name)s)"""

    def insert_into_table(self, datas):
        stores = []
        for data in datas:
            for attribute in data:
                purchase_store = attribute['stores']
                purchase_stores = purchase_store.split(',')
                for store in purchase_stores:
                    try:
                        if store[0] != " ":
                            stores.append(store)
                    except IndexError:
                        pass

        stores = list(dict.fromkeys(stores))
        for store in stores:
            store_to_add = {'store_name': store}
            self.database.cursor.execute(PurchaseStores.SQL_QUERY_INSERT_INTO,
                                         store_to_add)

        self.database.cnx.commit()


class Categories(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE Categories(
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        category_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB"""
    SQL_QUERY_INSERT_INTO = """INSERT INTO Categories
        (category_name)
        VALUES(%(category_name)s)"""

    def insert_into_table(self, datas):
        categories_list = []
        for data in datas:
            for attribute in data:
                categories = attribute['categories']
                categories = categories.split(',')
                categories_list.append(categories[0])

        categories_list = list(dict.fromkeys(categories_list))
        for category in categories_list:
            category_to_add = {'category_name': category}
            self.database.cursor.execute(Categories.SQL_QUERY_INSERT_INTO,
                                         category_to_add)

        self.database.cnx.commit()


class Products(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE Products (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        product_name VARCHAR(255) NOT NULL,
        nutriscore TEXT NOT NULL,
        link TEXT NOT NULL,
        details TEXT,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB"""
    SQL_QUERY_INSERT_INTO = """INSERT INTO Products
        (product_name, nutriscore, link, details)
        VALUES (%(product_name)s, %(nutriscore)s, %(link)s, %(details)s)"""

    def insert_into_table(self, datas):
        for data in datas:
            for attribute in data:
                attributes = {
                    'product_name': attribute['product_name_fr'],
                    'nutriscore': attribute['nutrition_grades_tags'][0],
                    'link': 'https://world.openfoodfacts.org/product/{}'.format(attribute['code']),
                    'details': attribute['generic_name_fr']
                }
                self.database.cursor.execute(Products.SQL_QUERY_INSERT_INTO, attributes)

                self.database.cnx.commit()

# class Favorites(Database):
#     SQL_QUERY_CREATE_TABLE = """CREATE TABLE Favorites (
#         id INT UNSIGNED NOT NULL AUTO_INCREMENT,
#         product_id_replaced INT UNSIGNED NOT NULL,
#         product_id_replacement INT UNSIGNED NOT NULL,
#         PRIMARY KEY (id),
#         CONSTRAINT fk_product_id_replaced
#             FOREIGN KEY (product_id_replaced)
#             REFERENCES Products(id),
#         CONSTRAINT fk_product_id_replacement
#             FOREIGN KEY (product_id_replacement)
#             REFERENCES Products(id)
#         ) ENGINE=InnoDB"""

#     def __init__(self):
#         Database.__init__(self, 'localhost', 'student_P5', 'studentOC97', 'openfoodfacts_P5')
#         Database.create_table(self, Favorites.SQL_QUERY_CREATE_TABLE)


# class ProductCategories(Database):
#     SQL_QUERY_CREATE_TABLE = """CREATE TABLE Product_categories (
#         product_id INT UNSIGNED NOT NULL,
#         category_product_id INT UNSIGNED NOT NULL,
#         CONSTRAINT fk_product_id_cat
#             FOREIGN KEY (product_id)
#             REFERENCES Products(id),
#         CONSTRAINT fk_category_product_id
#             FOREIGN KEY (category_product_id)
#             REFERENCES Categories(id)
#         ) ENGINE=InnoDB"""

#     def __init__(self):
#         Database.__init__(self, 'localhost', 'student_P5', 'studentOC97', 'openfoodfacts_P5')
#         Database.create_table(self, ProductCategories.SQL_QUERY_CREATE_TABLE)


# class ProductStores(Database):
#     SQL_QUERY_CREATE_TABLE = """CREATE TABLE Product_stores (
#         product_id INT UNSIGNED NOT NULL,
#         purchase_store_id INT UNSIGNED NOT NULL,
#         CONSTRAINT fk_product_id_stores
#             FOREIGN KEY (purchase_store_id)
#             REFERENCES Purchase_stores(id)
#         ) ENGINE=InnoDB"""

#     def __init__(self):
#         Database.__init__(self, 'localhost', 'student_P5', 'studentOC97', 'openfoodfacts_P5')
#         Database.create_table(self, ProductStores.SQL_QUERY_CREATE_TABLE)
