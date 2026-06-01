from fastapi import Depends, HTTPException
from app.core.user_service import get_current_user


def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if user.get('role') != required_role:
            raise HTTPException(status_code=403, detail="Not authorized!")

        return user
    return role_checker
