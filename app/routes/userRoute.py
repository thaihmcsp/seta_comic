from typing import Optional
from fastapi import APIRouter, Depends, Form, Query, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException, Body, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.userService import listUser, getUserByUserId, searchAuthorByText, searchAuthorByText, changePassword, updateUser
from ..core.dependencies import get_current_user, oauth2_scheme
from ..models.usersModel import User
from ..schemas.user import UserOut
from app.db.deps import get_session
from app.services.authService import hash_password, verify_password
from app.core.dependencies import oauth2_scheme
from ..schemas.user import ChangePasswordRequest, UpdateUserRequest

router = APIRouter(
  prefix="/user",
  tags=["user"],
  dependencies=[Depends(oauth2_scheme)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/me')
async def getMyInfo(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)

@router.get('/list')
async def getUserList(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
  if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Not authorized")
  users = await listUser(session)
  return users

@router.get('/authors')
async def searchAuthors(
    page: int = Query(1, ge=1),
    name: str | None = None,
    session: AsyncSession = Depends(get_session)
  ):
  return await searchAuthorByText(page, name, session)


@router.put('/change-password')
async def changePasswordAPI(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
  ):
  if 'guest' in current_user.role:
    raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot change password")
  return await changePassword(current_user.id, body.old_password, body.new_password, session)

@router.put('/me')
async def updateUserAPI(
    username: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
  ):
  if 'guest' in current_user.role:
    raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot update user")
  return await updateUser(current_user.id, username, email, avatar, session)


@router.get('/{user_id}')
async def getUserById(user_id: int, session: AsyncSession = Depends(get_session)):
  return await getUserByUserId(user_id, session)


