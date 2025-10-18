# LSM Unified App - AWS EC2 Deployment Guide

Complete guide for deploying the LSM Unified App on a single AWS EC2 instance.

## Architecture

All services run on **one EC2 instance**:
- Flask API (Port 5001) - Main dashboard, Upload/Label pages, API endpoints
- Streamlit Image Studio (Port 8502) - AI image generation and editing
- Streamlit Client Onboarding (Port 8501) - 5-step onboarding workflow

## Prerequisites

1. AWS Account
2. Basic knowledge of AWS EC2 and SSH
3. Your API credentials:
   - Google AI API Key
   - Cloudinary credentials

## Step 1: Launch EC2 Instance

### Instance Specifications

**Recommended:**
- **Instance Type:** t3.small or t3.medium (2 vCPU, 2-4GB RAM)
- **AMI:** Ubuntu 22.04 LTS
- **Storage:** 20GB gp3 SSD minimum
- **Region:** Choose closest to your users

### Security Group Rules

Create a security group with these inbound rules:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | Your IP | SSH access |
| HTTP | TCP | 80 | 0.0.0.0/0 | Web access |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Secure web access |
| Custom TCP | TCP | 5001 | 0.0.0.0/0 | Flask API (if not using nginx) |
| Custom TCP | TCP | 8501 | 0.0.0.0/0 | Client Onboarding (if not using nginx) |
| Custom TCP | TCP | 8502 | 0.0.0.0/0 | Image Studio (if not using nginx) |

**Note:** If using nginx reverse proxy, you only need ports 22, 80, and 443.

### Key Pair

- Create or use existing SSH key pair
- Download the `.pem` file and keep it secure
- Set permissions: `chmod 400 your-key.pem`

## Step 2: Connect to Your Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## Step 3: Run Deployment Script

```bash
# Update system first
sudo apt-get update

# Download and run deployment script
wget https://raw.githubusercontent.com/amardeep29/lsm-unified-app/main/deploy_aws.sh
sudo bash deploy_aws.sh
```

This script will:
1. Update system packages
2. Install Python 3.11, pip, Git, Nginx
3. Create application user
4. Clone the repository
5. Set up Python virtual environment
6. Install dependencies
7. Create `.env` template

## Step 4: Configure Environment Variables

```bash
sudo nano /home/lsmapp/lsm-unified-app/.env
```

Update with your actual credentials:

```bash
# Google AI API Key
GOOGLE_AI_API_KEY=your_actual_key_here

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_UPLOAD_PRESET=client_onboarding_unsigned

# Client Configuration
CLIENT_FOLDER_NAME=XV1

# Server Configuration
PORT=5001
STUDIO_PORT=8501
ONBOARDING_PORT=8502

# Public URL - Set to your domain or EC2 public IP
PUBLIC_URL=http://your-ec2-ip-or-domain.com

# Use nginx reverse proxy (recommended)
USE_NGINX=true
```

Save and exit (Ctrl+X, Y, Enter)

## Step 5: Set Up Systemd Services

```bash
cd /home/lsmapp/lsm-unified-app
sudo bash setup_services.sh
```

This creates three systemd services that:
- Start automatically on system boot
- Restart automatically if they crash
- Run as the `lsmapp` user (security best practice)

## Step 6: Configure Nginx (Recommended)

### Copy nginx configuration

```bash
sudo cp /home/lsmapp/lsm-unified-app/nginx.conf /etc/nginx/sites-available/lsm-unified-app
```

### Edit the configuration

```bash
sudo nano /etc/nginx/sites-available/lsm-unified-app
```

Update `server_name` to your domain or EC2 public IP:
```nginx
server_name your-domain.com;  # or your EC2 IP
```

### Enable the site

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/lsm-unified-app /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# If test passes, reload nginx
sudo systemctl reload nginx
```

## Step 7: Start All Services

```bash
sudo systemctl start lsm-flask lsm-studio lsm-onboarding
```

Check status:
```bash
sudo systemctl status lsm-flask
sudo systemctl status lsm-studio
sudo systemctl status lsm-onboarding
```

## Step 8: Access Your Application

If using **nginx** (recommended):
- Main Dashboard: `http://your-domain-or-ip/`
- Image Studio: `http://your-domain-or-ip/studio`
- Client Onboarding: `http://your-domain-or-ip/onboarding`

If using **direct ports**:
- Main Dashboard: `http://your-domain-or-ip:5001/`
- Image Studio: `http://your-domain-or-ip:8502/`
- Client Onboarding: `http://your-domain-or-ip:8501/`

## Optional: Set Up SSL with Let's Encrypt

For production, enable HTTPS:

```bash
# Install certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

Uncomment the SSL section in nginx.conf and reload nginx.

## Maintenance Commands

### View Logs

```bash
# Real-time logs
sudo journalctl -u lsm-flask -f
sudo journalctl -u lsm-studio -f
sudo journalctl -u lsm-onboarding -f

# Last 100 lines
sudo journalctl -u lsm-flask -n 100
```

### Restart Services

```bash
# Restart all
sudo systemctl restart lsm-flask lsm-studio lsm-onboarding

# Restart individual service
sudo systemctl restart lsm-flask
```

### Update Application

```bash
cd /home/lsmapp/lsm-unified-app
sudo -u lsmapp git pull
sudo systemctl restart lsm-flask lsm-studio lsm-onboarding
```

### Monitor Resource Usage

```bash
# CPU and memory
htop

# Disk usage
df -h

# Service status
sudo systemctl status lsm-*
```

## Troubleshooting

### Service won't start

```bash
# Check detailed logs
sudo journalctl -u lsm-flask --no-pager -n 50

# Check if ports are in use
sudo netstat -tlnp | grep -E '5001|8501|8502'
```

### Nginx errors

```bash
# Test configuration
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/lsm-app-error.log
```

### Out of memory

Upgrade to larger instance type (t3.medium or t3.large)

### Can't connect to services

- Check security group rules
- Verify services are running: `sudo systemctl status lsm-*`
- Check firewall: `sudo ufw status`

## Cost Estimation

### AWS Costs (us-east-1 region)

| Instance Type | vCPU | RAM | Price/month | Recommended For |
|---------------|------|-----|-------------|-----------------|
| t3.small | 2 | 2GB | ~$15 | Development/Testing |
| t3.medium | 2 | 4GB | ~$30 | Production (Light) |
| t3.large | 2 | 8GB | ~$60 | Production (Heavy) |

**Additional costs:**
- Storage: ~$2/month for 20GB
- Data transfer: First 100GB free, then $0.09/GB
- Elastic IP: Free if attached to running instance

**Total estimated cost:** $17-70/month depending on instance type

## Backup Strategy

### Manual Backup

```bash
# Backup .env file
sudo cp /home/lsmapp/lsm-unified-app/.env ~/lsm-app-backup.env

# Create AMI from EC2 console for full instance backup
```

### Automated Backups

Use AWS Backup or create snapshots via AWS CLI:
```bash
aws ec2 create-snapshot --volume-id vol-xxxxx --description "LSM App Backup"
```

## Security Best Practices

1. **Regular Updates**
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Enable UFW Firewall**
   ```bash
   sudo ufw allow ssh
   sudo ufw allow http
   sudo ufw allow https
   sudo ufw enable
   ```

3. **Use Strong SSH Keys**
   - Disable password authentication
   - Use ed25519 keys

4. **Regular Monitoring**
   - Set up CloudWatch alarms
   - Monitor logs daily

5. **Keep Secrets Secure**
   - Never commit .env to git
   - Use AWS Secrets Manager for production

## Support

- GitHub Issues: https://github.com/amardeep29/lsm-unified-app/issues
- AWS Documentation: https://docs.aws.amazon.com/ec2/

## License

Generated with Claude Code - https://claude.com/claude-code
