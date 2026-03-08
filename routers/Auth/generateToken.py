import jwt
from datetime import datetime, timedelta, timezone


from config.config import settings 

def create_access_token(data: dict, expires_minutes: int = 30):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt