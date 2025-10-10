# 📋 Client Onboarding System - Complete Guide

## Overview

The **Client Onboarding System** is a web-based interface that streamlines the process of adding new clients to your Cloudinary-based image management workflow. It replaces manual folder creation and file uploads with an automated, user-friendly multi-step process.

## Features

### ✅ Automated Folder Creation
- Creates standardized folder structure: `{client_name}/input/`, `{client_name}/generated/`, `{client_name}/edited/`
- Validates folder naming conventions
- Checks for existing clients to prevent duplicates

### ✅ Bulk Image Upload
- Integrated Cloudinary Upload Widget
- Support for 100+ images in single batch
- Multiple upload sources (local files, camera, URL)
- Real-time upload progress
- Thumbnail previews

### ✅ Client Name Validation
- 3-50 characters length requirement
- Alphanumeric and hyphens only
- Automatic space-to-hyphen conversion
- Case-insensitive duplicate checking

### ✅ Multi-Step Process
- **Step 1**: Client Information & Validation
- **Step 2**: Cloudinary Folder Creation
- **Step 3**: Bulk Image Upload
- **Step 4**: Completion Summary

## Architecture

### Components

```
Client Onboarding System
├── Frontend (Streamlit)
│   └── client_onboarding.py
├── Backend API (Flask)
│   └── api_server.py
│       ├── /api/check-client
│       ├── /api/create-client-folders
│       └── /api/get-upload-config
└── Cloudinary Manager
    └── cloudinary_utils.py
        ├── check_client_exists()
        ├── create_client_folders()
        └── get_upload_config()
```

### Data Flow

```
User Input → Validation → API Check → Folder Creation → Upload Config → Cloudinary Widget → Completion
```

## Installation & Setup

### 1. Prerequisites

```bash
# Ensure dependencies are installed
pip install -r requirements.txt
```

### 2. Environment Configuration

Update your `.env` file with Cloudinary credentials:

```bash
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
CLOUDINARY_UPLOAD_PRESET=ml_default  # Or your custom preset
```

### 3. Create Cloudinary Upload Preset

**In Cloudinary Dashboard:**

1. Go to **Settings** → **Upload**
2. Scroll to **Upload presets**
3. Click **Add upload preset**
4. Configure:
   - **Preset name**: `ml_default` (or your choice)
   - **Signing mode**: Unsigned
   - **Folder**: Leave empty (will be set dynamically)
   - **Access mode**: Public
5. Save the preset
6. Update `CLOUDINARY_UPLOAD_PRESET` in `.env`

### 4. Start the Services

**Terminal 1 - API Server:**
```bash
python api_server.py
# Running on http://localhost:5000
```

**Terminal 2 - Onboarding Interface:**
```bash
streamlit run client_onboarding.py
# Open browser to http://localhost:8501
```

## User Guide

### Step 1: Enter Client Information

1. **Enter client name** in the text input
   - Minimum 3 characters
   - Maximum 50 characters
   - Only letters, numbers, and hyphens
   - Spaces automatically converted to hyphens

2. **Click "Check Availability"**
   - Green success: Client name available
   - Yellow warning: Client already exists (can proceed to add images)
   - Red error: Invalid client name format

3. **Review sanitized name** (if different from input)

4. **Click "Continue to Folder Creation"** or **"Proceed with Existing Client"**

**Example:**
```
Input:  "ABC Company 2024"
Output: "abc-company-2024"
```

### Step 2: Create Folder Structure

1. **Review folder creation details**
   - Client name
   - Folders to be created (input, generated, edited)

2. **Click "Create Folders"**
   - System creates folder structure in Cloudinary
   - Shows loading spinner during creation
   - Displays success message with folder paths

3. **Automatically proceeds** to upload step on success

**Folder Structure Created:**
```
ClientName/
├── input/
├── generated/
└── edited/
```

### Step 3: Upload Images

1. **Click "Click to Upload Images"** button
   - Opens Cloudinary Upload Widget
   - Configured for client's `input/` folder

2. **Select upload source**:
   - **Local Files**: Browse computer
   - **Camera**: Take photo (mobile/webcam)
   - **URL**: Provide image URL

3. **Select multiple files** (up to 100)
   - Maximum file size: 10MB per image
   - Accepted formats: All image formats

4. **Monitor upload progress**
   - Progress bar for each file
   - Thumbnail previews
   - Upload count

5. **Close widget** when done
   - Click "Complete Onboarding" to proceed

**Upload Widget Features:**
- Drag & drop support
- Multi-file selection
- Upload queue management
- Error handling per file
- Automatic retry on failure

### Step 4: Completion Summary

1. **Review onboarding summary**
   - Client name
   - Folders created
   - Images uploaded count
   - Cloudinary folder path

2. **Choose next action**:
   - **Onboard Another Client**: Start new onboarding
   - **View Image Gallery**: Browse uploaded images
   - **Generate Images**: Start AI image generation

## API Reference

### POST /api/check-client

Check if a client folder exists in Cloudinary.

**Request:**
```json
{
  "client_name": "abc-company"
}
```

**Response (Exists):**
```json
{
  "success": true,
  "exists": true,
  "folder_path": "abc-company",
  "subfolders": ["input", "generated", "edited"]
}
```

**Response (Not Exists):**
```json
{
  "success": true,
  "exists": false,
  "folder_path": "abc-company"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Client name can only contain letters, numbers, and hyphens"
}
```

### POST /api/create-client-folders

Create folder structure for a new client.

**Request:**
```json
{
  "client_name": "abc-company"
}
```

**Response:**
```json
{
  "success": true,
  "folders_created": ["input", "generated", "edited"],
  "folder_path": "abc-company",
  "message": "Successfully created folder structure for abc-company"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Folder creation failed: Permission denied",
  "folders_created": []
}
```

### POST /api/get-upload-config

Get Cloudinary upload widget configuration.

**Request:**
```json
{
  "client_name": "abc-company"
}
```

**Response:**
```json
{
  "success": true,
  "cloud_name": "your-cloud",
  "api_key": "your-key",
  "folder": "abc-company/input",
  "upload_preset": "ml_default"
}
```

## Validation Rules

### Client Name Validation

| Rule | Requirement | Example Valid | Example Invalid |
|------|-------------|---------------|-----------------|
| Length | 3-50 characters | `abc`, `long-client-name-2024` | `ab`, `a-very-long-client-name-that-exceeds-fifty-characters` |
| Characters | Alphanumeric + hyphens | `ABC-Company`, `client123` | `ABC Company`, `client@123` |
| Spaces | Not allowed (auto-converted) | `abc-company` | `abc company` |
| Case | Case-insensitive | `ABC` = `abc` | N/A |

### Auto-Sanitization

The system automatically:
- Converts spaces to hyphens
- Removes invalid characters
- Converts to lowercase

**Examples:**
```
"ABC Company" → "abc-company"
"Client #123" → "client-123"
"TEST__NAME" → "testname"
```

## Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Client name is required" | Empty input | Enter a client name |
| "Client name must be at least 3 characters" | Too short | Use longer name |
| "Client name can only contain letters, numbers, and hyphens" | Invalid characters | Remove special characters |
| "Client folder already exists" | Duplicate client | Proceed with existing or choose different name |
| "Connection timeout" | Network issue | Check internet connection, retry |
| "Cloudinary not configured" | Missing credentials | Verify `.env` configuration |
| "Folder creation failed" | Cloudinary permission | Check API key permissions |
| "Upload failed for {filename}" | File issue | Check file size/format, retry |

### Retry Mechanisms

- **Folder Creation**: Manual retry via "Create Folders" button
- **Upload**: Per-file retry in Cloudinary widget
- **API Calls**: 30-second timeout with error display

## Technical Implementation

### Folder Creation Method

Cloudinary doesn't have a direct "create folder" API. The system creates folders by:

1. Uploading a placeholder file (1x1 transparent PNG) to each subfolder
2. Placeholder ensures folder appears in Cloudinary console
3. Future uploads to these folders work normally

**Code:**
```python
# Upload placeholder to create folder structure
placeholder_data = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
)

cloudinary.uploader.upload(
    placeholder_data,
    folder=f"{client_name}/{subfolder}",
    public_id='.placeholder'
)
```

### Upload Widget Integration

The Cloudinary Upload Widget is embedded via HTML/JavaScript iframe:

```javascript
cloudinary.openUploadWidget({
    cloudName: 'your-cloud',
    uploadPreset: 'ml_default',
    folder: 'client-name/input',
    sources: ['local', 'camera', 'url'],
    multiple: true,
    maxFiles: 100,
    maxFileSize: 10000000
}, (error, result) => {
    // Handle upload success/error
});
```

### Session State Management

Streamlit session state tracks:

```python
{
    'onboarding_step': 1-4,              # Current step
    'client_name': "abc-company",        # Validated name
    'client_exists': False,              # Duplicate flag
    'folders_created': ["input", ...],   # Created folders
    'uploaded_images': [...],            # Upload results
    'cloudinary_config': {...}           # Upload config
}
```

## Testing Checklist

### Manual Testing

- [ ] **Step 1 Tests**
  - [ ] Empty client name shows error
  - [ ] Short name (< 3 chars) shows error
  - [ ] Long name (> 50 chars) shows error
  - [ ] Special characters show error or get sanitized
  - [ ] Spaces convert to hyphens
  - [ ] Existing client shows warning
  - [ ] New client shows success

- [ ] **Step 2 Tests**
  - [ ] Folders create successfully
  - [ ] Creation failure shows error with retry
  - [ ] Existing client skips creation
  - [ ] Success transitions to Step 3

- [ ] **Step 3 Tests**
  - [ ] Upload widget opens correctly
  - [ ] Can select multiple files
  - [ ] Upload progress displays
  - [ ] Large files rejected (> 10MB)
  - [ ] Non-image files rejected
  - [ ] Uploaded images show thumbnails
  - [ ] Widget closes and proceeds

- [ ] **Step 4 Tests**
  - [ ] Summary displays correctly
  - [ ] Can start new onboarding
  - [ ] Session state resets properly

### API Testing

```bash
# Test check-client endpoint
curl -X POST http://localhost:5000/api/check-client \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test-client"}'

# Test create-client-folders endpoint
curl -X POST http://localhost:5000/api/create-client-folders \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test-client"}'

# Test get-upload-config endpoint
curl -X POST http://localhost:5000/api/get-upload-config \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test-client"}'
```

## Performance Metrics

### Target Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Folder creation time | < 5 seconds | TBD |
| Client check time | < 2 seconds | TBD |
| Upload time per image | < 3 seconds | TBD |
| Batch upload (50 images) | < 150 seconds | TBD |
| Success rate | > 99% | TBD |

### Limitations

- **Max files per upload**: 100 (widget limit)
- **Max file size**: 10MB per image
- **Network timeout**: 30 seconds for API calls
- **Browser compatibility**: Modern browsers only (Chrome, Firefox, Safari, Edge)

## Troubleshooting

### Widget Not Loading

**Problem**: Upload widget doesn't appear

**Solutions:**
1. Check browser console for JavaScript errors
2. Verify Cloudinary script loaded: `https://upload-widget.cloudinary.com/global/all.js`
3. Ensure upload preset exists and is unsigned
4. Check network tab for blocked requests

### Folder Creation Fails

**Problem**: Error message during folder creation

**Solutions:**
1. Verify Cloudinary API credentials in `.env`
2. Check API key has upload permissions
3. Ensure cloud name is correct
4. Try creating folder manually in Cloudinary dashboard first
5. Check Cloudinary usage limits

### Upload Failures

**Problem**: Images fail to upload

**Solutions:**
1. Check file size (< 10MB)
2. Verify file format (image only)
3. Ensure upload preset is unsigned
4. Check network connectivity
5. Try uploading directly in Cloudinary dashboard
6. Verify folder path is correct

### API Not Responding

**Problem**: API endpoints return errors

**Solutions:**
1. Ensure API server is running (`python api_server.py`)
2. Check correct port (default: 5000)
3. Verify Flask app started without errors
4. Test health endpoint: `http://localhost:5000/health`
5. Check firewall/port blocking

## Best Practices

### For Administrators

1. **Naming Convention**: Establish client naming standards
2. **Regular Cleanup**: Remove placeholder files if needed
3. **Monitor Usage**: Track Cloudinary storage and API usage
4. **Backup Config**: Keep `.env` backed up securely
5. **Document Clients**: Maintain client registry

### For Users

1. **Use Descriptive Names**: `ABC-Corp-2024` vs `client1`
2. **Check Existing First**: Avoid duplicate attempts
3. **Batch Similar Images**: Upload related images together
4. **Verify Uploads**: Check completion summary
5. **Report Errors**: Note exact error messages for support

## Security Considerations

### API Security

- Upload preset must be **unsigned** for widget to work
- API endpoints validate input strictly
- No client data stored server-side
- Cloudinary handles authentication

### Best Practices

- ✅ Keep `.env` file secure and never commit to Git
- ✅ Use unique upload presets per environment
- ✅ Monitor Cloudinary access logs
- ✅ Rotate API keys periodically
- ✅ Set appropriate folder permissions in Cloudinary

## Future Enhancements

Planned features:

1. **Data Storage**: Save client registry to database
2. **Upload History**: Track upload sessions per client
3. **Batch Operations**: Bulk client onboarding
4. **Email Notifications**: Notify on completion
5. **Advanced Validation**: Custom naming rules
6. **Folder Templates**: Different folder structures
7. **Multi-user Support**: User authentication
8. **Analytics Dashboard**: Usage statistics

---

**Version**: 1.0.0
**Last Updated**: October 2025
**Status**: ✅ Production Ready
