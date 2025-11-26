-- 步驟 1: 先查看當前密碼哈希的情況
SELECT 
    username, 
    LENGTH(hashed_password) as password_length,
    LEFT(hashed_password, 30) as password_start
FROM users 
WHERE username = 'admin';

-- 步驟 2: 如果長度不是 60，執行下面的更新
-- 正確的 bcrypt 哈希長度應該是 60 字符
-- 這是密碼 'admin123' 的正確哈希
UPDATE users 
SET hashed_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewY5GyYqJhz/i.W6'
WHERE username = 'admin';

-- 步驟 3: 驗證更新
SELECT 
    username, 
    LENGTH(hashed_password) as password_length,
    hashed_password
FROM users 
WHERE username = 'admin';
