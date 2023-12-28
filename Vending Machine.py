from datetime import datetime
import pyttsx3

items = [ #The list of ID, Item, and Price of the vending machine
    {"ID": 1, "Item": "Snickers", "Price": 3.00},
    {"ID": 2, "Item": "Clif Bar", "Price": 5.50},
    {"ID": 3, "Item": "Pop Tarts", "Price": 2.50},
    {"ID": 4, "Item": "Sun Chips", "Price": 3.00},
    {"ID": 5, "Item": "7UP", "Price": 3.25},
    {"ID": 6, "Item": "Reese’s Chocolate", "Price": 5.00},
    {"ID": 7, "Item": "Planters Trail Mix", "Price": 4.00},
    {"ID": 8, "Item": "Pepsi", "Price": 2.50},
    {"ID": 9, "Item": "Mountain Dew", "Price": 2.50},
    {"ID": 10, "Item": "Gatorade", "Price": 8.00}
]

def Voice(text):
    print("Fred : "+text)
    engine = pyttsx3.init() #Initializes the text-to-speech engine
    voices = engine.getProperty('voices') #Access to available voices
    engine.setProperty('voice', voices[0].id) #Sets the voice to the engine
    engine.say(text) #Makes the engine say the provided text
    engine.runAndWait() #Waits for the engine's speech to finish

def print_current_datetime():
    now = datetime.now() #uses the imported datetime
    hour = now.hour #used to get the hour from the time
    
    if hour >= 0 and hour < 12: #if/elif statements to check if it's morning or evening
        am_pm = "AM"
    elif hour >= 12 and hour < 24:
        am_pm = "PM"
        
    date_time = now.strftime("%d/%m/%Y %H:%M:%S") #sets the format of the date and time
    
    print("               ", date_time, am_pm, "               ")

def display_items(items, currency_symbol):
    print("------------ FRED'S VENDING MACHINE MENU ------------")
    for item in items: #This for loop shows the Menu
        print(f"Item ID: {item['ID']} | Item: {item['Item']} | Price: {currency_symbol}{item['Price']}")
    print("------------------------------------------------------------\n")

def select_currency():
    currencies = {'USD': "$", 'EUR': "€", 'PHP': "₱", 'AED': "AED"} #Currency stored in dict
    while True:
        print("Available currencies: USD, EUR, PHP, AED")
        selected_currency = input("Select your preferred currency: ").upper()
        if selected_currency in currencies: 
            symbol = currencies[selected_currency]
            print(f"Selected currency symbol: {symbol}")
            print()
            return currencies[selected_currency]
        else:
            print("Invalid currency. Please choose from the available options.")
            print()

def view_cart(cart, currency_symbol):
    if not cart: #if the cart is empty
        print("Your cart is empty.")
        print()
    else:
        print("------------------------- Your Cart -------------------------")
        for item in cart: #This for loop shows the items in the cart
            print(f"Item: {item['Item']} | Quantity: {item['Quantity']} | Total Price: {currency_symbol}{item['TotalPrice']}")
        print(f"\nTotal Amount Due: {currency_symbol}{sum(item['TotalPrice'] for item in cart)}")
        print("--------------------------------------------------------------\n")

def purchase_items(items, currency_symbol):
    
    selected_items = [] #The list where all the items the user chooses will go to
    Voice("Fred's vending machine menu.")
    print()
    
    while True:
        display_items(items, currency_symbol) #Displays the menu
        view_cart(selected_items, currency_symbol) #Displays the cart

        ID_input = input("Enter the ID of the item you want to add/remove (or 'q' to finish): ")
        
        if ID_input.isdigit():
            item_id = int(ID_input) #stored the variable ID_input in another variable
            selected_item = None
            
            for item in items: #This loop is to search if the ID exist in the items list
                if item['ID'] == item_id:
                    selected_item = item
                    break
                
            if selected_item: #If the loop finds that the ID exist then it's true
                quantity = int(input(f"Enter the quantity of {selected_item['Item']} (or '0' to remove): "))
                if quantity > 0:
                    existing_item = None
                    
                    for item in selected_items: #This loop is to search if the ID exist in the selected_items list
                        if item['ID'] == item_id:
                            existing_item = item
                            break
                        
                    if existing_item: #If the loop finds that the ID exist in the selected_items then it's true
                        existing_item['Quantity'] += quantity #Adds whatever is in the 'Quantity' key to the quantity
                        existing_item['TotalPrice'] += quantity * selected_item['Price'] #Adds whatever is in the 'TotalPrice' key to the quantity then multiply it to the selected_items['Price']
                    else: #append all data to selected_items
                        selected_items.append({
                                                'ID': selected_item['ID'],
                                                'Item': selected_item['Item'],
                                                'Quantity': quantity,
                                                'TotalPrice': quantity * selected_item['Price']
                                             })
                    print()
                    Voice(f"{quantity} {selected_item['Item']} added to your cart.")
                    print()
                elif quantity == 0:
                    selected_items = [item for item in selected_items if item['ID'] != item_id] #Removes the item in selected_items
                    print()
                    Voice(f"{selected_item['Item']} removed from your cart.")
                    print()
                else:
                    print("Invalid quantity. Please enter a non-negative integer.")
            else:
                print("Invalid item ID. Please try again.")
        elif ID_input.lower() == 'q': #The while loop breas if the user type 'q'
             break
        else:
            print("Invalid input. Please enter a valid item ID or 'q' to finish.")

    return selected_items

def generate_receipt(purchased_items, total_amount_due, currency_symbol):
    print("\n----------------------- Receipt -----------------------")
    for item in purchased_items:
        print(f"Item ID: {item['ID']} | Item: {item['Item']} | Quantity: {item['Quantity']} | Price: {currency_symbol}{item['TotalPrice']}")
    print()
    Voice(f"Total Amount: {currency_symbol}{total_amount_due}")
    
    print()
    print_current_datetime()
    print("-----------------------------------------------------\n")

def vending_machine():
    currency_symbol = select_currency()
    selected_items = purchase_items(items, currency_symbol)

    view_cart(selected_items, currency_symbol) #Displays the cart
    receipt = input("Do you want to print the receipt? (yes/no): ")
    if receipt.lower() == "yes": #If 'yes' then the receipt will generate
        generate_receipt(selected_items, sum(item['TotalPrice'] for item in selected_items), currency_symbol)
        Voice("Thank you for using Fred's Vending Machine!")   
    else: #else it will not
        Voice("Thank you for using Fred's Vending Machine!") 

Voice("Welcome to Fred's vending machine, please enter a valid currency") #Calls the Voice() function
print()
vending_machine() #The main code
while True: #Loop that loop through the whole code if the user will type yes, otherwise the code will end
    get_more = input("Do you want to buy again? (yes/no): ")
    print()
    if get_more.lower() == "yes":
        vending_machine()
    elif get_more.lower() == "no":
        Voice("Come back again next time!") 
        break