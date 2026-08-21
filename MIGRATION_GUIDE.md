# 🔄 Live Site Migration Guide

## Moving Das and Partners from Simple Hosting to VPS

**Safe migration with ZERO data loss and minimal downtime!** ✨

---

## 📊 Migration Overview

```
Current Status:
├── Live site on simple hosting ✅
├── Domain already working ✅
├── Has blogs, news, images ✅
└── Users accessing now ✅

Goal:
├── Deploy new version to VPS ✅
├── Keep old site running (safety) ✅
├── Test new site on VPS IP ✅
├── Switch domain when ready ✅
└── Minimal downtime (5-30 min) ✅
```

---

## 🎯 Migration Steps

### Phase 1: Deploy to VPS (Test Environment)

**1. Connect to VPS:**
```bash
ssh root@YOUR_VPS_IP
# Enter password when prompted
```

**2. Run Deployment Script:**
```bash
# Upload script from Mac
scp GODADDY_VPS_DEPLOYMENT.sh root@YOUR_VPS_IP:~/

# SSH to VPS
ssh root@YOUR_VPS_IP

# Run deployment
chmod +x GODADDY_VPS_DEPLOYMENT.sh
./GODADDY_VPS_DEPLOYMENT.sh
```

**3. Upload Django Code:**
```bash
# From your Mac
cd "/Users/haider/Desktop/new backup/dasandpartners-django-main"

# Option 1: SCP
scp -r * root@YOUR_VPS_IP:/var/www/dasandpartners/

# Option 2: Use FileZilla (GUI)
# Connect to VPS IP via SFTP and upload
```

**4. Test on VPS IP:**
```
Open browser: http://YOUR_VPS_IP
Should see new site! ✅
Old site still on domain ✅
```

---

### Phase 2: Export Data from Current Hosting

**Option A: If you have database access (cPanel/phpMyAdmin):**
```bash
1. Login to current hosting cPanel
2. Go to phpMyAdmin
3. Select your database
4. Click "Export" → "Go"
5. Download SQL file
```

**Option B: Use Django admin export:**
```bash
# On current hosting, run:
python manage.py dumpdata das_app.Blogs > blogs_backup.json
python manage.py dumpdata das_app.News > news_backup.json

# Download these files
```

**Option C: Use my export script:**
```python
# Run export_data.py on current hosting
# Creates CSV files with all data
```

---

### Phase 3: Import Data to New VPS

**1. Upload old data:**
```bash
# From Mac to VPS
scp blogs_backup.json root@YOUR_VPS_IP:/var/www/dasandpartners/
scp news_backup.json root@YOUR_VPS_IP:/var/www/dasandpartners/
```

**2. Import data:**
```bash
# SSH to VPS
ssh root@YOUR_VPS_IP
cd /var/www/dasandpartners
source venv/bin/activate

# Import
python manage.py loaddata blogs_backup.json
python manage.py loaddata news_backup.json
```

**3. Copy images:**
```bash
# Download images from old hosting
# Upload to VPS:
scp -r old_media/* root@YOUR_VPS_IP:/var/www/dasandpartners/media/
```

---

### Phase 4: Test Everything

**Test checklist:**
```
□ Homepage loads: http://YOUR_VPS_IP
□ All blogs show correctly
□ All news show correctly
□ Images display properly
□ Admin login works: http://YOUR_VPS_IP/admin/
□ Content dashboard works: http://YOUR_VPS_IP/content-dashboard/
□ Can add new blog
□ Can add new news
□ Upload images work
```

---

### Phase 5: DNS Switch (Go Live!)

**When everything tested and ready:**

**1. Update DNS A Records:**
```
Login to your domain DNS management (GoDaddy?)

Add/Update A Records:
├── @ (root) → YOUR_VPS_IP
└── www → YOUR_VPS_IP

Save changes
```

**2. Wait for DNS propagation:**
```
Check: https://dnschecker.org
Enter your domain
Should show new VPS IP spreading globally
Takes 5-30 minutes usually
```

**3. Get SSL Certificate:**
```bash
# SSH to VPS
ssh root@YOUR_VPS_IP

# Run certbot
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts, enter email
# SSL installed! ✅
```

**4. Verify:**
```
Visit: https://yourdomain.com
Should see new site with SSL! 🎉
```

---

### Phase 6: Post-Migration

**1. Monitor for 24 hours:**
```
□ Check site works
□ Check logs: tail -f /var/www/dasandpartners/logs/gunicorn_error.log
□ Monitor traffic
□ Fix any issues
```

**2. Keep old hosting for 30 days:**
```
Safety backup!
If anything goes wrong:
- Change DNS back to old hosting
- Fix issue on VPS
- Switch again when ready
```

**3. After 30 days:**
```
✅ Everything works great?
✅ Cancel old hosting
✅ Save money! 💰
```

---

## 🔒 Safety Features

### Zero Data Loss:
```
✅ Old site stays active during migration
✅ Can test on VPS IP first
✅ Can rollback anytime (just change DNS)
✅ Old hosting = 30-day safety net
```

### Minimal Downtime:
```
DNS Switch: 5-30 minutes
During propagation:
├── Some users → old site (cached DNS)
└── Some users → new site (updated DNS)
Both work! No errors! ✅
```

---

## 📋 Timeline

```
Day 1: VPS Setup (2-3 hours)
├── Deploy to VPS
├── Test on VPS IP
└── Fix any issues

Day 2: Data Migration (2-4 hours)
├── Export from old hosting
├── Import to VPS
├── Copy images
└── Verify all data

Day 3-7: Testing (optional)
├── Team reviews new site
├── Test all features
├── Get approval
└── Plan DNS switch

Day 7: Go Live! (30 minutes)
├── Update DNS
├── Wait for propagation
├── Install SSL
└── Celebrate! 🎉
```

---

## 🚨 Troubleshooting

### Can't connect to VPS?
```bash
# Check VPS is running in GoDaddy panel
# Try: ping YOUR_VPS_IP
# Check firewall allows SSH (port 22)
```

### Can't access VPS IP in browser?
```bash
# Check nginx is running:
ssh root@YOUR_VPS_IP
sudo systemctl status nginx

# Check firewall:
sudo ufw status
```

### Images not showing after migration?
```bash
# Check permissions:
sudo chown -R www-data:www-data /var/www/dasandpartners/media
sudo chmod -R 775 /var/www/dasandpartners/media
```

### Domain not pointing to VPS?
```bash
# Check DNS propagation:
# Visit: https://dnschecker.org

# Check A records:
nslookup yourdomain.com
# Should show YOUR_VPS_IP
```

---

## 💡 Pro Tips

1. **Do migration on weekend** (less traffic)
2. **Test thoroughly on VPS IP** before DNS switch
3. **Keep old hosting active** for 30 days
4. **Announce maintenance** to users (optional)
5. **Have rollback plan** ready (change DNS back)

---

## 📞 Quick Commands

```bash
# Connect to VPS
ssh root@YOUR_VPS_IP

# Check status
cd /var/www/dasandpartners
./status.sh

# Restart services
./restart.sh

# View logs
tail -f logs/gunicorn_error.log

# Check DNS
nslookup yourdomain.com
```

---

## ✅ Migration Checklist

### Before DNS Switch:
- [ ] VPS deployed and working
- [ ] Tested on VPS IP
- [ ] All data imported
- [ ] All images migrated
- [ ] Admin login works
- [ ] Dashboard works
- [ ] Team approved

### During DNS Switch:
- [ ] Update A records
- [ ] Monitor DNS propagation
- [ ] Install SSL certificate
- [ ] Test domain access
- [ ] Verify HTTPS works

### After DNS Switch:
- [ ] Monitor for 24 hours
- [ ] Check logs
- [ ] Keep old hosting active
- [ ] Document any issues
- [ ] Celebrate success! 🎉

---

**Safe, professional migration with minimal risk!** ✨

**Need help? I'm here for every step!** 💪





