from fastapi import APIRouter

router = APIRouter(
  prefix="/category",
  tags=["category"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/')
async def listCategories():
  return ['war', 'school']