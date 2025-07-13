from fastapi import APIRouter

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("/")
async def addFavorite():
    return "added"
