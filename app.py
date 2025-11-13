"""
AI Image Studio - Streamlit Web Interface for Nano Banana
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
    from cloudinary_utils import CloudinaryManager
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Loudspeaker Marketing Image Playground",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Loudspeaker Marketing Dark Theme
st.markdown("""
<style>
    /* Dark theme for entire app */
    .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #06070B !important;
    }

    /* Light text everywhere */
    .main *, .stApp *, p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #E6E6E6 !important;
    }

    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(231, 254, 58, 0.1);
        margin-bottom: 2rem;
    }

    .cost-display {
        background-color: #272F35;
        color: #E6E6E6;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(231, 254, 58, 0.2);
        margin: 1rem 0;
    }

    .cost-display strong {
        color: #E7FE3A;
    }

    .success-box {
        background-color: #272F35;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #E7FE3A;
        margin: 1rem 0;
        color: #E6E6E6;
    }

    .error-box {
        background-color: #272F35;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #dc3545;
        margin: 1rem 0;
        color: #E6E6E6;
    }

    /* Input fields */
    input, textarea, .stTextInput input, .stTextArea textarea {
        background-color: #272F35 !important;
        color: #E6E6E6 !important;
        border: 2px solid rgba(231, 254, 58, 0.2) !important;
    }

    input:focus, textarea:focus {
        border-color: #E7FE3A !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #E7FE3A !important;
        color: #06070B !important;
        font-weight: bold !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s !important;
    }

    .stButton button, .stButton button * {
        color: #06070B !important;
    }

    .stButton button::after {
        content: " →" !important;
    }

    .stButton button:hover {
        background-color: #d4eb25 !important;
        transform: translateY(-2px) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #272F35 !important;
        border: 2px dashed rgba(231, 254, 58, 0.3) !important;
        border-radius: 0.75rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #06070B;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #272F35;
        color: #E6E6E6;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: #E7FE3A !important;
        color: #06070B !important;
    }

    .stTabs [aria-selected="true"] * {
        color: #06070B !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #272F35 !important;
        color: #E6E6E6 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #272F35 !important;
        color: #E6E6E6 !important;
        border-radius: 0.5rem !important;
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
    if 'cloudinary_initialized' not in st.session_state:
        st.session_state.cloudinary_initialized = False

def initialize_clients():
    """Initialize Nano Banana and Cloudinary clients"""
    try:
        # Initialize Nano Banana client
        if not st.session_state.client_initialized:
            nano_client = NanoBananaClient()
            st.session_state.nano_client = nano_client
            st.session_state.client_initialized = True
        
        # Initialize Cloudinary client
        if not st.session_state.cloudinary_initialized:
            cloudinary_client = CloudinaryManager()
            st.session_state.cloudinary_client = cloudinary_client
            st.session_state.cloudinary_initialized = True
        
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

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temp directory and return path"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

def generate_image_tab():
    """Tab for generating new images"""
    st.header("🎨 Generate New Image")

    st.write("")  # Spacing

    # Client folder selector
    st.markdown("### 🏢 Select Client Folder")

    if not st.session_state.cloudinary_initialized:
        st.error("❌ Cloudinary not initialized. Please check your environment variables.")
        return

    # Load client folders
    folders_result = st.session_state.cloudinary_client.list_client_folders()

    if not folders_result['success']:
        st.error(f"❌ Failed to load client folders: {folders_result.get('error')}")
        return

    client_folders = folders_result.get('folders', [])

    if not client_folders:
        st.warning("⚠️ No client folders found. Please create a client folder first via the onboarding process.")
        return

    selected_client_folder = st.selectbox(
        "Select a client folder to save the generated image:",
        options=[""] + client_folders,
        format_func=lambda x: "-- Select a client folder --" if x == "" else x,
        key="generate_client_selector"
    )

    st.write("")  # Spacing
    st.markdown("---")
    st.write("")  # Spacing

    # Prompt input
    st.markdown("### 📝 Image Description")
    prompt = st.text_area(
        "Describe the image you want to generate:",
        height=100,
        placeholder="Example: A majestic lion sitting on a rock in the African savanna at sunset, photorealistic, high detail...",
        key="generate_prompt_input"
    )

    st.write("")  # Spacing

    # Generate button
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("🚀 Generate Image", type="primary")

    if generate_btn:
        # Validation
        if not selected_client_folder:
            st.error("❌ Please select a client folder before generating.")
            return

        if not prompt:
            st.error("❌ Please enter a description for your image.")
            return

        if not st.session_state.client_initialized or not st.session_state.cloudinary_initialized:
            st.error("❌ Clients not properly initialized. Please check your environment variables.")
            return

        with st.spinner("🎨 Generating your image..."):
            try:
                # Generate image using Nano Banana
                generated_image = st.session_state.nano_client.generate_image(
                    prompt=prompt,
                    save_to_disk=False
                )

                if generated_image:
                    # Upload to Cloudinary with selected client folder
                    upload_result = st.session_state.cloudinary_client.upload_image(
                        image_data=generated_image,
                        folder_type="generated",
                        filename="generated_image",
                        client_folder=selected_client_folder
                    )
                    
                    if upload_result['success']:
                        # Add to session state
                        result_data = {
                            'type': 'generated',
                            'prompt': prompt,
                            'image': generated_image,
                            'cloudinary_url': upload_result['url'],
                            'cloudinary_public_id': upload_result['public_id'],
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
                            st.image(generated_image, caption="Generated Image", use_container_width=True)
                        
                        with col2:
                            st.write("**Cloudinary URL:**")
                            st.code(upload_result['url'], language=None)
                            
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
                        st.error(f"❌ Failed to upload to Cloudinary: {upload_result.get('error')}")
                else:
                    st.error("❌ Failed to generate image. Please try again.")

            except Exception as e:
                st.error(f"❌ Error generating image: {str(e)}")

def edit_image_tab():
    """Tab for editing existing images with image gallery selection"""
    st.header("✏️ Edit Existing Image")

    st.write("")  # Spacing

    # Client folder selector
    st.markdown("### 🏢 Select Client Folder")

    if not st.session_state.cloudinary_initialized:
        st.error("❌ Cloudinary not initialized. Please check your environment variables.")
        return

    # Load client folders
    folders_result = st.session_state.cloudinary_client.list_client_folders()

    if not folders_result['success']:
        st.error(f"❌ Failed to load client folders: {folders_result.get('error')}")
        return

    client_folders = folders_result.get('folders', [])

    if not client_folders:
        st.warning("⚠️ No client folders found. Please create a client folder first via the onboarding process.")
        return

    selected_client_folder = st.selectbox(
        "Select a client folder:",
        options=[""] + client_folders,
        format_func=lambda x: "-- Select a client folder --" if x == "" else x,
        key="edit_client_selector"
    )

    if not selected_client_folder:
        st.info("ℹ️ Please select a client folder to continue.")
        return

    st.write("")  # Spacing
    st.markdown("---")
    st.write("")  # Spacing

    # Input method selection
    st.markdown("### 📸 Choose Input Method")
    input_method = st.radio(
        "How would you like to select an image?",
        ["Upload New Image", "Select Existing Image"],
        horizontal=True,
        key="edit_input_method"
    )

    input_image = None
    input_image_url = None
    selected_image_public_id = None

    # Initialize session state for selected image
    if 'selected_image_for_edit' not in st.session_state:
        st.session_state.selected_image_for_edit = None

    st.write("")  # Spacing

    if input_method == "Upload New Image":
        # Reset selected image when switching methods
        st.session_state.selected_image_for_edit = None

        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
            help="Upload an image file to edit",
            key="edit_file_uploader"
        )

        if uploaded_file:
            input_image = Image.open(uploaded_file)
            st.write("")  # Spacing
            st.markdown("**Preview:**")
            st.image(input_image, caption="Uploaded Image", use_container_width=True)

    else:  # Select Existing Image
        st.markdown("**Select an image from your input folder:**")
        st.write("")  # Spacing

        # Load images from input folder
        with st.spinner("📥 Loading images..."):
            images_result = st.session_state.cloudinary_client.list_images(
                folder_type="input",
                max_results=100,
                client_folder=selected_client_folder
            )

        if not images_result['success']:
            st.error(f"❌ Failed to load images: {images_result.get('error')}")
            return

        images = images_result.get('images', [])

        if not images:
            st.warning(f"⚠️ No images found in `{selected_client_folder}/input/` folder. Please upload images first.")
            return

        # Check if we already have a selected image
        if st.session_state.selected_image_for_edit:
            # Show selected image preview
            selected_img = st.session_state.selected_image_for_edit
            st.success(f"✓ Selected: {selected_img['filename']}")

            # Show large preview
            st.image(selected_img['url'], caption=selected_img['filename'], use_container_width=True)

            # Change image button
            if st.button("🔄 Change Image", key="change_image_btn"):
                st.session_state.selected_image_for_edit = None
                st.rerun()

            # Set the input image for processing
            input_image_url = selected_img['url']
            selected_image_public_id = selected_img['public_id']

        else:
            # Show image gallery for selection
            st.info(f"📊 Found {len(images)} image(s). Click an image to select it.")
            st.write("")  # Spacing

            # Display images in 3-column grid
            cols_per_row = 3
            for i in range(0, len(images), cols_per_row):
                cols = st.columns(cols_per_row)

                for j, col in enumerate(cols):
                    if i + j < len(images):
                        img = images[i + j]
                        with col:
                            # Display thumbnail
                            img_url = img.get('secure_url', '')
                            filename = img.get('public_id', '').split('/')[-1]

                            st.image(img_url, use_container_width=True)
                            st.caption(f"**{filename}**")

                            # Select button
                            if st.button(f"✓ Select", key=f"select_img_{i+j}"):
                                st.session_state.selected_image_for_edit = {
                                    'url': img_url,
                                    'filename': filename,
                                    'public_id': img.get('public_id')
                                }
                                st.rerun()

    # Only show edit section if we have an image selected
    if input_image or input_image_url:
        st.write("")  # Spacing
        st.markdown("---")
        st.write("")  # Spacing

        st.markdown("### ✨ Edit Instructions")

        edit_prompt = st.text_area(
            "Describe how you want to edit the image:",
            height=100,
            placeholder="Example: Add sunglasses and a hat, make the background more colorful, change to cartoon style...",
            key="edit_prompt_textarea"
        )

        st.write("")  # Spacing

        col1, col2 = st.columns([1, 4])
        with col1:
            edit_btn = st.button("✨ Edit Image", type="primary", key="edit_image_btn")

        if edit_btn:
            # Validation
            if not edit_prompt:
                st.error("❌ Please enter edit instructions.")
                return

            if not st.session_state.client_initialized or not st.session_state.cloudinary_initialized:
                st.error("❌ Clients not properly initialized. Please check your environment variables.")
                return

            with st.spinner("✨ Editing your image..."):
                try:
                    # If uploaded file, upload to Cloudinary first
                    if input_image:
                        upload_result = st.session_state.cloudinary_client.upload_image(
                            image_data=input_image,
                            folder_type="input",
                            filename="temp_input",
                            client_folder=selected_client_folder
                        )

                        if not upload_result['success']:
                            st.error(f"❌ Failed to upload input image: {upload_result.get('error')}")
                            return

                        input_image_url = upload_result['url']

                    # Edit image using Nano Banana (using URL)
                    edited_image = st.session_state.nano_client.edit_image(
                        image_path="",
                        prompt=edit_prompt,
                        save_to_disk=False,
                        image_url=input_image_url
                    )

                    if edited_image:
                        # Upload edited image to Cloudinary
                        upload_result = st.session_state.cloudinary_client.upload_image(
                            image_data=edited_image,
                            folder_type="edited",
                            filename=f"edited_{int(time.time())}",
                            client_folder=selected_client_folder
                        )

                        if upload_result['success']:
                            # Add to session state
                            result_data = {
                                'type': 'edited',
                                'prompt': edit_prompt,
                                'edited_image': edited_image,
                                'cloudinary_url': upload_result['url'],
                                'cloudinary_public_id': upload_result['public_id'],
                                'timestamp': time.time(),
                                'client_folder': selected_client_folder
                            }
                            st.session_state.generated_images.append(result_data)
                            add_to_session_cost()

                            # Display success
                            st.markdown("""
                            <div class="success-box">
                                ✅ <strong>Image Edited Successfully!</strong>
                            </div>
                            """, unsafe_allow_html=True)

                            # Display before/after comparison
                            st.subheader("🔄 Before & After Comparison")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.image(input_image_url, caption="📄 Original Image", use_container_width=True)
                            with col2:
                                st.image(edited_image, caption="✨ Edited Image", use_container_width=True)

                            # Cloudinary URL and download
                            st.write("**Edited Image Cloudinary URL:**")
                            st.code(upload_result['url'], language=None)

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
                            st.error(f"❌ Failed to upload edited image: {upload_result.get('error')}")
                    else:
                        st.error("❌ Failed to edit image. Please try again.")

                except Exception as e:
                    st.error(f"❌ Error editing image: {str(e)}")
    else:
        st.info("📁 Please select or upload an image to start editing.")

def image_gallery_tab():
    """Tab for browsing all images in Cloudinary"""
    st.header("🖼️ Image Gallery")

    if not st.session_state.cloudinary_initialized:
        st.error("❌ Cloudinary not initialized. Please check your environment variables.")
        return

    # Initialize pagination state
    if 'gallery_page_cursor' not in st.session_state:
        st.session_state.gallery_page_cursor = None
    if 'gallery_current_page' not in st.session_state:
        st.session_state.gallery_current_page = 1

    # Load client folders
    folders_result = st.session_state.cloudinary_client.list_client_folders()

    if not folders_result['success']:
        st.error(f"❌ Failed to load client folders: {folders_result.get('error')}")
        return

    client_folders = folders_result.get('folders', [])

    if not client_folders:
        st.info("ℹ️ No client folders found in Cloudinary. Generate some images first!")
        return

    # Filters section
    st.subheader("🔍 Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_client = st.selectbox(
            "Select Client Folder:",
            options=client_folders,
            key="gallery_client_selector"
        )

    with col2:
        folder_type = st.selectbox(
            "Image Type:",
            options=["all", "generated", "edited"],
            key="gallery_folder_type"
        )

    with col3:
        images_per_page = st.selectbox(
            "Images per page:",
            options=[20, 30, 50],
            index=1,
            key="gallery_per_page"
        )

    # Date range filter
    st.markdown("**Filter by Date Range** (optional)")
    col_date1, col_date2 = st.columns(2)

    with col_date1:
        start_date = st.date_input(
            "Start Date:",
            value=None,
            key="gallery_start_date"
        )

    with col_date2:
        end_date = st.date_input(
            "End Date:",
            value=None,
            key="gallery_end_date"
        )

    # Reset button
    if st.button("🔄 Reset Filters & Reload"):
        st.session_state.gallery_page_cursor = None
        st.session_state.gallery_current_page = 1
        st.rerun()

    st.markdown("---")

    # Load images
    with st.spinner("📥 Loading images..."):
        try:
            # Convert dates to ISO format
            start_date_str = start_date.isoformat() if start_date else None
            end_date_str = end_date.isoformat() if end_date else None

            images_result = st.session_state.cloudinary_client.list_images_paginated(
                client_folder=selected_client,
                folder_type=folder_type,
                max_results=images_per_page,
                next_cursor=st.session_state.gallery_page_cursor,
                start_date=start_date_str,
                end_date=end_date_str
            )

            if not images_result['success']:
                st.error(f"❌ Failed to load images: {images_result.get('error')}")
                return

            images = images_result.get('images', [])
            total_count = images_result.get('total_count', 0)
            has_more = images_result.get('has_more', False)
            next_cursor = images_result.get('next_cursor')

            # Display count
            st.info(f"📊 Showing {len(images)} images (Total in folder: {total_count})")

            if not images:
                st.warning("⚠️ No images found with the current filters.")
                return

            # Bulk export section
            st.markdown("### 📋 Bulk Actions")
            col_bulk1, col_bulk2 = st.columns([1, 3])

            with col_bulk1:
                if st.button("📤 Export All URLs"):
                    # Create CSV content
                    csv_content = "filename,url,width,height,created_at,public_id\n"
                    for img in images:
                        filename = img.get('public_id', '').split('/')[-1]
                        url = img.get('secure_url', '')
                        width = img.get('width', '')
                        height = img.get('height', '')
                        created = img.get('created_at', '')
                        public_id = img.get('public_id', '')
                        csv_content += f"{filename},{url},{width},{height},{created},{public_id}\n"

                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_content,
                        file_name=f"cloudinary_export_{selected_client}_{int(time.time())}.csv",
                        mime="text/csv"
                    )

            # Display images in grid
            st.markdown("### 🖼️ Images")

            # Create grid with 3 columns
            for i in range(0, len(images), 3):
                cols = st.columns(3)

                for j, col in enumerate(cols):
                    if i + j < len(images):
                        img = images[i + j]

                        with col:
                            # Display image
                            img_url = img.get('secure_url', '')
                            st.image(img_url, use_container_width=True)

                            # Image metadata
                            filename = img.get('public_id', '').split('/')[-1]
                            st.markdown(f"**{filename}**")

                            # Dimensions
                            width = img.get('width', 'N/A')
                            height = img.get('height', 'N/A')
                            st.caption(f"📏 {width} × {height}")

                            # Date
                            created_at = img.get('created_at', '')
                            if created_at:
                                # Parse and format date
                                from datetime import datetime
                                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                                formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                                st.caption(f"📅 {formatted_date}")

                            # Copy URL button
                            st.code(img_url, language=None)

                            # Info button
                            with st.expander("ℹ️ Details"):
                                st.json({
                                    'public_id': img.get('public_id'),
                                    'format': img.get('format'),
                                    'bytes': img.get('bytes'),
                                    'resource_type': img.get('resource_type')
                                })

            # Pagination controls
            st.markdown("---")
            col_prev, col_info, col_next = st.columns([1, 2, 1])

            with col_prev:
                if st.session_state.gallery_current_page > 1:
                    if st.button("⬅️ Previous Page"):
                        st.session_state.gallery_current_page -= 1
                        st.session_state.gallery_page_cursor = None  # Reset to first page
                        st.rerun()

            with col_info:
                st.markdown(f"**Page {st.session_state.gallery_current_page}**")

            with col_next:
                if has_more and next_cursor:
                    if st.button("➡️ Next Page"):
                        st.session_state.gallery_current_page += 1
                        st.session_state.gallery_page_cursor = next_cursor
                        st.rerun()

        except Exception as e:
            st.error(f"❌ Error loading gallery: {str(e)}")

def session_gallery():
    """Display session gallery"""
    if st.session_state.generated_images:
        st.header("📸 Session Gallery")

        for i, result in enumerate(reversed(st.session_state.generated_images)):
            with st.expander(f"{result['type'].title()} #{len(st.session_state.generated_images) - i}"):
                col1, col2 = st.columns([1, 1])

                with col1:
                    if result['type'] == 'edited':
                        st.image(result['edited_image'], caption="Result", use_container_width=True)
                    else:
                        st.image(result['image'], caption="Generated Image", use_container_width=True)

                with col2:
                    st.write(f"**Prompt:** {result['prompt']}")
                    st.write(f"**Cloudinary URL:**")
                    st.code(result['cloudinary_url'], language=None)
                    st.write(f"**Created:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['timestamp']))}")

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📢 Loudspeaker Marketing Image Playground</h1>
        <p>Create fresh images and product mockups for your marketing campaigns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize clients
    success, error = initialize_clients()
    if not success:
        st.error(f"❌ **Configuration Error:** {error}")
        st.markdown("""
        **Required Environment Variables:**
        - `GOOGLE_AI_API_KEY` - Your Google AI API key
        - `CLOUDINARY_CLOUD_NAME` - Your Cloudinary cloud name
        - `CLOUDINARY_API_KEY` - Your Cloudinary API key
        - `CLOUDINARY_API_SECRET` - Your Cloudinary API secret
        - `CLIENT_FOLDER_NAME` - Folder name for organizing uploads (e.g., 'XV1')
        """)
        st.stop()
    
    # Display cost information
    display_cost_info()

    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "✨ Generate Fresh Image",
        "🎨 Generate Product Mockup Image",
        "🖼️ Image Gallery"
    ])

    with tab1:
        generate_image_tab()

    with tab2:
        edit_image_tab()

    with tab3:
        image_gallery_tab()

    # Session gallery (always visible at bottom)
    session_gallery()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <small>AI Image Studio powered by Nano Banana (Gemini 2.5 Flash Image) • 
        Images stored on Cloudinary • Built with Streamlit</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()