# FaceMatch

This project is a website that allows users to upload an image of a person and find the most similar matches from a historical archive. This was developed for the Department of Information Technology at Uppsala University, with the aim of being featured on Stockholm City's webpage. 

The purpose is to enable the public to easily search through the database and retrieve images that closely resemble the one they uploaded.

The project was built using Python, Streamlit for the web interface, and Supabase with its vector search feature for efficient image similarity matching.

## Installation

**1. Install requirements**

```bash
pip install -r requirements.txt
``` 

**2. Set up Supabase**

Create an account and project on [Supabase](https://supabase.com/)

Rename [.env.example](.env.example) to .env and add the required enviroment variables from Supabase

**3. Set up Streamlit**

Create an account and project on [Streamlit](https://streamlit.io/)
Add the same environment you added in .env as secrets in Streamlit

## Local development

```bash
python -m streamlit run main.py
```

## Upload images
```bash
python upload_images.py replace_with_path_to_image_folder_root
```
