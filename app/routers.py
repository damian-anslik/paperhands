import datetime
import tinydb
import fastapi
import dotenv
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import models

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_router = fastapi.APIRouter(tags=["user"])
portfolio_router = fastapi.APIRouter(tags=["portfolio"])
orders_router = fastapi.APIRouter(tags=["order"])

orders_db = tinydb.TinyDB("orders.json", indent=4)
users_db = tinydb.TinyDB("users.json", indent=4)
portfolio_db = tinydb.TinyDB("portfolios.json", indent=4)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: tinydb.TinyDB, username: str):
    user = db.get(tinydb.Query().username == username)
    if user:
        return models.UserInDB(**user)


def authenticate_user(db, username: str, password: str) -> models.UserInDB | None:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: datetime.timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = fastapi.Depends(oauth2_scheme),
) -> models.UserInDB | None:
    """
    Get the current user from the database. If the user is not found in the database, or if the user is disabled,
    """
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = fastapi.Depends(get_current_user),
) -> models.UserInDB | None:
    """
    Get the current active user from the database. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    if current_user.disabled:
        raise fastapi.HTTPException(status_code=400, detail="Inactive user")
    return current_user


@user_router.post("/token", response_model=models.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
):
    """
    Get an access token for a user. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/signup", status_code=fastapi.status.HTTP_201_CREATED)
async def create_user(
    email: str = fastapi.Form(...),
    username: str = fastapi.Form(...),
    password: str = fastapi.Form(...),
):
    """
    Create a new user in the database. If the user already exists, then raise an exception.
    """
    user_in_db = get_user(users_db, username)
    if user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = get_password_hash(password)
    user_in_db = models.UserInDB(
        username=username,
        email=email,
        disabled=False,
        hashed_password=hashed_password,
    )
    users_db.insert(user_in_db.dict())


@user_router.get("/users/me/", response_model=models.User)
async def read_users_me(
    current_user: models.User = fastapi.Depends(get_current_active_user),
):
    """
    Get the current active user from the database. If the user is not found in the database, or if the user is disabled,
    then raise an exception.
    """
    return current_user


@portfolio_router.get("/portfolio", response_model=models.Portfolio)
def get_portfolio(
    id: str, user: models.User = fastapi.Depends(get_current_active_user)
):
    portfolio = portfolio_db.get(tinydb.where("id") == id)
    if not portfolio:
        return fastapi.Response(status_code=404, content="Portfolio not found")
    portfolio_id = portfolio.get("id")
    if portfolio_id in user.portfolio_ids:
        return portfolio
    is_public_portfolio = portfolio.get("is_public")
    if is_public_portfolio:
        return portfolio
    return fastapi.Response(
        status_code=403, content="You do not have access to this portfolio"
    )


@portfolio_router.post("/portfolio", response_model=models.Portfolio)
def create_portfolio(
    portfolio_name: str = fastapi.Form(...),
    is_public: bool = fastapi.Form(False),
    user: models.User = fastapi.Depends(get_current_active_user),
):
    portfolio = models.Portfolio(
        name=portfolio_name, owner_id=user.id, is_public=is_public
    )
    portfolio_db.insert(portfolio.dict())
    users_db.update(
        {"portfolio_ids": user.portfolio_ids + [portfolio.id]},
        tinydb.where("id") == user.id,
    )
    return portfolio


@portfolio_router.put("/portfolio", response_model=models.Portfolio)
def update_portfolio(
    id: str,
    portfolio_name: str = fastapi.Form(...),
    is_public: bool = fastapi.Form(False),
    user: models.User = fastapi.Depends(get_current_active_user),
):
    portfolio = portfolio_db.get(tinydb.where("id") == id)
    if portfolio.get("owner_id") != user.id:
        return fastapi.Response(status_code=403)
    portfolio_db.update(
        {
            "name": portfolio_name,
            "is_public": is_public,
        },
        tinydb.where("id") == id,
    )
    return portfolio_db.get(tinydb.where("id") == id)


@portfolio_router.delete("/portfolio")
def delete_portfolio(
    id: str,
    user: models.User = fastapi.Depends(get_current_active_user),
):
    portfolio = portfolio_db.get(tinydb.where("id") == id)
    if portfolio.get("owner_id") != user.id:
        return fastapi.Response(status_code=403)
    portfolio_db.remove(tinydb.where("id") == id)
    filtered_portfolio_ids = [
        portfolio_id for portfolio_id in user.portfolio_ids if portfolio_id != id
    ]
    users_db.update(
        {"portfolio_ids": filtered_portfolio_ids},
        tinydb.where("id") == user.id,
    )
    orders_db.remove(tinydb.where("portfolio_id") == id)
    return fastapi.Response(status_code=204)


@orders_router.get("/order", response_model=models.Order)
def get_order(id: str, user: models.User = fastapi.Depends(get_current_active_user)):
    order = orders_db.get(tinydb.where("id") == id)
    if order is None:
        raise fastapi.HTTPException(status_code=404)
    user_portfolio_ids = user.portfolio_ids
    order_portfolio_id = order.get("portfolio_id")
    if order_portfolio_id in user_portfolio_ids:
        return order
    raise fastapi.HTTPException(status_code=403)


@orders_router.post("/order", response_model=models.Order)
def create_order(
    symbol: str = fastapi.Form(...),
    quantity: float = fastapi.Form(...),
    portfolio_id: str = fastapi.Form(...),
    user: models.User = fastapi.Depends(get_current_active_user),
):
    portfolio = portfolio_db.get(tinydb.where("id") == portfolio_id)
    if not portfolio:
        raise fastapi.HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio.get("owner_id") != user.id:
        return fastapi.Response(
            status_code=403, detail="You do not have access to this portfolio"
        )
    order = models.Order(symbol=symbol, quantity=quantity, portfolio_id=portfolio_id)
    orders_db.insert(order.dict())
    portfolio_db.update(
        {"order_ids": portfolio.get("order_ids") + [order.id]},
        tinydb.where("id") == portfolio_id,
    )
    return order


@orders_router.delete("/order", response_model=models.Order)
def cancel_order(
    id: str,
    user: models.User = fastapi.Depends(get_current_active_user),
):
    order = orders_db.get(tinydb.where("id") == id)
    if order is None:
        raise fastapi.HTTPException(status_code=404)
    portfolio_id = order.get("portfolio_id")
    user_portfolio_ids = user.portfolio_ids
    if portfolio_id not in user_portfolio_ids:
        raise fastapi.HTTPException(status_code=403)
    orders_db.remove(tinydb.where("id") == id)
    portfolio = portfolio_db.get(tinydb.where("id") == portfolio_id)
    portfolio_order_ids = portfolio.get("order_ids")
    filtered_portfolio_order_ids = [
        portfolio_order_id
        for portfolio_order_id in portfolio_order_ids
        if portfolio_order_id != id
    ]
    portfolio_db.update({"order_ids": filtered_portfolio_order_ids})
    return order
