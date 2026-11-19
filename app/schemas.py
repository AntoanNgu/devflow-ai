from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str=Field(min_length=15, max_length=64)  

    

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str=Field(max_length=64)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    



