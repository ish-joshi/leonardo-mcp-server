import datetime
import json
import os
import sys
import time

from leonardo_ai_sdk import LeonardoAiSDK
from leonardo_ai_sdk.models.operations import CreateGenerationRequestBody, CreateGenerationRequestBodyTypedDict
from leonardo_ai_sdk.models.shared import JobStatus
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Leonardo AI MCP", "0.1.0", stateless_http=True)


def validate_env_vars():
    """Validate that the required environment variables are set"""
    required_vars = ["LEONARDO_API_KEY"]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Environment variable {var} is not set.")


validate_env_vars()
leo_client = LeonardoAiSDK(bearer_auth=os.getenv("LEONARDO_API_KEY"))


@mcp.tool()
def get_available_models() -> str:
    """Returns a list of available models name, description and model IDs in Leonardo AI. Use this information to select a model for image generation or other tasks."""
    models = leo_client.models.list_platform_models()
    # Trim down the output to reduce context size.
    # Only include model ID, name, and description.
    trimmed_model_info = [
        {
            "id": model.id,
            "name": model.name,
            "description": model.description,
        }
        for model in models.object.custom_models
    ]
    return json.dumps(trimmed_model_info)


@mcp.tool()
def get_generation_job_status(job_id: str) -> str:
    """Returns the status of a specific image generation job in Leonardo AI. Use this to check if the job is still processing, completed, or failed."""
    response = leo_client.image.get_generation_by_id(id=job_id)
    return response.object.model_dump_json(by_alias=True)


@mcp.tool()
def get_current_users_generation_jobs(user_id, last_n: int = 5) -> str:
    """Returns a list of image generation jobs created by the current user in Leonardo AI. This can help you track your previous jobs and their statuses.
    Use the user ID from who_ami tool"""
    response = leo_client.image.get_generations_by_user_id(user_id=user_id, limit=last_n)
    return response.object.model_dump_json(by_alias=True)


@mcp.tool()
def create_image_job(request_overrides: CreateGenerationRequestBodyTypedDict) -> str:
    """Creates an image generation job in Leonardo AI. Focus on providing the necessary parameters for image generation, such as model ID, prompt, and other configurations.
    Most parameters are optional, but you can override them using the request_overrides parameter."""
    request = CreateGenerationRequestBody()
    # Apply overrides from the request
    for key, value in request_overrides.items():
        if hasattr(request, key):
            setattr(request, key, value)

    response = leo_client.image.create_generation(
        request=request
    )

    job_max_wait = 15  # seconds to wait for the job to complete
    # now wait for the job to complete or if a certain timeout is reached
    now = datetime.datetime.now()
    wait_between_polls = 2  # seconds to wait between status checks
    latest_response = response
    while datetime.datetime.now() - now < datetime.timedelta(seconds=job_max_wait):
        status_response = leo_client.image.get_generation_by_id(id=response.object.sd_generation_job.generation_id)
        current_status = status_response.object.generations_by_pk.status
        if current_status in [JobStatus.COMPLETE, JobStatus.FAILED]:
            latest_response = status_response
            break
        time.sleep(wait_between_polls)

    return latest_response.object.model_dump_json(by_alias=True)


@mcp.tool()
def who_ami() -> str:
    """Returns the details of the user connected to Leonardo AI"""
    user = leo_client.user.get_user_self().object
    print(f"User details: {user.model_dump_json()}")
    return "You are connected as: " + user.model_dump_json(by_alias=True)


def get_mode():
    """Determine the mode to run: 'stdio' or 'http'. Defaults to 'http'."""
    # Priority: command-line arg > env var > default
    if len(sys.argv) > 1 and sys.argv[1] in ("stdio", "http"):
        return sys.argv[1]
    return os.getenv("MCP_MODE", "http")


def main():
    mode = get_mode()
    if mode == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
