import uuid
import datetime
import pydantic


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: str | None = None


class Position(pydantic.BaseModel):
    symbol: str
    quantity: float
    price: float
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))


class Order(pydantic.BaseModel):
    symbol: str
    quantity: float
    portfolio_id: str
    created_at: str = pydantic.Field(default_factory=lambda: str(datetime.datetime.utcnow()))
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))


class MarketOrder(Order):
    pass


class LimitOrder(Order):
    limit_price: float


class Portfolio(pydantic.BaseModel):
    name: str
    owner_id: str
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    is_public: bool = False
    position_ids: list[Position] = []
    order_ids: list[str] = []


class User(pydantic.BaseModel):
    username: str
    email: str
    disabled: bool = False
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    portfolio_ids: list[str] = []


class UserInDB(User):
    hashed_password: str
