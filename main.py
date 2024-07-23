import streamlit as st
from PIL import Image
import numpy as np
from supabase import create_client
from dotenv import load_dotenv
import vecs 
import os
from deepface import DeepFace
import time

from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")

DB_CONNECTION = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
vx = vecs.create_client(DB_CONNECTION)
images = vx.get_or_create_collection(name="images", dimension=128)

def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image

upload_file = st.file_uploader(label="Upload image", type=['jpg', 'png'])

if upload_file is not None:
    img = load_image(upload_file)
    st.image(img)
    st.write("Image Uploaded Successfully")

    with st.spinner("Finding matches..."):
        represent = DeepFace.represent(img,model_name="Facenet", enforce_detection=False)
        dicti = represent[0]
        result = dicti.get("embedding")

        similar_images = images.query(data=result, limit=2)
        response = supabase.storage.from_('images').get_public_url(f"{similar_images[0]}")
        response1 = supabase.storage.from_('images').get_public_url(f"{similar_images[1]}")
        if response and response1:
            st.write("The best match was following image:")
            st.image(response,width=400)
            st.image(response1,width=400)
            st.write("If you want to download the images then click on the following URL link:")
            st.write(response, response1)
            
else:
    st.write("Make sure your image is in JPG/PNG format.")

