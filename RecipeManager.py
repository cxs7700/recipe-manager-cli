
import dbconnect as db
import queries as q

HOST = "reddwarf.cs.rit.edu"
USER = "p320_13"
PASS = "aiyohleiCahc2xahtee1"
PORT = "5432"
LANG = "postgresql"
DATABASE = "%s://%s:%s@%s:%s/%s" % (LANG, USER, PASS, HOST, PORT, USER)

# Returns True if there is a valid user ID in the database. Otherwise, returns False
def login_user(id):
    res = connect1.execute_query(q.select_users_kwargs, uid=id)
    if res is None:
        return False
    return True

def register():
    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    response = input(f'Is your name, {first_name} {last_name}, correct? (Y/N)')

    if response.upper() == "Y":
        connect1.execute_query(q.insert_user, firstname=first_name, lastname=last_name)
        user_id = connect1.execute_query(q.select_user_id_kwargs, firstname=first_name, lastname=last_name)
        id = user_id.fetchone()[0]
        login_prompt = input("Thank you! Your new ID number is: %s. Please remember it for the next time you log in. Would you like to login? (Y/N)" % id)
        if login_prompt.upper() == "Y":
            login_user(id)
        elif login_prompt.upper() == "N":
            print("Returning to the main menu...\n")
            start()
    elif response.upper() == "N":
        print("We apologize for any inconvenience. Let's try again!")
        register()

def store_ingredient(ingredient_option, reference_num):
    if ingredient_option == '1':
        ingredient_name = input("Enter name of the ingredient or leave blank to go back: ")
        unit = input("Enter unit type for ingredient or leave blank to go back: ")
    elif ingredient_option == '2':
        ingredient_id = input("Enter the ID for the ingredient or leave blank to go back: ")
        ingredient_quantity = input("Enter the quantity of the ingredient: ")
        print("\n1. Fridge")
        print("2. Pantry")
        print("3. Go back to main menu\n")
        ingredient_location = input("Where are you storing the ingredient?: ")
        if ingredient_location == '1':
            # Fridge
            pass
        if ingredient_location == '2':
            # Pantry
            pass
        if ingredient_location == '3':
            # Go back to enter ID for the ingredient
            print("Returning to Add Existing Ingredient flow...\n")
            store_ingredient('2', reference_num)
            pass
    elif ingredient_option == '3':
        # View list of ingredients
        # Go back to select an option to add an ingredient
        pass
    elif ingredient_option == '4':
        # Go back to main menu
        pass
    else:
        print("Invalid command")
        
def create_new_recipe():
    input("Enter the recipe: \n")

def handle_command(num):
    if num == '1':
        print("Select an option for ingredients:")
        print("1. Add new ingredient")
        print("2. Add an existing ingredient")
        print("3. View list of ingredients")
        print("4. Go back to main menu\n")
        ingredient_option = input("What would you like to do? ")
        print(f"You have entered {ingredient_option}")
        store_ingredient(ingredient_option, num)
    elif num == '2':
        create_new_recipe()
    elif num == '3':
        recipe_name = input("Enter a recipe name to search: \n")
    elif num == '4':
        modify = input("Enter the change that you want to modify: \n")
    else:
        print("Invalid command")

def start():
    print("Hello! Welcome to Recipe Manager!")
    id = input("Please log in with your ID number or leave blank if you are a new user: ")
    
    # Loops if invalid input (integer or blank)
    while not id.isdigit() and id != "":
        id = input("Please enter a valid ID or leave blank: ")
    
    # Checks if user entered a valid integer and valid id that matches a database entry
    if id.isdigit() and login_user(id) is True: 
        print(f"You are now logged in with ID {id}.\n")
    else:
        if id == "": 
            register()

if __name__ == "__main__":
    connect1 = db.Connection(DATABASE)
    start()
    print("Welcome to the main menu! Here are the possible commands:")            
    print("1. Store an ingredient in refrigerator or pantry")
    print("2. Create a recipe")
    print("3. Search for recipes using an ingredient or recipe name")
    print("4. Modify recipes\n")
    num = input("What would you like to do? ")
    print(f"You have entered {num}.\n")
    handle_command(num)
    