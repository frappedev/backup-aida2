from datetime import datetime
from time import time
from dotenv import load_dotenv
import os
from git import Repo
import dotenv

load_dotenv()

BACKED_UP_FILE_NAME = (
    f"aida2_backup_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}")

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = f"{CURRENT_FILE_DIR}/backup"
CODEBASE_DIR = f"{BACKUP_DIR}/codebase"
DOWNLOADS_DIR = f"{BACKUP_DIR}/downloads"

# Pre-requesties
# 1. first you need to install two cli tools cloudinary-cli and aws-cli
# 2. both can be installed with pip3 install cloudinary-cli & pip3 install aws-cli
# 3. later you need to configure those,
# 4. for cloudinary, run `export CLOUDINARY_URL={can be found in cloudinary dashboard}`
# 5. for aws-cli, run 'aws config'
# 6. now you just need to add .env file
# 7. if still didn't work, you might need to install python-dotenv and gitpython packages

if os.path.exists(BACKUP_DIR):
    os.system(f"rm -r {BACKUP_DIR}")
else:
    os.makedirs(BACKUP_DIR)

os.makedirs(CODEBASE_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(f"{DOWNLOADS_DIR}/cloudinary", exist_ok=True)
os.makedirs(f"{DOWNLOADS_DIR}/s3", exist_ok=True)


# 1. clone repo (move app and api folder into backup/codebase)
Repo.clone_from('https://github.com/singhhrpreet/aida-2.0.git', CODEBASE_DIR)

# 2. export sql database and move file into backup/sql_export
load_dotenv()

exportCmd = f"mysqldump -h {dotenv.get_key('./.env', 'DB_HOST')} -u {dotenv.get_key('./.env', 'DB_USER')} -p{dotenv.get_key('./.env', 'DB_PASSWORD')} {dotenv.get_key('./.env', 'DB_DATABASE')} > ./backup/something.sql"
print(exportCmd)
os.system(exportCmd)

# 3. backup files from cloudinary and S3 bucket.
print(os.path.abspath(__file__))

cloudinary_dir = f"{DOWNLOADS_DIR}/cloudinary"
os.chdir(cloudinary_dir)
os.system(f"cld sync --pull {cloudinary_dir} shanikas")

s3_dir = f"{DOWNLOADS_DIR}/s3"
os.chdir(s3_dir)
os.system(f"aws s3 sync s3://hardevbucketsdf {s3_dir}")

os.chdir(CURRENT_FILE_DIR)
os.system(f"tar -czvf {BACKED_UP_FILE_NAME}.tar.gz backup")

os.system("rm -r backup")
