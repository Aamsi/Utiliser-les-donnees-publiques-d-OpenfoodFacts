import requests


class Openfoodfacts:

    def __init__(self):
        pass

    def search_product(self, terms):
        products_list = []
        products = []

        for term in terms:
            payload = {
                'search_terms': term,
                'sort_by': 'unique_scans_n',
                'page_size': 10,
                'json': 1
            }

            res = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?',
                            params=payload)
            results = res.json()
            products_list.append(results)

        for prod in products_list:
            product = prod['products']
            products.append(product)

        return products

    def create_dict(self, datas):
        all_products = []
        for data in datas:
            for attribute in data:
                attributes = {
                    'product_name': attribute['product_name_fr'],
                    'nutriscore': attribute['nutrition_grades_tags'][0],
                    'link': 'https://world.openfoodfacts.org/product/{}'.format(attribute['code']),
                    'details': self.generic_name(attribute),
                    'stores': self.filter_store(attribute),
                    'categories': self.filter_category(attribute['categories_tags'])
                }
                all_products.append(attributes)

        return all_products

    def filter_store(self, attribute):
        try:
            return attribute['stores_tags'][0]
        except IndexError:
            return 0

    def filter_category(self, categories):
        for category in categories:
            if category[0:2] == "fr":
                return category[3:]
                break;

        return 0;

    def generic_name(self, attribute):
        try:
            return attribute['generic_name_fr']
        except KeyError:
            return 0
