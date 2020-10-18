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
    SELECT * FROM ingredients ORDER BY iid;
"""

select_requires = """
    SELECT * FROM requires ORDER BY rid;
"""

insert_step = """
    INSERT INTO steps (rid, number, direction)
    VALUES (:rid, :number, :step);
"""
