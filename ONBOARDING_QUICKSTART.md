# 🚀 Client Onboarding - Quick Start Guide

## Setup (5 minutes)

### 1. Configure Environment

```bash
# Edit .env file
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_UPLOAD_PRESET=ml_default  # Create this in Cloudinary dashboard
```

### 2. Create Upload Preset in Cloudinary

1. Login to Cloudinary Dashboard
2. Go to **Settings** → **Upload**
3. Click **Add upload preset**
4. Set:
   - Name: `ml_default`
   - Signing mode: **Unsigned**
   - Save
5. Copy preset name to `.env`

### 3. Start Services

**Terminal 1 - API Server:**
```bash
python api_server.py
```

**Terminal 2 - Onboarding Interface:**
```bash
streamlit run client_onboarding.py
```

**Open Browser:**
```
http://localhost:8501
```

## Usage (2 minutes per client)

### Step 1: Enter Client Name
1. Type client name (e.g., `ABC-Company`)
2. Click **"Check Availability"**
3. Click **"Continue to Folder Creation"**

### Step 2: Create Folders
1. Click **"Create Folders"**
2. Wait for success message
3. Auto-advances to upload

### Step 3: Upload Images
1. Click **"Click to Upload Images"**
2. Select files (up to 100 images)
3. Wait for uploads to complete
4. Close widget
5. Click **"Complete Onboarding"**

### Step 4: Done!
- View summary
- Start new client or return to main app

## API Endpoints

### Check if Client Exists
```bash
curl -X POST http://localhost:5000/api/check-client \
  -H "Content-Type: application/json" \
  -d '{"client_name":"abc-company"}'
```

### Create Client Folders
```bash
curl -X POST http://localhost:5000/api/create-client-folders \
  -H "Content-Type: application/json" \
  -d '{"client_name":"abc-company"}'
```

### Get Upload Configuration
```bash
curl -X POST http://localhost:5000/api/get-upload-config \
  -H "Content-Type: application/json" \
  -d '{"client_name":"abc-company"}'
```

## Cloudinary Folder Structure

```
abc-company/
├── input/          ← Uploaded images go here
├── generated/      ← AI-generated images
└── edited/         ← AI-edited images
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Widget doesn't load | Check upload preset is unsigned |
| Folder creation fails | Verify Cloudinary credentials |
| API not responding | Ensure API server is running |
| Upload fails | Check file size < 10MB |

## Validation Rules

- **Length**: 3-50 characters
- **Characters**: Letters, numbers, hyphens only
- **Spaces**: Auto-converted to hyphens
- **Example**: `ABC Company` → `abc-company`

## Next Steps After Onboarding

1. **Generate Images**: Use client folder in generation requests
2. **View Gallery**: Browse uploaded images in Image Gallery tab
3. **Edit Images**: Select images for AI editing

## Support

- 📖 Full guide: `CLIENT_ONBOARDING_GUIDE.md`
- 🔧 API docs: `http://localhost:5000/`
- 🐛 Issues: Check browser console & server logs

---

**Quick Reference:**

✅ **Valid Names**: `ABC-Company`, `client-2024`, `test-client`
❌ **Invalid Names**: `ABC Company` (space), `ab` (too short), `client@123` (special char)

**Upload Limits:**
- Max files: 100 per batch
- Max size: 10MB per file
- Formats: All image formats (PNG, JPG, GIF, etc.)
