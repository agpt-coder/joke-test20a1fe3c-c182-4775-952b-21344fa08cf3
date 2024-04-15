import prisma
import prisma.models
from pydantic import BaseModel


class DeleteJokeResponse(BaseModel):
    """
    Acknowledgment response indicating the deletion operation's outcome.
    """

    message: str


async def admin_delete_joke(jokeId: str) -> DeleteJokeResponse:
    """
    Allows an admin to delete an existing joke from the database.

    Utilizes Prisma Client to interact with the database for performing the deletion operation.
    Ensures that the joke exists before attempting to delete it. If the joke doesn't exist or the deletion fails,
    it raises an appropriate HTTPException.

    Args:
        jokeId (str): The unique identifier of the joke to be deleted.

    Returns:
        DeleteJokeResponse: An instance containing a message indicating the outcome of the operation.

    """
    joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
    if not joke:
        raise Exception("Joke not found")
    await prisma.models.Joke.prisma().delete(where={"id": jokeId})
    return DeleteJokeResponse(message=f"Joke with id {jokeId} successfully deleted.")
