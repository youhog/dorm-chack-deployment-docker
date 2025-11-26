"""
CRUD operations for announcements.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
import uuid

from app.models import Announcement
from app.schemas import AnnouncementCreate, AnnouncementUpdate


async def get_announcement(db: AsyncSession, announcement_id: str) -> Optional[Announcement]:
    """獲取單一公告（僅返回啟用的）"""
    result = await db.execute(
        select(Announcement).where(
            Announcement.id == announcement_id,
            Announcement.is_active == True
        )
    )
    return result.scalar_one_or_none()


async def get_announcement_by_id(db: AsyncSession, announcement_id: str) -> Optional[Announcement]:
    """獲取單一公告（管理員用，包含非啟用的）"""
    result = await db.execute(
        select(Announcement).where(Announcement.id == announcement_id)
    )
    return result.scalar_one_or_none()


async def get_announcements(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10,
    active_only: bool = True
) -> List[Announcement]:
    """獲取公告列表"""
    query = select(Announcement)
    
    if active_only:
        query = query.where(Announcement.is_active == True)
    
    query = query.order_by(desc(Announcement.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_announcements_count(db: AsyncSession, active_only: bool = True) -> int:
    """獲取公告總數"""
    query = select(func.count()).select_from(Announcement)
    
    if active_only:
        query = query.where(Announcement.is_active == True)
    
    result = await db.execute(query)
    return result.scalar()


async def create_announcement(
    db: AsyncSession, 
    announcement: AnnouncementCreate, 
    creator_id: str
) -> Announcement:
    """建立新公告"""
    db_announcement = Announcement(
        id=str(uuid.uuid4()),
        title=announcement.title,
        content=announcement.content,
        tag=announcement.tag,
        tag_type=announcement.tag_type,
        created_by=creator_id
    )
    db.add(db_announcement)
    await db.commit()
    await db.refresh(db_announcement)
    return db_announcement


async def update_announcement(
    db: AsyncSession,
    announcement_id: str,
    announcement_update: AnnouncementUpdate
) -> Optional[Announcement]:
    """更新公告"""
    db_announcement = await get_announcement_by_id(db, announcement_id)
    if not db_announcement:
        return None
    
    update_data = announcement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_announcement, field, value)
    
    await db.commit()
    await db.refresh(db_announcement)
    return db_announcement


async def delete_announcement(db: AsyncSession, announcement_id: str) -> bool:
    """刪除公告"""
    db_announcement = await get_announcement_by_id(db, announcement_id)
    if not db_announcement:
        return False
    
    await db.delete(db_announcement)
    await db.commit()
    return True
