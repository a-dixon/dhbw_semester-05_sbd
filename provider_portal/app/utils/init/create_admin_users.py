from config.config import InitAdminUsers
from app.utils.validation.string_validation import input_validation


def insert_users_from_file(mysql_db):
    """
    Inserts users into the 'users' table from a file.
    """
    # Open and read the file
    with open(InitAdminUsers.ADMIN_USERS_FILE, 'r') as file:
        for line in file:
            # Assuming each line in the file contains username and api_key separated by a comma
            username, api_key = line.strip().split(',')

            if input_validation([username, api_key]):
                # Use the insert_user function
                mysql_db.insert_user(username, api_key)
