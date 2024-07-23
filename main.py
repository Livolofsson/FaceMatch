import streamlit as st
from PIL import Image
import numpy as np
from supabase import create_client
from dotenv import load_dotenv
import vecs 
import os

from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image

upload_file = st.file_uploader(label="Upload image", type=['jpg', 'png'])

if upload_file is not None:
    img = load_image(upload_file)
    st.image(img)
    st.write("Image Uploaded Successfully")

    with BytesIO() as output:
        upload_file.seek(0)
        img.save(output, format='PNG')
        image_data = output.getvalue()
        image_name = upload_                                                              file.name

        # Upload image to Supabase storage
        supabase.storage.from_('images').upload(image_name, image_data)
        st.write("Image saved to Supabase Storage")
else:
    st.write("Make sure your image is in JPG/PNG format.")

def fetch_image_from_db():                                                                                                                                                                             
    response = supabase.storage.from_('images').get_public_url('/shakira1.png')
    print(response)
    if response:
        st.image(
            response,
            width=400
            )
        
fetch_image_from_db()