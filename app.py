"""
module 3 ui
khushi + madhuri
"""
import io
import streamlit as st
from PIL import Image

from encode_gauri_team import text_to_binary, encode_message, calculate_capacity
from decode_veera_team import decode_message
from encryption_arpita_team import encrypt_message, decrypt_message



st.set_page_config(
    page_title="Steganography Tool",
    page_icon="🕵️",
    layout="wide"
)

# UI → Khushi & Madhuri
st.markdown("""
<style>

.stApp {
    background-color: #D9F3FF;
}

.stApp, .stApp p, .stApp span, .stApp label,
.stApp div, .stApp li, .stApp small {
    color: #0F172A !important;
}

h1 {
    color: #1E3A8A !important;
    font-weight: 700;
}
h2, h3, h4 {
    color: #1D4ED8 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A8A, #172554);
}
[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton > button {
    background-color: #2563EB;
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    padding: 0.5rem 1rem;
    transition: 0.3s;
}
.stButton > button:hover {
    background-color: #1D4ED8;
    color: white !important;
}

.stDownloadButton > button {
    background-color: #16A34A;
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
.stDownloadButton > button:hover {
    background-color: #15803D;
    color: white !important;
}

.stTextInput input {
    background-color: #ffffff !important;
    color: #0F172A !important;
    border-radius: 10px;
    border: 2px solid #2563EB;
}
.stTextInput label {
    color: #0F172A !important;
    font-weight: 600;
}

.stTextArea textarea {
    background-color: #ffffff !important;
    color: #0F172A !important;
    border-radius: 10px;
    border: 2px solid #2563EB;
}
.stTextArea label {
    color: #0F172A !important;
    font-weight: 600;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748B !important;
}

[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border: 2px dashed #2563EB;
    border-radius: 10px;
    padding: 10px;
}
[data-testid="stFileUploader"] * {
    color: #0F172A !important;
}

.stRadio label, .stCheckbox label {
    color: #0F172A !important;
    font-weight: 500;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: #334155 !important;
}

.stAlert {
    border-radius: 10px;
}
.stAlert p, .stAlert div {
    color: inherit !important;
}

hr {
    border: 1px solid #CBD5E1;
}

[data-testid="InputInstructions"] {
    display: none !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #0F172A !important;
}

</style>
""", unsafe_allow_html=True)


def main():
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

    if mode == "🔐 Encode Mode":
        st.header("🔐 Encode Secret Message")
        st.caption("Upload a carrier image and type a secret text message to hide it inside pixel data.")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("1. Carrier Image Setup")

            uploaded_file = st.file_uploader(
                "Upload a PNG or BMP carrier image",
                type=["png", "bmp", "jpg", "jpeg"],
                key="encode_uploader",
                help="PNG and BMP images only. JPEG format is blocked."
            )

            carrier_image = None
            if uploaded_file is not None:
                file_ext = uploaded_file.name.split('.')[-1].lower()
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
                        capacity = calculate_capacity(carrier_image)  # Gauri
                        char_capacity = capacity // 8
                        st.caption(f"📦 This image can store up to **{char_capacity} characters**")
                    except Exception as img_err:
                        st.error(f"Error loading image: {img_err}")

        with col2:
            st.subheader("2. Secret Message & Security")
            secret_message = st.text_area(
                "Secret Text Message",
                placeholder="Type the confidential text message you wish to hide...",
                height=150
            )

            password = st.text_input(
                "Encryption Password (Optional)",
                type="password",
                placeholder="Enter password if encryption is required",
                help="Leave blank to hide without encryption."
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

                            if password.strip():
                                message_to_hide = encrypt_message(secret_message, password)  # encryption_arpita.py
                            else:
                                message_to_hide = secret_message

                            binary_message = text_to_binary(message_to_hide)  # encode_gauri.py

                            capacity = calculate_capacity(carrier_image)  # encode_gauri.py
                            if len(binary_message) > capacity:
                                st.error("❌ Message is too large for this image. Please use a larger image or a shorter message.")
                                return

                            encoded_image = encode_message(carrier_image, binary_message)  # encode_gauri.py

                            buf = io.BytesIO()
                            encoded_image.save(buf, format="PNG")
                            stego_bytes = buf.getvalue()

                            st.session_state["stego_bytes"] = stego_bytes
                            st.session_state["stego_name"] = f"stego_{uploaded_file.name.rsplit('.', 1)[0]}.png"
                            st.session_state["encode_success"] = True

                        st.success("🎉 Encoding completed successfully! Your stego-image is ready for download.")

                    except Exception as e:
                        st.error(f"❌ Encoding failed: {e}")

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
                image = Image.open(uploaded_file).convert("RGB")

                st.image(
                    image,
                    caption=f"Uploaded Stego Image ({image.width} × {image.height} px)",
                    use_container_width=True
                )

                is_encrypted = st.checkbox("🔐 Is this message encrypted?")

                password = ""

                if is_encrypted:
                    password = st.text_input(
                        "Decryption Password",
                        type="password",
                        key="decode_password"
                    )

                decode_btn = st.button("🔓 Decode Message", type="primary")

                if decode_btn:
                    try:
                        with st.spinner("Extracting hidden message..."):
                            hidden_message = decode_message(image)  # decode_veera.py

                        if hidden_message:
                            looks_encrypted = hidden_message.startswith("gAAAAA")

                            if looks_encrypted and not is_encrypted:
                                st.error("🔐 This image contains an encrypted message. Please check **'Is this message encrypted?'** above and enter the password.")

                            elif is_encrypted:
                                if not password.strip():
                                    st.error("❌ Please enter the decryption password.")
                                else:
                                    try:
                                        final_message = decrypt_message(hidden_message, password)  # encryption_arpita.py
                                        st.success("🎉 Hidden message extracted and decrypted successfully!")
                                        st.text_area("Hidden Message", final_message, height=150)
                                    except ValueError as ve:
                                        st.error(f"❌ {ve}")
                            else:
                                st.success("🎉 Hidden message extracted successfully!")
                                st.text_area("Hidden Message", hidden_message, height=150)
                        else:
                            st.warning("⚠️ No hidden message was found in this image.")

                    except Exception as e:
                        st.error(f"❌ Decoding failed: {e}")


if __name__ == "__main__":
    main()
