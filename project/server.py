import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.admin_add_joke_service
import project.admin_delete_joke_service
import project.admin_update_joke_service
import project.fetch_random_joke_service
import project.fetch_user_profile_service
import project.update_user_profile_service
import project.user_login_service
import project.user_registration_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joke-test",
    lifespan=lifespan,
    description="To create a joke API with a single endpoint that returns one joke, leveraging the given tech stack, the steps are as follows: \n\n1. **Programming Language**: Use Python for its simplicity and extensive libraries.\n2. **API Framework**: Implement FastAPI for the API development. FastAPI is chosen for its high performance and ease of use for building APIs with Python.\n3. **Database**: Store the jokes in PostgreSQL. Although a simple API returning one joke might initially not require a database, using PostgreSQL allows for scalability, such as adding more jokes or functionalities in the future.\n4. **ORM (Object-Relational Mapping)**: Utilize Prisma with Python to interact with the PostgreSQL database. Prisma facilitates developing and querying the database schema more efficiently and securely.\n\n**API Development Steps**:\n- Initialize a new FastAPI project.\n- Set up Prisma with PostgreSQL to define the model for a joke. This model will include fields such as `id` and `content`.\n- Create a database migration to generate the jokes table, then populate it with a selection of jokes.\n- Implement an endpoint in FastAPI (e.g., `/joke`) that queries the PostgreSQL database via Prisma to randomly select and return one joke from the table.\n- Ensure proper testing and validation of the endpoint to return jokes correctly. Optionally, add rate limiting to manage request load.\n- Deploy the API to a cloud provider or a local server, depending on the use case and audience.\n\n**Additional Consideration**:\n- For enhancement, you could implement additional endpoints to add, update, or delete jokes, turning the API into a more interactive platform.\n\nThis outline provides a comprehensive approach to developing a joke API with the specified tech stack, focusing on a scalable and efficient deployment.",
)


@app.delete(
    "/admin/jokes/delete/{jokeId}",
    response_model=project.admin_delete_joke_service.DeleteJokeResponse,
)
async def api_delete_admin_delete_joke(
    jokeId: str,
) -> project.admin_delete_joke_service.DeleteJokeResponse | Response:
    """
    Allows admin to delete an existing joke
    """
    try:
        res = await project.admin_delete_joke_service.admin_delete_joke(jokeId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Authenticates a user and returns a token
    """
    try:
        res = await project.user_login_service.user_login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/admin/jokes/update/{jokeId}",
    response_model=project.admin_update_joke_service.AdminUpdateJokeResponse,
)
async def api_put_admin_update_joke(
    jokeId: str, content: str
) -> project.admin_update_joke_service.AdminUpdateJokeResponse | Response:
    """
    Allows admin to update an existing joke
    """
    try:
        res = await project.admin_update_joke_service.admin_update_joke(jokeId, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/admin/jokes/add",
    response_model=project.admin_add_joke_service.AdminAddJokeResponse,
)
async def api_post_admin_add_joke(
    content: str,
) -> project.admin_add_joke_service.AdminAddJokeResponse | Response:
    """
    Allows admin to add a new joke
    """
    try:
        res = await project.admin_add_joke_service.admin_add_joke(content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/register",
    response_model=project.user_registration_service.UserRegistrationResponse,
)
async def api_post_user_registration(
    email: str, password: str, username: Optional[str], role: Optional[str]
) -> project.user_registration_service.UserRegistrationResponse | Response:
    """
    Registers a new user into the system
    """
    try:
        res = await project.user_registration_service.user_registration(
            email, password, username, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/joke", response_model=project.fetch_random_joke_service.FetchRandomJokeResponse
)
async def api_get_fetch_random_joke() -> project.fetch_random_joke_service.FetchRandomJokeResponse | Response:
    """
    Fetches a random joke from the database and returns it
    """
    try:
        res = await project.fetch_random_joke_service.fetch_random_joke()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/me/update",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    name: Optional[str],
    email: Optional[str],
    profile_picture_url: Optional[str],
    bio: Optional[str],
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Updates the profile information of a logged-in user
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            name, email, profile_picture_url, bio
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/me",
    response_model=project.fetch_user_profile_service.FetchUserProfileResponse,
)
async def api_get_fetch_user_profile() -> project.fetch_user_profile_service.FetchUserProfileResponse | Response:
    """
    Retrieves the profile information of a logged-in user
    """
    try:
        res = await project.fetch_user_profile_service.fetch_user_profile()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
