from database import Init
import argparse
import sys


class Display():

    def __init__(self):
        self.init = Init()
        self.category_list = self.init.categories.return_categories()
        self.prod_cat = self.init.products.return_prod_cat()

    def input(self, nb, message=""):
        answer = 0
        not_int = True
        while not_int or answer < 0 or answer > nb:
            try:
                answer = int(input(message))
                print('\n')
                not_int = False
            except ValueError:
                print('Entrez un nombre\n')

            if answer < 0 or answer > nb:
                print('Entrez un nombre valide\n')

        return answer

    def disp_categories(self):
        print('Choisissez une categorie\n')
        for i, category in enumerate(self.category_list):
            print("{} - {}".format(i + 1, category))

    def disp_products(self, answer):
        print('Choisissez un produit\n')
        i = 0
        prod_list = []
        for item in self.prod_cat:
            if self.category_list[answer - 1] == item[1]:
                print("{} - {}".format(i + 1, item[0]))
                prod_to_add = (item[0],)
                prod_list.append(prod_to_add)
                i += 1

        return prod_list

    def disp_favs(self, fav_names):
        for i, name in enumerate(fav_names):
            print("{} - {}".format(i + 1, name[0]))

    def disp_details(self, prod):
        print("Nom: {}\nNutriscore: {}\nLien: {}\nDescription: {}\n\
Ou l'acheter?: {}\n".format(prod[0][0], prod[0][1], prod[0][2],
                            prod[0][3], prod[0][4]))


class Interface():

    def __init__(self):
        self.init = Init()
        self.display = None

    def init_db(self):
        parser = argparse.ArgumentParser(description='Chercher et/ou remplacer\
 vos aliments')
        parser.add_argument('--init', help='Initialise la base de donnee',
                            action='store_true')
        args = parser.parse_args()
        if args.init:
            self.init.sync_products()
            self.init.create_tables()
            self.init.insert_datas()
            self.display = Display()
        else:
            print('Vous devez initialiser la base de donnee (--help)')
            sys.exit()

    def print_favs(self):
        fav_names = self.init.favorites.return_fav_names()
        self.display.disp_favs(fav_names)

        if len(fav_names) > 0:
            answer = self.display.input(len(fav_names),
                                        "Choisissez un produit pour\
 afficher sa description: ")
            if answer == 0:
                return 0

            prod_details = self.init.products.return_details(
                fav_names[answer - 1])
            self.display.disp_details(prod_details)

        elif len(fav_names) == 0:
            print("Il n'y a pas de produit(s) sauvegardes")

        return 0

    def initial_menu(self):
        print("Pour revenir au menu initial, appuyez sur 0\n")
        answer = self.display.input(2, '1 - Selectionner une categorie\n\
2 - Aliments sauvegardes\n')

        return answer

    def print_cat_prod(self):
        self.display.disp_categories()
        answer = self.display.input(len(self.display.category_list))
        if answer == 0:
            return answer

        prod_list = self.display.disp_products(answer)
        answer = self.display.input(len(prod_list))
        if answer == 0:
            return answer

        prod_details = self.init.products.return_details(
            prod_list[answer - 1])
        self.display.disp_details(prod_details)
        prod_replace = self.init.products.return_replace((prod_details[0][0],))

        return (prod_details, prod_replace)

    def save_prod(self, prods):
        while True:
            try:
                prod_replace_details = self.init.products.return_details(
                    prods[1][0])
                self.display.disp_details(prod_replace_details)
                replace = input('Voulez-vous le remplacer par ce produit?\
 y/n: ')
            except IndexError:
                print("Sorry, on n'a rien trouve!\n")
                break

            if replace == 'n':
                break
            elif replace == 'y':
                product_names_saved = (prods[0][0][0],
                                       prods[1][0][0])
                self.init.favorites.insert_into_table(product_names_saved)
                print('Votre favori a ete sauvegarde\n')
                break

        return 0
