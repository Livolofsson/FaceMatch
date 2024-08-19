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

upload_file = st.file_uploader(label="Upload image", type=['jpg', 'png', 'webp'])

if upload_file is not None:
    img = load_image(upload_file)
    st.image(img)

    with st.spinner("Finding matches..."):
        try:
            represent = DeepFace.represent(img,model_name="Facenet", enforce_detection=False)
            dicti = represent[0]
            result = dicti.get("embedding")

            similar_images = images.query(data=result, limit=3, include_metadata=True, include_value=True)
            signed_urls = []
            for sim_image in similar_images:
                file_path = sim_image[2].get("image_path")
                res = supabase.storage.from_("images").create_signed_url(file_path, expires_in=60)
                signed_urls.append(res["signedURL"])

            if len(signed_urls) != 0:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(signed_urls[0], width=200)
                    with col2:
                        st.image(signed_urls[1], width=200)
                    with col3:
                        st.image(signed_urls[2], width=200)


            # tuple_0 = similar_images[0]
            # tuple_1 = similar_images[1]
            # tuple_2 = similar_images[2]
            # response = tuple_0[2].get("image_url")
            # response1 = tuple_1[2].get("image_url")
            # response2 = tuple_2[2].get("image_url")
        
            # if response and response1 and response2:
            #     col1, col2, col3 = st.columns(3)

            #     with col1:
            #         st.image(response, width=200)
            #     with col2:
            #         st.image(response1, width=200)
            #     with col3:
            #         st.image(response2, width=200)

                    st.markdown("Right click on an image to download it")  
        except Exception as e:
            st.error(f"An error occurred: {e}")    