from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

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

class RepoCreate(BaseModel):
    repo_url: str
    requested_ref: str | None = None 
    @field_validator("repo_url")
    @classmethod
    def check_repo_url(cls, value: str) -> str:
        cleaned = value.removeprefix("https://").rstrip("/")
        parts = cleaned.split("/")
        if len(parts) != 3 or parts[0] != "github.com" or not parts[1] or not parts[2]:
            raise ValueError("Not a valid URL")
        return cleaned
    
class RepoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    repo_url: str
    id: int 
    requested_ref: str | None = None 
    status: str 


    
    



