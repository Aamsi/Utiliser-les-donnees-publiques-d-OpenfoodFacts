from ui import Interface


def main():
    ui = Interface()
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


if __name__ == '__main__':
    main()
