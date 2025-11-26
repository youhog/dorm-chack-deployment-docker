"""
使用當前程式碼的加密方式生成正確的密碼哈希
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成 admin/admin 的哈希
password = "admin"
hashed = pwd_context.hash(password)

print(f"密碼: {password}")
print(f"哈希: {hashed}")
print(f"哈希長度: {len(hashed)}")

# 生成 SQL 更新語句
print(f"\n執行此 SQL：")
print(f"UPDATE users SET hashed_password = '{hashed}' WHERE username = 'admin';")
