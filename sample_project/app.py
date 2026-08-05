from auth import AuthenticationService
from database import Database


def start_application():

    db = Database()
    auth = AuthenticationService()

    db.connect()

    auth.login(
        "admin",
        "password"
    )


if __name__ == "__main__":

    start_application()
