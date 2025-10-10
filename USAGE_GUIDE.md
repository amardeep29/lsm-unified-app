# 📖 Nano Banana Usage Guide

Comprehensive guide for getting the most out of your Nano Banana (Gemini 2.5 Flash Image) project.

## 🚀 Getting Started

### 1. First Setup

1. **Get your API key** from [Google AI Studio](https://aistudio.google.com)
2. **Enable billing** on your Google Cloud project
3. **Set your API key**:
   ```bash
   export GOOGLE_AI_API_KEY='your_api_key_here'
   ```
4. **Test your setup**:
   ```bash
   python quick_demo.py
   ```

### 2. Project Structure Overview

```
nano_banana_project/
├── src/nano_banana_client.py     # Main API wrapper
├── config/config.py              # Configuration settings
├── examples/                     # Example scripts
├── images/input/                 # Your input images
├── images/output/                # Generated outputs
└── quick_demo.py                 # Quick test script
```

## 🎨 Image Generation Techniques

### Basic Generation

```python
from src.nano_banana_client import NanoBananaClient

client = NanoBananaClient()

# Simple generation
image_path = client.generate_image(
    prompt="A majestic lion in the African savanna",
    output_filename="lion.png"
)
```

### Advanced Prompting Techniques

#### 1. Style Specifications
```python
# Photorealistic
prompt = "A photorealistic portrait of a wise elderly woman, studio lighting, high detail"

# Artistic styles
prompt = "An oil painting of a stormy seascape in the style of Turner"
prompt = "A minimalist geometric design, flat colors, Bauhaus inspired"
prompt = "Anime-style illustration of a cyberpunk cityscape"
```

#### 2. Composition Control
```python
# Camera angles
prompt = "Bird's eye view of a bustling marketplace"
prompt = "Low angle shot of a towering skyscraper"

# Framing
prompt = "Close-up portrait of a cat's face, shallow depth of field"
prompt = "Wide landscape shot of mountains at golden hour"
```

#### 3. Lighting and Mood
```python
# Lighting
prompt = "Portrait lit by warm candlelight, dramatic shadows"
prompt = "Bright daylight scene with soft shadows"

# Weather and atmosphere
prompt = "Misty forest morning with rays of sunlight"
prompt = "Neon-lit street on a rainy night"
```

### Quality Enhancement Keywords

Add these to improve image quality:
- "high resolution"
- "detailed"
- "sharp focus"
- "professional photography"
- "award-winning"
- "masterpiece"

## ✏️ Image Editing Mastery

### Editing Principles

1. **Be specific** about changes
2. **Reference the original** elements to preserve
3. **Use action words** (add, remove, transform, enhance)
4. **Describe positioning** and relationships

### Common Editing Tasks

#### Adding Elements
```python
# Add objects
prompt = "Add a rainbow arcing across the sky in this landscape"
prompt = "Place a red sports car in the foreground of this street scene"

# Add effects
prompt = "Add magical sparkles and glowing particles around the wizard"
prompt = "Create lens flares and dramatic lighting"
```

#### Changing Environment
```python
# Season changes
prompt = "Transform this summer scene to winter with snow"
prompt = "Change this day scene to a beautiful sunset"

# Location changes  
prompt = "Move this person from indoors to a beach setting"
prompt = "Transform this modern room to Victorian era"
```

#### Style Transfers
```python
prompt = "Convert this photo to look like a watercolor painting"
prompt = "Transform this realistic image to cartoon/anime style"
prompt = "Make this image look like it was taken in the 1970s"
```

#### Character Modifications
```python
# Clothing
prompt = "Change the person's outfit to a formal business suit"
prompt = "Dress the character as a medieval knight"

# Expressions and poses
prompt = "Make the person smile warmly"
prompt = "Change the pose to arms crossed confidently"
```

## 🔧 Photo Restoration Tips

### Understanding Different Types of Damage

#### Common Issues to Address
- **Fading**: "restore faded colors to vibrant tones"
- **Scratches**: "remove scratches and surface damage"
- **Spots**: "clean up dust spots and stains"
- **Torn areas**: "repair torn or missing sections"

### Era-Appropriate Colorization

```python
# 1920s-1940s
prompt = "Colorize with muted earth tones typical of the 1930s"

# 1950s-1960s  
prompt = "Add bright, optimistic colors popular in the 1950s"

# 1970s-1980s
prompt = "Colorize with the warm, saturated tones of the 1970s"
```

### Restoration Quality Levels

#### Conservative Restoration
```python
prompt = "Gently restore while preserving the vintage character and patina"
```

#### Standard Restoration
```python
prompt = "Restore and colorize, removing damage while maintaining period authenticity"
```

#### Modern Enhancement
```python
prompt = "Fully restore and enhance to modern photo quality standards"
```

## 💡 Advanced Techniques

### Batch Processing

```python
import os
from src.nano_banana_client import NanoBananaClient

client = NanoBananaClient()

# Process multiple images
input_dir = "images/input"
prompts = [
    "Make this image more vibrant and colorful",
    "Add dramatic lighting effects",
    "Convert to vintage sepia tone"
]

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpg', '.png')):
        for i, prompt in enumerate(prompts):
            client.edit_image(
                image_path=os.path.join(input_dir, filename),
                prompt=prompt,
                output_filename=f"{filename}_edit_{i}.png"
            )
```

### Error Handling and Retries

```python
import time
from src.nano_banana_client import NanoBananaClient

def generate_with_retry(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.generate_image(prompt)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2)  # Brief pause before retry
            else:
                print(f"All attempts failed: {e}")
                return None
```

### Cost Management

```python
# Check cost before batch operations
client = NanoBananaClient()
num_images = 10

estimated_cost = client.estimate_cost(num_images)
if estimated_cost > 1.00:  # $1 limit
    print(f"Cost ${estimated_cost:.2f} exceeds limit")
    # Ask for confirmation or reduce batch size
```

## 🎯 Prompt Engineering Best Practices

### Structure Your Prompts

1. **Subject** - What/who is in the image
2. **Action** - What they're doing
3. **Setting** - Where it takes place
4. **Style** - Artistic style or mood
5. **Technical** - Camera settings, quality

Example:
```
Subject: "A professional chef"
Action: "preparing pasta in a kitchen" 
Setting: "in a modern restaurant kitchen"
Style: "warm lighting, professional photography"
Technical: "shallow depth of field, high resolution"
```

### Negative Prompting (What NOT to Include)

While Nano Banana doesn't have explicit negative prompts, you can guide away from unwanted elements:

```python
# Instead of just "portrait", be specific
prompt = "Clean portrait of a person, professional headshot, neutral background"

# Guide away from complexity when you want simplicity
prompt = "Simple geometric pattern, minimal design, clean lines"
```

## 🐛 Troubleshooting Common Issues

### Poor Image Quality
- Add quality keywords: "high resolution", "detailed", "sharp"
- Be more specific about what you want
- Try different artistic styles

### Inconsistent Results
- Use more descriptive prompts
- Include style and mood keywords
- Test prompts in AI Studio first

### API Errors
- Check your API key is valid
- Verify billing is enabled
- Monitor your usage quotas
- Check for prompt policy violations

### Character/Object Consistency
- Be very specific about appearance details
- Reference colors, shapes, and styles explicitly
- Use "maintaining the same [feature]" in edits

## 📊 Performance Optimization

### Efficient Workflow

1. **Test in AI Studio** first (free)
2. **Start with simple prompts**, then refine
3. **Batch similar operations** together
4. **Save successful prompts** for reuse

### Cost Optimization

- Use AI Studio for experimentation (free)
- Plan your generations carefully
- Consider prompt efficiency vs. multiple attempts
- Monitor cumulative costs during sessions

## 🔗 Integration Ideas

### Web Applications
```python
# Flask example
from flask import Flask, request, jsonify
from src.nano_banana_client import NanoBananaClient

app = Flask(__name__)
client = NanoBananaClient()

@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.json['prompt']
    result = client.generate_image(prompt, save_to_disk=False)
    return jsonify({'image_data': result})
```

### Automation Scripts
```python
# Automated social media content
import schedule
import time

def daily_image_generation():
    client = NanoBananaClient()
    prompt = f"Motivational quote image for {time.strftime('%A')}"
    client.generate_image(prompt, f"daily_{time.strftime('%Y%m%d')}.png")

schedule.every().day.at("09:00").do(daily_image_generation)
```

## 📚 Additional Resources

- [Google AI Studio](https://aistudio.google.com) - Free testing environment
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs) - Official documentation
- [Community Examples](https://ai.studio/apps) - Explore community apps
- [Pricing Calculator](https://ai.google.dev/pricing) - Cost planning

---

**🍌 Happy creating with Nano Banana!**