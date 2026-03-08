
from fastapi import APIRouter, HTTPException, status


from models.users import User, UserCreate , UserLogin
from .passwords import hash_password, verify_password
from .generateToken import create_access_token



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
async def login_user(credentials: UserLogin):
   
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
    

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }