import unittest
from receipt import Receipt

class TestReceipt(unittest.TestCase):
    """Тест модуля receipt"""

    def setUp(self):
        receipt_from_api = {
            "title": "Фо Бо",
            "ingredients_list": [
                ('Говядина на косточке', 175, 100, 125),
                ('Говяжья вырезка', 50, 38, 75),
                ('Репчатый лук', 50, 50, 2),
                ('Вода', 500, 500, 15),
                ('Рисовая лапша', 75, 100, 37),
                ('Зеленый лук', 13, 13, 13),
                ('Острый перец', 1, 1, 2),
                ('Лайм', 13, 13, 15),
                ('Петрушка', 13, 13, 14)
            ],
        }
        self.receipt = Receipt(receipt_from_api['title'], receipt_from_api['ingredients_list'])

    def test_calc_cost_first(self):
        """Правильно ли считается цена"""
        self.assertEqual(self.receipt.calc_cost(), 298)
    def test_calc_raw_weight(self):
        """Правильно ли считается вес сырого продукта"""
        self.assertEqual(self.receipt.calc_weight(), 890)
    def test_calc_weight(self):
        """Правильно ли считается вес готового продукта"""
        self.assertEqual(self.receipt.calc_weight(raw=False), 828)

    def tearDown(self):
        del self.receipt

if __name__ == "__main__":
    unittest.main(verbosity=2)