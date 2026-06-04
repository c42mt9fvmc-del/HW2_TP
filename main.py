import math

from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList


def show_menu():
    print("\n1. Добавить рецепт")
    print("2. Показать рецепты")
    print("3. Масштабировать рецепт")
    print("4. Добавить рецепт в покупки")
    print("5. Показать покупки")
    print("6. Удалить рецепт из покупок")
    print("0. Выход")


def read_float(text):
    try:
        value = float(input(text))
        if math.isfinite(value):
            return value
        print("Введите обычное число")
        return None
    except ValueError:
        print("Введите число")
        return None


def choose_recipe(recipes):
    if not recipes:
        print("Рецептов пока нет")
        return None

    for n, r in enumerate(recipes, 1):
        print(n, r.title)

    try:
        n = int(input("Номер: "))
        if n < 1:
            raise IndexError
        return recipes[n - 1]
    except (ValueError, IndexError):
        print("Неверный номер")
        return None


def add_recipe(recipes):
    title = input("Название рецепта: ").strip()
    if title == "":
        print("Название не должно быть пустым")
        return

    diet = input("Категория, Enter если нет: ").strip()
    if diet == "":
        recipe = Recipe(title)
    else:
        recipe = DietaryRecipe(title, diet)

    while True:
        name = input("Ингредиент, Enter для конца: ").strip()
        if name == "":
            break

        quantity = read_float("Количество: ")
        if quantity is None:
            continue

        unit = input("Единица: ").strip()
        if unit == "":
            print("Единица не должна быть пустой")
            continue

        try:
            recipe.add_ingredient(Ingredient(name, quantity, unit))
        except ValueError as e:
            print(e)

    if len(recipe) == 0:
        print("Пустой рецепт не добавлен")
        return

    recipes.append(recipe)
    print("Рецепт добавлен")


def show_recipes(recipes):
    if not recipes:
        print("Рецептов пока нет")
        return

    for r in recipes:
        print()
        print(r)


def scale_recipe(recipes):
    recipe = choose_recipe(recipes)
    if recipe is None:
        return

    ratio = read_float("Коэффициент: ")
    if ratio is None:
        return

    try:
        print()
        print(recipe.scale(ratio))
    except ValueError as e:
        print(e)


def add_to_shop(recipes, shop):
    recipe = choose_recipe(recipes)
    if recipe is None:
        return

    portions = read_float("Порции: ")
    if portions is None:
        return

    try:
        shop.add_recipe(recipe, portions)
        print("Добавлено")
    except ValueError as e:
        print(e)


def show_shop(shop):
    items = shop.get_list()
    if not items:
        print("Список покупок пуст")
        return

    for i in items:
        print(i)


def remove_from_shop(shop):
    if not shop._items:
        print("Список покупок пуст")
        return

    title = input("Название рецепта: ").strip()
    if title == "":
        print("Название не должно быть пустым")
        return

    old = len(shop._items)
    shop.remove_recipe(title)
    if len(shop._items) == old:
        print("Такого рецепта в списке покупок нет")
    else:
        print("Удалено")


def main():
    recipes = []
    shop = ShoppingList()

    while True:
        show_menu()
        cmd = input("Выбор: ").strip()

        if cmd == "":
            print("Введите пункт меню")
        elif cmd == "1":
            add_recipe(recipes)
        elif cmd == "2":
            show_recipes(recipes)
        elif cmd == "3":
            scale_recipe(recipes)
        elif cmd == "4":
            add_to_shop(recipes, shop)
        elif cmd == "5":
            show_shop(shop)
        elif cmd == "6":
            remove_from_shop(shop)
        elif cmd == "0":
            print("Выход")
            break
        else:
            print("Нет такой команды")


if __name__ == "__main__":
    main()