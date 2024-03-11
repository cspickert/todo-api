import os
from typing import Annotated

from fastapi import Header, Request, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from readme_metrics.VerifyWebhook import VerifyWebhook

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Webhooks


README_SECRET = os.getenv("README_SECRET")


@router.post(
    "/readme",
    status_code=status.HTTP_200_OK,
    description="Handle ReadMe webhooks",
)
async def readme_webhook(
    request: Request,
    readme_signature: Annotated[str | None, Header()] = None,
) -> dict:
    # Verify the request is legitimate and came from ReadMe.
    try:
        VerifyWebhook(await request.json(), readme_signature, README_SECRET)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid ReadMe webhook: {error}",
        )
    # Fetch the user from the database and return their data for use with OpenAPI variables.
    # user = User.objects.get(email__exact=request.values.get("email"))
    return {
        # OAS Security variables
        "HTTPBearer": "HTTPBearer",
    }
