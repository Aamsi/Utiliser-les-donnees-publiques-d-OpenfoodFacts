import sys
import argparse
import mysql.connector
from mysql.connector import errorcode

from ui import Interface


def main():
    ui = Interface()

    parser = argparse.ArgumentParser(description='Chercher et/ou remplacer\
 vos aliments')
    parser.add_argument('--init', help='Initialise la base de donnée',
                        action='store_true')
    parser.add_argument('--sync', help='Synchronise les données',
                        action='store_true')
    args = parser.parse_args()

    if args.sync & args.init:
        ui.sync_products()
        ui.init_db()
        print("Données d'Openfoodfacts récupérées")
        print('Création des tables et insertion des données\n')
    elif args.init & (not args.sync):
        print("Vous ne pouvez pas initialiser la base de données\
 sans synchroniser les données")
        sys.exit()

    try:
        ui.init_disp()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            print('Vous devez intialiser vos données (--help)')
            sys.exit()

    answer = 0
    while answer == 0:
        answer = ui.initial_menu()
        if answer == 1:
            prods = ui.print_cat_prod()
            if prods == 0:
                answer = prods
                continue
            answer = ui.save_prod(prods)
            continue
        elif answer == 2:
            answer = ui.print_favs()
            if answer == 0:
                continue


if __name__ == '__main__':
    main()
