select_users = """
    SELECT * FROM users;
"""

select_users_kwargs = """
    SELECT * FROM users
    WHERE users.uid = :uid;
"""
select_recipes = """
    SELECT * FROM recipes;
"""

select_ingredients = """
    SELECT * FROM ingredients;
"""
