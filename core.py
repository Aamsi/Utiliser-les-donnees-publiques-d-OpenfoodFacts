import mysql.connector
from mysql.connector import errorcode

import requests

from SQL_variables import TERMS


class Create_tables:
    """Create tables for database"""

    def __init__(self):
        self.cursor = None

    def connect(self, host, user, password):
        """Connect to mysql server"""
        cnx = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = cnx.cursor()

    def use_db(self, database):
        """To use a database"""
        self.cursor.execute('USE {}'.format(database))

    def creating_tables(self, tables):
        """Creating tables"""
        for table in tables:
            try:
                self.cursor.execute(table)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)


class Get_datas:
    """Get datas from openfoodfacts API"""

    def __init__(self):
        self.products = None
        self.product_name = []
        self.nutriscores = []
        self.categories = []
        self.links = []
        self.stores = []
        self.details = []
        self.dictionnary_datas = []

    def get_json(self, term):
        """Get datas in json format from openfoodfacts API"""
        payload = {
            'search_terms': term,
            'sort_by': 'unique_scans_n',
            'page_size': 10,
            'json': 1
        }

        res = requests.get('https://world.openfoodfacts.org/cgi/search.pl?', 
                        params=payload)
        results = res.json()
        products_list = results['products']

        self.products = products_list

    def get_attribute(self, attribute_name):
        """Get attribute we need from openfoodfacts API"""
        for product in self.products:
            try:
                attribute = product[attribute_name]
            except KeyError:
                attribute = 0

            # J'aime pas du tout mais je vois pas comment faire autrement
                if attribute_name == 'product_name':
                    self.product_name.append(attribute)
                elif attribute_name == 'nutriscores':
                    self.nutriscores.append(attribute)
                elif attribute_name == 'link':
                    self.links.append(attribute)
                elif attribute_name == 'details':
                    self.details.append(attribute)
                elif attribute_name == 'categories':
                    self.categories.append(attribute)
                elif attribute_name == 'stores':
                    self.stores.append(attribute)

    def set_dictionnary(self):
        """Create dictionnary to insert datas into the db"""
        i = 0
        for item in self.product_name:
            line = {
                'product_name': item,
                'nutriscore': self.nutriscores[i],
                'link': self.links[i],
                'details': self.details[i],
                'categories': self.categories[i],
                'stores': self.stores[i]
            }

            self.dictionnary_datas.append(line)

            i += 1

            return self.dictionnary_datas


class Insert_datas:

    def __init__(self, datas, cursor):
        self.datas = datas
        self.cursor = cursor

    def insert_datas_products(self, insert_into_products):
        for data in self.datas:
            self.cursor.execute(insert_into_products, data)
