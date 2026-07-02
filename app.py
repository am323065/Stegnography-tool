"""
Steganography Tool - Main Application
======================================

Integrated by: [Your Name / Lead]

Module Credits:
- Module 1 (LSB Encoding)  : Gauri
- Module 2 (LSB Decoding)  : Veera
- Module 3 (Encryption)    : Arpita and Team
- UI Design                : Khushi and Madhuri
- Sample Images            : Archana
- Additional Decode Work   : Shreyaj, Vatsal

Project: Steganography Tool
Organization: UpToSkills

Description:
This app integrates all intern modules into a single working
Streamlit application. Users can hide a secret message inside
a PNG/BMP image (Encode Mode) and retrieve it later (Decode Mode).
Optionally, the message can be encrypted with a password before hiding.
"""

import io
import streamlit as st
from PIL import Image

# =========================================================================
# IMPORTING INTERN MODULES
# =========================================================================
# Gauri's Encode Module (Module 1)
from encode import text_to_binary, encode_message, calculate_capacity

# Veera's Decode Module (Module 2)
from decode import decode_message

# Arpita and Team's Encryption Module (Module 3)
from encryption import encrypt_message, decrypt_message

# =========================================================================
# PAGE CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="Steganography Tool",
    page_icon="🕵️",
    layout="wide"
)

# =========================================================================
# STYLING (UI by Khushi and Madhuri)
# =========================================================================
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


# =========================================================================
# MAIN APP
# =========================================================================
def main():

    # ---- Header (UI by Khushi and Madhuri) ----
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

    # ---- Sidebar Navigation (UI by Khushi and Madhuri) ----
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

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Module Credits")
    st.sidebar.markdown("""
    <div style="font-size:13px; line-height:1.8;">
    🔐 <b>Encode:</b> Gauri, Aman & Team<br>
    🔓 <b>Decode:</b> Veera, Shreyaj, Vatsal & Team<br>
    🔒 <b>Encryption:</b> Arpita & Rakshita<br>
    🔒 <b>Encryption Research:</b> Aftab<br>
    🎨 <b>UI:</b> Khushi & Madhuri<br>
    🖼️ <b>Images:</b> Archana<br>
    📋 <b>Requirements:</b> Muskan<br>
    📝 <b>Documentation:</b> Srajit
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

            # Image uploader - PNG and BMP only (block JPEG with warning)
            # UI by Khushi and Madhuri
            uploaded_file = st.file_uploader(
                "Upload a PNG or BMP carrier image",
                type=["png", "bmp", "jpg", "jpeg"],
                key="encode_uploader",
                help="PNG and BMP images only. JPEG format is blocked."
            )

            carrier_image = None
            if uploaded_file is not None:
                file_ext = uploaded_file.name.split('.')[-1].lower()

                # Block JPEG uploads with clear warning (UI by Khushi and Madhuri)
                if file_ext in ["jpg", "jpeg"]:
                    st.error("❌ JPEG format blocked! JPEG compression destroys the hidden bits. Please upload a PNG or BMP image.")
                else:
                    try:
                        carrier_image = Image.open(uploaded_file).convert("RGB")
                        st.image(
                            carrier_image,
                            caption=f"Carrier Image ({carrier_image.width} × {carrier_image.height} px)",
                            use_container_width=True
                        )

                        # Show image capacity using Gauri's calculate_capacity function
                        capacity = calculate_capacity(carrier_image)
                        char_capacity = capacity // 8
                        st.caption(f"📦 This image can store up to **{char_capacity} characters**")

                    except Exception as img_err:
                        st.error(f"Error loading image: {img_err}")

        with col2:
            st.subheader("2. Secret Message & Security")

            # Multiline text box for secret message (UI by Khushi and Madhuri)
            secret_message = st.text_area(
                "Secret Text Message",
                placeholder="Type the confidential text message you wish to hide...",
                height=150
            )

            # Optional password field — connects to Arpita's encryption module
            password = st.text_input(
                "Encryption Password (Optional)",
                type="password",
                placeholder="Enter password to encrypt message before hiding",
                help="If provided, message will be encrypted using Arpita & Team's encryption module before embedding."
            )

            st.subheader("3. Action")
            encode_btn = st.button("🔐 Encode Message Into Image", type="primary")

            if encode_btn:
                if carrier_image is None:
                    st.warning("⚠️ Please upload a valid PNG or BMP carrier image first.")
                elif not secret_message.strip():
                    st.warning("⚠️ Please enter a secret message to hide.")
                else:
                    try:
                        with st.spinner("Encoding your secret message..."):

                            # STEP A: If password given, encrypt first (Arpita & Team's Module 3)
                            if password.strip():
                                message_to_hide = encrypt_message(secret_message, password)
                                st.info("🔒 Message encrypted successfully before hiding.")
                            else:
                                message_to_hide = secret_message

                            # STEP B: Convert message to binary (Gauri's Module 1)
                            binary_message = text_to_binary(message_to_hide)

                            # STEP C: Check capacity
                            capacity = calculate_capacity(carrier_image)
                            if len(binary_message) > capacity:
                                st.error("❌ Message is too large for this image. Please use a larger image or a shorter message.")
                                return

                            # STEP D: Encode message into image (Gauri's Module 1)
                            encoded_image = encode_message(carrier_image, binary_message)

                            # STEP E: Save encoded image to bytes for download
                            buf = io.BytesIO()
                            encoded_image.save(buf, format="PNG")
                            stego_bytes = buf.getvalue()

                            # Store in session state
                            st.session_state["stego_bytes"] = stego_bytes
                            st.session_state["stego_name"] = f"stego_{uploaded_file.name.rsplit('.', 1)[0]}.png"
                            st.session_state["encode_success"] = True

                        st.success("🎉 Encoding completed successfully! Your stego-image is ready for download.")

                    except Exception as e:
                        st.error(f"❌ Encoding failed: {e}")

        # Show download button only after successful encode (UI by Khushi and Madhuri)
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

        # UI by Khushi and Madhuri
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
                image = Image.open(uploaded_file).convert("RGB")

                st.image(
                    image,
                    caption=f"Uploaded Stego Image ({image.width} × {image.height} px)",
                    use_container_width=True
                )

                # Optional password for decryption (connects to Arpita's Module 3)
                password = st.text_input(
                    "Password (Leave blank if no encryption was used)",
                    type="password",
                    key="decode_password",
                    placeholder="Enter password only if you encrypted the message during encoding"
                )

                decode_btn = st.button(
                    "🔓 Decode Message",
                    type="primary"
                )

                if decode_btn:
                    try:
                        with st.spinner("Extracting hidden message..."):

                            # STEP A: Extract hidden message from image (Veera's Module 2)
                            hidden_message = decode_message(image)

                        if hidden_message:

                            # STEP B: If password given, decrypt using Arpita's Module 3
                            if password.strip():
                                try:
                                    final_message = decrypt_message(hidden_message, password)
                                    st.success("🎉 Hidden message extracted and decrypted successfully!")
                                except ValueError:
                                    st.error("❌ Incorrect password. The message could not be decrypted.")
                                    return
                            else:
                                final_message = hidden_message
                                st.success("🎉 Hidden message extracted successfully!")

                            st.text_area(
                                "🔍 Hidden Message",
                                final_message,
                                height=150
                            )

                        else:
                            st.warning("⚠️ No hidden message was found in this image.")

                    except Exception as e:
                        st.error(f"❌ Decoding failed: {e}")

    # Footer
    st.markdown("---")
    st.caption("Steganography Tool · UpToSkills Intern Project · All module credits belong to respective authors")


if __name__ == "__main__":
    main()
