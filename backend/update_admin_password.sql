-- 更新管理員密碼為 'admin'
-- 使用 PBKDF2-SHA256 加密

UPDATE users 
SET hashed_password = '$pbkdf2-sha256$29000$lZLSOkcIYSxlbC1l7L03Rg$IL9dKfZAX8R.QhKjMHzuaTaxCH5AhHdH3femEjvF81RT9Oz'
WHERE username = 'admin';

-- 驗證更新
SELECT username, LEFT(hashed_password, 30) as hash_preview, LENGTH(hashed_password) as hash_length
FROM users 
WHERE username = 'admin';
