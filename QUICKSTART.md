# 🚀 AI Image Studio - Quick Start

## ⚡ Instant Setup (2 minutes)

### 1. **Test Components**
```bash
python test_app.py
```

### 2. **Start the Web App**
```bash
./start_app.sh
```
The app will open at: http://localhost:8501

### 3. **Set Up Cloudinary (Optional)**
For full functionality, get your Cloudinary credentials:

1. Sign up at [Cloudinary](https://cloudinary.com)
2. Get your credentials from the dashboard
3. Set environment variables:
```bash
export CLOUDINARY_CLOUD_NAME='your_cloud_name'
export CLOUDINARY_API_KEY='your_api_key'
export CLOUDINARY_API_SECRET='your_api_secret'
```

## 🎯 What You Can Do

### **Without Cloudinary:**
- ✅ Generate images from text
- ✅ Test the web interface
- ✅ See the complete UI design
- ✅ Download generated images

### **With Cloudinary:**
- ✅ All of the above PLUS:
- ✅ Upload images for editing
- ✅ Paste Cloudinary URLs for editing  
- ✅ Automatic cloud storage
- ✅ Get shareable URLs
- ✅ Organized folder structure (XV1/generated, XV1/edited, etc.)

## 📱 Using the Web Interface

### **Generate Tab:**
1. Enter your image description
2. Click "🚀 Generate Image"
3. View and download the result

### **Edit Tab:**
1. **Option A**: Upload a local image file
2. **Option B**: Paste a Cloudinary image URL
3. Describe your edits (e.g., "add sunglasses", "make it cartoon style")
4. Click "✨ Edit Image"
5. See before/after comparison

## 💰 Cost Information
- **Per image**: ~$0.039 (4¢)
- **Session tracking**: Real-time cost display
- **Very affordable**: 25+ images per $1

## 🔧 Command Line Options

### **One-liner image editing:**
```bash
./run.sh easy 'images/input/photo.jpg' 'make it look like a painting'
```

### **Interactive testing:**
```bash
./run.sh test
```

### **Generate sample images:**
```bash
python examples/image_generation_example.py
```

## 🌐 Deploy to Production

### **Deploy to Render:**
1. Push code to GitHub
2. Connect to Render
3. Use the included `render.yaml`
4. Set environment variables in Render dashboard
5. Deploy!

## 🎨 Example Prompts

### **Generation:**
- "A serene mountain lake at sunrise, photorealistic"
- "Cartoon cat wearing a wizard hat, colorful"
- "Futuristic city with flying cars, neon lights"

### **Editing:**
- "Add sunglasses and a hat"
- "Change the background to a beach scene"
- "Make it look like a watercolor painting"
- "Add rainbow in the sky"

## 🆘 Need Help?

1. **Check `test_app.py` results** - diagnoses issues
2. **Read `DEPLOYMENT.md`** - detailed setup guide
3. **Check `USAGE_GUIDE.md`** - advanced techniques
4. **Run `./start_app.sh`** - shows any missing setup

---

**🍌 Ready to create amazing AI images!**