import dbconnect as db
import queries as q

HOST = "reddwarf.cs.rit.edu"
USER = "p320_13"
PASS = "aiyohleiCahc2xahtee1"
PORT = "5432"
LANG = "postgresql"
DATABASE = "%s://%s:%s@%s:%s/%s" % (LANG, USER, PASS, HOST, PORT, USER)

def input_int(message):
    somein = input(message)
    while not somein.isdigit():
        if somein == '':
            return somein
        print("Was expecting an int or empty string")
        somein = input(message)
    return int(somein)


def login_user(id):
    """
    Returns True if there is a valid user ID in the database.
    Otherwise, returns False

    Parameters
    ----------
    id : int
        user id
    """

    res = connect1.execute_query(q.check_user_exists, uid=id)
    return res[0][0]


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
        id = user_id.fetchone()[0]  # After fetchone(), user_id is changed. Must store in a variable for reuse
        login_prompt = input(
            "Thank you! Your new ID number is: %s. Please remember it for the next time you log in. Would you like to login? (Y/N)" % id)
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


def list_ingredient(uid, reference_num):
    """
    Lists all the user ingredients stored in the database.
    Parameters
    ----------
    uid : int
        user id

    :return:
    """
    print("Displaying all user ingredients")
    ingredients = connect1.execute_query(q.select_user_ingredients, uid=uid)
    for ing in ingredients:
        print(ing)
    response = input("Press enter to return to main menu:")
    if response == "":
        print("\nReturning to the main menu... ")
        main_menu(uid)


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
        ingredient_name = input("Enter name of the ingredient or press enter to go back: ")
        if ingredient_name == "":
            print("Returning to options for storing ingredients...\n")
            handle_command(reference_num, uid)

        ingredient_in_database = connect1.execute_query(q.select_ingredients_by_name, iname=ingredient_name)
        if ingredient_in_database != []:
            print("ERROR! Ingredient is already in database")
            print("Returning to the main menu...\n")
            main_menu(uid)

        ingredient_unit = input("Enter unit type for ingredient or press enter to go back: ")
        if ingredient_unit == "":
            print("Returning to options for storing ingredients...\n")
            handle_command(reference_num, uid)

        confirm_ingredient = input(
            f"You want to create a new ingredient called {ingredient_name} measured in {ingredient_unit}? (Y/N)")
        # if Y, insert ingredient into the database
        if confirm_ingredient.upper() == "Y":
            connect1.execute_query(q.insert_ingredient, iname=ingredient_name, unit=ingredient_unit)
        # if N, restart "Add ingredient" action
        elif confirm_ingredient.upper() == "N":
            store_ingredient(ingredient_option, reference_num, uid)

        confirm_add_ingredient = input("Do you want to add this new ingredient to your storage? (Y/N): ")
        if confirm_add_ingredient.upper() == "Y":
            ingredient_id = connect1.execute_query(q.select_ingredient_id_from_ingredient_name, iname=ingredient_name)
            print("Ingredient ID: ", ingredient_id)
            iid = ingredient_id[0][0]
            store_ingredient('2', reference_num, uid, iid=iid, iname=ingredient_name)
        elif confirm_add_ingredient.upper() == "N":  # Command finished - nothing else to do, so returns to main menu
            main_menu(uid)

    # Add existing ingredient
    elif ingredient_option == '2':
        if kwargs.get('iid', None) is not None:
            ingredient_id = kwargs['iid']
        else:
            ingredient_id = input("Enter the ID for the ingredient or press enter to go back: ")

        if ingredient_id == "":
            handle_command(reference_num, uid)

        ingredient_quantity = input("How much are you storing? Press enter to go back: ")
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
            confirm_location = input(
                f"You would like to store {ingredient_quantity} of Ingredient {kwargs['iname']} into the {ingredient_location}? (Y/N): ")
            if confirm_location.upper() == "Y":
                connect1.execute_query(q.insert_user_ingredients, quantity=int(ingredient_quantity), uid=uid, iid=ingredient_id, location=ingredient_location)
            elif confirm_location.upper() == "N":
                print("\nReturning to the entering ingredient ID... ")
                store_ingredient('2', reference_num, uid, iid=None)
            print("Add successful!\n")
            print("Returning to the main menu...\n")
            main_menu(uid)

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


def create_or_edit_recipe(uid, recipe_id=None):
    recipe_name = input("Enter a name for the recipe: \n")
    if recipe_id is None:
        recipe_id = connect1.execute_query(q.select_new_recipie_id)
    response = input(f'Your recipe name is {recipe_name} with recipe_id: {recipe_id}. Press Y or N to confirm')
    if response.upper() == "N":
        create_or_edit_recipe(uid)
    elif response.upper() == "Y":
        connect1.execute_query(q.insert_or_update_recipe, rid=recipe_id, rname=recipe_name)
        # Loop for feeding in the ingredients
        while True:
            iid = input_int("Enter ingredient id or press enter to finish")

            if iid == "":
                break
            quantity = input_int("Enter Quantity of ingredient")
            connect1.execute_query(q.insert_or_update_requires, rid=recipe_id, iid=iid, quantity=quantity)
        count = 1
        connect1.execute_query(q.delete_steps_for_rec, rid=recipe_id)
        while True:
            step = input(f'Enter step {count} or press enter to finish')
            if step == "":
                break
            connect1.execute_query(q.insert_or_update_step, rid=recipe_id, number=count, direction=step)
            count += 1

    main_menu(uid)

def search_recipe_by_recipe_name(name):
    return connect1.execute_query(q.search_recipe_name, rname=name)

def search_recipe_by_recipe_id(rid):
    return connect1.execute_query(q.search_recipe_id, rid=rid)

def search_recipe_by_ingredient_id(iid):
    return connect1.execute_query(q.search_recipe_ing_id, iid=iid)

def make_recipe(uid, rid):
    sql = """
        SELECT ingredients.iid, requires.quantity FROM requires, ingredients
        WHERE requires.iid = ingredients.iid
        AND requires.rid = :rid;
    """
    if connect1.execute_query(q.ingredients_user_doesnt_have_enough_of, rid=rid, uid=uid):
        return False
    else:
        required_ingredients = connect1.execute_query(sql, rid=rid)
        for x in required_ingredients:
            iid = x[0]
            quantity = x[1]
            # print("iid ", x[0])
            # print("quantity ", x[1])
            connect1.execute_query(q.update_user_ingredients, quantity=quantity, uid=uid, iid=iid)
        # TODO: insert into dates made
        return True

def handle_command(num, uid):
    if num == '1':
        print("Select an option for ingredients:")
        print("1. Add new ingredient")
        print("2. Add an existing ingredient")
        print("3. View list of ingredients")
        print("4. Go back to main menu\n")
        ingredient_option = input("What would you like to store? ")
        print(f"You have entered {ingredient_option}")
        store_ingredient(ingredient_option, num, uid)
    elif num == '2':
        # View user's list of ingredients
        list_ingredient(uid, num)

    elif num == '3':
        create_or_edit_recipe(uid)
    elif num == '4':
        resp = input("Please press A for recipe search by recipe name or press B to search by recipe id or C for ingredient id")
        if resp.upper() == 'A':
            recipe_name = input("Enter the recipe name you would like to search: \n")
            while recipe_name.isdigit() or recipe_name == "":
                recipe_name = input("Please enter a valid recipe name: ")
            recipe_results = search_recipe_by_recipe_name(recipe_name)
        elif resp.upper() == "B":
            recipe_id = input("Enter the recipe id you would like to search: \n")
            recipe_results = search_recipe_by_recipe_id(int(recipe_id))
        elif resp.upper() == "C":
            ingredient_id = input("Enter the ingredient id you would like to search: \n")
            recipe_results = search_recipe_by_ingredient_id(int(ingredient_id))
        else:
            print("Please enter a valid option: ")
            print("Heading to the main menu...\n")
            main_menu(uid)
        if recipe_results == None:
            print("No results found.\n")
        else:
            for x in recipe_results:
                print(x)
            recipe_choice = input_int("Select recipe ID number or leave blank to go to the main menu: ")
            print("1. Make this recipe. ")
            print("2. Modify this recipe. ")
            print("3. Go back")
            recipe_action = input_int("Select an option")
            if recipe_action == '1':
                confirm = input("Make this recipe? This will remove corresponding ingredients from your storage (Y/N): ")
                if confirm.upper() == 'Y':
                    is_made = make_recipe(uid, recipe_choice)
                    if is_made == True:
                        print("Recipe successfully made!")
                    elif is_made == False:
                        print("You do not have enough ingredients to make this recipe.")
                        print("Returning to the main menu...\n")
                        main_menu(uid)
                    else:
                        print("ERROR! Returning to the main menu\n")
                        main_menu(uid)

                elif confirm.upper() == 'N':
                    handle_command(num, uid)
            if recipe_choice == '2':
                # TODO: Wait for create_new_recipe() to finish before redirecting user
                # create_or_edit_recipe(uid, recipe_id=recipe_choice)
                pass
            if recipe_choice == '3':
                print("Going back...")
                handle_command(num, uid)

        print("Returning to the main menu...\n")
        main_menu(uid)

    elif num == '5':
        print("Logging out...\n")
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

    id = input_int("Please log in with your ID number or press enter if you are a new user: ")

    # Checks if user entered a valid integer and valid id that matches a registered user
    # Otherwise, register the user

    if not id:
        register()
    else:
        valid = login_user(id)
        if valid:
            return id
        else:
            print("Please log in with a valid ID")
            start()


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
    print("Hello! Welcome to Recipe Manager!")
    uid = start()
    main_menu(uid)
    print("Successfully logged out. Have a nice day!")
