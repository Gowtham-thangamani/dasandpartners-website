# 🚀 Das And Partners - GoDaddy VPS Deployment Guide

## Complete Step-by-Step Guide to Deploy Your Django Website

---

## 📋 Prerequisites

### What You Need:
1. ✅ GoDaddy VPS Server (Ubuntu 22.04 recommended)
2. ✅ Root SSH access to your VPS
3. ✅ Domain: dasandpartners.com
4. ✅ Basic terminal knowledge

---

## 💰 GoDaddy VPS Plans

| Plan | RAM | CPU | Storage | Bandwidth | Cost |
|------|-----|-----|---------|-----------|------|
| Economy | 1 GB | 1 Core | 40 GB | 1 TB | ~$19.99/month |
| Deluxe | 2 GB | 2 Cores | 80 GB | 2 TB | ~$29.99/month |
| Ultimate | 4 GB | 2 Cores | 120 GB | 3 TB | ~$49.99/month |

**Recommended**: Deluxe plan for professional website

---

## 🎯 Step 1: Purchase GoDaddy VPS

1. Go to https://www.godaddy.com/hosting/vps-hosting
2. Select **Ubuntu 22.04 LTS**
3. Choose **Deluxe Plan** (2GB RAM)
4. Complete purchase
5. Wait for setup email (5-10 minutes)
6. Note down:
   - IP Address
   - Root Password
   - SSH Port (usually 22)

---

## 🔐 Step 2: Connect to Your VPS

### On Mac/Linux:
```bash
ssh root@YOUR_VPS_IP
```

### On Windows:
Use **PuTTY** or **Windows Terminal**:
```bash
ssh root@YOUR_VPS_IP
```

When prompted, enter your root password.

---

## 📦 Step 3: Upload Your Project Files

### Option A: Using Git (Recommended)

1. **On your local Mac**, create GitHub repository:
```bash
cd "/Users/haider/Desktop/new backup/dasandpartners-django-main"
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub repo** at https://github.com/new
   - Name: dasandpartners-django-main
   - Make it Private
   - Create repository

3. **Push code**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/dasandpartners-django-main.git
git push -u origin master
```

4. **On VPS**, clone the repo:
```bash
cd /root
git clone https://github.com/YOUR_USERNAME/dasandpartners-django-main.git
```

### Option B: Using SCP (Alternative)

```bash
# From your Mac terminal
cd "/Users/haider/Desktop/new backup/"
scp -r dasandpartners-django-main root@YOUR_VPS_IP:/root/
```

---

## 🚀 Step 4: Run Automated Deployment

### On your VPS (as root):

```bash
cd /root/dasandpartners-django-main
chmod +x deploy.sh
./deploy.sh
```

**This script will automatically:**
- ✅ Install all required packages
- ✅ Set up PostgreSQL database
- ✅ Configure Python environment
- ✅ Install dependencies
- ✅ Run migrations
- ✅ Collect static files
- ✅ Create superuser
- ✅ Configure Nginx
- ✅ Set up SSL certificate
- ✅ Start all services

**Wait time**: 10-15 minutes

---

## 🌐 Step 5: Point Your Domain to VPS

### In GoDaddy DNS Management:

1. Go to https://dcc.godaddy.com/domains
2. Click on **dasandpartners.com**
3. Click **DNS** → **Manage DNS**
4. Update/Add these records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_VPS_IP | 600 |
| A | www | YOUR_VPS_IP | 600 |

5. Click **Save**
6. Wait 10-30 minutes for DNS propagation

---

## ✅ Step 6: Verify Deployment

### Check if services are running:
```bash
# Check Nginx
sudo systemctl status nginx

# Check Gunicorn
sudo supervisorctl status dasandpartners

# Check PostgreSQL
sudo systemctl status postgresql
```

### Test your website:
```bash
curl http://localhost
curl https://dasandpartners.com
```

---

## 🔑 Step 7: Access Admin Panel

1. Go to: `https://dasandpartners.com/admin`
2. Login with:
   - **Username**: `admin`
   - **Password**: `Admin@2024!`
3. **IMPORTANT**: Change password immediately!
   - Click on your username
   - Change password
   - Use a strong password

---

## 📝 Step 8: Add Your First Blog/News

1. Go to admin panel: `https://dasandpartners.com/admin`
2. Click **"Blog Categories"** → **"Add Blog Category"**
   - Create categories like: Engineering, Projects, Innovation
3. Click **"Blogs"** → **"Add Blog"**
   - Fill in all details
   - Upload image
   - Save
4. Check homepage: `https://dasandpartners.com`
5. Your blog should appear in the "Latest Insights" section!

---

## 🔧 Common Commands

### Restart Services:
```bash
# Restart Gunicorn
sudo supervisorctl restart dasandpartners

# Restart Nginx
sudo systemctl restart nginx

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Update Your Code:
```bash
cd /home/dasandpartners
sudo -u dasandpartners git pull
sudo -u dasandpartners /home/dasandpartners/venv/bin/python manage.py migrate
sudo -u dasandpartners /home/dasandpartners/venv/bin/python manage.py collectstatic --noinput
sudo supervisorctl restart dasandpartners
```

### View Logs:
```bash
# Application logs
sudo tail -f /var/log/supervisor/dasandpartners.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Database Backup:
```bash
sudo -u postgres pg_dump dasandpartners_db > backup_$(date +%Y%m%d).sql
```

---

## 🔒 Security Checklist

After deployment, ensure:

- [ ] Changed admin password
- [ ] Updated SECRET_KEY in .env
- [ ] Configured firewall (UFW)
- [ ] SSL certificate installed (HTTPS)
- [ ] DEBUG = False in production
- [ ] Database password is strong
- [ ] Regular backups scheduled
- [ ] Server security updates enabled

---

## 📊 Monitoring

### Check Server Resources:
```bash
# CPU and Memory
htop

# Disk space
df -h

# Network
netstat -tulpn
```

### Website Performance:
```bash
# Test response time
curl -w "@-" -o /dev/null -s https://dasandpartners.com <<'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
          time_total:  %{time_total}\n
EOF
```

---

## 🆘 Troubleshooting

### Website Not Loading?

1. **Check Nginx**:
```bash
sudo nginx -t
sudo systemctl status nginx
```

2. **Check Gunicorn**:
```bash
sudo supervisorctl status dasandpartners
sudo tail -f /var/log/supervisor/dasandpartners.log
```

3. **Check Firewall**:
```bash
sudo ufw status
```

### Database Connection Error?

```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -d dasandpartners_db
```

### Static Files Not Loading?

```bash
cd /home/dasandpartners
sudo -u dasandpartners /home/dasandpartners/venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

---

## 📞 Support

If you encounter issues:

1. Check logs first
2. Review this guide
3. Check Django documentation
4. Contact GoDaddy support for VPS issues
5. Google specific error messages

---

## 🎉 Success Checklist

Your deployment is successful if:

- [ ] Website loads at https://dasandpartners.com
- [ ] Homepage displays correctly
- [ ] Admin panel accessible
- [ ] Can add blogs and news
- [ ] Blogs appear on homepage
- [ ] Contact form works
- [ ] Newsletter subscription works
- [ ] SSL certificate (HTTPS) working
- [ ] Mobile responsive

---

## 📚 Next Steps

1. **Add Content**:
   - Create blog categories
   - Write your first blog post
   - Add company news
   - Upload project images

2. **SEO Optimization**:
   - Submit sitemap to Google
   - Set up Google Analytics
   - Verify Google Search Console
   - Add meta descriptions

3. **Performance**:
   - Enable Cloudflare (free CDN)
   - Optimize images
   - Enable caching

4. **Backup**:
   - Set up automated database backups
   - Configure file backups
   - Test restore process

---

## 💡 Pro Tips

1. **Use screen for long deployments**:
```bash
screen -S deployment
./deploy.sh
# Press Ctrl+A then D to detach
# screen -r deployment to reattach
```

2. **Set up automatic updates**:
```bash
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

3. **Monitor uptime**:
   - Use UptimeRobot.com (free)
   - Get alerts if site goes down

4. **Regular maintenance**:
   - Update packages monthly
   - Review logs weekly
   - Test backups monthly

---

## 🎯 Summary

Your Django website is now:
- ✅ Running on GoDaddy VPS
- ✅ Using PostgreSQL database
- ✅ Secured with SSL/HTTPS
- ✅ Professional setup
- ✅ Production-ready
- ✅ Connected to dasandpartners.com

**Total Deployment Time**: 30-45 minutes

**Your website is LIVE!** 🎉

Visit: https://dasandpartners.com


