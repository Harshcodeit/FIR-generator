from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv() # load env variables

# project root = app/rag/configy.py -> go up 2+1 levels
BASE_DIR = Path(__file__).resolve().parents[2]

# raw documents folder
DOCS_PATH = BASE_DIR / os.getenv('DOCS_PATH','documents')

# vector DB storage
VECTOR_DB_PATH = BASE_DIR / os.getenv('VECTOR_DB_PATH','storage/vector_db')
