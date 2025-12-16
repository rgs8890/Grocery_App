def get_grocery_list():
    '''
    Retreiving the grocery_list from the path specified by the constants variable in utils.py
    '''

    os.makedirs(constants.EXPORT_PATH, exist_ok=True)

    file_path = os.path.join(constants.EXPORT_PATH, f"{constants.GROCERY_LIST}.json")

    if os.path.exists(file_path):
        grocery_list = utils.load_data(file_path)
    
    else:
        print("No JSON path found, creating JSON path")
        grocery_list = []
        utils.save_data(file_path, grocery_list)
    
    return grocery_list


grocery_list = get_grocery_list()


def get_index_from_id(id, grocery_list):
    '''
    Function to get the index from the ID
    '''

    index = 0
    for item in grocery_list:
        if item["id"] == id:
            return index
        else:
            index += 1


def get_index_from_name(name, grocery_list):
    
    index = 0

    for item in grocery_list:
        if item["name"] == name:
            return index
        else:
            index += 1


def add_item(grocery_list, name, store, cost, amount, priority, buy, category = None, expiration_date = None):
    '''
    Adding an item to the grocery list
    '''

    unique_id = int(uuid.uuid4())

    item = {
    "name": name, 
    "store": store, 
    "cost": cost, 
    "amount": amount, 
    "priority": priority, 
    "buy": buy, 
    "category": category, 
    "expiration_date": expiration_date,
    "unique_id": unique_id
    }
    
    grocery_list.append(item)

    file_path = os.path.join(
        constants.EXPORT_PATH, f"{constants.GROCERY_LIST}.json"
    )

    utils.save_data(file_path, grocery_list)
    logging.info(
        f"Added: {name} {store} {cost} {amount} {priority} {buy} {unique_id}"
    )


def search_item(id: int, grocery_list: list) -> None:

    try:
        index = get_index_from_id(id)
        item = grocery_list[index]
        return item
    except IndexError:
        print("Item is not found")
        return None


def remove_item(id, grocery_list):
    index = get_index_from_id(id)

    grocery_list.pop(index)


def edit_item(grocery_list, name, id, store = None, cost = None, amount = None, priority = None, buy = "skip"):
    
    index = get_index_from_id(id)

    old_item = grocery_list[index]

    if not store:
        store = old_item["store"]
    
    if not cost:
        cost = old_item["cost"]
    
    if not amount:
        amount = old_item["amount"]

    if not priority:
        priority = old_item["priority"]
    
    if buy == "skip":
        buy = old_item["buy"]
    
    if not id:
        id = old_item["id"]
    
    item = {
        "name": name,
        "store": store,
        "cost": cost, 
        "amount": amount, 
        "priority": priority, 
        "buy": buy,
        "id": id
        }

    grocery_list[index] = item


def list_items(grocery_list):
    for item in grocery_list:
        print(item)

def calculate_total_cost(list, round_cost = True):
    total_cost = 0
    for item in list:
        if round_cost:
            total_cost += round(item["cost"] * item["amount"])
        else:
            total_cost += (item["cost"] * item["amount"])
    return total_cost
    

def export_items(grocery_list):
    buy_list = []

    os.makedirs(constants.EXPORT_PATH, exist_ok=True)

    file_path = os.path.join(constants.EXPORT_PATH, "export_grocery_list.txt")

    if utils.check_file_exists(file_path):
        print("The file already exists. \n" \
        "The file will be overwritten.")
    
    buy_list = [item for item in grocery_list if item["buy"]]

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
            total_cost = calculate_total_cost(buy_list, round_cost=True)
            file.write(f"The total cost is ${total_cost}\n")

            print(f"Export complete → {file_path}")
    
    except PermissionError as E:
        print("Error: Unable to write to the export file due to permissions.")
        print("Try running the program with different permissions or choose another folder.")
        logging.error("PermissionError while writing to %s: %s", file_path, E)