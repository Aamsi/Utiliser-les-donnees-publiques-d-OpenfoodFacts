from database import (Database, PurchaseStores, Categories, Products,
                      ProductCategories, ProductStores, Favorites, Interface)
from openfoodfacts import Openfoodfacts

terms = ["Snacks sucres", "Pates a tartiner"]

db = Database('localhost', 'student_p5', 'studentOC97', 'openfoodfacts')

datas = Openfoodfacts()
products_data = datas.search_product(terms)
data_dict = datas.create_dict(products_data)

purchase_stores = PurchaseStores(db)
purchase_stores.create_table()
purchase_stores.insert_into_table(data_dict)

categories = Categories(db)
categories.create_table()
categories.insert_into_table(data_dict)

products = Products(db)
products.create_table()
products.insert_into_table(data_dict)

products_categories = ProductCategories(db)
products_categories.create_table()
products_categories.insert_into_table(data_dict)

products_stores = ProductStores(db)
products_stores.create_table()
products_stores.insert_into_table(data_dict)

favorites = Favorites(db)
favorites.create_table()

interface = Interface(db)
category_list = interface.return_categories()
prod_cat_store = interface.return_prod_cat_store()

answer = int(input('1 - Selectionner une categorie\n2 - Aliments sauvegardes\n'))

if answer == 1:
    print("Choisissez une categorie\n")

    for i, category in enumerate(category_list):
        print("{} - {}".format(i + 1, category))
    answer = int(input())

    print("Choisissez un produit\n")
    i = 0
    prod_list = []
    for el in prod_cat_store:
        if category_list[answer - 1] == el[1]:
            print("{} - {}".format(i + 1, el[0]))
            tuple_to_add = (el[0],)
            prod_list.append(tuple_to_add)
            i += 1

    answer = int(input())

    prod_details = interface.return_details(prod_list[answer - 1])

    print("Nom: {}\nNutriscore: {}\nLien: {}\nDescription: {}\nOu l'acheter?: {}\n".format(prod_details[0][0],
                                                                  prod_details[0][1],
                                                                  prod_details[0][2],
                                                                  prod_details[0][3],
                                                                  prod_details[0][4]))

    prod_replace_details = interface.return_replace(prod_details[0][1], prod_list)

    try:
        print("Nom: {}\nNutriscore: {}\nLien: {}\nDescription: {}\nOu l'acheter?: {}\n".format(prod_replace_details[0][0],
                                                                  prod_replace_details[0][1],
                                                                  prod_replace_details[0][2],
                                                                  prod_replace_details[0][3],
                                                                  prod_replace_details[0][4]))

        replace = input("Voulez-vous le remplacer par ce produit? y/n\n")
    except TypeError:
        print("Sorry, on n'a rien trouve!")

    if replace == 'y':
        product_names_saved = (prod_details[0][0], prod_replace_details[0][0])
        print(product_names_saved)
        favorites.insert_into_table(product_names_saved)

if answer == 2:
    fav_names = interface.return_fav_names()
    for i, name in enumerate(fav_names):
        print("{} - {}".format(i + 1, name[0]))

    answer = int(input("Choisissez un produit pour afficher sa description: "))

    prod_details = interface.return_details(fav_names[answer - 1])

    print("Nom: {}\nNutriscore: {}\nLien: {}\nDescription: {}\nOu l'acheter?: {}\n".format(prod_details[0][0],
                                                                  prod_details[0][1],
                                                                  prod_details[0][2],
                                                                  prod_details[0][3],
                                                                  prod_details[0][4]))

