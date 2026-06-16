import bcrypt
from datetime import datetime


class User:

    def __init__(
        self,
        username,
        email,
        password,
        role="admin"
    ):

        self.username = username
        self.email = email

        self.password = self.hash_password(
            password
        )

        self.role = role

        self.created_at = datetime.utcnow()

    # -----------------------------
    # PASSWORD HASHING
    # -----------------------------

    @staticmethod
    def hash_password(password):

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    # -----------------------------
    # PASSWORD VERIFICATION
    # -----------------------------

    @staticmethod
    def verify_password(
        stored_password,
        entered_password
    ):

        return bcrypt.checkpw(
            entered_password.encode("utf-8"),
            stored_password.encode("utf-8")
        )

    # -----------------------------
    # CONVERT TO DICTIONARY
    # -----------------------------

    def to_dict(self):

        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "created_at": self.created_at
        }

