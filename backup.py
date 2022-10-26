from datetime import datetime
import logging
from dotenv import load_dotenv
import os
from git import Repo
import dotenv

load_dotenv()

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    "%(asctime)s:  %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

BACKED_UP_FILE_NAME = (
    f"aida2_backup_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}")

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = f"{CURRENT_FILE_DIR}/backup"
CODEBASE_DIR = f"{BACKUP_DIR}/codebase"
DOWNLOADS_DIR = f"{BACKUP_DIR}/downloads"

if os.path.exists(BACKUP_DIR):
    logger.info('Deleting backup folder')
    os.system(f"rm -r {BACKUP_DIR}")
else:
    os.makedirs(BACKUP_DIR)

os.makedirs(CODEBASE_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(f"{DOWNLOADS_DIR}/cloudinary", exist_ok=True)
os.makedirs(f"{DOWNLOADS_DIR}/s3", exist_ok=True)


# 1. clone repo (move app and api folder into backup/codebase)
logger.info(
    'Cloning codebase, please wait, it takes time, we are working on big project! 😉')
Repo.clone_from('https://github.com/singhhrpreet/aida-2.0.git', CODEBASE_DIR)

# 2. export sql database and move file into backup/sql_export
logger.info('Exporting Database')
export_cmd = f"mysqldump -h {dotenv.get_key('./.env', 'DB_HOST')} -u {dotenv.get_key('./.env', 'DB_USER')} -p{dotenv.get_key('./.env', 'DB_PASSWORD')} {dotenv.get_key('./.env', 'DB_DATABASE')} > ./backup/database.sql"
os.system(export_cmd)

# 3. backup files from cloudinary and S3 bucket.
logger.info('Backing up cloudinary resources')

cloudinary_dir = f"{DOWNLOADS_DIR}/cloudinary"
os.chdir(cloudinary_dir)
remote_cloudinary_dir = input(
    'Enter cloudinary directory name(if any, else whole cloudinary account resources will be downloaded): ') or '/'
os.system(f"cld sync --pull {cloudinary_dir} {remote_cloudinary_dir}")

logger.info('Backing up S3 bucket')
s3_dir = f"{DOWNLOADS_DIR}/s3"
os.chdir(s3_dir)
remote_s3_bucket_url = input(
    'Enter S3 bucket url(if not passed S3 backup will be skipped): ')

if(remote_s3_bucket_url):
    os.system(f"aws s3 sync s3://hardevbucketsdf {s3_dir}")
else:
    logger.warning('Skipping S3 bucket')

logger.info('Generating zip file')
os.chdir(CURRENT_FILE_DIR)
os.system(f"tar -czvf {BACKED_UP_FILE_NAME}.tar.gz backup")

os.system("rm -r backup")
logger.info('Backup complete!')
