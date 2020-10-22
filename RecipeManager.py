
import dbconnect as db
import queries as q

HOST = "reddwarf.cs.rit.edu"
USER = "p320_13"
PASS = "aiyohleiCahc2xahtee1"
PORT = "5432"
LANG = "postgresql"
DATABASE = "%s://%s:%s@%s:%s/%s" % (LANG, USER, PASS, HOST, PORT, USER)

# TODO: Needs error handling on None return value
def login_user(id):
    """
    Returns True if there is a valid user ID in the database. 
    Otherwise, returns False
    
    Parameters
    ----------
    id : int
        user id
    """
    
    res = connect1.execute_query(q.select_users_kwargs, uid=id)
    if res is None:
        return False
    return True

def register():
    """
        Prompts for user information
        Adds user to the database
        If the user wants to log in, head to main menu. If not, 
    """
    
    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    response = input(f'Is your name, {first_name} {last_name}, correct? (Y/N)')

    # If the user confirms that the information is correct, log in or return to the start menu
    if response.upper() == "Y":
        connect1.execute_query(q.insert_user, firstname=first_name, lastname=last_name)
        user_id = connect1.execute_query(q.select_user_id_kwargs, firstname=first_name, lastname=last_name)
        id = user_id.fetchone()[0] # After fetchone(), user_id is changed. Must store in a variable for reuse
        login_prompt = input("Thank you! Your new ID number is: %s. Please remember it for the next time you log in. Would you like to login? (Y/N)" % id)
        if login_prompt.upper() == "Y":
            print("Heading to the main menu...\n")
            main_menu(id)
        elif login_prompt.upper() == "N":
            print("Returning to the start menu...\n")
            start()
            
    # If information is incorrect, user has the option to restart registration
    elif response.upper() == "N":
        print("We apologize for any inconvenience. Let's try again!")
        register()
        
def store_ingredient(ingredient_option, reference_num, uid, **kwargs):
    """
    Handles different commands based on user input.
    
    Parameters
    ----------
    ingredient_option : str
        user's desired action
        
    reference_num : int
        initial command number used as a reference to go back to the previous menu/step
        
    uid : int
        user id
        
    **kwargs : optional
        keyworded arguments (iid, rid, etc.)
    """
    
    # Add ingredient
    if ingredient_option == '1':
        ingredient_name = input("Enter name of the ingredient or leave blank to go back: ")
        if ingredient_name == "":
            print("Returning to options for storing ingredients...\n")
            handle_command(reference_num, uid)
        
        # TODO: Provide loop here to ensure that user is not adding duplicate Ingredient into database
        
        ingredient_unit = input("Enter unit type for ingredient or leave blank to go back: ")
        if ingredient_unit == "":
            print("Returning to options for storing ingredients...\n")
            handle_command(reference_num, uid)
            
        confirm_ingredient = input(f"You want to create a new ingredient called {ingredient_name} measured in {ingredient_unit}? (Y/N)")
        # if Y, insert ingredient into the database
        if confirm_ingredient.upper() == "Y": 
            connect1.execute_query(q.insert_ingredient, iname=ingredient_name, unit=ingredient_unit)
        # if N, restart "Add ingredient" action
        elif confirm_ingredient.upper() == "N": 
            store_ingredient(ingredient_option, reference_num, uid)
            
        confirm_add_ingredient = input("Do you want to add this new ingredient to your storage? (Y/N): ")
        if confirm_add_ingredient.upper() == "Y":
            ingredient_id = connect1.execute_query(q.select_ingredient_id_from_ingredient_name, iname=ingredient_name).fetchone()[0]
            store_ingredient('2', reference_num, uid, iid=ingredient_id, iname=ingredient_name)
        elif confirm_add_ingredient.upper() == "N": # Command finished - nothing else to do, so returns to main menu
            main_menu(uid)
            
    # Add existing ingredient
    elif ingredient_option == '2':
        if kwargs.get('iid', None) is not None:
            ingredient_id = kwargs['iid']
        else:
            ingredient_id = input("Enter the ID for the ingredient or leave blank to go back: ")
            
        if ingredient_id == "":
            handle_command(reference_num, uid)
            
        ingredient_quantity = input("How much are you storing? Leave blank to go back: ")
        if ingredient_quantity == "":
            print("Returning to options for storing ingredients...\n")
            handle_command(reference_num, uid)
            
        print("\nHere are the options for storing ingredients:")
        print("1. Fridge")
        print("2. Pantry")
        print("3. Go back to main menu\n")
        ingredient_location = input("Where are you storing the ingredient?: ")
        if ingredient_location == '1' or ingredient_location == '2':
            ingredient_location = "Fridge" if ingredient_location == '1' else "Pantry"
            confirm_location = input(f"You would like to store {ingredient_quantity} of Ingredient {kwargs['iname']} into the {ingredient_location}? (Y/N): ")
            if confirm_location.upper() == "Y":
                # TODO: Insert into user ingredients
                # Currently ends the script and logs out the user
                pass
            elif confirm_location.upper() == "N":
                print("\nReturning to the entering ingredient ID... ")
                store_ingredient('2', reference_num, uid, iid=None)
                
        elif ingredient_location == '3':
            print("\nReturning to the main menu... ")
            main_menu(uid)
            
    # View list of ALL ingredients
    elif ingredient_option == '3':
        ingredients = connect1.execute_query(q.select_ingredients)
        for x in ingredients:
            print(x)
        print("\nReturning to the main menu... ")
        main_menu(uid)
        
    # Go back to main menu
    elif ingredient_option == '4':
        print("\nReturning to the main menu... ")
        main_menu(uid)
        
    # Default case
    else:
        print("\nInvalid command")
        
def create_new_recipe():
    input("Enter the recipe: \n")
    

def handle_command(num, uid):
    if num == '1':
        print("Select an option for ingredients:")
        print("1. Add new ingredient")
        print("2. Add an existing ingredient")
        print("3. View list of ingredients")
        print("4. Go back to main menu\n")
        ingredient_option = input("What would you like to do? ")
        print(f"You have entered {ingredient_option}")
        store_ingredient(ingredient_option, num, uid)
    elif num == '2':
        # View user's list of ingredients
        pass
    elif num == '3':
        create_new_recipe()
    elif num == '4':
        modify = input("Enter the recipe name you would like to search: \n")
    elif num == '5':
        print("Logging out...")
        return
    else:
        print("Invalid command")

# TODO: Should add another option where they want to exit out of the program
def start():
    """
    Runs when program is booted up.
    
    Returns
    -------
    id
        user id (int) that is used for database manipulation
    """
    
    print("Hello! Welcome to Recipe Manager!")
    id = input("Please log in with your ID number or leave blank if you are a new user: ")
    
    # If invalid input (not an integer or blank), loop until valid.
    while not id.isdigit() and id != "":
        id = input("Please enter a valid ID or leave blank: ")
    
    # Checks if user entered a valid integer and valid id that matches a registered user
    # Otherwise, register the user
    if id.isdigit() and login_user(id) is True: 
        print(f"You are now logged in with ID {id}.\n")
        return id
    else:
        if id == "": 
            register()
    
def main_menu(uid):
    """
    Main menu that lists initial commands
    Passes down initial command number into handle_command() for further actions
    
    Parameters
    ----------
    uid : int
        user id
    """
    
    print("Welcome to the main menu! Here are the possible commands:")            
    print("1. Store an ingredient in refrigerator or pantry")
    print("2. View my list of ingredients")
    print("3. Create a recipe")
    print("4. Search for an existing recipe")
    print("5. Log out\n")
    num = input("What would you like to do? ")
    print(f"You have entered {num}.\n")
    handle_command(num, uid)

if __name__ == "__main__":
    connect1 = db.Connection(DATABASE)
    uid = start()
    main_menu(uid)
    print("Successfully logged out. Have a nice day!")