from pydantic import BaseModel, Field
# (Ф)едулова -> (Ф)о бо
# (М)ария -> (М)орковь по-корейски

class Ingredient(BaseModel):
    """Ингредиент"""
    name:str = Field(min_length=1, alias='name')
    raw_weight:int = Field(gt=0, alias='raw_weight')
    weight:int= Field(gt=0, alias='weight')
    cost:int = Field(gt=0, alias='cost')

class Receipt:
    """Рецепт"""
    def __init__(self, name:str, ingredient_list:list[tuple[str, int, int, int]]) -> None:
        self.name = name
        self.ingredients = [Ingredient(name=elem[0], raw_weight=elem[1],weight=elem[2],cost=elem[3]) for elem in ingredient_list]

    def calc_cost(self, portions=1):
        cost = 0
        for i in range(len(self.ingredients)):
            cost += self.ingredients[i].cost * portions
        return cost

    def calc_weight(self, portions=1, raw=True):
        weight = 0
        for i in range(len(self.ingredients)):
            if raw==True:
                weight += self.ingredients[i].raw_weight * portions
            else:
                weight += self.ingredients[i].weight * portions
        return weight

if __name__ == '__main__':

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
    receipt = Receipt(receipt_from_api['title'], receipt_from_api['ingredients_list'])

    print(receipt.calc_cost(), "руб.")
    print(receipt.calc_weight(), "г")
    print(receipt.calc_weight(raw=False), "г")