from database import (Database, PurchaseStores, Categories, Products,
                      ProductCategories, ProductStores, Favorites, ReturnDatas, Display)
from openfoodfacts import Openfoodfacts

terms = ["Snacks", "Pates a tartiner"]

db = Database('localhost', 'student_p5', 'studentOC97', 'openfoodfacts')

datas = Openfoodfacts(terms)
product_dict = datas.create_dict()

purchase_stores = PurchaseStores(db)
purchase_stores.create_table()
purchase_stores.insert_into_table(product_dict)

categories = Categories(db)
categories.create_table()
categories.insert_into_table(product_dict)

products = Products(db)
products.create_table()
products.insert_into_table(product_dict)

products_categories = ProductCategories(db)
products_categories.create_table()
products_categories.insert_into_table(product_dict)

products_stores = ProductStores(db)
products_stores.create_table()
products_stores.insert_into_table(product_dict)

favorites = Favorites(db)
favorites.create_table()

return_datas = ReturnDatas(db)
category_list = return_datas.return_categories()
prod_cat = return_datas.return_prod_cat()

display = Display()

print("Pour revenir au menu initial, appuyez sur 0\n")
answer = 0
while answer == 0:
    answer = display.input(2, "1 - Selectionner une categorie\n2 - Aliments sauvegardes\n")

    if answer == 1:
        display.disp_categories(category_list)
        answer = display.input(len(category_list))
        if answer == 0:
            continue

        prod_list = display.disp_products(category_list, prod_cat, answer)
        answer = display.input(len(prod_list))
        if answer == 0:
            continue

        prod_details = return_datas.return_details(prod_list[answer - 1])

        display.disp_details(prod_details)
        prod_replace_details = return_datas.return_replace(prod_details[0][1], prod_list)

        while True:
            try:
                display.disp_details(prod_replace_details)
                replace = input("Voulez-vous le remplacer par ce produit? y/n: ")
            except TypeError:
                print("Sorry, on n'a rien trouve!\n")
                break

            if replace == 'n':
                prod_list.remove((prod_replace_details[0][0],))
                prod_replace_details = return_datas.return_replace(prod_details[0][1], prod_list)

            elif replace == 'y':
                product_names_saved = (prod_details[0][0], prod_replace_details[0][0])
                favorites.insert_into_table(product_names_saved)
                print("Votre favori a ete sauvegarde")
                break

        answer = 0
        continue

    if answer == 2:
        fav_names = return_datas.return_fav_names()
        display.disp_favs(fav_names)
        if len(fav_names) > 0:
            answer = display.input(len(fav_names), "Choisissez un produit pour afficher sa description: ")
            if answer == 0:
                continue
            prod_details = return_datas.return_details(fav_names[answer - 1])
            display.disp_details(prod_details)
            answer = 0
            continue
        elif len(fav_names) == 0:
            print("Il n'y a pas de produit(s) dans la liste selectionnee\n")
            answer = 0
            continue
