# app/models/user.py
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from . import BaseModel, _require_str, _require_bool, _require_email

class User(BaseModel):
    """
    User:
      - first_name (required, <= 50)
      - last_name  (required, <= 50)
      - email      (required, unique, email format)
      - password   (required, hashed)
      - is_admin   (bool, default False)
    """
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)

    # Relationships (will be updated in Task 8)
    places = relationship("Place", back_populates="owner")
    reviews = relationship("Review", back_populates="user")

    # simple in-memory uniqueness guard for emails (per-process)
    _emails_registry = set()

    def __init__(self, first_name: str, last_name: str, email: str,
                 password: str = None, is_admin: bool = False, **kwargs):
        super().__init__(**kwargs)
        
        # validate basic fields
        _require_str("first_name", first_name, max_len=50, required=True)
        _require_str("last_name", last_name, max_len=50, required=True)
        _require_email("email", email)
        _require_bool("is_admin", is_admin)
        
        # validate email uniqueness
        if email in User._emails_registry:
            raise ValueError("email must be unique")
            
        # assign basic attributes
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        
        # handle password
        if password:
            self.hash_password(password)
        else:
            self.password = None  # Will be set later via hash_password()
        
        # register email
        User._emails_registry.add(self.email)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        # Import here to avoid circular imports
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        
        # Validate password (add your own password requirements here)
        _require_str("password", password, required=True)
        
        # Hash and store the password
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        # Import here to avoid circular imports
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        
        if not self.password:
            return False
        
        return bcrypt.check_password_hash(self.password, password)

    def _validate_field(self, key, value):
        """Validate individual field updates"""
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
        elif key == "password":
            # If updating password, hash it
            _require_str("password", value, required=True)
            # Note: the actual hashing will be done in update() method

    def update(self, data: dict):
        """Update user attributes with special handling for email and password"""
        # handle email uniqueness swap safely
        new_email = data.get("email", self.email)
        if new_email != self.email:
            # validate first to avoid losing current reservation on error
            self._validate_field("email", new_email)
            # commit email change: free old, reserve new
            User._emails_registry.discard(self.email)
            User._emails_registry.add(new_email)
        
        # handle password hashing if password is being updated
        if "password" in data:
            password = data.pop("password")  # Remove from data to handle separately
            self.hash_password(password)
        
        # call parent update for other fields
        super().update(data)

    def to_dict(self, include_password=False):
        """
        Convert user to dictionary representation
        By default, excludes password for security
        """
        user_dict = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        # Only include password if explicitly requested (should be rare)
        if include_password and self.password:
            user_dict['password'] = self.password
            
        return user_dict
