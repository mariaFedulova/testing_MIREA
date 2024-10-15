import unittest
from receipt import Receipt

class TestReceipt(unittest.TestCase):
    """Тест модуля receipt"""

    def setUp(self):
        receipt_from_api = {
            "title": "Морковь по-корейски",
            "ingredients_list": [
                ('Морковь', 100, 100, 10),
                ('Уксус', 10, 10, 1),
                ('Сахар', 7, 7, 2),
                ('Масло подсолнечное', 30, 30, 15),
                ('Перец красный жгучий', 1, 1, 4),
                ('Паприка сладкая', 2, 2, 8),
                ('Карри', 1, 1, 3),
                ('Чеснок', 5, 5, 10),
                ('Лук репчатый', 10, 10, 1)
            ],
        }
        self.receipt = Receipt(receipt_from_api['title'], receipt_from_api['ingredients_list'])

    def test_calc_cost_first(self):
        """Правильно ли считается цена"""
        self.assertEqual(self.receipt.calc_cost(), 54)
    def test_calc_raw_weight(self):
        """Правильно ли считается вес сырого продукта"""
        self.assertEqual(self.receipt.calc_weight(), 166)
    def test_calc_weight(self):
        """Правильно ли считается вес готового продукта"""
        self.assertEqual(self.receipt.calc_weight(raw=False), 166)

    def tearDown(self):
        del self.receipt

if __name__ == "__main__":
    unittest.main(verbosity=2)