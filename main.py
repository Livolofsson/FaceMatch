import streamlit as st
from PIL import Image
import numpy as np
from supabase import create_client
import vecs 
from deepface import DeepFace

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)
db_user = st.secrets["db_user"]
db_password = st.secrets["db_password"]
db_host = st.secrets["db_host"]
db_port = st.secrets["db_port"]
db_name = st.secrets["db_name"]

DB_CONNECTION = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
vx = vecs.create_client(DB_CONNECTION)
images = vx.get_or_create_collection(name="images", dimension=128)

st.title('Face Recognition from Historical Database')
st.markdown("Within seconds the most similar images are displayed. You might discover intriguing look-aliked from centuries past or unexpected resemblances\
            to famous historical figures. This integration of modern technology with historical archives offers a glimpse into the past,\
             connecting present-day faces with those from history. **Enjoy!**")

def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image

upload_file = st.file_uploader(label="Upload image", type=['jpg', 'png'])

if upload_file is not None:
    img = load_image(upload_file)
    st.image(img)
    st.markdown("Image Uploaded Successfully")

    with st.spinner("Finding matches..."):
        try:
            represent = DeepFace.represent(img,model_name="Facenet", enforce_detection=False)
            dicti = represent[0]
            result = dicti.get("embedding")

            similar_images = images.query(data=result, limit=3)
            response = supabase.storage.from_('images').get_public_url(f"{similar_images[0]}")
            response1 = supabase.storage.from_('images').get_public_url(f"{similar_images[1]}")
            response2 = supabase.storage.from_('images').get_public_url(f"{similar_images[2]}")
        
            if response and response1 and response2:
                st.markdown("The best match was following image:")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.image(response, width=200)
                with col2:
                    st.image(response1, width=200)
                with col3:
                    st.image(response2, width=200)

                #st.image([response, response1, response2],width=200)
                st.markdown("If you want to download the images, then click on the following buttons:")
                st.link_button("Download image 1", response)
                st.link_button("Download image 2", response1)
                st.link_button("Download image 3", response2)   
        except Exception as e:
            print(e)    
else:
    st.write("Make sure your image is in JPG/PNG format.")
