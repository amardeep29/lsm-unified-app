"""
Client Onboarding System - Streamlit Interface
Handles client folder creation and bulk image uploads to Cloudinary
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import re
import time
import json
import os
from typing import Optional

# Get API server URL from environment variable or use localhost as fallback
API_SERVER_URL = os.getenv('API_SERVER_URL', 'http://localhost:5001')

# Page configuration
st.set_page_config(
    page_title="Client Onboarding System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Loudspeaker Marketing Dark Theme
st.markdown("""
<style>
    /* Dark background everywhere */
    .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #06070B !important;
    }

    /* Light text on all elements */
    .main *, .stApp *, p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #E6E6E6 !important;
    }

    /* Markdown and text elements */
    .stMarkdown, .stMarkdown *, .stText, .stText * {
        color: #E6E6E6 !important;
    }

    /* Headers - bold white text */
    h1, h2, h3, h4, h5, h6 {
        color: #E6E6E6 !important;
        font-weight: bold !important;
    }

    /* Input fields - dark theme with yellow focus */
    label, .stTextInput label {
        color: #E6E6E6 !important;
    }

    input, textarea, .stTextInput input, .stTextArea textarea {
        background-color: #272F35 !important;
        color: #E6E6E6 !important;
        border: 2px solid rgba(231, 254, 58, 0.2) !important;
        border-radius: 0.5rem !important;
    }

    input:focus, textarea:focus {
        border-color: #E7FE3A !important;
        background-color: #06070B !important;
    }

    input::placeholder, textarea::placeholder {
        color: #666666 !important;
    }

    /* Main header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(231, 254, 58, 0.1);
        margin-bottom: 2rem;
        background-color: #06070B !important;
    }
    .main-header h1, .main-header p {
        color: #E6E6E6 !important;
    }

    /* Step indicator - dark theme */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 0 2rem;
        background-color: #06070B !important;
    }
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        position: relative;
        background-color: #272F35 !important;
        color: #E6E6E6 !important;
        font-weight: bold;
        border: 2px solid rgba(231, 254, 58, 0.15);
        margin: 0 0.5rem;
        border-radius: 0.5rem;
    }
    .step div {
        color: #E6E6E6 !important;
    }
    .step.active {
        background-color: #E7FE3A !important;
        border-color: #E7FE3A !important;
    }
    .step.active, .step.active div, .step.active * {
        color: #06070B !important;
    }
    .step.completed {
        background-color: #272F35 !important;
        border-color: #E7FE3A !important;
    }
    .step.completed, .step.completed div, .step.completed * {
        color: #E7FE3A !important;
    }

    /* Buttons - yellow theme with arrows */
    .stButton button {
        background-color: #E7FE3A !important;
        color: #06070B !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        border-radius: 0.5rem !important;
        cursor: pointer !important;
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

    .stButton button:disabled {
        background-color: #272F35 !important;
        color: #666666 !important;
        cursor: not-allowed !important;
    }

    .stButton button:disabled * {
        color: #666666 !important;
    }

    /* Info boxes - dark cards */
    .stAlert {
        background-color: #272F35 !important;
        border: 1px solid rgba(231, 254, 58, 0.15) !important;
        color: #E6E6E6 !important;
    }

    /* Success/Warning/Error boxes */
    [data-baseweb="notification"] {
        background-color: #272F35 !important;
        border-left: 4px solid #E7FE3A !important;
    }

    /* Number input */
    .stNumberInput input {
        background-color: #272F35 !important;
        color: #E6E6E6 !important;
        border: 2px solid rgba(231, 254, 58, 0.2) !important;
    }

    /* Footer */
    footer, footer * {
        color: #B0B0B0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    if 'client_name' not in st.session_state:
        st.session_state.client_name = ""
    if 'client_exists' not in st.session_state:
        st.session_state.client_exists = False
    if 'folders_created' not in st.session_state:
        st.session_state.folders_created = []
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = []
    if 'cloudinary_config' not in st.session_state:
        st.session_state.cloudinary_config = None
    if 'submit_clicked' not in st.session_state:
        st.session_state.submit_clicked = False
    if 'check_clicked' not in st.session_state:
        st.session_state.check_clicked = False

# Validate client name
def validate_client_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate client name format

    Returns:
        tuple: (is_valid, error_message)
    """
    if not name:
        return False, "Client name is required"

    if len(name) < 3:
        return False, "Client name must be at least 3 characters"

    if len(name) > 50:
        return False, "Client name must be 50 characters or less"

    if not re.match(r'^[a-zA-Z0-9-]+$', name):
        return False, "Client name can only contain letters, numbers, and hyphens"

    return True, None

# Sanitize client name
def sanitize_client_name(name: str) -> str:
    """Replace spaces with hyphens and remove invalid characters"""
    # Replace spaces with hyphens
    name = name.replace(' ', '-')
    # Remove any characters that aren't alphanumeric or hyphens
    name = re.sub(r'[^a-zA-Z0-9-]', '', name)
    # Convert to lowercase for consistency
    name = name.lower()
    return name

# API helper functions
def check_client_exists(client_name: str, api_url: str = None) -> dict:
    if api_url is None:
        api_url = API_SERVER_URL
    """Check if client folder exists via API"""
    try:
        response = requests.post(
            f"{api_url}/api/check-client",
            json={"client_name": client_name},
            timeout=10
        )
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

def create_client_folders(client_name: str, api_url: str = None) -> dict:
    if api_url is None:
        api_url = API_SERVER_URL
    """Create client folders via API"""
    try:
        response = requests.post(
            f"{api_url}/api/create-client-folders",
            json={"client_name": client_name},
            timeout=30
        )
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

def get_upload_config(client_name: str, api_url: str = None) -> dict:
    if api_url is None:
        api_url = API_SERVER_URL
    """Get Cloudinary upload configuration via API"""
    try:
        response = requests.post(
            f"{api_url}/api/get-upload-config",
            json={"client_name": client_name},
            timeout=10
        )
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

# Step indicator
def display_step_indicator(current_step: int):
    """Display progress indicator for onboarding steps"""
    steps = [
        {"num": 1, "title": "Client Info"},
        {"num": 2, "title": "Folder Setup"},
        {"num": 3, "title": "Upload Images"},
        {"num": 4, "title": "Complete"}
    ]

    st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
    for step in steps:
        step_class = ""
        if step["num"] == current_step:
            step_class = "active"
        elif step["num"] < current_step:
            step_class = "completed"

        st.markdown(f'''
            <div class="step {step_class}">
                <div style="font-size: 1.5rem; font-weight: bold;">{step["num"]}</div>
                <div>{step["title"]}</div>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Step 1: Client Information
def step_1_client_info():
    """Step 1: Collect and validate client information"""
    st.title("📋 Step 1: Enter Client Information")

    st.write("")  # Spacing

    # Instructions with better formatting
    st.info("""
    **Instructions:**
    - Enter a client name (3-50 characters)
    - Only letters, numbers, and hyphens are allowed
    - Spaces will be automatically converted to hyphens
    - Example: "ABC Company" becomes "abc-company"
    """)

    st.write("")  # Spacing

    # Client name input with larger text
    st.markdown("### Enter Client Name")
    client_name_raw = st.text_input(
        "Client Name",
        value=st.session_state.client_name,
        placeholder="Enter client name (e.g., ABC-Company, Client-2024)",
        label_visibility="collapsed",
        key="client_name_input"
    )

    st.write("")  # Spacing

    # Submit button
    if st.session_state.submit_clicked:
        st.markdown("""
        <div style="background-color: #28a745; color: white; padding: 0.75rem; text-align: center; border-radius: 0.5rem; font-weight: bold;">
            ✓ Client Name Submitted
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("✓ **Submit Client Name**", type="primary", use_container_width=True, disabled=(not client_name_raw), key="submit_btn"):
            st.session_state.submit_clicked = True
            st.rerun()

    st.write("")  # Spacing

    # Show validation and buttons only when button is clicked
    if client_name_raw and st.session_state.submit_clicked:
        sanitized_name = sanitize_client_name(client_name_raw)

        # Show sanitized name if different
        if sanitized_name != client_name_raw:
            st.warning(f"**Auto-corrected to:** `{sanitized_name}`")

        # Validate
        is_valid, error_message = validate_client_name(sanitized_name)

        if not is_valid:
            st.error(f"❌ **Error:** {error_message}")
        else:
            st.success(f"✅ **Valid client name:** `{sanitized_name}`")

            st.write("")  # Spacing
            st.write("---")  # Divider
            st.write("")  # Spacing

            # Check availability button and results
            if not st.session_state.check_clicked:
                if st.button("🔍 **Check Client Availability**", type="primary", use_container_width=True, key="check_btn"):
                    st.session_state.check_clicked = True
                    st.rerun()

            # Show results after checking
            if st.session_state.check_clicked:
                with st.spinner("⏳ Checking if client exists..."):
                    result = check_client_exists(sanitized_name)

                    if result.get('success'):
                        if result.get('exists'):
                            st.session_state.client_exists = True
                            subfolders = result.get('subfolders', [])

                            st.warning(f"""
                            **⚠️ Client Already Exists**

                            - **Folder:** `{result.get('folder_path')}`
                            - **Existing folders:** {', '.join(subfolders)}

                            You can proceed to add more images to this existing client.
                            """)
                        else:
                            st.session_state.client_exists = False

                            st.success(f"""
                            **✅ Client Name Available!**

                            The client name `{sanitized_name}` is available.

                            Ready to create folder structure.
                            """)

                        st.write("")  # Spacing
                        st.session_state.client_name = sanitized_name

                        # Show continue button
                        if st.session_state.client_exists:
                            if st.button("📁 **Proceed with Existing Client →**", type="primary", use_container_width=True):
                                st.session_state.onboarding_step = 2
                                st.session_state.submit_clicked = False
                                st.session_state.check_clicked = False
                                st.rerun()
                        else:
                            if st.button("➡️ **Continue to Folder Creation →**", type="primary", use_container_width=True):
                                st.session_state.onboarding_step = 2
                                st.session_state.submit_clicked = False
                                st.session_state.check_clicked = False
                                st.rerun()
                    else:
                        st.error(f"""
                        **❌ Error Checking Client**

                        {result.get('error')}

                        Please try again or contact support.
                        """)

# Step 2: Folder Creation
def step_2_folder_creation():
    """Step 2: Create Cloudinary folder structure"""
    st.title("📁 Step 2: Create Folder Structure")

    st.write("")  # Spacing

    # Show client details
    st.info(f"""
    **Client Name:** `{st.session_state.client_name}`

    **Folders to create:**
    - `{st.session_state.client_name}/input/` - For uploaded images
    - `{st.session_state.client_name}/generated/` - For AI-generated images
    - `{st.session_state.client_name}/edited/` - For edited images
    """)

    st.write("")  # Spacing

    if st.session_state.client_exists:
        st.warning("""
        **ℹ️ Client Folder Already Exists**

        This client already has folders in Cloudinary.
        You can skip this step and proceed to upload images.
        """)

        st.write("")  # Spacing
        st.write("---")
        st.write("")  # Spacing

        # Navigation buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ **Back to Client Info**", use_container_width=True):
                st.session_state.onboarding_step = 1
                st.rerun()

        with col2:
            if st.button("➡️ **Continue to Upload →**", type="primary", use_container_width=True):
                st.session_state.onboarding_step = 3
                st.rerun()
    else:
        st.markdown("### Ready to Create Folders")
        st.write("Click the button below to create the folder structure in Cloudinary.")

        st.write("")  # Spacing
        st.write("---")
        st.write("")  # Spacing

        # Create folders button
        if st.button("📁 **Create Folders Now**", type="primary", use_container_width=True):
            with st.spinner("⏳ Creating folder structure..."):
                result = create_client_folders(st.session_state.client_name)

                if result.get('success'):
                    st.session_state.folders_created = result.get('folders_created', [])

                    st.success(f"""
                    **✅ Folders Created Successfully!**

                    - **Created folders:** {', '.join(st.session_state.folders_created)}
                    - **Cloudinary path:** `{result.get('folder_path')}`

                    Ready to upload images!
                    """)

                    st.write("")  # Spacing
                    time.sleep(1)
                    st.session_state.onboarding_step = 3
                    st.rerun()
                else:
                    st.error(f"""
                    **❌ Folder Creation Failed**

                    {result.get('error')}

                    Please try again or contact support.
                    """)

        st.write("")  # Spacing

        # Back button
        if st.button("⬅️ **Back to Client Info**", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()

# Step 3: Image Upload
def step_3_image_upload():
    """Step 3: Upload images using Cloudinary widget"""
    st.title("📤 Step 3: Upload Images")

    st.write("")  # Spacing

    # Show client details
    st.info(f"""
    **Client Name:** `{st.session_state.client_name}`

    **Upload Destination:** `{st.session_state.client_name}/input/`

    **Supported:**
    - Multiple images (up to 100 per batch)
    - Maximum file size: 10MB per image
    - Formats: JPG, PNG, GIF, WebP, and more
    """)

    st.write("")  # Spacing

    # Get upload configuration
    if not st.session_state.cloudinary_config:
        with st.spinner("⏳ Loading upload configuration..."):
            config_result = get_upload_config(st.session_state.client_name)
            if config_result.get('success'):
                st.session_state.cloudinary_config = config_result
            else:
                st.error(f"""
                **❌ Failed to Get Upload Configuration**

                {config_result.get('error')}

                Please try again or contact support.
                """)

                st.write("")  # Spacing

                if st.button("⬅️ **Back to Folder Setup**", use_container_width=True):
                    st.session_state.onboarding_step = 2
                    st.rerun()
                return

    config = st.session_state.cloudinary_config

    st.markdown("### Open Upload Page")
    st.write("Click the button below to open the upload page in a new tab.")

    st.write("")  # Spacing

    # Build the upload URL with parameters
    upload_url = f"{API_SERVER_URL}/upload?client={st.session_state.client_name}&cloud={config.get('cloud_name')}&preset={config.get('upload_preset')}&folder={config.get('folder')}"

    # Create a clickable link button
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="{upload_url}" target="_blank" style="text-decoration: none;">
            <button style="
                background-color: #0078FF;
                color: white;
                padding: 1rem 3rem;
                border: none;
                border-radius: 0.5rem;
                font-size: 1.125rem;
                font-weight: bold;
                cursor: pointer;
                transition: background-color 0.2s;
            ">
                📤 Open Upload Page (New Tab)
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # Spacing
    st.write("---")
    st.write("")  # Spacing

    st.info("""
    **Instructions:**

    1. Click the button above to open the upload page in a new tab
    2. Upload your images using the Cloudinary widget
    3. After uploading, return to this page
    4. Enter the number of images you uploaded below
    5. Click "Complete Onboarding" to finish

    **Note:** You can view and copy image links anytime from the "Browse Images" page on the main dashboard.
    """)

    st.write("")  # Spacing

    # Manual input for uploaded images
    st.markdown("### Confirm Upload Count")

    uploaded_count = st.number_input(
        "Number of images uploaded:",
        min_value=0,
        max_value=1000,
        value=len(st.session_state.uploaded_images),
        key="manual_upload_count"
    )

    st.write("")  # Spacing
    st.write("---")
    st.write("")  # Spacing

    # Navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ **Back to Folder Setup**", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()

    with col2:
        if st.button("✅ **Complete Onboarding →**", type="primary", use_container_width=True):
            st.session_state.onboarding_step = 4
            st.rerun()

# Step 4: Completion
def step_4_completion():
    """Step 4: Display completion summary"""
    st.title("🎉 Onboarding Complete!")

    st.write("")  # Spacing

    # Success summary
    st.success(f"""
    **✅ Client Successfully Onboarded!**

    Your client has been set up and is ready to use.
    """)

    st.write("")  # Spacing

    # Client details
    st.info(f"""
    **📋 Client Summary:**

    - **Client Name:** `{st.session_state.client_name}`
    - **Folders Created:** {', '.join(st.session_state.folders_created) if st.session_state.folders_created else 'Used existing folders'}
    - **Images Uploaded:** {len(st.session_state.uploaded_images)}
    - **Cloudinary Path:** `{st.session_state.client_name}/input/`
    """)

    st.write("")  # Spacing

    # Next steps
    st.markdown("### 📋 What You Can Do Next:")
    st.markdown("""
    1. ✅ **Images are now available in Cloudinary**
       - Access them via the client folder path

    2. 🎨 **Generate or edit images for this client**
       - Use the image generation tools with this client's folder

    3. 🖼️ **View uploaded images in the Image Gallery**
       - Browse and manage all client images

    4. 📤 **Upload more images anytime**
       - Return to this onboarding system to add more images
    """)

    st.write("")  # Spacing
    st.write("---")
    st.write("")  # Spacing

    # Action buttons
    st.markdown("### Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 **Onboard Another Client**", type="primary", use_container_width=True):
            # Reset session state
            st.session_state.onboarding_step = 1
            st.session_state.client_name = ""
            st.session_state.client_exists = False
            st.session_state.folders_created = []
            st.session_state.uploaded_images = []
            st.session_state.cloudinary_config = None
            st.rerun()

    with col2:
        # Link to Cloudinary Media Library for this client
        cloudinary_media_url = f"https://cloudinary.com/console/c-{st.session_state.cloudinary_config.get('cloud_name', 'console')}/media_library/folders/{st.session_state.client_name}"
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{cloudinary_media_url}" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #6c757d;
                    color: white;
                    padding: 0.75rem 2rem;
                    border: none;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    font-weight: bold;
                    cursor: pointer;
                    width: 100%;
                ">
                    📊 View Image Gallery
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Link to main Streamlit app (you'll need to create this)
        st.markdown("""
        <div style="text-align: center;">
            <a href="http://localhost:8502" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #6c757d;
                    color: white;
                    padding: 0.75rem 2rem;
                    border: none;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    font-weight: bold;
                    cursor: pointer;
                    width: 100%;
                ">
                    🎨 Generate Images
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

# Main application
def main():
    """Main application function"""
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📋 Client Onboarding System</h1>
        <p>Create client folders and upload images to Cloudinary</p>
    </div>
    """, unsafe_allow_html=True)

    # Display step indicator
    display_step_indicator(st.session_state.onboarding_step)

    st.markdown("---")

    # Route to appropriate step
    if st.session_state.onboarding_step == 1:
        step_1_client_info()
    elif st.session_state.onboarding_step == 2:
        step_2_folder_creation()
    elif st.session_state.onboarding_step == 3:
        step_3_image_upload()
    elif st.session_state.onboarding_step == 4:
        step_4_completion()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <small>Client Onboarding System • Powered by Cloudinary • Built with Streamlit</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
