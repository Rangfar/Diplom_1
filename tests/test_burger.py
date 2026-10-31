import pytest
from unittest.mock import Mock

class TestBurger:

    def test_set_buns(self, burger):
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient(self, burger):
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert burger.ingredients == [mock_ingredient]

    def test_remove_ingredient(self, burger):
        burger.ingredients = ["hot sauce", "sour cream", "chili sauce"]
        burger.remove_ingredient(0)
        assert burger.ingredients == ["sour cream", "chili sauce"]

    def test_move_ingredient(self, burger):
        burger.ingredients = ["hot sauce", "sour cream", "chili sauce"]
        burger.move_ingredient(2, 1)
        assert burger.ingredients == ["hot sauce", "chili sauce", "sour cream"]

    @pytest.mark.parametrize("bun_price, ingredient_price, total_price", [
        (100, [], 200),
        (200, [300, 200], 900),
        (300, [200, 300, 100], 1200),
        (100, [100, 100, 200, 200], 800)
    ])
    def test_get_price(self, burger, bun_price, ingredient_price, total_price):
        mock_bun = Mock()
        burger.bun = mock_bun
        mock_bun.get_price.return_value = bun_price
        for ingredient in ingredient_price:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = ingredient
            burger.ingredients.append(mock_ingredient)
        assert burger.get_price() == total_price

    @pytest.mark.parametrize("bun_name, bun_price, ingredient_name, ingredient_price, ingredient_type", [
        ("black bun", 100, ["hot sauce", "cutlet"], [100, 100], ['SAUCE', 'FILLING']),
        ("white bun", 200, ["sour cream", "chili sauce"], [200, 300], ['SAUCE', 'SAUCE']),
        ("red bun", 300, ["dinosaur", "sausage"], [200, 300], ['FILLING', 'FILLING'])
    ])
    def test_get_receipt(self, burger, bun_name, bun_price, ingredient_name, ingredient_price, ingredient_type):
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name   #подмена функции bun.get_name
        mock_bun.get_price.return_value = bun_price #подмена функции bun.get_price
        burger.bun = mock_bun                       #сохранение подмененных функций в настоящую
        for index, ingredient in enumerate(ingredient_name):
            mock_ingredient = Mock()
            mock_ingredient.get_type.return_value = ingredient_type[index]  #подмена функции ingredient.get_type
            mock_ingredient.get_name.return_value = ingredient              #подмена функции ingredient.get_name
            burger.ingredients.append(mock_ingredient)                      #созранение подмененных функций в список ingredients
        price = bun_price * 2 + ingredient_price[0] + ingredient_price[1]   #расчет общей суммы для сверки с отчетом функции
        burger.get_price = Mock(return_value = price)                       #подмена функции burger.get_price

        expected_result = (f'(==== {bun_name} ====)\n'
                           f'= {str(ingredient_type[0]).lower()} {ingredient_name[0]} =\n'
                           f'= {str(ingredient_type[1]).lower()} {ingredient_name[1]} =\n'
                           f'(==== {bun_name} ====)\n\n'
                           f'Price: {price}'
        )
        assert burger.get_receipt() == expected_result
