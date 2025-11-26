"""
重置管理員密碼腳本
執行此腳本將重置管理員帳號的密碼為 'admin123'
"""
import asyncio
from sqlalchemy import select, update
from app.database import AsyncSessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def reset_admin_password():
    """重置管理員密碼"""
    async with AsyncSessionLocal() as db:
        # 查找管理員用戶（通常 username 是 admin）
        result = await db.execute(
            select(User).where(User.username == "admin")
        )
        admin_user = result.scalar_one_or_none()
        
        if not admin_user:
            print("❌ 找不到管理員帳號 'admin'")
            print("請確認資料庫中存在 username='admin' 的用戶")
            return
        
        # 生成新的密碼哈希
        new_password = "admin123"
        hashed_password = pwd_context.hash(new_password)
        
        # 更新密碼
        admin_user.hashed_password = hashed_password
        await db.commit()
        
        print("✅ 成功重置管理員密碼！")
        print(f"   用戶名: admin")
        print(f"   新密碼: {new_password}")
        print("\n現在可以使用這些憑證登入了。")

if __name__ == "__main__":
    asyncio.run(reset_admin_password())
