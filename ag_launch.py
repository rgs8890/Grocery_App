import ag_core
import re
import uuid

import constants
import utils

def launch():
    grocery_list = ag_core.get_grocery_list()
    while True:
        command = input("Enter a command (add, remove, edit, search, list, export, quit): ")

        if command == "add":
            name, store, cost, amount, priority, buy = get_inputs()
            ag_core.add_item(grocery_list, name = name, store = store, cost = cost, amount = amount, priority = priority, buy = buy)
        
        if command == "remove":
            handle_remove_command(grocery_list)
        
        if command == "edit":
            handle_edit_command(grocery_list)
        
        if command == "search":
            search_keyword = input("What is the name of the item you would like to search? ") # Day 7 - Task 1
            itemX = ag_core.search_item_name(search_keyword, grocery_list)
            if itemX:
                print(f"These items match your search: {itemX}")
            else:
                print(f"No items match the provided search keyword.")

        if command == "list":
            ag_core.list_items(grocery_list)
        
        if command == "export":
            ag_core.export_items(grocery_list)
        
        if command == "quit":
            break


def get_inputs():
    while True:
        name = input("item name: ")
        if name:
            break
        print("Invalid input. Please enter a valid item")

    while True:
        store = input("Store name: ")
        if store == "skip":
            store = None
            break
        elif store:
            store = store
            break
        print("Invalid input. Please add a valid store name")

    while True:
        try:
            cost = input("item price: ")
            if cost == "skip":
                cost = None
                break
            else:
                cost = float(cost)
                break
        except ValueError:
            print("Invalid input. Please enter a valid price")

    while True:
        try:
            amount = input("Item quantity: ")
            if amount == "skip":
                amount = None
                break
            elif int(amount) > 0:
                amount = int(amount)
                break
            else:
                print("Quantity must be a positive number")
        except ValueError:
            print("Invalid input. Please enter a valid quantity")

    while True:
        try:
            priority = input("Priority: ")
            if priority == "skip":
                priority = None
                break
            elif 1 <= int(priority) <= 5:
                break
            else:
                print("Priority must be between 1 and 5")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5")

    while True:
        try:
            buy = input("Buy: ")
            if buy.lower() =="true":
                buy = True
                break
            elif buy.lower() == "false":
                buy = False
                break
            elif buy == "skip":
                buy = "skip"
                break
            else:
                print("Invalid input. Please enter true or false")
        except ValueError:
            print("Invalid input. Please enter 'true' or 'false'")

    return name, store, cost, amount, priority, buy


def handle_remove_command(grocery_list):
    
    matches = user_input("remove")
    
    if len(matches) > 1:
        match_item = get_match_item(matches, "remove")
        ag_core.remove_item(match_item["id"], grocery_list)
        print(f"The target item has been removed {match_item["name"]}")
    else:
        match_item = matches[0]
        ag_core.remove_item(match_item["id"], grocery_list)
        print(f"The target item has been removed {match_item["name"]}")


def handle_edit_command(grocery_list):
    
    matches = user_input("edit")
            
    if len(matches) > 1:
        match_item = get_match_item(matches, "edit")
        name, store, cost, amount, priority, buy = get_inputs()
        # index = ag_core.get_index_from_name(name)
        # item = ag_core.grocery_list[index]
        # id = item["id"]
        ag_core.edit_item(
            grocery_list,
            name,
            match_item["id"],
            store,
            cost,
            amount,
            priority,
            buy
        )
        print(f"The target item has been edited {match_item["name"]} ")
    else:
        match_item = matches[0]
        print(match_item)
        name, store, cost, amount, priority, buy = get_inputs()
        ag_core.edit_item(
            name,
            match_item["id"],
            store,
            cost,
            amount,
            priority,
            buy
        )
        print(f"The target item has been edited {match_item["name"]} ")


def user_input(action, grocery_list):

    target_item = input(f"Which item would you like to {action}?")
    
    matches = ag_core.search_item_name(target_item, grocery_list)

    if not matches:
        print(f"There are no items with {target_item}")
        return None

    return matches


def get_match_item(matches, action):
    
    match_num = 1

    for match in matches:
        match_string = (
            f"item {match_num} "
            f"| name: {match["name"]} "
            f"| store: {match["store"]} "
            f"| cost: {match["cost"]} "
            f"| amount: {match["amount"]} "
            f"| priority: {match["priority"]} "
            f"| buy: {match["buy"]} "
        )

        print(match_string)
        match_num +=1

    item_num = input(
        f"Which item number do you want to {action}? (ex. 2) "
    )
    
    match_item = matches[int(item_num) - 1]

    return match_item


if __name__ == "__main__":
    launch()
    #print(ag_core.search_item_name('MILK'))