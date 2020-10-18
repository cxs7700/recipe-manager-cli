print("Welcome to Recipe Manager")

print("Here are the commands that you can use")

print("1. Store an ingredient in refrigerator or pantry")

print("2. Create a recipe")

print("3. Search for recipes using an ingedient or recipe name")

print("4. Modify recipes ")

num = input("Enter the number command: ")

def choice_switcher(num):
     switcher = {
        1: input("Enter an ingedient: \n"),
        2: input("Enter the recipe: \n"),
        3: input("Enter a recipe name to search: \n"),
        4: input("Enter the change that you want to modify: \n")
    }
if __name__ == "__main__":
    while True:
        num = input("Enter the number command: ")
        choice_switcher(num)