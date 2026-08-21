#%%
class UserPurePython:
    def __init__(self, id: int, name: str, email: str):
        if not isinstance(id, int):
            raise ValueError('id must be an integer')
        if not isinstance(name, str):
            raise ValueError('name must be a string')
        if not isinstance(email, str):
            raise ValueError('email must be a string')
        self.id = id
        self.name = name
        self.email = email

#%%
from dataclasses import dataclass

@dataclass
class UserDataClass:
    id: int
    name: str
    email: str

#%%
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
# %%
user = User(id=1, name="John Doe", email="johndoe@example.com")
print(user)
# %%
try:
    #invalid_user = User(id="abc", name="Jane", email="not-an-email")
    pass
except ValueError as e:
    print(e)
# %%
class Address(BaseModel):
    street: str
    city: str
    zip_code: int

class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: Address

address = Address(street="123 Main St", city="New York", zip_code=10001)
user_with_address = UserWithAddress(id=2, name="Jane Doe", email="jane@example.com", address=address)
print(user_with_address)
# %%
import json

# Convert model to JSON
user_json = user_with_address.model_dump_json()
print(user_json)

# Load model from JSON
user_dict = json.loads(user_json)
user_from_json = UserWithAddress(**user_dict)
print(user_from_json)
# %%
