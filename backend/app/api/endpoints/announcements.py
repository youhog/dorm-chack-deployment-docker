"""
Announcement API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import get_current_user, PermissionChecker
from app.models import User
from app.schemas import (
    AnnouncementResponse,
    AnnouncementCreate,
    AnnouncementUpdate,
    PaginatedAnnouncements
)
from app.crud import crud_announcement

router = APIRouter()


# --- Public Endpoints ---

@router.get("/", response_model=PaginatedAnnouncements)
async def get_announcements(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    獲取公告列表（公開，僅返回啟用的公告）
    - **skip**: 跳過的記錄數
    - **limit**: 返回的最大記錄數
    """
    announcements = await crud_announcement.get_announcements(
        db, skip=skip, limit=limit, active_only=True
    )
    total = await crud_announcement.get_announcements_count(db, active_only=True)
    
    return PaginatedAnnouncements(total=total, records=announcements)


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
    announcement_id: str,
    db: Session = Depends(get_db)
):
    """
    獲取單一公告（公開，僅返回啟用的公告）
    """
    announcement = await crud_announcement.get_announcement(db, announcement_id)
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="公告不存在或已停用"
        )
    return announcement


# --- Admin Endpoints (require permission) ---

@router.post("/", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    announcement: AnnouncementCreate,
    current_user: User = Depends(PermissionChecker("admin:full_access")),
    db: Session = Depends(get_db)
):
    """
    建立新公告（需要管理員權限）
    """
    new_announcement = await crud_announcement.create_announcement(
        db, announcement, creator_id=current_user.id
    )
    return new_announcement


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: str,
    announcement_update: AnnouncementUpdate,
    current_user: User = Depends(PermissionChecker("admin:full_access")),
    db: Session = Depends(get_db)
):
    """
    更新公告（需要管理員權限）
    """
    updated_announcement = await crud_announcement.update_announcement(
        db, announcement_id, announcement_update
    )
    if not updated_announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="公告不存在"
        )
    return updated_announcement


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: str,
    current_user: User = Depends(PermissionChecker("admin:full_access")),
    db: Session = Depends(get_db)
):
    """
    刪除公告（需要管理員權限）
    """
    success = await crud_announcement.delete_announcement(db, announcement_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="公告不存在"
        )
    return None
