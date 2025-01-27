from ninja import Schema
from typing import Optional

class UserRegistrationSchema(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None