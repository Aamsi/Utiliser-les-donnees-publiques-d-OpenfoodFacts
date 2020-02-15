import requests

terms = ["coca-cola", "butter", "peanut butter", "milk product", "mayonnaise", "ketchup", "barbecue sauce", "milk"
            "yogurt", "biscuits", "chips"]

payload = {"search_terms": "peanut butter",
        "search_tag": 'nutrition_grades',
        "sort_by": "unique_scans_n",
        "page_size": 10,
        "json": 1}

res = requests.get("https://world.openfoodfacts.org/cgi/search.pl?", params=payload)

results = res.json()
link = res.url

products = results["products"]

print(link)

for product in products:
    print('Nom du produit: ', product["product_name_fr"], '/ Nutriscore: ', product["nutrition_grades"])




