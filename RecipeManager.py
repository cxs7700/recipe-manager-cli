
import queries
import dbconnect

# def login_user(uid ):

def define_name( ):
    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    response = input(f' Your name is {first_name} {last_name} correct?')


    if response.lower() == "yes":
        print("INSERT CODE FOR USERS")
        return "Thank you, your id number is: . Would you like to login is "
    elif response.lower() == "no":
        define_name()


def store_ingedient():
    ingredient = input("Enter an ingedient: \n")




def create_new_recipe():
    input("Enter the recipe: \n")



num = input("Enter the number command: ")

def choice_switcher(num):
    pass


if __name__ == "__main__":
    print("Welcome to Recipe Manager")

    id = input("Please log in with id number or leave blank if you are a new user.")


    # num = input("Enter the number command: ")

    # print("1. Store an ingredient in refrigerator or pantry")
    #
    # print("2. Create a recipe")
    #
    # print("3. Search for recipes using an ingredient or recipe name")
    #
    # print("4. Modify recipes ")

    switcher = {
        1: store_ingedient(),
        2: create_new_recipe(),
        3: input("Enter a recipe name to search: \n"),
        4: input("Enter the change that you want to modify: \n")
    }

