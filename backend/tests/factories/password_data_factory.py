from mimesis import Generic

from app.models import PasswordTestData  # type: ignore


class PasswordDataFactory:
    def __init__(self):
        self.gen = Generic("en")

    def __call__(self) -> PasswordTestData:
        return PasswordTestData(
            service_name=self.gen.internet.hostname(),
            password=self.gen.person.password(length=12),
        )
