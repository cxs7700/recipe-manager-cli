select_users = """
    SELECT * FROM users;
"""

select_users_kwargs = """
    SELECT * FROM users
    WHERE users.uid = :uid;
"""
