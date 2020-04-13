import requests


class Openfoodfacts:
    """Request data and treat it"""

    def __init__(self):
        self.search_terms = ['Confitures de fruits rouges',
                             'Chocolats en poudre', 'Cookies au chocolat',
                             'Mayonnaises', 'Yaourts aux fruits rouges',
                             'Glaces et sorbets',  'Cookies au chocolat',
                             'Céréales fourrées', 'Céréales au chocolat',
                             'Chips de pommes de terre', 'Limonades']

    def search_product(self):
        products = []

        for search_term in self.search_terms:
            payload = {
                'search_terms': search_term,
                'sort_by': 'unique_scans_n',
                'page_size': 20,
                'json': 1
            }

            res = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?',
                               params=payload)
            results = res.json()
            products.append(results['products'])

        return products

    def create_dict(self):
        products = self.search_product()
        ordered_products = []
        for product in products:
            for attribute in product:
                attributes = {
                    'product_name': attribute['product_name_fr'],
                    'nutriscore': attribute['nutrition_grades_tags'][0],
                    'link': 'https://world.openfoodfacts.org/product/{}'.
                    format(attribute['code']),
                    'details': self.generic_name(attribute),
                    'stores': self.filter_store(attribute),
                    'categories': self.filter_category(attribute)
                }
                ordered_products.append(attributes)

        return ordered_products

    def filter_store(self, attribute):
        try:
            return attribute['stores_tags'][0].strip().capitalize()\
                .replace('-', ' ')
        except (IndexError, KeyError):
            return 'Aucun'

    def filter_category(self, attribute):
        categories = attribute['categories'].split(',')
        for term in self.search_terms:
            for category_to_add in categories:
                category = category_to_add.strip().capitalize()
                if category == term:
                    return category

    def generic_name(self, attribute):
        try:
            return attribute['generic_name_fr']
        except KeyError:
            return 'Aucun'
