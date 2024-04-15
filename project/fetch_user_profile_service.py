from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class FetchUserProfileResponse(BaseModel):
    """
    Response model for a user's profile information. It provides comprehensive details about the user, including ID, email, role, and any other necessary fields defined in the Users table in the database.
    """

    id: str
    email: str
    role: prisma.enums.Role
    createdAt: datetime
    updatedAt: datetime


class Role(Enum):
    ADMIN: str = "ADMIN"
    USER: str = "USER"
    EDITOR: str = "EDITOR"


async def fetch_user_profile() -> FetchUserProfileResponse:
    """
    Retrieves the profile information of a logged-in user.

    This function queries the Prisma ORM to find the first User record from the database, simulating
    fetching the logged-in user's profile information. It returns a comprehensive model of the user's information.

    Note: For a real application scenario, the function should be adapted to identify the user via authentication
    token/session and query by user's unique identifier.

    Returns:
        FetchUserProfileResponse: Response model for a user's profile information, providing details about the user.

    Example:
        # Assuming there is a user logged in and their ID is known,
        # This function would return an instance of FetchUserProfileResponse with the user's details.
    """
    user_record = await prisma.models.User.prisma().find_first()
    if not user_record:
        raise Exception("User not found")
    user_profile = FetchUserProfileResponse(
        id=user_record.id,
        email=user_record.email,
        role=prisma.enums.Role(user_record.role),
        createdAt=user_record.createdAt,
        updatedAt=user_record.updatedAt,
    )
    return user_profile
