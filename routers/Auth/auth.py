
from fastapi import APIRouter, HTTPException, status,Response


from models.users import User, UserCreate , UserLogin
from .passwords import hash_password, verify_password, check_password_strength
from .generateToken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



# register
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    existing_user = await User.find_one(User.email == user_data.email)
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
        
    password_strength = check_password_strength(user_data.password)
    
    if not password_strength["is_strong"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_strength["message"]
        )
        
    
   
    hashed_pw = hash_password(user_data.password)
    
    
   
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_pw  
    )
    
  
    await new_user.insert()
    
    return {"message": "User registered successfully!"}


# login
@router.post("/login")
async def login_user(credentials: UserLogin, response: Response):
   
    user = await User.find_one(User.email == credentials.email)
    
  
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    
    token_payload = {
        "sub": str(user.id), 
        "email": user.email
    }
    
   
    access_token = create_access_token(data=token_payload)
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  
        secure=False,   
        samesite="lax",
        max_age=1800   
    )

    return {"message": "Successfully logged in!"}