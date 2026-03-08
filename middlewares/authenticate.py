from fastapi import Request, HTTPException, status

async def verify_jwt_cookie(request: Request):
  
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication cookie. Please log in."
        )
    
    
    return token