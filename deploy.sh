#!/bin/bash
# Das And Partners - GoDaddy VPS Deployment Script
# This script automates the entire deployment process

set -e  # Exit on error

echo "🚀 Starting Das And Partners Deployment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="dasandpartners"
DOMAIN="dasandpartners.com"
APP_DIR="/home/$PROJECT_NAME"
VENV_DIR="$APP_DIR/venv"
REPO_URL="https://github.com/yourusername/dasandpartners-django-main.git"  # Update this with your repo

echo -e "${BLUE}Step 1: Updating system packages...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

echo -e "${BLUE}Step 2: Installing required packages...${NC}"
sudo apt-get install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx supervisor git ufw

echo -e "${BLUE}Step 3: Setting up PostgreSQL database...${NC}"
# Create database user and database
sudo -u postgres psql <<EOF
CREATE DATABASE ${PROJECT_NAME}_db;
CREATE USER ${PROJECT_NAME}_user WITH PASSWORD 'YourSecurePassword123!';
ALTER ROLE ${PROJECT_NAME}_user SET client_encoding TO 'utf8';
ALTER ROLE ${PROJECT_NAME}_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ${PROJECT_NAME}_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ${PROJECT_NAME}_db TO ${PROJECT_NAME}_user;
\q
EOF

echo -e "${BLUE}Step 4: Creating project user and directories...${NC}"
sudo useradd -m -d $APP_DIR -s /bin/bash $PROJECT_NAME || true
sudo mkdir -p $APP_DIR
sudo chown -R $PROJECT_NAME:$PROJECT_NAME $APP_DIR

echo -e "${BLUE}Step 5: Setting up Python virtual environment...${NC}"
sudo -u $PROJECT_NAME python3.11 -m venv $VENV_DIR

echo -e "${BLUE}Step 6: Copying project files...${NC}"
sudo cp -r /root/dasandpartners-django-main/* $APP_DIR/
sudo chown -R $PROJECT_NAME:$PROJECT_NAME $APP_DIR

echo -e "${BLUE}Step 7: Installing Python dependencies...${NC}"
sudo -u $PROJECT_NAME $VENV_DIR/bin/pip install --upgrade pip
sudo -u $PROJECT_NAME $VENV_DIR/bin/pip install -r $APP_DIR/requirements.txt

echo -e "${BLUE}Step 8: Creating environment file and media directories...${NC}"
sudo mkdir -p $APP_DIR/media/blogs $APP_DIR/media/news
sudo chown -R $PROJECT_NAME:$PROJECT_NAME $APP_DIR/media

sudo -u $PROJECT_NAME cat > $APP_DIR/.env <<EOF
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN

DB_NAME=${PROJECT_NAME}_db
DB_USER=${PROJECT_NAME}_user
DB_PASSWORD=YourSecurePassword123!
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=findmejoinme.com
EMAIL_PORT=587
EMAIL_HOST_USER=no-reply@findmejoinme.com
EMAIL_HOST_PASSWORD=ZH1B[8}0)Qsf
EOF

echo -e "${BLUE}Step 9: Running Django migrations...${NC}"
sudo -u $PROJECT_NAME $VENV_DIR/bin/python $APP_DIR/manage.py migrate

echo -e "${BLUE}Step 10: Collecting static files...${NC}"
sudo -u $PROJECT_NAME $VENV_DIR/bin/python $APP_DIR/manage.py collectstatic --noinput

echo -e "${BLUE}Step 11: Creating superuser...${NC}"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@dasandpartners.com', 'Admin@2024!')" | sudo -u $PROJECT_NAME $VENV_DIR/bin/python $APP_DIR/manage.py shell

echo -e "${BLUE}Step 12: Configuring Gunicorn...${NC}"
sudo cat > /etc/supervisor/conf.d/$PROJECT_NAME.conf <<EOF
[program:$PROJECT_NAME]
directory=$APP_DIR
command=$VENV_DIR/bin/gunicorn --workers 3 --bind unix:$APP_DIR/gunicorn.sock das_project.wsgi:application
user=$PROJECT_NAME
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/$PROJECT_NAME.log
EOF

echo -e "${BLUE}Step 13: Configuring Nginx...${NC}"
sudo cat > /etc/nginx/sites-available/$PROJECT_NAME <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/gunicorn.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;
    }

    client_max_body_size 10M;
}
EOF

sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo -e "${BLUE}Step 14: Configuring firewall...${NC}"
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

echo -e "${BLUE}Step 15: Starting services...${NC}"
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart $PROJECT_NAME
sudo systemctl restart nginx

echo -e "${BLUE}Step 16: Installing SSL certificate...${NC}"
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}Your website is now live at: https://$DOMAIN${NC}"
echo -e "${GREEN}Admin panel: https://$DOMAIN/admin${NC}"
echo -e "${GREEN}Username: admin${NC}"
echo -e "${GREEN}Password: Admin@2024!${NC}"
echo -e "${GREEN}Please change the admin password immediately!${NC}"

