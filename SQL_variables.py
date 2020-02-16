PURCHASE_STORES = """CREATE TABLE Purchase_stores (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT,
   store_name VARCHAR(255) NOT NULL,
   PRIMARY KEY (id)
   ) ENGINE=InnoDB"""

CATEGORIES = """CREATE TABLE Categories(
   id INT UNSIGNED NOT NULL AUTO_INCREMENT,
   category_name VARCHAR(255) NOT NULL,
   PRIMARY KEY (id)
   ) ENGINE=InnoDB"""

PRODUCTS = """CREATE TABLE Products (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT,
   product_name VARCHAR(255) NOT NULL,
   nutriscore VARCHAR(1) NOT NULL,
   link TEXT NOT NULL,
   details TEXT,
   PRIMARY KEY (id)
) ENGINE=InnoDB"""

FAVORITES = """CREATE TABLE Favorites (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_product_id 
        FOREIGN KEY (Product_id)
        REFERENCES Products(id)

) ENGINE=InnoDB"""

PRODUCT_CATEGORIES = """CREATE TABLE Product_categories (
   product_id INT UNSIGNED NOT NULL,
   category_product_id INT UNSIGNED NOT NULL,

   CONSTRAINT fk_product_id
      FOREIGN KEY (product_id)
      REFERENCES Products(id),

   CONSTRAINT fk_category_product_id INT UNSIGNED NOT NULL,
      FOREIGN KEY (category_product_id)
      REFERENCES Categories(id)
) ENGINE=InnoDB"""

STORE_PRODUCTS = """CREATE TABLE Store_products (
   product_id INT UNSIGNED NOT NULL,
   purchase_store_id INT UNSIGNED NOT NULL,

   CONSTRAINT fk_product_id
      FOREIGN KEY (product_id)
      REFERENCES Products(id)

   CONSTRAINT fk_product_id
      FOREIGN KEY (purchase_store_id)
      REFERENCES Purchase_stores(id)
) ENGINE=InnoDB"""

INSERT_INTO_PRODUCTS = """INSERT INTO Products
   (product_name, nutriscore, link, details)
   VALUES (%(product_name)s, %(nutriscore)s, %(link)s, %(details)s)"""

INSERT_INTO_PURCHASE_STORES = """INSERT INTO Purchase_stores
   (store_name)
   VALUES (%(store_name)s)"""

INSERT_INTO_CATEGORIES = """INSERT INTO Categories
   (category_name)
   VALUES(%(category_name)s)"""

TERMS = ['soda', 'butter', 'peanut butter', 'milk product', 'mayonnaise', 'ketchup', 'barbecue sauce', 'milk'
            'yogurt', 'biscuits', 'chips']

ATTRIBUTES = ['product_name', 'nutriscores', 'link', 'details', 'categories', 'stores']

TABLES = [PURCHASE_STORES, CATEGORIES, PRODUCTS, FAVORITES]

INSERTS = [INSERT_INTO_PRODUCTS, INSERT_INTO_CATEGORIES, INSERT_INTO_PURCHASE_STORES]

