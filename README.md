# 🍌 Nano Banana (Gemini 2.5 Flash Image) Developer Project

A comprehensive Python SDK and example collection for building with Google's Nano Banana (Gemini 2.5 Flash Image) model - a powerful AI for image generation and editing.

## 🚀 Features

- **Image Generation**: Create images from text descriptions
- **Image Editing**: Modify existing images with text prompts
- **Photo Restoration**: Restore and colorize old photographs
- **Easy-to-use Client**: Simple Python wrapper for the Gemini API
- **Cost Tracking**: Built-in cost estimation and monitoring
- **Comprehensive Examples**: Ready-to-run example scripts

## 📋 Requirements

- Python 3.7+
- Google AI API Key (from [Google AI Studio](https://aistudio.google.com))
- Google Cloud Project with billing enabled

## 🛠️ Installation

1. **Clone or download this project**
   ```bash
   cd nano_banana_project
   ```

2. **Install dependencies**
   ```bash
   pip install google-genai Pillow
   ```

3. **Get your API key**
   - Visit [Google AI Studio](https://aistudio.google.com)
   - Click "Get API key" in the left navigation
   - Create a new API key or use an existing one
   - Enable billing on your Google Cloud project

4. **Configure your API key**
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   export GOOGLE_AI_API_KEY='your_api_key_here'
   ```
   
   **Option B: Create .env file**
   ```bash
   cp .env.template .env
   # Edit .env and add your API key
   ```

## 💰 Pricing

- **Cost per image**: $0.039 USD (~2.6¢ per image)
- **Images per dollar**: ~25 images
- **Free tier**: Unlimited in Google AI Studio for prototyping
- **API usage**: Requires billing enabled on Google Cloud project

> Pricing is based on $0.30/1M input tokens and $30/1M output tokens. A standard 1024x1024px output image consumes ~1290 tokens.

## 🎯 Quick Start

### Basic Usage

```python
from src.nano_banana_client import NanoBananaClient

# Initialize client (will use GOOGLE_AI_API_KEY env var)
client = NanoBananaClient()

# Generate an image
image_path = client.generate_image(
    prompt="A serene mountain lake at sunset",
    output_filename="mountain_sunset.png"
)
print(f"Generated: {image_path}")
```

### Image Editing

```python
# Edit an existing image
edited_path = client.edit_image(
    image_path="path/to/your/image.jpg",
    prompt="Add a rainbow in the sky and make it more vibrant",
    output_filename="edited_image.png"
)
```

### Photo Restoration

```python
# Restore an old photo
restored_path = client.restore_photo(
    image_path="path/to/old_photo.jpg",
    output_filename="restored_photo.png"
)
```

## 📚 Examples

Run the included example scripts:

### 1. Image Generation
```bash
cd examples
python image_generation_example.py
```
Demonstrates generating various types of images from text prompts.

### 2. Image Editing
```bash
python image_editing_example.py
```
Shows how to edit images using text instructions, with character consistency.

### 3. Photo Restoration
```bash
python photo_restoration_example.py
```
Demonstrates restoring and colorizing old photographs.

## 📁 Project Structure

```
nano_banana_project/
├── src/
│   └── nano_banana_client.py      # Main client wrapper
├── config/
│   └── config.py                  # Configuration settings
├── examples/
│   ├── image_generation_example.py
│   ├── image_editing_example.py
│   └── photo_restoration_example.py
├── images/
│   ├── input/                     # Place input images here
│   └── output/                    # Generated images saved here
├── .env.template                  # Environment template
└── README.md                      # This file
```

## 🔧 API Reference

### NanoBananaClient

#### `__init__(api_key=None)`
Initialize the client with optional API key override.

#### `generate_image(prompt, output_filename=None, save_to_disk=True)`
Generate an image from a text prompt.

**Parameters:**
- `prompt` (str): Text description of the image
- `output_filename` (str, optional): Custom filename
- `save_to_disk` (bool): Whether to save to disk

**Returns:** File path (if saved) or PIL Image object

#### `edit_image(image_path, prompt, output_filename=None, save_to_disk=True)`
Edit an existing image with text instructions.

**Parameters:**
- `image_path` (str): Path to input image
- `prompt` (str): Edit instructions
- `output_filename` (str, optional): Custom filename
- `save_to_disk` (bool): Whether to save to disk

#### `restore_photo(image_path, output_filename=None, custom_prompt=None, save_to_disk=True)`
Restore and colorize an old photograph.

**Parameters:**
- `image_path` (str): Path to old photo
- `output_filename` (str, optional): Custom filename
- `custom_prompt` (str, optional): Custom restoration instructions
- `save_to_disk` (bool): Whether to save to disk

#### `estimate_cost(num_images)`
Estimate cost for generating a number of images.

#### `get_pricing_info()`
Get current pricing information.

## 💡 Best Practices

### For Better Image Generation:
- Be specific and descriptive in your prompts
- Mention style, lighting, mood, and composition
- Include details about colors, textures, and atmosphere
- Specify image quality (e.g., "photorealistic", "high resolution")

### For Image Editing:
- Clearly describe what you want to change
- Mention what should be preserved from the original
- Use action words like "add", "remove", "transform", "enhance"
- Be specific about positioning and relationships

### For Photo Restoration:
- Mention the era or time period for better colorization
- Specify the type of damage to fix (scratches, fading, spots)
- Describe the desired color style (vintage, modern, natural)
- Consider the original lighting conditions

## 🔗 Related Resources

- [Google AI Studio](https://aistudio.google.com) - Test prompts for free
- [Nano Banana Direct Link](https://ai.studio/banana) - Quick access to the model
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs) - Official API docs
- [Pricing Information](https://ai.google.dev/pricing) - Current pricing details

## 🤝 Contributing

This project is a learning resource based on the [official tutorial](https://dev.to/googleai/how-to-build-with-nano-banana-complete-developer-tutorial-646). Feel free to:

- Add more examples
- Improve error handling
- Add new features
- Create utility functions
- Share your use cases

## 📝 License

This project is for educational purposes. Please respect Google's Terms of Service and API usage policies.

## ❓ Troubleshooting

### Common Issues:

1. **"API key not provided"**
   - Set the `GOOGLE_AI_API_KEY` environment variable
   - Or create a `.env` file with your API key

2. **Billing errors**
   - Enable billing on your Google Cloud project
   - Visit the Google Cloud Console → Billing

3. **Image generation fails**
   - Check your prompt for policy violations
   - Ensure your API key has proper permissions
   - Verify billing is enabled

4. **Module import errors**
   - Ensure you're running from the project directory
   - Check that dependencies are installed

### Getting Help:

- Check the [Google AI Studio](https://aistudio.google.com) for testing
- Review the [official documentation](https://ai.google.dev/gemini-api/docs)
- Test your prompts in AI Studio first

---

**Happy creating with Nano Banana! 🍌✨**