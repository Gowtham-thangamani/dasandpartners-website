#!/bin/bash
# ============================================================================
# GoDaddy VPS Deployment Script for Das and Partners Django Website
# Optimized for: 4 vCPU / 8GB RAM / 200GB SSD
# ============================================================================

set -e  # Exit on any error

echo "=========================================="
echo "Das and Partners - VPS Deployment Script"
echo "=========================================="
echo ""

# Configuration
PROJECT_NAME="dasandpartners"
DOMAIN="yourdomain.com"  # Change this to your actual domain
APP_DIR="/var/www/$PROJECT_NAME"
VENV_DIR="$APP_DIR/venv"
USER="www-data"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# ============================================================================
# STEP 1: System Update & Dependencies
# ============================================================================
print_status "Step 1: Updating system and installing dependencies..."

sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    nginx \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    supervisor \
    git \
    curl \
    certbot \
    python3-certbot-nginx \
    redis-server \
    fail2ban \
    ufw

print_success "System dependencies installed!"

# ============================================================================
# STEP 2: Configure Firewall
# ============================================================================
print_status "Step 2: Configuring firewall..."

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

print_success "Firewall configured!"

# ============================================================================
# STEP 3: PostgreSQL Database Setup
# ============================================================================
print_status "Step 3: Setting up PostgreSQL database..."

sudo -u postgres psql <<EOF
CREATE DATABASE ${PROJECT_NAME}_db;
CREATE USER ${PROJECT_NAME}_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
ALTER ROLE ${PROJECT_NAME}_user SET client_encoding TO 'utf8';
ALTER ROLE ${PROJECT_NAME}_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ${PROJECT_NAME}_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ${PROJECT_NAME}_db TO ${PROJECT_NAME}_user;
\q
EOF

print_success "PostgreSQL database created!"

# ============================================================================
# STEP 4: Create Project Directory
# ============================================================================
print_status "Step 4: Creating project directory..."

sudo mkdir -p $APP_DIR
sudo mkdir -p $APP_DIR/media/{blogs,news,uploads}
sudo mkdir -p $APP_DIR/static
sudo mkdir -p $APP_DIR/logs

print_success "Project directories created!"

# ============================================================================
# STEP 5: Upload Your Code
# ============================================================================
print_status "Step 5: Upload your Django project..."
echo ""
echo "MANUAL STEP REQUIRED:"
echo "Upload your project files to: $APP_DIR"
echo ""
echo "Options:"
echo "1. Use SCP:"
echo "   scp -r /path/to/your/project/* root@your-vps-ip:$APP_DIR/"
echo ""
echo "2. Use Git:"
echo "   cd $APP_DIR"
echo "   git clone your-repository-url ."
echo ""
echo "3. Use SFTP/FileZilla"
echo ""
read -p "Press Enter when files are uploaded..."

# ============================================================================
# STEP 6: Python Virtual Environment
# ============================================================================
print_status "Step 6: Creating Python virtual environment..."

cd $APP_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

print_success "Virtual environment created!"

# ============================================================================
# STEP 7: Install Python Dependencies
# ============================================================================
print_status "Step 7: Installing Python packages..."

pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

print_success "Python dependencies installed!"

# ============================================================================
# STEP 8: Environment Variables
# ============================================================================
print_status "Step 8: Creating environment file..."

cat > $APP_DIR/.env <<EOF
# Django Settings
DEBUG=False
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,your-vps-ip

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=${PROJECT_NAME}_db
DB_USER=${PROJECT_NAME}_user
DB_PASSWORD=CHANGE_THIS_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Email (Update with your SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Media & Static
MEDIA_URL=/media/
STATIC_URL=/static/
EOF

print_success "Environment file created!"
echo "⚠️  IMPORTANT: Edit $APP_DIR/.env and update passwords!"

# ============================================================================
# STEP 9: Django Setup
# ============================================================================
print_status "Step 9: Running Django migrations and collectstatic..."

cd $APP_DIR
source $VENV_DIR/bin/activate

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

print_success "Django setup complete!"

# ============================================================================
# STEP 10: Create Superuser
# ============================================================================
print_status "Step 10: Creating Django superuser..."

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='das_admin').exists():
    User.objects.create_superuser('das_admin', 'admin@dasandpartners.com', 'admindasandpartners123')
    print('Superuser created!')
else:
    print('Superuser already exists.')
EOF

print_success "Superuser created!"

# ============================================================================
# STEP 11: Gunicorn Configuration
# ============================================================================
print_status "Step 11: Configuring Gunicorn..."

cat > $APP_DIR/gunicorn_config.py <<'EOF'
import multiprocessing

# Server socket
bind = "unix:/var/www/dasandpartners/gunicorn.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1  # 4 vCPU = 9 workers
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/var/www/dasandpartners/logs/gunicorn_access.log"
errorlog = "/var/www/dasandpartners/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "dasandpartners"

# Server mechanics
daemon = False
pidfile = "/var/www/dasandpartners/gunicorn.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/key.pem"
# certfile = "/path/to/cert.pem"
EOF

print_success "Gunicorn configured!"

# ============================================================================
# STEP 12: Supervisor Configuration
# ============================================================================
print_status "Step 12: Configuring Supervisor..."

sudo cat > /etc/supervisor/conf.d/$PROJECT_NAME.conf <<EOF
[program:${PROJECT_NAME}]
command=$VENV_DIR/bin/gunicorn das_project.wsgi:application -c $APP_DIR/gunicorn_config.py
directory=$APP_DIR
user=$USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$APP_DIR/logs/supervisor.log
environment=PATH="$VENV_DIR/bin"
EOF

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start $PROJECT_NAME

print_success "Supervisor configured and application started!"

# ============================================================================
# STEP 13: Nginx Configuration
# ============================================================================
print_status "Step 13: Configuring Nginx..."

sudo cat > /etc/nginx/sites-available/$PROJECT_NAME <<'NGINXCONF'
# Upstream to Gunicorn
upstream dasandpartners_app {
    server unix:/var/www/dasandpartners/gunicorn.sock fail_timeout=0;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration (after running certbot)
    # ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 100M;  # For bulk image uploads
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/www/dasandpartners/logs/nginx_access.log;
    error_log /var/www/dasandpartners/logs/nginx_error.log;

    # Static files
    location /static/ {
        alias /var/www/dasandpartners/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/dasandpartners/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Main application
    location / {
        proxy_pass http://dasandpartners_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts for bulk uploads
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
NGINXCONF

# Enable site
sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

print_success "Nginx configured!"

# ============================================================================
# STEP 14: SSL Certificate (Let's Encrypt)
# ============================================================================
print_status "Step 14: Setting up SSL certificate..."

echo ""
echo "Run this command after updating domain in nginx config:"
echo "sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""

# ============================================================================
# STEP 15: Set Permissions
# ============================================================================
print_status "Step 15: Setting file permissions..."

sudo chown -R $USER:$USER $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 775 $APP_DIR/media
sudo chmod -R 775 $APP_DIR/logs

print_success "Permissions set!"

# ============================================================================
# STEP 16: Fail2Ban for Security
# ============================================================================
print_status "Step 16: Configuring Fail2Ban..."

sudo cat > /etc/fail2ban/jail.local <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
EOF

sudo systemctl restart fail2ban

print_success "Fail2Ban configured!"

# ============================================================================
# STEP 17: Automated Backups
# ============================================================================
print_status "Step 17: Setting up automated backups..."

# Create backup script
sudo cat > /usr/local/bin/backup_dasandpartners.sh <<'BACKUPSCRIPT'
#!/bin/bash
# Daily backup script

BACKUP_DIR="/var/backups/dasandpartners"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/var/www/dasandpartners"

mkdir -p $BACKUP_DIR

# Backup database
sudo -u postgres pg_dump dasandpartners_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $APP_DIR media/

# Keep only last 14 days of backups
find $BACKUP_DIR -type f -mtime +14 -delete

echo "Backup completed: $DATE"
BACKUPSCRIPT

sudo chmod +x /usr/local/bin/backup_dasandpartners.sh

# Add to crontab (runs daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup_dasandpartners.sh >> /var/log/dasandpartners_backup.log 2>&1") | crontab -

print_success "Automated backups configured!"

# ============================================================================
# STEP 18: Performance Monitoring
# ============================================================================
print_status "Step 18: Installing monitoring tools..."

sudo apt install -y htop iotop nethogs

print_success "Monitoring tools installed!"

# ============================================================================
# STEP 19: Create Management Scripts
# ============================================================================
print_status "Step 19: Creating management scripts..."

# Restart script
cat > $APP_DIR/restart.sh <<'EOF'
#!/bin/bash
echo "Restarting Das and Partners application..."
sudo supervisorctl restart dasandpartners
sudo systemctl reload nginx
echo "Application restarted!"
EOF
chmod +x $APP_DIR/restart.sh

# Deploy script
cat > $APP_DIR/deploy.sh <<'EOF'
#!/bin/bash
echo "Deploying updates..."
cd /var/www/dasandpartners
source venv/bin/activate
git pull origin main
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart dasandpartners
sudo systemctl reload nginx
echo "Deployment complete!"
EOF
chmod +x $APP_DIR/deploy.sh

# Status check script
cat > $APP_DIR/status.sh <<'EOF'
#!/bin/bash
echo "=== Das and Partners Status ==="
echo ""
echo "Application:"
sudo supervisorctl status dasandpartners
echo ""
echo "Nginx:"
sudo systemctl status nginx | grep Active
echo ""
echo "PostgreSQL:"
sudo systemctl status postgresql | grep Active
echo ""
echo "Disk Usage:"
df -h /var/www/dasandpartners
echo ""
echo "Memory Usage:"
free -h
echo ""
echo "CPU Usage:"
uptime
EOF
chmod +x $APP_DIR/status.sh

print_success "Management scripts created!"

# ============================================================================
# STEP 20: Performance Optimizations
# ============================================================================
print_status "Step 20: Applying performance optimizations..."

# PostgreSQL optimization for 8GB RAM
sudo cat >> /etc/postgresql/*/main/postgresql.conf <<EOF

# Das and Partners Optimizations for 8GB RAM
shared_buffers = 2GB
effective_cache_size = 6GB
maintenance_work_mem = 512MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 4
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
EOF

sudo systemctl restart postgresql

# Nginx optimization
sudo cat > /etc/nginx/conf.d/optimization.conf <<'EOF'
# Nginx optimizations for 4 vCPU
worker_processes 4;
worker_connections 2048;

# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1000;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;

# Buffer sizes
client_body_buffer_size 128k;
client_max_body_size 100m;
client_header_buffer_size 1k;
large_client_header_buffers 4 16k;
EOF

sudo systemctl reload nginx

print_success "Performance optimizations applied!"

# ============================================================================
# STEP 21: Redis Caching Setup
# ============================================================================
print_status "Step 21: Configuring Redis caching..."

sudo systemctl enable redis-server
sudo systemctl start redis-server

print_success "Redis configured!"

# ============================================================================
# STEP 22: Log Rotation
# ============================================================================
print_status "Step 22: Setting up log rotation..."

sudo cat > /etc/logrotate.d/dasandpartners <<EOF
$APP_DIR/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        sudo supervisorctl restart dasandpartners > /dev/null
    endscript
}
EOF

print_success "Log rotation configured!"

# ============================================================================
# FINAL STEPS
# ============================================================================
echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Edit environment file:"
echo "   sudo nano $APP_DIR/.env"
echo ""
echo "2. Update settings.py for production:"
echo "   - Set DEBUG = False"
echo "   - Update ALLOWED_HOSTS"
echo "   - Configure database settings"
echo ""
echo "3. Create superuser (if needed):"
echo "   cd $APP_DIR && source venv/bin/activate"
echo "   python manage.py createsuperuser"
echo ""
echo "4. Get SSL certificate:"
echo "   sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "5. Test your site:"
echo "   http://your-vps-ip"
echo "   https://$DOMAIN (after SSL)"
echo ""
echo "🔧 Useful Commands:"
echo "   Restart app:  cd $APP_DIR && ./restart.sh"
echo "   Check status: cd $APP_DIR && ./status.sh"
echo "   Deploy updates: cd $APP_DIR && ./deploy.sh"
echo "   View logs:    tail -f $APP_DIR/logs/*.log"
echo ""
echo "📞 Access Points:"
echo "   Website:  https://$DOMAIN"
echo "   Admin:    https://$DOMAIN/admin/"
echo "   Dashboard: https://$DOMAIN/content-dashboard/"
echo "   Login:    https://$DOMAIN/login/"
echo ""
echo "🎉 Your website is ready for production!"
echo "=========================================="





