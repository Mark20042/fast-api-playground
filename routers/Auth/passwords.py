from passlib.context import CryptContext
from zxcvbn import zxcvbn

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def check_password_strength(password: str) -> dict:
   
    result = zxcvbn(password)
    score = result['score']
    
    if score >= 3:
        return {
            "is_strong": True, 
            "message": f"Strong enough password. Score: {score}"
        }
    
    
    feedback = result.get('feedback', {})
    warning = feedback.get('warning', '')
    suggestions = feedback.get('suggestions', [])
    
  
    response = f"Weak password. Score: {score}"
    if warning:
        response += f" | Warning: {warning}"
    if suggestions:
        response += f" | Suggestions: {', '.join(suggestions)}"
        
    return {
        "is_strong": False, 
        "message": response
    }

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)