from passlib.hash import sha256_crypt

# 生成密碼 'admin' 的 sha256_crypt 哈希
password = "admin"
hash_value = sha256_crypt.hash(password)

print(f"密碼: {password}")
print(f"SHA256 Crypt 哈希: {hash_value}")
print(f"\n請在 phpMyAdmin 執行:")
print(f"UPDATE users SET hashed_password = '{hash_value}' WHERE username = 'admin';")
