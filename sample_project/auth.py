class AuthenticationService:

    def login(self, username, password):

        if self.authenticate(username, password):
            return "Login successful"

        return "Invalid credentials"


    def authenticate(self, username, password):

        # Sample authentication logic
        return username == "admin" and password == "password"
