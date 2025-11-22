import ag_core
import re
import uuid
import logging

import constants
import utils
from decimal import Decimal, InvalidOperation
import log_config


def launch():
    grocery_list = ag_core.get_grocery_list()
    print("Welcome to your Agamid Grocery List Manager!")
    while True:
        command = input("Enter a command (add, remove, edit, search, list, export, quit): ")

        if command == "add":
            name, store, cost, amount, priority, buy = get_inputs()
            ag_core.add_item(grocery_list, 
                             name = name, 
                             store = store, 
                             cost = cost, 
                             amount = amount, 
                             priority = priority, 
                             buy = buy)
        
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


def get_line_delimiter():
    print("-----------------")


def get_inputs():
        
    name = get_name_input()
    get_line_delimiter()

    store = get_store_input()
    get_line_delimiter()

    cost = get_cost_input()
    get_line_delimiter()

    amount = get_amount_input()
    get_line_delimiter()

    priority = get_priority_input()
    get_line_delimiter()

    buy = get_buy_input()
    get_line_delimiter()
    
    return name, store, cost, amount, priority, buy


def get_name_input():
    
    name = input("Item Name: ").strip()
    if not name:
        name = constants.NAME_DEFAULT
        
    return name


def get_store_input():

    store = input("Store name: ").strip()
    if store == "skip" or store == "":
        store = constants.STORE_DEFAULT

    return store


def get_cost_input():
    raw = input("Item Price: ").strip()

    # Handle skip / empty
    if raw.lower() == "skip" or raw == "":
        return constants.COST_DEFAULT

    # Try convert to Decimal
    try:
        return Decimal(raw)
    except InvalidOperation:
        print(
            "Invalid input. Please enter a valid price with numbers ONLY,\n"
            "and no currency symbols."
        )
        return get_cost_input()


def get_amount_input():

    amount = input("Item Quantity: ").strip()

    if amount == "skip" or amount == "":
        amount = None
    
    try:
        int(amount)
        if amount > 0:
            return amount
        else:
            print("Please enter a positive number.")
            return get_amount_input()
    except ValueError:
        print(
            "Invalid Input. Please enter a positive number."
        )
        return get_amount_input()


def get_priority_input():

    priority = input("Priority (1-5): ").strip()

    if priority == "skip" or priority == "":
        priority = None
        return priority
    
    try:
        priority = int(priority)
        if 1 <= priority <= 5:
            return priority
        else:
            print("Priority must be between 1 and 5.")
            return get_priority_input()
    except ValueError:
        print("Invalid input. Enter a number between 1 and 5.")
        return get_priority_input()


def get_buy_input():

    try:
        buy = input("Buy: ")
        if buy.lower() == "true":
            buy = True
            return buy
        elif buy.lower() == "false":
            buy = False
            return buy
        elif buy == "skip":
            return None
        else:
            print("Invalid input. Please enter true or false.")
            return get_buy_input()
    except ValueError:
        print("Invalid Input. Please enter 'true' or 'false'")
        return get_buy_input()


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