import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Steganography Tool",
    page_icon="🕵️",
    layout="wide"
)

st.markdown("""
<style>

/* ===========================
   Main App Background
=========================== */
.stApp {
    background-color: #D9F3FF;
}

/* ========================
   Sidebar
=========================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A8A, #172554);
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===========================
   Main Title
=========================== */
h1 {
    color: #1E3A8A;
    font-weight: 700;
}

/* Headers */
h2, h3 {
    color: #2563EB;
}

/* ===========================
   Buttons
=========================== */
.stButton > button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    padding: 0.5rem 1rem;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

/* ===========================
   Download Button
=========================== */
.stDownloadButton > button {
    background-color: #16A34A;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stDownloadButton > button:hover {
    background-color: #15803D;
    color: white;
}

/* ===========================
   Text Input
=========================== */
.stTextInput input {
    border-radius: 10px;
    border: 2px solid #2563EB;
}

/* ===========================
   Text Area
=========================== */
.stTextArea textarea {
    border-radius: 10px;
    border: 2px solid #2563EB;
}

/* ===========================
   File Uploader
=========================== */
[data-testid="stFileUploader"] {
    border: 2px dashed #2563EB;
    border-radius: 10px;
    padding: 10px;
}

/* ===========================
   Info Boxes
=========================== */
.stAlert {
    border-radius: 10px;
}

/* ===========================
   Horizontal Line
=========================== */
hr {
    border: 1px solid #D1D5DB;
}
            
/* Hide "Press Enter to apply" helper text */
[data-testid="InputInstructions"] {
    display: none !important;
}            

</style>
""", unsafe_allow_html=True)

def decode_image(image):
    binary_data = ""

    pixels = list(image.getdata())

    for pixel in pixels:
        for value in pixel[:3]:
            binary_data += str(value & 1)

    bytes_data = [
        binary_data[i:i+8]
        for i in range(0, len(binary_data), 8)
    ]

    message = ""

    for byte in bytes_data:
        if len(byte) < 8:
            break

        message += chr(int(byte, 2))

        if message.endswith("#####"):
            return message[:-5]

    return ""

def main():
    # Header Section
    st.markdown("""
    <h1 style="text-align:center; color:#1E3A8A; margin-bottom:10px;">
    🕵️ Steganography Tool
    </h1>

    <h4 style="text-align:center; color:#4B5563; font-weight:normal; margin-top:0;">
    Hide and Reveal Secret Messages Securely
    </h4>
    """, unsafe_allow_html=True)

    st.info("""
    ### ✨ Welcome!

    This application allows you to securely hide confidential text messages inside **PNG** and **BMP** images using **Least Significant Bit (LSB) Steganography**.

    After encoding, the hidden message can be retrieved without visibly altering the image.
    """)

    st.markdown("---")

    # Sidebar Navigation with Encode and Decode Mode Buttons
    st.sidebar.title("📌 Navigation")
    mode = st.sidebar.radio(
        "Select Mode",
        ["🔐 Encode Mode", "🔓 Decode Mode"],
        index=0,
        help="Switch between Encode and Decode modes."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Suggestions")
    st.sidebar.markdown("""
    <div style="
    background-color: rgba(255,255,255,0.08);
    padding:15px;
    border-radius:10px;
    line-height:1.0;
    font-size:14px;                                      
    ">

    ✔️ <b>Use PNG or BMP Images</b><br><br>

    ❌ <b>JPEG Images are not Supported</b><br><br>

    ✔️ <b>High Resolution Images give Better Results</b>

    </div>
    """, unsafe_allow_html=True)
    # =========================================================================
    # ENCODE MODE 
    # =========================================================================
    if mode == "🔐 Encode Mode":
        st.header("🔐 Encode Secret Message")
        st.caption("Upload a carrier image and type a secret text message to hide it inside pixel data.")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.subheader("1. Carrier Image Setup")

            # Image uploader (PNG and BMP only, block JPEG with warning)
            uploaded_file = st.file_uploader(
                "Upload a PNG or BMP carrier image",
                type=["png", "bmp", "jpg", "jpeg"],
                key="encode_uploader",
                help="PNG and BMP images only. JPEG format is blocked."
            )
            
            carrier_image = None
            if uploaded_file is not None:
                file_ext = uploaded_file.name.split('.')[-1].lower()
                # Requirement: Block JPEG uploads with clear warning
                if file_ext in ["jpg", "jpeg"]:
                    st.error("❌ JPEG format blocked! JPEG compression destroys the hidden bits. Please upload a PNG or BMP image.")
                else:
                    try:
                        carrier_image = Image.open(uploaded_file)
                        st.image(
                            carrier_image, 
                            caption=f"Carrier Image ({carrier_image.width} × {carrier_image.height} px)",
                            use_container_width=True
                        )
                    except Exception as img_err:
                        st.error(f"Error loading image: {img_err}")

        with col2:
            st.subheader("2. Secret Message & Security")
            # Multiline text box for secret message
            secret_message = st.text_area(
                "Secret Text Message",
                placeholder="Type the confidential text message you wish to hide...",
                height=150
            )
            
            # Password field for Module 3 encryption flow
            password = st.text_input(
                "Encryption Password (Optional)",
                type="password",
                placeholder="Enter password if encryption is required",
                help="Optional password field for encryption flow."
            )
            
            st.subheader("3. Action")
            # Encode button
            encode_btn = st.button("🔐 Encode Message Into Image", type="primary")
            
            if encode_btn:
                if carrier_image is None:
                    st.warning("⚠️ Please upload a valid PNG or BMP carrier image first.")
                elif not secret_message.strip():
                    st.warning("⚠️ Please enter a secret message to hide.")
                else:
                    # To do: Replace this placeholder with Module 1 encoding function during integration.
                    # For now, the original uploaded image is used for UI demonstration.

                    # Set session state to trigger successful encode UI display
                    st.session_state["stego_bytes"] = uploaded_file.getvalue()
                    st.session_state["stego_name"] = f"stego_{uploaded_file.name.rsplit('.', 1)[0]}.png"
                    st.session_state["encode_success"] = True
                    st.success("🎉 Encoding completed successfully! Your stego-image is ready for download.")

        # Requirement: Only show the download button after a successful encode (Don't show on load!)
        if st.session_state.get("encode_success") and "stego_bytes" in st.session_state:
            st.markdown("---")
            st.subheader("📥 Download Stego-Image")
            st.info("Your stego-image is generated. Click the button below to download.")
            st.download_button(
                label="📥 Download Stego-Image (PNG)",
                data=st.session_state["stego_bytes"],
                file_name=st.session_state["stego_name"],
                mime="image/png"
            )

    # =========================================================================
    # DECODE MODE 
    # =========================================================================
    else:
        st.header("🔓 Decode Secret Message")
        st.caption("Upload an encoded PNG/BMP image to reveal the hidden message.")

        st.info("📩 Upload the encoded PNG/BMP image to retrieve the hidden message.")

        uploaded_file = st.file_uploader(
            "Upload Stego Image",
            type=["png", "bmp", "jpg", "jpeg"],
            key="decode_uploader"
        )

        if uploaded_file:

            file_ext = uploaded_file.name.split('.')[-1].lower()

            if file_ext in ["jpg", "jpeg"]:
                st.error("❌ JPEG format is not recommended. Hidden data may be lost because of JPEG compression.")

            else:

                image = Image.open(uploaded_file)

                st.image(
                    image,
                    caption=f"Uploaded Stego Image ({image.width} × {image.height} px)",
                    use_container_width=True
                )

                password = st.text_input(
                    "Password (Optional)",
                    type="password",
                    key="decode_password"
                )

                decode_btn = st.button(
                    "🔓 Decode Message",
                    type="primary"
                )

                if decode_btn:
                    # Decode the hidden message from the uploaded stego-image.
                    # This function works after the image has been encoded by Module 1.
                    hidden_message = decode_image(image)

                    if hidden_message:

                        # Expected format: password::message
                        # This format depends on Module 3 (Encryption) and may change after integration.

                        if "::" in hidden_message:

                            stored_password, message = hidden_message.split("::", 1)

                            if password == stored_password:

                                st.success("🎉 Hidden message extracted successfully!")

                                st.text_area(
                                    "Hidden Message",
                                    message,
                                    height=150
                                )

                            else:

                                st.error("❌ Incorrect Password. Please try again.")

                        else:

                            st.success("🎉 Hidden message extracted successfully!")

                            st.text_area(
                                "Hidden Message",
                                hidden_message,
                                height=150
                            )

                    else:

                        st.warning("⚠️ No hidden message was found in this image.")

if __name__ == "__main__":
    main()



