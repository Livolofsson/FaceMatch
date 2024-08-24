import os
from supabase import create_client
from dotenv import load_dotenv
import vecs 
from deepface import DeepFace
import sys
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

def upload(image_folder_root: str):
    count = 0
    for root, _, filenames in os.walk(image_folder_root):
        for filename in filenames:
            image_path = str(os.path.join(root, filename))
            if count % 10 == 0:
                print(count)
            count += 1
            if not (image_path.endswith(".png") or image_path.endswith(".jpg")):
                log_error(image_path, "Not a valid image (.png, .jpg)")
                continue 
            try: 
                extract_and_store_feature(image_path)
                insert_into_storage(image_path)
            except Exception as e:
                log_error(image_path, repr(e))

def log_error(filepath: str, error: str):
    with open("errors.txt", "a") as f:
        f.write(f"{filepath}, {error}\n")

def insert_into_storage(image_path: str):
    with open(image_path, "rb") as image_file:
        filename = os.path.basename(image_path)
        supabase.storage.from_("images").upload(file=image_file, path=filename, file_options={"content-type": "image/png+jpeg"})
    
def extract_and_store_feature(image_path: str):
    filename = os.path.basename(image_path)
    feature_vectors = DeepFace.represent(
        image_path, 
        model_name="Facenet", 
        detector_backend="yolov8", 
        enforce_detection=False
    )
    embeddings = [feature_vector["embedding"] for feature_vector in feature_vectors]
    records = [(f"{filename}_{i}", embedding ,{"image_path": filename}) for i, embedding in enumerate(embeddings)]
    images.upsert(records)

upload(sys.argv[1])
images.create_index()
vx.disconnect()