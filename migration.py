import os
from supabase import create_client
from dotenv import load_dotenv
import vecs 
from deepface import DeepFace
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")

supabase = create_client(url, key)

def upload_image_to_storage():
    for _, _, filenames in os.walk("C:\\Users\\astri\\summer24\\FaceMatch\\test_bilder"):
        for filename in filenames: 
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = str(os.path.join("test_bilder",filename))
                with open(image_path, "rb") as image_file:
                    image_name = os.path.basename(image_path)
                    supabase.storage.from_("images").upload(file=image_file, path=image_name, file_options={"content-type": "image/png+jpeg"})

DB_CONNECTION = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
vx = vecs.create_client(DB_CONNECTION)
images = vx.get_or_create_collection(name="images", dimension=128)

def insert_image_feature_vector():
    for _, _, filenames in os.walk("C:\\Users\\astri\\summer24\\FaceMatch\\test_bilder"):
        for filename in filenames: 
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = str(os.path.join("test_bilder",filename))
                with open(image_path, "rb") as image_file:
                    url = f"https://thzrfpngunhhpdsgqiac.supabase.co/storage/v1/object/public/images/{filename}"
                    represent = DeepFace.represent(image_path,model_name="Facenet", enforce_detection=False)
                    dicti = represent[0]
                    result = dicti.get("embedding")
                    try:
                        images.upsert(
                            records=[
                                (filename,
                                result, 
                                {"image_url": url}
                                )
                            ]
                        )
                        print("success")
                    except Exception as e:
                        print(f"Failed to upsert records due to {e}")
                    
#upload_image_to_storage()
insert_image_feature_vector()

index_response = images.create_index()

try:
    images.create_index()
    print("Index created successfully.")
except Exception as e:
    print("Failed to create index.")


vx.disconnect()

print(os.name)