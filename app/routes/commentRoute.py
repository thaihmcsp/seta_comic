from fastapi import APIRouter

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/comic/:comic_id")
async def listComment():
    return [{"user_id": 1, "comic_id": 1, "chapter_id": 1, "content": "test"}]
