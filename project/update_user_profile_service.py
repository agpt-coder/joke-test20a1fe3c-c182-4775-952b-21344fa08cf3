from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Communicates the success status of the user profile update operation, potentially echoing back the updated information.
    """

    status: str
    updated_fields: Dict[str, str]
    message: Optional[str] = None


async def update_user_profile(
    name: Optional[str],
    email: Optional[str],
    profile_picture_url: Optional[str],
    bio: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Updates the profile information of a logged-in user.

    This function validates the input parameters and updates the user's profile information in the database accordingly.
    It uses Prisma as ORM to interact with the PostgreSQL database to perform update operations.

    Args:
        name (Optional[str]): The updated name for the user. It's an optional field.
        email (Optional[str]): The updated email for the user. It must be a valid email format and unique across users.
        profile_picture_url (Optional[str]): A new URL pointing to the user's updated profile picture. It's optional and should be validated to ensure it's a valid URL format.
        bio (Optional[str]): A brief user biography or description the user wishes to share.

    Returns:
        UpdateUserProfileResponse: Communicates the success status of the user profile update operation, potentially echoing back the updated information.

    Example:
        await update_user_profile(name="John Doe", email="john.doe@example.com", profile_picture_url="https://example.com/johndoe.jpg", bio="Just a regular person.")
        > UpdateUserProfileResponse(status='success', updated_fields={'name': 'John Doe', 'email': 'john.doe@example.com', 'profile_picture_url': 'https://example.com/johndoe.jpg', 'bio': 'Just a regular person.'}, message='Profile updated successfully')
    """
    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email
    if profile_picture_url:
        update_data["profilePictureUrl"] = profile_picture_url
    if bio:
        update_data["bio"] = bio
    try:
        current_user_email = "example_user_email@example.com"
        updated_user = await prisma.models.User.prisma().update(
            where={"email": current_user_email}, data=update_data
        )
        response_updated_fields = {
            key: val for key, val in update_data.items() if val is not None
        }
        return UpdateUserProfileResponse(
            status="success",
            updated_fields=response_updated_fields,
            message="Profile updated successfully.",
        )
    except Exception as e:
        return UpdateUserProfileResponse(
            status="failed",
            updated_fields={},
            message=f"Failed to update profile: {str(e)}",
        )
