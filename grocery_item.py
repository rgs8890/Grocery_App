import constants

'''
Getters
- while we add our getter and setter methods
- simply use @property decorator
- over a method with the attribute name
- and return the value of the protected attribute

'''

# class GroceryItem:
#     def __init__(self, name, store, cost, amount, priority, buy, item_id):
#         self.name = name
#         self.store = store
#         self.cost = cost
#         self.amount = amount
#         self.priority = priority
#         self.buy = buy
#         self.id = item_id

class GroceryItem:
    def __init__(self):
        self._name = constants.NAME_DEFAULT
        self._store = constants.STORE_DEFAULT
        self._cost = constants.COST_DEFAULT
        self._amount = constants.AMOUNT_DEFAULT
        self._priority = constants.PRIORITY_DEFAULT
        self._buy = constants.BUY_DEFAULT
        self._id = constants.ID_DEFAULT
    
    @property
    def name(self):
        return self._name
    
    @property
    def store(self):
        return self._store

    @property
    def cost(self):
        return self._cost

    @property
    def amount(self):
        return self._amount
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def buy(self):
        return self._buy
    
    @property
    def id(self):
        return self._id
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        self._name = value
    
    @priority.setter
    def priority(self, value):
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        if not value:
            pass

        if not isinstance(value, int):
            raise ValueError(f"Priority must be an int, {value}")
        
        if p_min <= value <= p_max:
            pass
        else:
            raise ValueError(f"Priority must be between {p_min} and {p_max} ")
        self._priority = value
    
    @buy.setter
    def buy(self, value):
        if not isinstance(value, bool):
            raise ValueError("Buy must be a boolean.")
        self._buy = value
    
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer.")
        self._id = value
    
    @cost.setter
    def cost(self, value):
        if not isinstance(value, float):
            raise ValueError("Cost must be a float.")
        self._cost = value
    
    @store.setter
    def store(self, value):
        if not isinstance(value, str):
            raise ValueError("Store must be a string.")
        self._store = value

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            raise ValueError("Amount must be an integer.")
        self._amount = value