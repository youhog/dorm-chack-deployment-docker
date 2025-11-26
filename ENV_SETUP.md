# 環境變數設定指南 (.env)

這個指南將說明如何設定專案所需的環境變數。環境變數用於儲存敏感資訊（如密鑰、資料庫憑證）以及根據部署環境（開發、測試、生產）調整應用程式行為。

## 1. 建立 `.env` 檔案

首先，請將專案根目錄下的 `.env.example` 檔案複製一份，並將新檔案重新命名為 `.env`。

*   **Linux/macOS:**
    ```bash
    cp .env.example .env
    ```
*   **Windows (Command Prompt):**
    ```bash
    copy .env.example .env
    ```
*   **Windows (PowerShell):**
    ```powershell
    Copy-Item .env.example .env
    ```

**重要提示**：`.env` 檔案通常會包含敏感資訊，並且已經被 `.gitignore` 排除在版本控制之外。**請勿將您的 `.env` 檔案提交到 Git 儲存庫中。**

## 2. 開啟 `.env` 檔案進行編輯

使用任何文字編輯器開啟您剛才建立的 `.env` 檔案。您會看到類似 `.env.example` 中的變數列表。

## 3. 依據您的環境修改重要變數

請仔細閱讀 `.env` 檔案中的註解，並根據您的實際需求和部署環境修改以下關鍵變數。標記為 `[REQUIRED]` 的變數是必須修改的，而 `[OPTIONAL]` 變數則可以根據需要調整。

---

### 核心安全設定

*   `SECRET_KEY`
    *   **說明**：這是用於 JWT (JSON Web Token) 權杖編碼的加密密鑰，對於應用程式的安全性至關重要。
    *   **如何修改**：**[REQUIRED] 您必須修改此值！** 請務必將 `SECRET_KEY="CHANGE_THIS_TO_A_SECURE_RANDOM_STRING"` 替換為一個長且複雜的隨機字串。您可以使用命令列工具生成一個：
        ```bash
        openssl rand -hex 32
        ```
        然後將生成的字串貼到 `=` 符號後面。

### 資料庫設定

*   `SQLALCHEMY_DATABASE_URL`
    *   **說明**：定義了應用程式連接資料庫的方式。
    *   **如何修改**：
        *   **[OPTIONAL] 開發環境 (預設 SQLite)**：`sqlite:///./sql_app.db` 會在專案根目錄下建立一個名為 `sql_app.db` 的檔案，這對於本地開發通常足夠。
        *   **[REQUIRED for Production] 生產環境 (例如 PostgreSQL)**：您需要根據您的資料庫設定來修改。例如，如果您使用 PostgreSQL：
            ```
            postgresql://您的使用者名稱:您的密碼@您的資料庫主機:您的資料庫埠/您的資料庫名稱
            ```
            範例：`postgresql://user:password@db.example.com:5432/mydatabase`

### 初始管理員帳號 (應用程式首次啟動時使用)

*   `FIRST_SUPERUSER`
    *   **說明**：應用程式首次啟動時，如果資料庫中沒有使用者，將會建立一個超級管理員帳號。這是該帳號的預設使用者名稱。
    *   **如何修改**：**[OPTIONAL]** 您可以將 `admin` 改為您偏好的初始管理員帳號名稱。

*   `FIRST_SUPERUSER_PASSWORD`
    *   **說明**：上述超級管理員帳號的預設密碼。
    *   **如何修改**：**[REQUIRED for Production] 強烈建議在實際部署前修改此密碼！** 將 `admin_password` 改為一個安全且複雜的密碼。

### 電子郵件服務設定 (用於密碼重設等功能)

*   `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_TLS`, `MAIL_SSL`
    *   **說明**：這些變數用於設定應用程式發送電子郵件（例如「忘記密碼」連結、通知郵件）所需的 SMTP 伺服器資訊。
    *   **如何修改**：**[REQUIRED for Email Features]** 如果您需要啟用電子郵件功能，請填寫您的 SMTP 伺服器詳細資訊（例如 Gmail、Outlook 或其他郵件服務提供者）。如果未設定，相關郵件功能將無法正常運作。在 `DEBUG=True` 時，密碼重設連結會印在後端 Console 中。

### 開發與部署相關設定

*   `DEBUG`
    *   **說明**：設定為 `True` 時，應用程式會顯示更詳細的錯誤訊息，適合開發階段。設定為 `False` 則會提供更精簡的錯誤訊息，適合生產環境。
    *   **如何修改**：**[REQUIRED for Production] 在生產環境中務必設定為 `False`**，以避免洩漏敏感資訊。

*   `API_BASE_URL`
    *   **說明**：後端 API 的基本 URL。前端可能會使用它來構建完整的 API 請求路徑。
    *   **如何修改**：**[OPTIONAL]** 通常在本地開發時設定為 `http://localhost:8000`。部署時，請改為您實際的 API 網址 (例如 `https://api.yourdomain.com`)。

*   `BACKEND_CORS_ORIGINS`
    *   **說明**：定義了允許跨域請求的來源 (Origins) 列表。
    *   **如何修改**：**[OPTIONAL]** 請確保此列表中包含您前端應用程式的網域。例如，如果您的前端運行在 `http://yourfrontend.com`，則應將其加入此列表。多個來源請用逗號分隔，例如：`http://localhost:3000,http://yourfrontend.com`。

*   `NODE_ENV` (前端使用)
    *   **說明**：前端應用程式的運行環境模式。
    *   **如何修改**：**[OPTIONAL]** `development` 適用於開發，`production` 適用於部署。在 `production` 模式下，通常會啟用最佳化和禁用開發工具。

## 4. 保存檔案並重新啟動應用程式

修改完 `.env` 檔案後，請保存它。然後，您需要**重新啟動**後端和前端應用程式，以確保所有新的環境變數都被載入和應用。

---

## `.env.example` 檔案內容參考

為了方便參考，以下是 `.env.example` 的完整內容：

```ini
# Instructions:
# 1. Copy this file to a new file named ".env" in the project root (same directory as this file).
# 2. Update the values below according to your environment.
#    Items marked with [REQUIRED] must be set for the application to start securely.
#    Items marked with [OPTIONAL] can be left as defaults for local development.

# ==============================================
# CORE SETTINGS
# ==============================================

# [REQUIRED] A strong, unique secret key for JWT token encoding.
# IMPORTANT: Change this to a random string for production!
# You can generate one using: openssl rand -hex 32
SECRET_KEY="CHANGE_THIS_TO_A_SECURE_RANDOM_STRING"

# [REQUIRED] Database connection string.
# Default is SQLite for local development.
# For PostgreSQL use: postgresql://user:password@host:port/database_name
SQLALCHEMY_DATABASE_URL="sqlite:///./sql_app.db"

# [OPTIONAL] Algorithm for JWT token encoding (default: HS256)
ALGORITHM="HS256"

# [OPTIONAL] Access token expiration time in minutes (default: 60)
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ==============================================
# ADMIN ACCOUNT INITIALIZATION
# ==============================================

# [OPTIONAL] Username for the first superuser account created on startup.
FIRST_SUPERUSER="admin"

# [OPTIONAL] Password for the first superuser account.
# CHANGE THIS for production environments!
FIRST_SUPERUSER_PASSWORD="admin_password"

# ==============================================
# EMAIL SETTINGS (REQUIRED for Forgot Password)
# ==============================================
# If these are not configured, email features (like password reset) will not work.
# In development (DEBUG=True), links will be printed to the console if email fails.

MAIL_USERNAME=""
MAIL_PASSWORD=""
MAIL_FROM="noreply@example.com"
MAIL_PORT=587
MAIL_SERVER="smtp.gmail.com"
MAIL_TLS=True
MAIL_SSL=False

# ==============================================
# GENERAL SETTINGS
# ==============================================

# [OPTIONAL] Set to True for development (shows detailed errors), False for production.
DEBUG=True

# [OPTIONAL] Directory to store uploaded files
UPLOAD_DIR="uploads"

# [OPTIONAL] Base URL for the backend API.
API_BASE_URL="http://localhost:8000"

# [OPTIONAL] CORS Allowed Origins
# Comma-separated list of origins that are allowed to make cross-origin requests.
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"

# Project Metadata
PROJECT_NAME="Chack"
PROJECT_VERSION="1.0.0"
API_V1_STR="/api/v1"

# ==============================================
# FRONTEND / NODE SETTINGS
# ==============================================

# [OPTIONAL] Node environment (development/production)
NODE_ENV="development"
```
