# API Changes - Dynamic Client Folder Support

## Overview

The API server has been updated to accept `client_folder` as a **request parameter** instead of relying solely on the `CLIENT_FOLDER_NAME` environment variable. This allows different clients to use the same API instance while organizing their images in separate Cloudinary folders.

## What Changed

### Version 2.0.0 Updates

1. **CloudinaryManager** (`src/cloudinary_utils.py`)
   - `upload_image()` method now accepts optional `client_folder` parameter
   - Falls back to `CLIENT_FOLDER_NAME` environment variable if not provided
   - Returns error if neither is available

2. **API Server** (`api_server.py`)
   - `/generate` endpoint now accepts `client_folder` in request body
   - `/edit` endpoint now accepts `client_folder` in request body
   - Both endpoints validate that `client_folder` is provided when using Cloudinary
   - API version bumped to 2.0.0

3. **Environment Variables**
   - `CLIENT_FOLDER_NAME` is now **optional**
   - Can be provided per-request instead of via environment
   - Updated `.env.template` to reflect this change

## API Usage

### Before (Version 1.0.0)

**Environment Required:**
```bash
CLIENT_FOLDER_NAME=CompanyABC  # Hardcoded for all requests
```

**Request:**
```json
POST /generate
{
  "prompt": "A sunset over mountains"
}
```

**Result:** Images stored in `CompanyABC/generated/`

---

### After (Version 2.0.0)

**Environment Optional:**
```bash
CLIENT_FOLDER_NAME=  # Can be empty or omitted
```

**Request:**
```json
POST /generate
{
  "prompt": "A sunset over mountains",
  "client_folder": "CompanyXYZ"
}
```

**Result:** Images stored in `CompanyXYZ/generated/`

## Request Examples

### Generate Image

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cute robot in a field of flowers",
    "client_folder": "ClientA"
  }'
```

**Response:**
```json
{
  "success": true,
  "image_url": "https://res.cloudinary.com/.../ClientA/generated/generated_1728345678.png",
  "public_id": "ClientA/generated/generated_1728345678",
  "prompt": "A cute robot in a field of flowers",
  "client_folder": "ClientA"
}
```

### Edit Image

```bash
curl -X POST http://localhost:5000/edit \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "prompt": "Add sunglasses and a hat",
    "client_folder": "ClientB"
  }'
```

**Response:**
```json
{
  "success": true,
  "image_url": "https://res.cloudinary.com/.../ClientB/edited/edited_1728345679.png",
  "public_id": "ClientB/edited/edited_1728345679",
  "prompt": "Add sunglasses and a hat",
  "original_url": "https://example.com/image.jpg",
  "client_folder": "ClientB"
}
```

## Cloudinary Folder Structure

With dynamic `client_folder`, you can organize images for multiple clients:

```
cloudinary_root/
├── ClientA/
│   ├── generated/
│   │   └── generated_1728345678.png
│   └── edited/
│       └── edited_1728345679.png
├── ClientB/
│   ├── generated/
│   │   └── generated_1728345680.png
│   └── edited/
│       └── edited_1728345681.png
└── ClientC/
    ├── generated/
    │   └── generated_1728345682.png
    └── edited/
        └── edited_1728345683.png
```

## Error Handling

### Missing client_folder

**Request without client_folder:**
```json
POST /generate
{
  "prompt": "A sunset"
}
```

**Response:**
```json
{
  "success": false,
  "error": "Missing required field: client_folder (required when using Cloudinary)"
}
```

### Fallback to Environment Variable

If `CLIENT_FOLDER_NAME` is set in environment and no `client_folder` is provided in the request, the environment variable will be used as a fallback.

**Environment:**
```bash
CLIENT_FOLDER_NAME=DefaultClient
```

**Request (no client_folder):**
```json
POST /generate
{
  "prompt": "A sunset"
}
```

**Result:** Images stored in `DefaultClient/generated/`

## Migration Guide

### For Existing Deployments

**Option 1: Keep Current Behavior (Recommended for single-client deployments)**
```bash
# Keep CLIENT_FOLDER_NAME in .env
CLIENT_FOLDER_NAME=YourClientName

# Requests work without client_folder parameter
# (but you can override with client_folder in request)
```

**Option 2: Switch to Per-Request Folders (Recommended for multi-client deployments)**
```bash
# Remove or leave empty in .env
CLIENT_FOLDER_NAME=

# Always provide client_folder in requests
```

### For n8n Workflows

Update your HTTP Request nodes to include `client_folder`:

**Before:**
```json
{
  "prompt": "{{$json.prompt}}"
}
```

**After:**
```json
{
  "prompt": "{{$json.prompt}}",
  "client_folder": "{{$json.client_name}}"
}
```

## Benefits

1. **Multi-tenancy**: Single API instance can serve multiple clients
2. **Flexibility**: Choose client folder per request
3. **Organization**: Better Cloudinary folder structure
4. **Backward Compatible**: Still works with environment variable
5. **No Breaking Changes**: Existing deployments continue to work

## API Documentation

Updated API documentation is available at the root endpoint:

```bash
curl http://localhost:5000/
```

This will return full API documentation including the new `client_folder` parameter.

---

**Version**: 2.0.0
**Date**: October 2025
**Breaking Changes**: None (backward compatible)
