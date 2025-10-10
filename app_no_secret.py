"""
AI Image Studio - Streamlit Web Interface for Nano Banana (No Secret Required Version)
A minimal MVP for image generation and editing using Nano Banana (Gemini 2.5 Flash Image)
"""

import streamlit as st
import os
import sys
import io
import time
import tempfile
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Import our custom modules
try:
    from nano_banana_client import NanoBananaClient
    # Skip cloudinary for now
    # from cloudinary_utils import CloudinaryManager
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .cost-display {
        background-color: #f0f9ff;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: 1px solid #0ea5e9;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fdf4;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #22c55e;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fffbeb;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f59e0b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'total_cost' not in st.session_state:
        st.session_state.total_cost = 0.0
    if 'client_initialized' not in st.session_state:
        st.session_state.client_initialized = False

def initialize_clients():
    """Initialize Nano Banana client"""
    try:
        # Initialize Nano Banana client
        if not st.session_state.client_initialized:
            nano_client = NanoBananaClient()
            st.session_state.nano_client = nano_client
            st.session_state.client_initialized = True
        
        return True, None
        
    except Exception as e:
        return False, str(e)

def display_cost_info():
    """Display current session cost information"""
    cost_per_image = 0.039
    st.markdown(f"""
    <div class="cost-display">
        <strong>💰 Cost Information</strong><br>
        • Cost per image: ${cost_per_image:.3f}<br>
        • Session total: ${st.session_state.total_cost:.3f}<br>
        • Images generated: {len(st.session_state.generated_images)}
    </div>
    """, unsafe_allow_html=True)

def add_to_session_cost():
    """Add the cost of one image generation to session total"""
    st.session_state.total_cost += 0.039

def generate_image_tab():
    """Tab for generating new images"""
    st.header("🎨 Generate New Image")
    
    # Prompt input
    prompt = st.text_area(
        "Describe the image you want to generate:",
        height=100,
        placeholder="Example: A majestic lion sitting on a rock in the African savanna at sunset, photorealistic, high detail..."
    )
    
    # Generate button
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("🚀 Generate Image", type="primary")
    
    if generate_btn and prompt:
        if not st.session_state.client_initialized:
            st.error("❌ Nano Banana client not properly initialized. Please check your Google AI API key.")
            return
        
        with st.spinner("🎨 Generating your image..."):
            try:
                # Generate image using Nano Banana
                generated_image = st.session_state.nano_client.generate_image(
                    prompt=prompt,
                    save_to_disk=False
                )
                
                if generated_image:
                    # Add to session state (no Cloudinary for now)
                    result_data = {
                        'type': 'generated',
                        'prompt': prompt,
                        'image': generated_image,
                        'timestamp': time.time()
                    }
                    st.session_state.generated_images.append(result_data)
                    add_to_session_cost()
                    
                    # Display success
                    st.markdown("""
                    <div class="success-box">
                        ✅ <strong>Image Generated Successfully!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display image
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.image(generated_image, caption="Generated Image", use_column_width=True)
                    
                    with col2:
                        st.write("**Image Ready!**")
                        st.info("💡 Cloudinary upload would happen here with full setup")
                        
                        # Download button
                        img_bytes = io.BytesIO()
                        generated_image.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        
                        st.download_button(
                            label="📥 Download Image",
                            data=img_bytes,
                            file_name=f"generated_{int(time.time())}.png",
                            mime="image/png"
                        )
                else:
                    st.error("❌ Failed to generate image. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error generating image: {str(e)}")
    
    elif generate_btn and not prompt:
        st.warning("⚠️ Please enter a description for your image.")

def edit_image_tab():
    """Tab for editing existing images"""
    st.header("✏️ Edit Existing Image")
    
    # Show warning about Cloudinary
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Limited Mode:</strong> Image editing requires full Cloudinary setup. 
        You can still test with local file uploads!
    </div>
    """, unsafe_allow_html=True)
    
    # File upload only for now
    uploaded_file = st.file_uploader(
        "Choose an image file to edit",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
        help="Upload an image file to edit"
    )
    
    if uploaded_file:
        input_image = Image.open(uploaded_file)
        st.image(input_image, caption="Uploaded Image", use_column_width=True)
        
        # Edit prompt
        edit_prompt = st.text_area(
            "Describe how you want to edit the image:",
            height=100,
            placeholder="Example: Add sunglasses and a hat, make the background more colorful, change to cartoon style..."
        )
        
        # Edit button
        if edit_prompt:
            col1, col2 = st.columns([1, 4])
            with col1:
                edit_btn = st.button("✨ Edit Image", type="primary")
            
            if edit_btn:
                if not st.session_state.client_initialized:
                    st.error("❌ Nano Banana client not properly initialized.")
                    return
                
                with st.spinner("✨ Editing your image..."):
                    try:
                        # Save input image temporarily for processing
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            input_image.save(tmp_file.name)
                            tmp_path = tmp_file.name
                        
                        try:
                            # Edit image using Nano Banana
                            edited_image = st.session_state.nano_client.edit_image(
                                image_path=tmp_path,
                                prompt=edit_prompt,
                                save_to_disk=False
                            )
                            
                            if edited_image:
                                # Add to session state
                                result_data = {
                                    'type': 'edited',
                                    'prompt': edit_prompt,
                                    'original_image': input_image,
                                    'edited_image': edited_image,
                                    'timestamp': time.time()
                                }
                                st.session_state.generated_images.append(result_data)
                                add_to_session_cost()
                                
                                # Display success
                                st.markdown("""
                                <div class="success-box">
                                    ✅ <strong>Image Edited Successfully!</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display before/after
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.image(input_image, caption="Original Image", use_column_width=True)
                                with col2:
                                    st.image(edited_image, caption="Edited Image", use_column_width=True)
                                
                                # Download button
                                img_bytes = io.BytesIO()
                                edited_image.save(img_bytes, format='PNG')
                                img_bytes.seek(0)
                                
                                st.download_button(
                                    label="📥 Download Edited Image",
                                    data=img_bytes,
                                    file_name=f"edited_{int(time.time())}.png",
                                    mime="image/png"
                                )
                            else:
                                st.error("❌ Failed to edit image. Please try again.")
                        
                        finally:
                            # Clean up temp file
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass
                                
                    except Exception as e:
                        st.error(f"❌ Error editing image: {str(e)}")
        elif input_image and not edit_prompt:
            st.warning("⚠️ Please describe how you want to edit the image.")

def session_gallery():
    """Display session gallery"""
    if st.session_state.generated_images:
        st.header("📸 Session Gallery")
        
        for i, result in enumerate(reversed(st.session_state.generated_images)):
            with st.expander(f"{result['type'].title()} #{len(st.session_state.generated_images) - i}"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if result['type'] == 'edited':
                        st.image(result['edited_image'], caption="Result", use_column_width=True)
                    else:
                        st.image(result['image'], caption="Generated Image", use_column_width=True)
                
                with col2:
                    st.write(f"**Prompt:** {result['prompt']}")
                    st.write(f"**Created:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['timestamp']))}")

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 AI Image Studio</h1>
        <p>Generate and edit images using Nano Banana (Gemini 2.5 Flash Image)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize clients
    success, error = initialize_clients()
    if not success:
        st.error(f"❌ **Configuration Error:** {error}")
        st.markdown("""
        **Required Environment Variables:**
        - `GOOGLE_AI_API_KEY` - Your Google AI API key ✅ (Set)
        
        **Optional for full functionality:**
        - `CLOUDINARY_CLOUD_NAME` - Your Cloudinary cloud name
        - `CLOUDINARY_API_KEY` - Your Cloudinary API key  
        - `CLOUDINARY_API_SECRET` - Your Cloudinary API secret
        - `CLIENT_FOLDER_NAME` - Folder name for organizing uploads (e.g., 'XV1')
        """)
        st.stop()
    
    # Display cost information
    display_cost_info()
    
    # Show Cloudinary status
    st.markdown("""
    <div class="warning-box">
        🌟 <strong>Demo Mode:</strong> Basic functionality active. 
        Images will be generated and can be downloaded. For full cloud storage and editing features, 
        complete the Cloudinary API Secret setup.
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2 = st.tabs(["🎨 Generate", "✏️ Edit"])
    
    with tab1:
        generate_image_tab()
    
    with tab2:
        edit_image_tab()
    
    # Session gallery (always visible at bottom)
    session_gallery()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <small>AI Image Studio powered by Nano Banana (Gemini 2.5 Flash Image) • 
        Built with Streamlit</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()