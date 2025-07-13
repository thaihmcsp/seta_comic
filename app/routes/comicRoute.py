from fastapi import APIRouter

router = APIRouter(
  prefix="/comic",
  tags=["comic"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/:comic_id')
async def getComicInfo():
  return {"title": "test", "description": "test txt"}