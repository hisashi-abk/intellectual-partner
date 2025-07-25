#!/bin/bash

# Django プロジェクト初期設定スクリプト
# 「知的な伴走者」学習支援アプリケーション

echo "🧠 Django プロジェクト「知的な伴走者」初期設定を開始します..."

# 1. プロジェクト作成
echo "📁 プロジェクト作成中..."
django-admin startproject config .

# 2. 各アプリケーション作成
echo "🔧 アプリケーション作成中..."
python manage.py startapp accounts
python manage.py startapp goals
python manage.py startapp tickets
python manage.py startapp emotions
python manage.py startapp journal
python manage.py startapp analytics
python manage.py startapp teacher_support
python manage.py startapp notifications
python manage.py startapp gamification
python manage.py startapp core

# 3. 環境変数ファイル作成
echo "🔐 環境変数設定ファイル作成中..."
cat > .env << 'EOF'
# Django設定
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_SETTINGS_MODULE=config.settings

# データベース設定
DB_NAME=intellectual_partner
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis設定
REDIS_URL=redis://localhost:6379/0

# Celery設定
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# メール設定（開発環境）
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Sentry設定（本番環境用）
SENTRY_DSN=

# Twilio設定
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=

# 日本語設定
LANGUAGE_CODE=ja
TIME_ZONE=Asia/Tokyo
EOF

# 4. gitignore作成
echo "📝 .gitignore作成中..."
cat > .gitignore << 'EOF'
# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment variables
.env
.env.local
.env.production

# Virtual environment
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Coverage
htmlcov/
.coverage
.coverage.*
coverage.xml

# Pytest
.pytest_cache/

# Celery
celerybeat-schedule
celerybeat.pid

# Node.js (フロントエンド用)
node_modules/
npm-debug.log
yarn-error.log

# Distribution / packaging
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Backup files
*.bak
*.orig
EOF

# 5. 初期migration
echo "🗃️ 初期migration実行中..."
python manage.py makemigrations
python manage.py migrate

# 6. スーパーユーザー作成案内
echo "👤 スーパーユーザー作成（後で実行）:"
echo "python manage.py createsuperuser"

# 7. 開発サーバー起動案内
echo "🚀 開発サーバー起動コマンド:"
echo "python manage.py runserver"

echo "✅ 初期設定完了！次に settings.py の設定を行います。"
