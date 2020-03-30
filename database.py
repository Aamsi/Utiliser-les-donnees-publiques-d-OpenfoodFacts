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
        self.database.cursor.execute(self.__class__.SQL_QUERY_CREATE_TABLE)


class PurchaseStores(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Purchase_stores (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        store_name VARCHAR(255) NOT NULL UNIQUE,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB"""
    SQL_QUERY_INSERT_INTO = """INSERT IGNORE INTO Purchase_stores
        (store_name)
        VALUES (%(store_name)s)"""

    def insert_into_table(self, datas):
        stores = []
        for data in datas:
            if data['stores'] != 0:
                stores.append(data['stores'])

        stores = list(dict.fromkeys(stores))
        for store in stores:
            store_to_add = {'store_name': store}
            self.database.cursor.execute(PurchaseStores.SQL_QUERY_INSERT_INTO,
                                         store_to_add)

        self.database.cnx.commit()


class Categories(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Categories(
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        category_name VARCHAR(255) NOT NULL UNIQUE,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB"""
    SQL_QUERY_INSERT_INTO = """INSERT IGNORE INTO Categories
        (category_name)
        VALUES(%(category_name)s)"""
    SQL_QUERY_PRINT = """SELECT category_name FROM
                            Categories"""

    def insert_into_table(self, datas):
        categories_list = []
        for data in datas:
            if data['categories'] != 0:
                categories_list.append(data['categories'])

        categories_list = list(dict.fromkeys(categories_list))
        for category in categories_list:
            category_to_add = {'category_name': category}
            self.database.cursor.execute(Categories.SQL_QUERY_INSERT_INTO,
                                         category_to_add)

        self.database.cnx.commit()


class Products(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Products (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        product_name VARCHAR(255) NOT NULL UNIQUE,
        nutriscore TEXT NOT NULL,
        link TEXT NOT NULL,
        details TEXT,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB"""
    SQL_QUERY_INSERT_INTO = """INSERT IGNORE INTO Products
        (product_name, nutriscore, link, details)
        VALUES (%(product_name)s, %(nutriscore)s, %(link)s, %(details)s)"""

    def insert_into_table(self, datas):
        for data in datas:
            attributes = {
                'product_name': data['product_name'],
                'nutriscore': data['nutriscore'],
                'link': data['link'],
                'details': data['details']
            }
            self.database.cursor.execute(Products.SQL_QUERY_INSERT_INTO, attributes)

            self.database.cnx.commit()


class Favorites(Table):
    SQL_QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Favorites (
         id INT UNSIGNED NOT NULL AUTO_INCREMENT,
         product_id_replaced INT UNSIGNED NOT NULL,
         product_id_replacement INT UNSIGNED NOT NULL,
         PRIMARY KEY (id),
         CONSTRAINT fk_product_id_replaced
             FOREIGN KEY (product_id_replaced)
             REFERENCES Products(id),
         CONSTRAINT fk_product_id_replacement
             FOREIGN KEY (product_id_replacement)
             REFERENCES Products(id)
         ) ENGINE=InnoDB"""

    SQL_QUERY_INSERT_INTO = """INSERT INTO
                                Favorites(product_id_replaced, product_id_replacement)
                            SELECT
                                p0.id,
                                p1.id
                            FROM
                                Products as p0
                            INNER JOIN
                                Products as p1
                            WHERE
                                p0.product_name = %s
                            AND
                                p1.product_name = %s"""

    def insert_into_table(self, product_names):
        self.database.cursor.execute(Favorites.SQL_QUERY_INSERT_INTO, product_names)
        self.database.cnx.commit()


class ProductCategories(Table):

    SQL_QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Product_categories (
         product_id INT UNSIGNED NOT NULL UNIQUE,
         category_product_id INT UNSIGNED NOT NULL,
         CONSTRAINT fk_product_id_cat
             FOREIGN KEY (product_id)
             REFERENCES Products(id),
         CONSTRAINT fk_category_product_id
             FOREIGN KEY (category_product_id)
             REFERENCES Categories(id)
         ) ENGINE=InnoDB"""

    SQL_QUERY_INSERT_INTO = """INSERT IGNORE INTO
                            Product_categories(product_id, category_product_id)
                        SELECT
                            p.id,
                            c.id
                        FROM
                            Products as p
                        CROSS JOIN
                            Categories as c
                        WHERE
                            product_name = %s
                        and
                            category_name = %s"""

    def insert_into_table(self, datas):
        prod_cat = []
        for data in datas:
            attribute = (data['product_name'], data['categories'])
            if attribute[1] != 0:
                prod_cat.append(attribute)

        for duo in prod_cat:
           self.database.cursor.execute(ProductCategories.SQL_QUERY_INSERT_INTO, duo)

        self.database.cnx.commit()

        return prod_cat


class ProductStores(Table):
    SQL_QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Product_stores (
         product_id INT UNSIGNED NOT NULL UNIQUE,
         purchase_store_id INT UNSIGNED NOT NULL,
         CONSTRAINT fk_product_id_stores
             FOREIGN KEY (purchase_store_id)
             REFERENCES Purchase_stores(id)
         ) ENGINE=InnoDB"""

    SQL_QUERY_INSERT_INTO = """INSERT IGNORE INTO Product_stores
                                (product_id, purchase_store_id)
                            SELECT
                                p.id,
                                ps.id
                            FROM
                                Products as p
                            CROSS JOIN
                                Purchase_stores as ps
                            WHERE
                                p.product_name = %s
                            AND
                                ps.store_name = %s"""

    def insert_into_table(self, datas):
        prod_store = []
        for data in datas:
            attribute = data['product_name'], data['stores']
            if attribute[1] != 0:
                prod_store.append(attribute)

        for duo in prod_store:
            self.database.cursor.execute(ProductStores.SQL_QUERY_INSERT_INTO, duo)

        self.database.cnx.commit()


class Interface(Table):

    SQL_QUERY_PRINT_CATEGORIES = """SELECT category_name FROM
                                    Categories"""

    SQL_QUERY_SELECT_PROD_CAT = """SELECT
                                    p.product_name,
                                    c.category_name,
                                    pc.product_id,
                                    pc.category_product_id
                                FROM
                                    Products as p
                                CROSS JOIN
                                    Categories as c
                                CROSS JOIN
                                    Product_categories as pc
                                WHERE
                                    p.id = pc.product_id
                                AND
                                    c.id = pc.category_product_id"""

    SQL_QUERY_SELECT_DETAILS = """SELECT
                                    product_name,
                                    nutriscore,
                                    link,
                                    details,
                                    s.store_name
                                FROM
                                    Products as p
                                CROSS JOIN
                                    Purchase_stores as s
                                CROSS JOIN
                                    Product_stores as ps
                                WHERE
                                    p.product_name = %s
                                AND
                                    p.id = ps.product_id
                                AND
                                    ps.purchase_store_id = s.id"""

    SQL_QUERY_RETURN_FAV_NAMES = """SELECT
                                product_name
                            FROM
                                Products as p
                            CROSS JOIN
                                Favorites as f
                            WHERE
                                p.id = f.product_id_replacement"""

    SQL_QUERY_RETURN_FAV_DETAILS = """SELECT
                                        product_name,
                                        link,
                                        details,
                                        s.store_name
                                    FROM
                                        Products as p
                                    CROSS JOIN
                                        Purchase_stores as s
                                    CROSS JOIN
                                        Product_stores as ps
                                    WHERE
                                        p.product_name = %s
                                    AND
                                        p.id = ps.product_id
                                    AND
                                        ps.purchase_store_id = s.id"""

    def return_categories(self):
        self.database.cursor.execute(Interface.SQL_QUERY_PRINT_CATEGORIES)
        categories = []
        for category in self.database.cursor:
            cat_to_add = category[0]
            categories.append(cat_to_add)

        return categories

    def return_prod_cat_store(self):
        self.database.cursor.execute(Interface.SQL_QUERY_SELECT_PROD_CAT)
        prod_cat_store = []
        for el in self.database.cursor:
            el_to_add = el[0], el[1]
            prod_cat_store.append(el_to_add)

        return prod_cat_store

    def return_details(self, product_name):
        self.database.cursor.execute(Interface.SQL_QUERY_SELECT_DETAILS, product_name)
        details = []
        for detail in self.database.cursor:
            details.append(detail)

        return details

    def return_replace(self, nutriscore_bef, prod_list):
        to_return = None
        for prod in prod_list:
            prod_replace_details = self.return_details(prod)
            if prod_replace_details[0][1] < nutriscore_bef:
                to_return = prod_replace_details
                self.return_replace(prod_replace_details[0][1], prod_list)

        return to_return

    def return_fav_names(self):
        self.database.cursor.execute(Interface.SQL_QUERY_RETURN_FAV_NAMES)
        favs_names = []
        for fav_name in self.database.cursor:
            favs_names.append(fav_name)

        return favs_names

