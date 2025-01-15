from flask import request
import jwt
from functools import wraps
from config.config import secret_key

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return {"message": "You need to be authenticated"}, 403
        
        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = {
                'id': data['id'],
                'username': data['username'],
                'authority': data['authority']
            }
      
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 403
        except Exception as e:
            return {"message": "Invalid token"}, 403
        
        return f(current_user, *args, **kwargs)
    
    return decorator