import prisma
import prisma.models
from pydantic import BaseModel


class Joke(BaseModel):
    """
    Represents an individual joke record, including id, content, and timestamps.
    """

    id: str
    content: str
    createdAt: str
    updatedAt: str


class AdminUpdateJokeResponse(BaseModel):
    """
    Response model indicating the successful update of a joke, including the updated joke details.
    """

    success: bool
    updatedJoke: Joke


async def admin_update_joke(jokeId: str, content: str) -> AdminUpdateJokeResponse:
    """
    Allows admin to update an existing joke.

    Args:
    jokeId (str): The unique identifier of the joke to be updated.
    content (str): The new content for the joke to be updated.

    Returns:
    AdminUpdateJokeResponse: Response model indicating the successful update of a joke, including the updated joke details.
    """
    joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
    if joke is None:
        return AdminUpdateJokeResponse(success=False, updatedJoke=None)
    updated_joke = await prisma.models.Joke.prisma().update(
        where={"id": jokeId}, data={"content": content}
    )
    updated_joke_model = Joke(
        id=updated_joke.id,
        content=updated_joke.content,
        createdAt=updated_joke.createdAt.isoformat(),
        updatedAt=updated_joke.updatedAt.isoformat(),
    )
    return AdminUpdateJokeResponse(success=True, updatedJoke=updated_joke_model)
