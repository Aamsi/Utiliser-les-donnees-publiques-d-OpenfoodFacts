from initdb import Interface

search_terms = ["Snacks", "Pates a tartiner"]

ui = Interface(search_terms)
ui.init_db()
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
