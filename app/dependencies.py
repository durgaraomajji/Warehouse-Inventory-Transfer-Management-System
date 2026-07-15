from fastapi import Depends, HTTPException, status

from app.oauth2 import get_current_user


def admin_required(current_user=Depends(get_current_user)):

    if current_user.role != "Admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can perform this action"
        )

    return current_user


def warehouse_manager_required(current_user=Depends(get_current_user)):

    if current_user.role not in ["Admin", "Warehouse Manager"]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )

    return current_user