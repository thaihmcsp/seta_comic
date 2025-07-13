from fastapi import APIRouter

router = APIRouter(
    prefix="/chapter",
    tags=["chapter"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@router.get("/comic/:comic_id")
async def getListChapterOfComic():
    return [{"comic_id": 1, "title": "test", "chapter_number": 1}]
