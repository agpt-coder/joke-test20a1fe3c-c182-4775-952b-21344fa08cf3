import random
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class FetchRandomJokeResponse(BaseModel):
    """
    Response model for delivering a randomly selected joke to the user.
    """

    id: str
    content: str


async def fetch_random_joke() -> FetchRandomJokeResponse:
    """
    Fetches a random joke from the database and returns it.

    Args:
        None

    Returns:
        FetchRandomJokeResponse: Response model for delivering a randomly selected joke to the user.
    """
    jokes: List[prisma.models.Joke] = await prisma.models.Joke.prisma().find_many()
    if not jokes:
        return FetchRandomJokeResponse(id="N/A", content="No jokes available.")
    random_joke = random.choice(jokes)
    return FetchRandomJokeResponse(id=random_joke.id, content=random_joke.content)
