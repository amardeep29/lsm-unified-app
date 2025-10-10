# 🚀 AI Image Studio Deployment Guide

## 📋 Quick Setup Checklist

### ✅ **Local Development**

1. **Install dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.streamlit .env
   # Edit .env with your actual API keys
   ```

3. **Required Environment Variables:**
   - `GOOGLE_AI_API_KEY` - From [Google AI Studio](https://aistudio.google.com)
   - `CLOUDINARY_CLOUD_NAME` - From Cloudinary dashboard
   - `CLOUDINARY_API_KEY` - From Cloudinary dashboard  
   - `CLOUDINARY_API_SECRET` - From Cloudinary dashboard
   - `CLIENT_FOLDER_NAME` - Folder name (e.g., "XV1")

4. **Run locally:**
   ```bash
   source venv/bin/activate
   export GOOGLE_AI_API_KEY='your_key_here'
   export CLOUDINARY_CLOUD_NAME='your_cloud_name'
   export CLOUDINARY_API_KEY='your_api_key'
   export CLOUDINARY_API_SECRET='your_api_secret'
   export CLIENT_FOLDER_NAME='XV1'
   streamlit run app.py
   ```

### 🌐 **Deploy to Render**

1. **Connect GitHub repo to Render**

2. **Use the included `render.yaml` configuration**

3. **Set environment variables in Render dashboard:**
   - `GOOGLE_AI_API_KEY` = Your Google AI API key
   - `CLOUDINARY_CLOUD_NAME` = Your Cloudinary cloud name
   - `CLOUDINARY_API_KEY` = Your Cloudinary API key
   - `CLOUDINARY_API_SECRET` = Your Cloudinary API secret
   - `CLIENT_FOLDER_NAME` = XV1 (or your preferred folder name)

4. **Deploy!** - One-click deployment with the render.yaml file

## 📱 **App Features**

### 🎨 **Generate Tab**
- Text-to-image generation
- Automatic Cloudinary upload
- Download generated images
- Cost tracking

### ✏️ **Edit Tab**
- Upload local images OR paste Cloudinary URLs
- AI-powered image editing with text prompts
- Before/after comparison
- Automatic Cloudinary storage

### 📸 **Session Gallery**
- View all generated/edited images in current session
- Access Cloudinary URLs
- Session cost tracking

## 🔧 **Technical Architecture**

```
User Input → Streamlit UI → Nano Banana Client → Google AI API
                                    ↓
Cloudinary ← Upload Results ← PIL Image Processing
```

### **File Structure:**
```
nano_banana_project/
├── app.py                    # Main Streamlit application
├── src/
│   ├── nano_banana_client.py # Existing Nano Banana wrapper
│   └── cloudinary_utils.py   # Cloudinary integration
├── requirements.txt          # Dependencies
├── render.yaml              # Render deployment config
└── .env.streamlit           # Environment template
```

## 💰 **Cost Tracking**

- **Per image:** ~$0.039 (4¢)
- **Session tracking:** Real-time cost display
- **No persistent storage:** Costs reset each session

## 🛡️ **Security Notes**

- API keys stored as environment variables
- No authentication in MVP (add later)
- All images uploaded to Cloudinary with organized folder structure
- Session-based, no persistent user data

## 🔍 **Testing Checklist**

- [ ] Generate image from text prompt
- [ ] Upload local image and edit
- [ ] Paste Cloudinary URL and edit  
- [ ] Download generated/edited images
- [ ] View session gallery
- [ ] Check Cloudinary folder structure
- [ ] Verify cost tracking
- [ ] Test error handling

## 🚨 **Troubleshooting**

### **"Import Error"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### **"Configuration Error"**  
- Check all environment variables are set correctly
- Verify API keys are valid

### **"Failed to upload to Cloudinary"**
- Check Cloudinary credentials
- Verify cloud name format (no spaces/special chars)

### **"Failed to generate image"**
- Check Google AI API key
- Ensure billing is enabled on Google Cloud project
- Try simpler prompts

## 📈 **Next Steps (Post-MVP)**

1. **User Authentication** - Login/signup system
2. **Database Integration** - Store user history
3. **Airtable Integration** - As specified in requirements
4. **Gallery Features** - Browse previous generations
5. **Batch Processing** - Multiple images at once
6. **Advanced Editing** - More editing options

## 🆘 **Support**

- Check environment variables first
- Test individual components (Nano Banana, Cloudinary)
- Use local development mode for debugging
- Check Streamlit logs for detailed errors

---

**🎨 Ready to deploy your AI Image Studio!**