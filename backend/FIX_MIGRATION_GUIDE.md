# 資料庫遷移問題修正方案

## 問題描述
後端啟動失敗，錯誤訊息：
```
FAILED: Can't locate revision identified by '8220a7569c30'
```

這是因為資料庫的 `alembic_version` 資料表記錄了一個不存在的遷移版本。

## 解決方案

### 方案 1：直接更新資料庫（推薦）
執行以下 SQL 命令來修正 alembic_version：

```sql
-- 刪除舊的版本記錄
DELETE FROM alembic_version;

-- 插入當前最新版本
INSERT INTO alembic_version (version_num) VALUES ('503107688e81');
```

### 方案 2：重置資料庫（如果可以接受資料遺失）
如果是開發環境且可以接受資料遺失：

```powershell
# 停止後端
# 刪除資料庫（或使用資料庫管理工具）
# 執行遷移
cd backend
.venv\Scripts\python.exe -m alembic upgrade head
```

### 方案 3：暫時停用自動遷移
修改 `main.py` 暫時註釋掉自動遷移的程式碼（第 21-30 行）：

```python
# 暫時註釋以避免啟動失敗
# print("Running database migrations...")
# backend_dir = os.path.dirname(os.path.abspath(__file__))
# alembic_path = os.path.join(backend_dir, ".venv", "Scripts", "alembic.exe")
# subprocess.run([alembic_path, "upgrade", "head"], check=True, cwd=backend_dir)
# print("Database migrations complete.")
```

然後手動執行遷移修正後再啟用。

## 建議步驟
1. 使用資料庫管理工具（如 MySQL Workbench）執行方案 1 的 SQL
2. 重啟後端伺服器
3. 檢查是否正常啟動
