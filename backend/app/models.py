from sqlmodel import Field, SQLModel
import uuid


class PasswordBase(SQLModel):
    service_name: str = Field(unique=True, index=True, max_length=255)


class PasswordCreate(SQLModel):
    password: str = Field(min_length=8, max_length=40)


class PasswordResponse(PasswordBase):
    password: str


class Password(PasswordBase, table=True):
    __tablename__ = 'passwords'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    hashed_password: str = Field(nullable=False)
