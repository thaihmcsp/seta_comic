from fastapi import APIRouter

router = APIRouter(
    prefix="/page",
    tags=["page"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@router.get("/chapter/:chapter_id")
async def getListPageOfChapter():
    return [{"chapter_id": 1, "image_url": "....", "page_index": 1}]
