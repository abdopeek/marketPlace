"""
Text file has 2 lines, first is inventory, second is just zero
Changes made:
    1- Turned the inventory to a txt file and got the add/remove working
    2- Got the process coins working, returns amount of bills and coins
    3- Minor bugs like program won't exit when told to, shopping doesn't end, if-statement rearrangements, etc
"""

admin_user_id = {
    "abdulrahem": '1111',
    "humaid": '2222',
    "chris": '3333'
}

profit = 0
customer_total = 0

receipt = {}

print("Welcome to our supermarket! Enjoy!!!")


def admin_login():
    admin_login_username = input("Please enter your Username: ")
    admin_login_password = input("Please Input Your Password: ")
    if admin_login_username in admin_user_id and admin_login_password == admin_user_id[admin_login_username]:
        print("Admin Login successful\nWelcome {}".format(admin_login_username))
        return True
    else:
        print("Login unsuccessful. Invalid Username/Password")
        return False


def add_inventory():
    with open('inventory.txt', 'r') as inv:
        file = inv.readlines()  # Returns content as a list
        tmp = dict(eval(file[0]))  # Turn string into dictionary
        print(f"Current inventory is: {tmp}")
        inv.close()
    with open('inventory.txt', 'w') as inv:
        item_name = input("Enter item name: ").lower()
        item_price = float(input("Enter item price: "))
        tmp[item_name] = item_price
        file[0] = str(tmp) + '\n'  # Turn string to dict and add a new line at the end
        inv.writelines(file)
        inv.close()


def remove_inventory():
    # Basically same as above function
    item_name = input("Item to remove: ").lower()
    with open('inventory.txt', 'r') as inv:
        file = inv.readlines()
        tmp = dict(eval(file[0]))
        inv.close()
    with open('inventory.txt', 'w') as inv:
        if item_name in tmp:
            del tmp[item_name]
            file[0] = str(tmp) + '\n'
            inv.writelines(file)
            inv.close()
            print(f"{item_name} deleted successfully")
        else:
            print("Item does not exist")


# Return something like => "Your change is X, you've been given Y bills and Z coins"
# Return value is (Bool -> True if transaction has went through, Dict -> Contains amount of bills and coins to return)
def process_coins(money_inserted, price):
    global profit
    bills = [200, 100, 50, 20, 10, 5, 1]
    coins = [50, 25, 10, 5, 1]
    returned = {'cash': 0, 'coins': 0}
    if money_inserted < price:
        print("sorry, that's not enough money, money refunded")
        return False, 0

    else:
        change = money_inserted - price
        for bill in bills:
            while (change - bill) >= 0:
                change -= bill
                returned['cash'] += 1

        change = change * 100  # To avoid floating number errors
        for coin in coins:
            while (change - coin) >= 0:
                change -= coin
                returned['coins'] += 1
        return True, returned


def view_inventory():
    with open('inventory.txt', 'r') as inv:
        file = inv.readlines()
        print(file[0])


def admin_interface():
    if admin_login():
        while True:
            admin_action_options = input("Which action do you want to perform?\nAdd an item (0)"
                                         "\nRemove an item(1)\nView inventory (2)\nINPUT A NUMBER: ")
            if admin_action_options == "exit":
                return 0

            if len(admin_action_options) == 0 or not admin_action_options.isdigit():
                print("Please input a number or 'exit'")

            elif admin_action_options == "0":
                add_inventory()
                continue

            elif admin_action_options == "1":
                remove_inventory()
                continue

            elif admin_action_options == "2":
                view_inventory()
                continue


def customer_interface():
    global customer_total
    print("Here are the available items")
    with open('inventory.txt', 'r') as tmp:
        file = tmp.readlines()
        inventory = dict(eval(file[0]))
        tmp.close()

    for item, price in inventory.items():
        print(f"Item: {item.capitalize()} | Price: ${price}")

    done_shopping = False
    while not done_shopping:
        user_choice = input("What would you like to buy? ('exit' to cancel, (1) to view basket, or (0) to proceed to checkout): ").lower()
        if user_choice == "exit":
            return 0
        if user_choice == '0':
            done_shopping = True
        elif user_choice == '1':
            print(receipt)
        elif user_choice not in inventory:
            print("Item Not available")
        else:
            user_quantity = float(input("How much would you like to buy: "))
            receipt[user_choice] = user_quantity
            customer_total += inventory[user_choice]*user_quantity

    if done_shopping:
        customer_total = round(customer_total, 2)
        if customer_total > 0:
            print("Your total is {}".format(customer_total))
            paid = float(input("Please insert cash: "))
            is_money_enough, change = process_coins(paid, customer_total)
        if is_money_enough:
            print(f"Please take your change, make sure it consists of {change['cash']} bills and {change['coins']} coins")
            print("You can pick up your items\nThank you for shopping with us")
            customer_total = 0
            return 0


exit_application = False
while not exit_application:
    is_user_customer = (input("Press '0' for customer or '1' for admin: "))

    if is_user_customer == "exit":
        break
    if is_user_customer.isdigit():
        is_user_customer = int(is_user_customer)

        if is_user_customer == 1:
            admin = admin_interface()
            if admin == 0:
                exit_application = True

        elif is_user_customer == 0:
            user = customer_interface()
            if user == 0:
                exit_application = True
        else:
            print('Please enter a valid option')
    else:
        print("Please enter a valid option.")

