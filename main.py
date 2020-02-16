import core

from SQL_variables import TABLES, TERMS, ATTRIBUTES, INSERTS

#Creating tables
create_tables = core.Create_tables()
create_tables.connect('host', 'username', 'password')
create_tables.use_db('name_db')
create_tables.creating_tables(TABLES)

#Get datas from openfoodfacts API
get_datas = core.Get_datas()

for term in TERMS:
    get_datas.get_json(term)

for attribute in ATTRIBUTES:
    get_datas.get_attribute(attribute)

datas_dictionnary = get_datas.set_dictionnary()

#Put datas in the tables
insert_datas = core.Insert_datas(datas_dictionnary, create_tables.cursor)

for insert in INSERTS:
    insert_datas.insert_datas_products(insert)

#Build interface for user
answer = None
while answer != 1 or answer != 2:
    try:
        answer = input('1: Quel aliment souhaitez vous remplacer?\n', 
                        '2: Retrouver mes favoris')
    except TypeError or answer != 1 or answer != 2:
        print('Vous n\'avez pas choisi une option valable')

if answer == 1:
    category = input('Sélectionnez la catégorie:\n', '1: Sodas\n'
                    '2: Beurres\n', '3: Produits laitiers\n', '4: Sauces\n'
                    '5: Biscuits\n', '6: Chips')
#Get datas from tables and prompt it to user depending on the category

if answer == 2:
    #Get favorites from user in favorites table and prompt it to user