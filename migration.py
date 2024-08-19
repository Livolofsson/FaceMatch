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
DB_CONNECTION = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
vx = vecs.create_client(DB_CONNECTION)
images = vx.get_or_create_collection(name="images", dimension=128)

def upload_image_to_storage():
    error_file = open("errors.txt", "a")
    #for root, _, filenames in os.walk("C:\\Users\\astri\\Downloads\\SBL\\SBL\\sbl-bilder"):
    for root, _, filenames in os.walk("C:\\Users\\astri\\summer24\\FaceMatch\\test_bilder"):
        for filename in filenames: 
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = str(os.path.join(root, filename))
                try:
                    if 0 < len(DeepFace.extract_faces(img_path=image_path)):
                        try:
                            with open(image_path, "rb") as image_file:
                                image_name = os.path.basename(image_path)
                                supabase.storage.from_("images").upload(file=image_file, path=image_name, file_options={"content-type": "image/png+jpeg"})
                        except Exception as e:
                            print(f"Failed to upload image {e}")
                            error_file.write(f"{filename}, {e}\n")
                except Exception as e:
                    error_file.write(f"{filename}, {e}\n")
    error_file.close()


def insert_image_feature_vector():
    error_file = open("errors.txt", "a")
    #for root, _, filenames in os.walk("C:\\Users\\astri\\Downloads\\SBL\\SBL\\sbl-bilder"):
    for root, _, filenames in os.walk("C:\\Users\\astri\\summer24\\FaceMatch\\test_bilder"):
        for filename in filenames: 
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = str(os.path.join(root,filename))
                try: 
                    if 0 < len(DeepFace.extract_faces(img_path=image_path)):
                        with open(image_path, "rb") as image_file:
                            #url = f"https://thzrfpngunhhpdsgqiac.supabase.co/storage/v1/object/public/images/{filename}"
                            feature_vectors = DeepFace.represent(image_path,model_name="Facenet", enforce_detection=False)
                            embeddings = [feature_vector["embedding"] for feature_vector in feature_vectors]
                            try:
                                records = [(f"{filename}_{i}", embedding ,{"image_path": filename}) for i, embedding in enumerate(embeddings)]
                                images.upsert(records)
                                print("success")
                            except Exception as e:
                                print(f"Failed to upsert records {e}")
                                error_file.write(f"{filename}, {e}\n")
                except Exception as e:
                    error_file.write(f"{filename}, {e}\n")
    error_file.close()

# for i in []:
#     for j in []:
#         upload_image_to_storage()
#         insert_image_feature_vector()

             
upload_image_to_storage()
insert_image_feature_vector()

try:
    images.create_index()
    print("Index created successfully.")
except Exception as e:
    print("Failed to create index.")

vx.disconnect()