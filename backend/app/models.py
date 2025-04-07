from sqlmodel import Field, SQLModel
import uuid


class PasswordBase(SQLModel):
    service_name: str = Field(unique=True, index=True, max_length=255)


class PasswordCreate(SQLModel):
    password: str = Field(min_length=8, max_length=40)


class PasswordResponse(PasswordBase):
    password: str


class PasswordsResponse(SQLModel):
    data: list[PasswordResponse]
    count: int


class Password(PasswordBase, table=True):  # type: ignore
    __tablename__ = "passwords"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    encrypted_password: str = Field(nullable=False)
