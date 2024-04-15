from typing import Optional

import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Response model for a successful user registration. It confirms the user has been registered but does not expose sensitive information.
    """

    message: str
    user_id: str
    email: str
    username: Optional[str] = None


async def user_registration(
    email: str,
    password: str,
    username: Optional[str] = None,
    role: Optional[str] = None,
) -> UserRegistrationResponse:
    """
    Registers a new user into the system.

    Args:
        email (str): The email address for the user. This must be unique across the userbase.
        password (str): The user's chosen password. This will be hashed before storage for security.
        username (Optional[str]): An optional username for the user. This can be used for display purposes across the platform.
        role (Optional[str]): The initial role of the user in the system. Typically defaults to 'USER' if not specified.

    Returns:
        UserRegistrationResponse: Response model for a successful user registration. It confirms the user has been registered but does not expose sensitive information.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    final_role = (
        prisma.enums.Role.USER if role is None else prisma.enums.Role(role.upper())
    )
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password, "role": final_role}
    )
    return UserRegistrationResponse(
        message="User successfully registered.",
        user_id=new_user.id,
        email=new_user.email,
        username=username,
    )
