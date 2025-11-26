-- 修正 Alembic 版本並建立公告資料表
-- 請在 MySQL 資料庫中執行此腳本

-- 步驟 1: 修正 alembic_version
DELETE FROM alembic_version;
INSERT INTO alembic_version (version_num) VALUES ('503107688e81');

-- 步驟 2: 建立公告相關的 enum 和資料表（如果尚未存在）

-- 檢查並建立 tagtype enum（如果不存在）
-- 注意：MySQL 不支援 CREATE TYPE，這是 PostgreSQL 語法
-- 在 MySQL 中，我們直接在資料表中使用 ENUM

-- 建立 announcements 資料表
CREATE TABLE IF NOT EXISTS announcements (
    id CHAR(36) NOT NULL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    tag VARCHAR(50) NOT NULL,
    tag_type ENUM('primary', 'success', 'warning', 'danger', 'info') NOT NULL DEFAULT 'primary',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by CHAR(36) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- 驗證
SELECT * FROM alembic_version;
SHOW TABLES LIKE 'announcements';
