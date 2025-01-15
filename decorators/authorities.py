from functools import wraps

def admin_authority(f):
    @wraps(f)
    def decorator(current_user, *args, **kwargs):
        if current_user['authority'] == "admin":    
            return f(current_user, *args, **kwargs)
        return {"message": "You don't have the required authority"}, 403
    
    return decorator