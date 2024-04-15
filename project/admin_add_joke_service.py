import prisma
import prisma.models
from pydantic import BaseModel


class AdminAddJokeResponse(BaseModel):
    """
    Response model for the addition of a new joke. Includes details of the added joke along with a success message.
    """

    success: bool
    message: str
    jokeId: str
    content: str


async def admin_add_joke(content: str) -> AdminAddJokeResponse:
    """
    Allows admin to add a new joke to the database.

    Args:
        content (str): The textual content of the joke to be added to the database.

    Returns:
        AdminAddJokeResponse: Response model for the addition of a new joke. Includes details of the added joke along with a success message.
    """
    try:
        joke = await prisma.models.Joke.prisma().create(data={"content": content})
        response = AdminAddJokeResponse(
            success=True,
            message="Joke successfully added.",
            jokeId=joke.id,
            content=joke.content,
        )
    except Exception as e:
        response = AdminAddJokeResponse(
            success=False,
            message=f"Failed to add joke. Error: {str(e)}",
            jokeId="",
            content=content,
        )
    return response
