# Testing Guide - Unified Application

## ✅ All Services Are Currently Running!

Your unified application is live and all services have been verified:

```
✅ Main Dashboard       - http://localhost:5001/
✅ Health Check         - http://localhost:5001/health
✅ API Documentation    - http://localhost:5001/api/docs
✅ Streamlit Onboarding - http://localhost:8501/
✅ Streamlit Studio     - http://localhost:8502/
✅ Upload Page          - http://localhost:5001/upload
✅ Label Images Page    - http://localhost:5001/label-images
```

---

## Quick Test Checklist

### 1. **Main Dashboard** (http://localhost:5001/)

**What to Test:**
- [ ] Page loads with beautiful gradient design
- [ ] All 4 service cards are visible:
  - 🎨 Image Studio
  - 📋 Client Onboarding
  - 📤 Upload Images
  - 📝 Label Images
- [ ] API endpoints section shows links
- [ ] Status indicator is pulsing (green dot)

**Expected Result:** Professional dashboard with working navigation links

---

### 2. **Client Onboarding Flow** (http://localhost:8501/)

**What to Test:**

**Step 1: Client Info**
- [ ] Enter client name (e.g., "test-client-2025")
- [ ] Click "Submit Client Name"
- [ ] Verify auto-correction works (spaces → hyphens)
- [ ] Click "Check Client Availability"
- [ ] Should show "✅ Client Name Available!"
- [ ] Click "Continue to Folder Creation"

**Step 2: Folder Setup**
- [ ] Shows client name correctly
- [ ] Lists 3 folders to create (input, generated, edited)
- [ ] Click "Create Folders Now"
- [ ] Should show "✅ Folders Created Successfully!"
- [ ] Auto-proceeds to Step 3

**Step 3: Upload Images**
- [ ] Shows client name and upload destination
- [ ] Click "Open Upload Page (New Tab)"
- [ ] New tab opens with upload interface
- [ ] Upload 2-3 test images
- [ ] Return to onboarding tab
- [ ] Enter number of uploaded images
- [ ] Click "Continue to Label Images"

**Step 4: Label Images** ⭐ **NEW!**
- [ ] Shows client name and instructions
- [ ] Click "Open Image Labeling Page (New Tab)"
- [ ] New tab opens showing:
  - Status counter: "Labeled: 0 of X images"
  - All uploaded images with thumbnails (250x250px)
  - Text input for each image
  - Download button (initially disabled)
- [ ] Enter product names for each image
- [ ] Watch counter update: "Labeled: X of X images"
- [ ] Border turns green when labeled
- [ ] Download button becomes enabled
- [ ] Click "Download Labels File"
- [ ] File downloads as `test-client-2025_image_labels.txt`
- [ ] Open file and verify format: `product_name | cloudinary_url`
- [ ] Return to onboarding tab
- [ ] Click "Complete Onboarding"

**Step 5: Complete**
- [ ] Shows success message
- [ ] Displays client summary
- [ ] Shows next steps
- [ ] Has "Onboard Another Client" button
- [ ] Has "View Image Gallery" button
- [ ] Has "Generate Images" button

**Expected Result:** Complete 5-step workflow works smoothly

---

### 3. **Image Studio** (http://localhost:8502/)

**What to Test:**

**Image Generation:**
- [ ] Enter client folder name
- [ ] Enter a prompt (e.g., "a red sports car on a mountain road")
- [ ] Click "Generate Image"
- [ ] Image generates successfully
- [ ] Image is uploaded to Cloudinary
- [ ] URL is displayed
- [ ] Cost is calculated and shown
- [ ] Image preview appears

**Image Editing:**
- [ ] Upload or paste an image URL
- [ ] Enter edit prompt (e.g., "add sunglasses")
- [ ] Click "Edit Image"
- [ ] Edited image generates successfully
- [ ] Shows before/after comparison
- [ ] Cost is updated

**Expected Result:** Full image generation and editing workflow works

---

### 4. **Upload Page** (http://localhost:5001/upload)

**What to Test:**
- [ ] Page loads with drag-and-drop interface
- [ ] Enter client name in URL parameter: `/upload?client=test-client-2025`
- [ ] Drag and drop images OR click to select
- [ ] Upload progress shows
- [ ] Success message appears
- [ ] Images appear in Cloudinary folder

**Expected Result:** Standalone upload works without onboarding flow

---

### 5. **Label Images Page** (http://localhost:5001/label-images?client=test-client-2025)

**What to Test:**
- [ ] Replace `test-client-2025` with your actual client name
- [ ] Page loads showing client name
- [ ] All images from `{client}/input/` folder display
- [ ] Each image has:
  - 250x250px thumbnail
  - Full Cloudinary URL below
  - Product name input field
- [ ] Enter labels for all images
- [ ] Status counter updates in real-time
- [ ] Container borders change color (red → green)
- [ ] Download button enables when all labeled
- [ ] Click download
- [ ] File saves with correct filename
- [ ] File contains all labels in format: `label | url`

**Expected Result:** Standalone labeling works independently

---

### 6. **API Endpoints** (for n8n/external integration)

**Health Check:**
```bash
curl http://localhost:5001/health
```
Expected: JSON with status "healthy"

**API Documentation:**
```bash
curl http://localhost:5001/api/docs
```
Expected: JSON with all endpoint descriptions

**Generate Image:**
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a cute robot",
    "client_folder": "test-client-2025"
  }'
```
Expected: JSON with image_url and success=true

**Get Client Images:**
```bash
curl "http://localhost:5001/api/get-client-images?client=test-client-2025"
```
Expected: JSON array of image URLs

**Expected Result:** All API endpoints respond correctly

---

## Common Issues & Solutions

### Issue: Port Already in Use
**Solution:**
```bash
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9
lsof -ti:8502 | xargs kill -9
./start.sh
```

### Issue: Streamlit Service Not Loading
**Solution:**
- Wait 5-10 seconds for services to fully start
- Check logs: `tail -f /tmp/unified_app.log`
- Refresh the browser

### Issue: Images Not Uploading
**Solution:**
- Verify `.env` has correct Cloudinary credentials
- Check client folder exists
- Verify upload preset is configured

### Issue: Label Images Page Shows "No Images Found"
**Solution:**
- Ensure you've uploaded images to `{client}/input/` folder
- Verify client name in URL matches folder name
- Check Cloudinary for actual folder contents

---

## Success Criteria

✅ **ALL OF THESE SHOULD WORK:**

1. Main dashboard loads and looks professional
2. Can complete full 5-step onboarding workflow
3. Can generate images in Image Studio
4. Can edit images in Image Studio
5. Can upload images via standalone upload page
6. Can label images and download labels file
7. All API endpoints return 200 status
8. Health check shows all services "ready"
9. No errors in browser console
10. No errors in `/tmp/unified_app.log`

---

## Performance Test

**Load Time Expectations:**
- Main Dashboard: < 1 second
- Streamlit Apps: 2-5 seconds (first load)
- API Endpoints: < 2 seconds
- Image Generation: 5-15 seconds (depending on complexity)
- Image Upload: 2-10 seconds (depending on file size)

---

## Browser Compatibility

**Tested and Working:**
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

**Mobile Support:**
- ✅ Responsive design on all pages
- ✅ Touch-friendly buttons (44px minimum)
- ✅ Works on tablets and phones

---

## Next Steps After Testing

Once all tests pass:

1. **Document Any Issues:** Note any bugs or unexpected behavior
2. **Review Deployment Options:** See [UNIFIED_ARCHITECTURE.md](UNIFIED_ARCHITECTURE.md)
3. **Prepare for Production:**
   - Set up production environment variables
   - Choose deployment platform (Render, Heroku, Docker)
   - Configure domain and SSL
4. **Deploy:** Follow deployment guide in UNIFIED_ARCHITECTURE.md

---

## Support

If something doesn't work:
1. Check the logs: `tail -f /tmp/unified_app.log`
2. Verify all environment variables in `.env`
3. Ensure dependencies installed: `pip install -r requirements.txt`
4. Try restarting: `./start.sh`

---

**Happy Testing! 🎉**

Everything should work perfectly. If you find any issues, we'll fix them before deployment.
