def test_create_user(db):
    """
    Test the user creation process.
    Main test steps:
    1 - Create a user with the given email and username.
    2 - Check if the user was created successfully by verifying its existence in the database.
    """
    pass

def test_remove_user(db):
    """
    Test the user removal process.
    """
    pass

def test_check_if_email_exists(db):
    """
    Test the email existence check process.
    Main test steps:
    1 - Assure no user exists with the email to be tested.
    2 - Create a user with the email to be tested.
    3 - Check if the email existence check returns True.
    4 - Check if the email existence check returns False for a non-existing email.
    """
    pass

def test_check_if_user_exists(db):
    """
    Test the user existence check process.
    Main test steps:
    1 - Assure no user exists with the username to be tested.
    2 - Create a user with the username to be tested.
    3 - Check if the user existence check returns True.
    4 - Check if the user existence check returns False for a non-existing username.
    """
    pass
