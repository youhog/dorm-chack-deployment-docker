-- 先查看當前管理員用戶的密碼哈希
SELECT username, LENGTH(hashed_password) as hash_length, hashed_password 
FROM users 
WHERE username = 'admin';

-- 如果哈希太長或格式錯誤，執行以下更新
-- 使用正確的 bcrypt 哈希格式，密碼為 'admin'
UPDATE users 
SET hashed_password = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'
WHERE username = 'admin';

-- 驗證更新（哈希長度應該是 60）
SELECT username, LENGTH(hashed_password) as hash_length, LEFT(hashed_password, 20) as hash_prefix
FROM users 
WHERE username = 'admin';
