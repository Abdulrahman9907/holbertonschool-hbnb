# app/models/user.py
from . import BaseModel, _require_str, _require_bool, _require_email

class User(BaseModel):
    """
    User:
      - first_name (required, <= 50)
      - last_name  (required, <= 50)
      - email      (required, unique, email format)
      - is_admin   (bool, default False)
    """
    # simple in-memory uniqueness guard for emails (per-process)
    _emails_registry = set()

    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()
        # validate
        _require_str("first_name", first_name, max_len=50, required=True)
        _require_str("last_name", last_name, max_len=50, required=True)
        _require_email("email", email)
        _require_bool("is_admin", is_admin)
        if email in User._emails_registry:
            raise ValueError("email must be unique")

        # assign
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # register email
        User._emails_registry.add(self.email)

    def _validate_field(self, key, value):
        if key == "first_name":
            _require_str("first_name", value, max_len=50, required=True)
        elif key == "last_name":
            _require_str("last_name", value, max_len=50, required=True)
        elif key == "email":
            _require_email("email", value)
            # if changing email, enforce uniqueness
            if value != self.email and value in User._emails_registry:
                raise ValueError("email must be unique")
        elif key == "is_admin":
            _require_bool("is_admin", value)

    def update(self, data: dict):
        # handle email uniqueness swap safely
        new_email = data.get("email", self.email)
        if new_email != self.email:
            # validate first to avoid losing current reservation on error
            self._validate_field("email", new_email)
            # commit email change: free old, reserve new
            User._emails_registry.discard(self.email)
            User._emails_registry.add(new_email)
        super().update(data)
