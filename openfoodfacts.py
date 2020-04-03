import requests


class Openfoodfacts:
    """Request data and treat it"""

    def search_product(self, search_terms):
        products = []

        for search_term in search_terms:
            payload = {
                'search_terms': search_term,
                'sort_by': 'unique_scans_n',
                'page_size': 50,
                'json': 1
            }

            res = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?',
                               params=payload)
            results = res.json()
            products.append(results['products'])

        return products

    def create_dict(self, search_terms):
        products = self.search_product(search_terms)
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
        except IndexError:
            return 'Aucun'

    def filter_category(self, attribute):
        categories = attribute['categories'].split(',')
        category = categories[2].strip().capitalize()
        return category

    def generic_name(self, attribute):
        try:
            return attribute['generic_name_fr']
        except KeyError:
            return 'Aucun'
