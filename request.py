import requests

class RequestDatas:

    def __init__(self):
        self.products = []
        self.terms = ["mayonnaise", "ketchup", "milk", "biscuits", "chips"]

    def search_product(self):
        products_list = []

        for term in self.terms:
            payload = {
                'search_terms': term,
                'sort_by': 'unique_scans_n',
                'page_size': 10,
                'json': 1
            }

            res = requests.get('https://world.openfoodfacts.org/cgi/search.pl?', 
                            params=payload)
            results = res.json()
            products_list.append(results)

        for prod in products_list:
            product = prod['products']
            self.products.append(product)
        
        return self.products