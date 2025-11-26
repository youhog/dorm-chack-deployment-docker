from passlib.hash import pbkdf2_sha256

password = "admin"
hash_value = pbkdf2_sha256.hash(password)

with open("admin_hash.txt", "w") as f:
    f.write(f"完整哈希值:\n{hash_value}\n\n")
    f.write(f"SQL 更新語句:\n")
    f.write(f"UPDATE users SET hashed_password = '{hash_value}' WHERE username = 'admin';\n")

print("已生成 admin_hash.txt")
print(f"哈希長度: {len(hash_value)}")
print(f"哈希: {hash_value}")
