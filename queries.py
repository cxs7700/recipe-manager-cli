select_users = """
    SELECT * FROM users;
"""

select_users_kwargs = """
    SELECT * FROM users
    WHERE users.uid = :uid;
"""
select_recipies = """
    SELECT * FROM recipies;
"""

select_ingredients = """
    SELECT * FROM ingredients;
"""
