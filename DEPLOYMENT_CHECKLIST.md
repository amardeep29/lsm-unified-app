# 🚀 Client Onboarding System - Deployment Checklist

## Pre-Deployment Checklist

### ☑️ Environment Configuration

- [ ] **Cloudinary Account Setup**
  - [ ] Cloud name obtained
  - [ ] API key generated
  - [ ] API secret secured
  - [ ] Upload preset created (`ml_default` or custom)
  - [ ] Preset configured as **unsigned**
  - [ ] Billing enabled (if applicable)

- [ ] **Environment Variables**
  - [ ] `.env` file created from `.env.template`
  - [ ] `CLOUDINARY_CLOUD_NAME` set
  - [ ] `CLOUDINARY_API_KEY` set
  - [ ] `CLOUDINARY_API_SECRET` set
  - [ ] `CLOUDINARY_UPLOAD_PRESET` set
  - [ ] `GOOGLE_AI_API_KEY` set (for main app)
  - [ ] `.env` file added to `.gitignore`

- [ ] **Dependencies Installed**
  ```bash
  pip install -r requirements.txt
  ```
  - [ ] `cloudinary>=1.36.0`
  - [ ] `streamlit>=1.28.0`
  - [ ] `Flask>=3.0.0`
  - [ ] `requests>=2.31.0`
  - [ ] All other dependencies installed

### ☑️ Cloudinary Setup

#### Create Upload Preset

1. [ ] Login to [Cloudinary Dashboard](https://cloudinary.com/console)
2. [ ] Navigate to **Settings** → **Upload**
3. [ ] Scroll to **Upload presets** section
4. [ ] Click **"Add upload preset"**
5. [ ] Configure preset:
   ```
   Preset name: ml_default (or your choice)
   Signing mode: Unsigned ✓
   Folder: (leave empty - set dynamically)
   Access mode: Public
   Unique filename: true
   ```
6. [ ] Click **Save**
7. [ ] Copy preset name to `.env` file

#### Verify Cloudinary Access

```bash
# Test API access
curl -X GET "https://api.cloudinary.com/v1_1/YOUR_CLOUD_NAME/resources/image" \
  -u "YOUR_API_KEY:YOUR_API_SECRET"
```

### ☑️ File Structure Verification

```
nano_banana_project/
├── src/
│   ├── cloudinary_utils.py ✓
│   └── nano_banana_client.py ✓
├── config/
│   └── config.py ✓
├── client_onboarding.py ✓ (NEW)
├── api_server.py ✓ (UPDATED)
├── app.py ✓
├── .env ✓ (created from template)
├── .env.template ✓ (UPDATED)
├── requirements.txt ✓
└── Documentation:
    ├── CLIENT_ONBOARDING_GUIDE.md ✓
    ├── ONBOARDING_QUICKSTART.md ✓
    └── ONBOARDING_IMPLEMENTATION_SUMMARY.md ✓
```

## Testing Checklist

### ☑️ Local Testing

#### 1. API Server Tests

```bash
# Start API server
python api_server.py
```

- [ ] Server starts without errors
- [ ] Port 5000 is accessible
- [ ] Health check works: `http://localhost:5000/health`
- [ ] API documentation loads: `http://localhost:5000/`

**Test Endpoints:**

```bash
# Test /api/check-client
curl -X POST http://localhost:5000/api/check-client \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test-client"}'

# Expected: {"success": true, "exists": false, ...}
```
- [ ] Returns success response
- [ ] Validates client name
- [ ] Handles errors gracefully

```bash
# Test /api/create-client-folders
curl -X POST http://localhost:5000/api/create-client-folders \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test-client"}'

# Expected: {"success": true, "folders_created": [...], ...}
```
- [ ] Creates folders successfully
- [ ] Returns folder information
- [ ] Handles duplicate creation

```bash
# Test /api/get-upload-config
curl -X POST http://localhost:5000/api/get-upload-config \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test-client"}'

# Expected: {"success": true, "cloud_name": "...", ...}
```
- [ ] Returns valid configuration
- [ ] Includes all required fields

#### 2. Onboarding Interface Tests

```bash
# Start onboarding interface
streamlit run client_onboarding.py
```

- [ ] Interface loads at `http://localhost:8501`
- [ ] No console errors
- [ ] CSS styles render correctly

**Step 1: Client Information**
- [ ] Input field accepts text
- [ ] Validation works (length, characters)
- [ ] Sanitization converts spaces to hyphens
- [ ] "Check Availability" button works
- [ ] Existing client warning displays
- [ ] New client success message displays
- [ ] Proceed buttons work

**Step 2: Folder Creation**
- [ ] Displays client name correctly
- [ ] "Create Folders" button works
- [ ] Loading spinner shows during creation
- [ ] Success message displays
- [ ] Proceeds to next step automatically
- [ ] Back button works

**Step 3: Image Upload**
- [ ] Upload widget HTML renders
- [ ] "Click to Upload Images" button appears
- [ ] Widget opens when clicked
- [ ] Can select files
- [ ] Upload progress shows
- [ ] Images upload to correct folder
- [ ] Manual count input works
- [ ] Navigation buttons work

**Step 4: Completion**
- [ ] Summary displays correctly
- [ ] Statistics are accurate
- [ ] Action buttons work
- [ ] Can start new onboarding

#### 3. Integration Tests

**End-to-End Flow:**
- [ ] Start fresh session
- [ ] Enter client name "Test-Client-123"
- [ ] Check availability
- [ ] Create folders
- [ ] Upload 5 test images
- [ ] Verify completion summary
- [ ] Check Cloudinary dashboard:
  ```
  Test-Client-123/
  ├── input/ (5 images)
  ├── generated/ (.placeholder)
  └── edited/ (.placeholder)
  ```

**Edge Cases:**
- [ ] Empty client name
- [ ] Very short name (< 3 chars)
- [ ] Very long name (> 50 chars)
- [ ] Special characters
- [ ] Existing client with images
- [ ] Network timeout simulation
- [ ] Large file upload (> 10MB)
- [ ] Non-image file upload

### ☑️ Browser Compatibility

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

### ☑️ Performance Testing

- [ ] Folder creation < 5 seconds
- [ ] Client check < 2 seconds
- [ ] Upload 10 images < 30 seconds
- [ ] Upload 50 images < 150 seconds
- [ ] Interface responsive during operations

## Production Deployment

### ☑️ Pre-Production

- [ ] All local tests passed
- [ ] No console errors
- [ ] Documentation complete
- [ ] `.env` file configured for production
- [ ] Cloudinary limits verified
- [ ] Backup API keys stored securely

### ☑️ Security Review

- [ ] `.env` file not committed to Git
- [ ] API keys stored securely
- [ ] Upload preset is unsigned (required)
- [ ] HTTPS enabled (production)
- [ ] Rate limiting considered
- [ ] Error messages don't leak sensitive info
- [ ] Input validation comprehensive

### ☑️ Deployment Steps

#### Option 1: Local/Internal Deployment

```bash
# Terminal 1
python api_server.py

# Terminal 2
streamlit run client_onboarding.py --server.port 8501
```

#### Option 2: Server Deployment

```bash
# Using PM2 or similar process manager
pm2 start api_server.py --name "onboarding-api"
pm2 start "streamlit run client_onboarding.py" --name "onboarding-ui"
```

#### Option 3: Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000 8501
CMD ["sh", "-c", "python api_server.py & streamlit run client_onboarding.py --server.port 8501"]
```

### ☑️ Post-Deployment Verification

- [ ] API server accessible at production URL
- [ ] Streamlit interface accessible at production URL
- [ ] Health check endpoint responds
- [ ] Can onboard test client
- [ ] Cloudinary folders created correctly
- [ ] Images upload successfully
- [ ] No errors in production logs

### ☑️ Monitoring Setup

- [ ] API server logs monitored
- [ ] Streamlit logs monitored
- [ ] Cloudinary usage dashboard checked
- [ ] Error alerts configured
- [ ] Uptime monitoring enabled

## User Training

### ☑️ Documentation Distribution

- [ ] `ONBOARDING_QUICKSTART.md` shared with users
- [ ] `CLIENT_ONBOARDING_GUIDE.md` available for reference
- [ ] Naming conventions documented
- [ ] Support contact information provided

### ☑️ User Training

- [ ] Demo session conducted
- [ ] Walk through complete flow
- [ ] Explain validation rules
- [ ] Show error handling
- [ ] Demonstrate troubleshooting

### ☑️ Support Preparation

- [ ] Support team trained
- [ ] Common issues documented
- [ ] Troubleshooting guide distributed
- [ ] Escalation path defined
- [ ] Contact information shared

## Maintenance

### ☑️ Regular Checks

**Daily:**
- [ ] Monitor error logs
- [ ] Check Cloudinary usage
- [ ] Verify service uptime

**Weekly:**
- [ ] Review onboarding metrics
- [ ] Clean up test clients (if needed)
- [ ] Check API rate limits

**Monthly:**
- [ ] Rotate API keys (if policy requires)
- [ ] Review and archive logs
- [ ] Update documentation
- [ ] Test disaster recovery

### ☑️ Backup & Recovery

- [ ] `.env` file backed up securely
- [ ] API keys documented (secure location)
- [ ] Cloudinary account recovery plan
- [ ] Server configuration documented

## Rollback Plan

### ☑️ If Issues Occur

1. [ ] **Immediate Actions:**
   - Stop affected services
   - Notify users
   - Switch to backup/manual process

2. [ ] **Investigation:**
   - Check error logs
   - Review recent changes
   - Test in staging environment

3. [ ] **Rollback if Needed:**
   - Revert to previous version
   - Restore from backup
   - Verify functionality

4. [ ] **Communication:**
   - Notify stakeholders
   - Document issue
   - Plan fix deployment

## Success Criteria

### ☑️ Launch Requirements

- [ ] All tests passed
- [ ] Documentation complete
- [ ] Users trained
- [ ] Support ready
- [ ] Monitoring active
- [ ] Rollback plan in place

### ☑️ Post-Launch Metrics (Week 1)

- [ ] > 90% successful onboardings
- [ ] < 5% error rate
- [ ] Average completion time < 5 minutes
- [ ] Zero critical errors
- [ ] Positive user feedback

## Contact Information

**Support:**
- Technical Lead: _________________
- System Admin: _________________
- Cloudinary Support: support@cloudinary.com

**Emergency Contacts:**
- On-call engineer: _________________
- Backup contact: _________________

---

## Sign-Off

**Deployment Approval:**

- [ ] Development: _________________ Date: _______
- [ ] QA/Testing: _________________ Date: _______
- [ ] Security: _________________ Date: _______
- [ ] Management: _________________ Date: _______

**Production Release:**

- [ ] Deployment Date: _________________
- [ ] Deployed By: _________________
- [ ] Verified By: _________________

---

**Version**: 1.0.0
**Last Updated**: October 2025
**Status**: Ready for Deployment
