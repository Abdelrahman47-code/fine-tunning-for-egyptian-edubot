import sys
from huggingface_hub import HfApi

HF_TOKEN = ""

repo_id = "Abdelrahman04/egyptian-educational-chatbot-model"
folder_path = "egyptian-chatbot-final"

if HF_TOKEN == "hf_..." or not HF_TOKEN:
    print("Error: Please open this script and paste your Hugging Face token into the 'HF_TOKEN' variable.")
    sys.exit(1)

print(f"Uploading {folder_path} to {repo_id}...")

try:
    api = HfApi()
    api.upload_folder(
        folder_path=folder_path,
        repo_id=repo_id,
        repo_type="model",
        token=HF_TOKEN
    )
    print("Upload complete!")
except Exception as e:
    print(f"Error uploading: {e}")