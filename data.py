import requests

payload = {
    
}
res = requests.get("https://world.openfoodfacts.org/api/v0/product/3017620425400.json")

results = res.json()

print(results.keys())

