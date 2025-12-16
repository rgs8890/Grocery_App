import re
import uuid
import os
import logging

import constants
import utils

from grocery_item import GroceryItem

class GroceryList:
    def __init__(self):
        self.grocery_list_path = os.path.join(
            constants.EXPORT_PATH, f"{constants.GROCERY_LIST}.json"
        )

        self.grocery_list = []
        self.set_grocery_list()

    # def load_data(self):
    #     grocery_list = []
    #     json_data = utils.load_data(self.grocery_list_path)

    #     for item in json_data:
    #         grocery_item = GroceryItem()

    def add_item(self, grocery_list, name, store, cost, amount, priority, buy, category = None, expiration_date = None):
        '''
        Adding an item to the grocery list
        '''

        # Generate a random UUID
        unique_id = int(uuid.uuid4())

        grocery_item = GroceryItem()

        grocery_item.name = name
        grocery_item.store = store
        grocery_item.cost = cost
        grocery_item.amount = amount
        grocery_item.priority = priority
        grocery_item.buy = buy
        grocery_item.id = unique_id

        grocery_list = self.get_grocery_list()
        
        self.grocery_list.append(grocery_item)

        file_path = os.path.join(
            constants.EXPORT_PATH, f"{constants.GROCERY_LIST}.json"
        )

        utils.save_data(self.grocery_list_path, self.grocery_list)
        logging.info(
            f"Added: {name} {store} {cost} {amount} {priority} {buy} {unique_id}"
        )

    def edit_item(self, grocery_list, name, id, store = None, cost = None, amount = None, priority = None, buy = "skip"):
    
        index = self.get_index_from_id(id)

        current_item = self.grocery_list[index]

        if name:
            current_item.name = name
        
        if cost:
            current_item.cost = cost
        
        if amount:
            current_item.amount = amount

        if priority:
            current_item.priority = priority
        
        if buy == "skip":
            pass
        else:
            current_item.buy = buy
        
        if id:
           current_item.id = id
        
        utils.save_data(self.grocery_list_path, self.grocery_list)

    def list_items(self, grocery_list):
        '''
        Prints all items in the list.
        Adds the item number to the string.
        '''
        item_num = 1
        
        for item in grocery_list:
            print(item)

    def search_item(self, id: int, grocery_list: list) -> None:
        try:
            index = self.get_index_from_id(id)
            item = grocery_list[index]
            return item
        except IndexError:
            print("Item is not found")
            return None

    def remove_item(self, id, grocery_list):
        
        index = self.get_index_from_id(id)
        
        self.grocery_list.pop(index)

        utils.save_data(self.grocery_list_path, self.grocery_list)


    def get_index_from_name(self, name, grocery_list):  
        index = 0

        for item in grocery_list:
            if item["name"] == name:
                return index
            else:
                index += 1
    
    def get_index_from_id(self, id, grocery_list):
        '''
        Get the index from the given id

        Args:
            id (int): id number from the grocery_list item
        
        Returns:
            int: The index of the grocery item in the grocery_list
        '''
        index = 0
        for item in grocery_list:
            if item.id == id:
                return index
            else:
                index += 1

    def export_items(self, grocery_list):
        buy_list = []

        os.makedirs(constants.EXPORT_PATH, exist_ok=True)

        file_path = os.path.join(constants.EXPORT_PATH, "export_grocery_list.txt")

        if utils.check_file_exists(file_path):
            print("The file already exists. \n" \
            "The file will be overwritten.")
        
        buy_list = [item for item in grocery_list if item.buy]

        if not buy_list:
            print("No items to export")
            return None

        try:
            with open(file_path, "w") as file:
                for idx, item in enumerate(buy_list, start = 1):
                    line = (
                        f"item {idx} | "
                        f"name: {item['name']} | "
                        f"store: {item['store']} | "
                        f"cost: {item['cost']} | "
                        f"amount: {item['amount']} | "
                        f"priority: {item['priority']}\n"
                    )
                    file.write(line)

                # Add a separator line
                file.write("\n")

                # Calculate total cost
                total_cost = self.calculate_total_cost(buy_list, round_cost=True)
                file.write(f"The total cost is ${total_cost}\n")

                print(f"Export complete → {file_path}")
        
        except PermissionError as E:
            print("Error: Unable to write to the export file due to permissions.")
            print("Try running the program with different permissions or choose another folder.")
            logging.error("PermissionError while writing to %s: %s", file_path, E)