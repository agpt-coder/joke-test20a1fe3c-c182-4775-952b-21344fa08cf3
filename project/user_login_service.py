from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Response model for the login endpoint. Contains either the authentication token for the session or an error message in case of a failed login attempt.
    """

    token: str
    error: Optional[str] = None


async def user_login(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user by checking their email and password against the database, and returns a token
    or an error message if the authentication fails.

    Args:
        email (str): The email address supplied by the user for login.
        password (str): The password supplied by the user for login. In a real application, this password
            would need to be securely hashed and compared against a stored hash.

    Returns:
        UserLoginResponse: Response model for the login endpoint. Contains either the authentication token
        for the session or an error message in case of a failed login attempt.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        token = f"secure-token-for-{user.id}"
        return UserLoginResponse(token=token)
    else:
        return UserLoginResponse(token="", error="Invalid email or password")
