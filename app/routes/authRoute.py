import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.dependencies import oauth2_scheme
from app.db.deps import get_session
from app.models.userSessionModel import UserSession
from app.models.usersModel import User
from app.schemas.user import UserOut, RegisterRequest, LoginRequest, TokenResponse
from app.services.authService import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from fastapi.security import OAuth2PasswordRequestForm

expires_in = 30 * 24 * 60 * 60
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=UserOut)
async def register(req: RegisterRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where((User.username == req.username) | (User.email == req.email))
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    new_user = User(
        username=req.username,
        email=req.email,
        password_hash=hash_password(req.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserOut.model_validate(new_user)


@router.post("/login", response_model=TokenResponse)
async def login(
    req: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    # Try to find user by username
    result = await session.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    session_id = str(uuid.uuid4())

    # 2. Lưu session vào DB
    new_session = UserSession(id=session_id, user_id=user.id)

    session.add(new_session)
    await session.commit()

    expire_time = datetime.utcnow() + timedelta(seconds=expires_in)

    token = create_access_token(
        data={"sub": str(user.id), "sid": session_id, "role": user.role}
    )
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        role=user.role,
        session_uuid=session_id,
        exp=int(expire_time.timestamp()),
    )


@router.post("/login/json", response_model=TokenResponse)
async def login_json(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    # Try to find user by email or username
    result = await session.execute(
        select(User).where((User.email == login_data.email) | (User.username == login_data.email))
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password",
        )
    session_id = str(uuid.uuid4())

    # Save session to DB
    new_session = UserSession(id=session_id, user_id=user.id)

    session.add(new_session)
    await session.commit()

    expire_time = datetime.utcnow() + timedelta(seconds=expires_in)

    token = create_access_token(
        data={"sub": str(user.id), "sid": session_id, "role": user.role}
    )
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        role=user.role,
        session_uuid=session_id,
        exp=int(expire_time.timestamp()),
    )


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session_id = payload.get("sid")

    result = await session.execute(
        select(UserSession).where(UserSession.id == session_id)
    )
    user_session = result.scalar_one_or_none()
    if user_session:
        user_session.is_active = False
        await session.commit()

    return {"message": "Logged out successfully"}
