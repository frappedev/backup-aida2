from dotenv import load_dotenv
from datetime import datetime
import logging
import os
import sys
import requests
from BackupFile import BackupFile

# START: Create Logger
logger = logging.getLogger("aida_backup_log")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename='backups.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
log_handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=log_handlers
)
# END: Create Logger

logger.info('AIDA Backup -> Start')

# START: Check & Load ENV
if not os.path.exists('.env'):
    logger.error(".env file not found please create one before running backup script")
    sys.exit(1)

load_dotenv()
# END: Check & Load ENV

# START: Vars used in script
WEBHOOK_URL_BACKUP_START = os.environ.get('WEBHOOK_URL_BACKUP_START', None)
WEBHOOK_URL_BACKUP_FINISH = os.environ.get('WEBHOOK_URL_BACKUP_FINISH', None)

GITHUB_REPO = os.environ.get('GITHUB_REPO', None)
CLOUDINARY_FOLDER = os.environ.get('CLOUDINARY_FOLDER', None)
S3_BUCKET_URL = os.environ.get('S3_BUCKET_URL', None)
DB_HOST = os.environ.get('DB_HOST','localhost')
DB_USER = os.environ.get('DB_USER','root')
DB_PASSWORD = os.environ.get('DB_PASSWORD','password')
DB_DATABASE = os.environ.get('DB_DATABASE', 'test')
MONTHS_TO_KEEP = os.environ.get('MONTHS_TO_KEEP', 12)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_BACKUP_DIR = f"{CURRENT_DIR}/tempbackup"
CODEBASE_DIR = f"{TEMP_BACKUP_DIR}/codebase"
DOWNLOADS_DIR = f"{TEMP_BACKUP_DIR}/downloads"
BACKUPS_DIR = os.environ.get('BACKUPS_DIR', f"{CURRENT_DIR}/backups")
# END: Vars used in script

## Check if Temp Dir exists; if yes delete
if os.path.exists(TEMP_BACKUP_DIR):
    logger.info('Deleting temp backup folder')
    os.system(f"rm -r {TEMP_BACKUP_DIR}")


## Create a bunch of directories
os.makedirs(TEMP_BACKUP_DIR, exist_ok=True)
os.makedirs(BACKUPS_DIR, exist_ok=True)
os.makedirs(CODEBASE_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(f"{DOWNLOADS_DIR}/cloudinary", exist_ok=True)
os.makedirs(f"{DOWNLOADS_DIR}/s3", exist_ok=True)


## Send GET Request to Webhook; Backup Start
if WEBHOOK_URL_BACKUP_START:
    requests.get(WEBHOOK_URL_BACKUP_START)

# 1. Clone repo (move app and api folder into tempbackup/codebase)

if not GITHUB_REPO:
    logger.warning('Github -> Repo URL not provided. Skipping...')
else:
    logger.info('Github -> Start Clone')
    github_command = f'git clone {GITHUB_REPO} {CODEBASE_DIR}'
    logger.info('Github -> ' + github_command)
    os.system(github_command)
    logger.info('Github -> Finish Clone')

# 2. Export sql database and move file into tempbackup/
logger.info('DB -> Start Export')
export_cmd = f"mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_DATABASE} > {TEMP_BACKUP_DIR}/database.sql"
print(os.system(export_cmd))
logger.info('DB -> Finish Export')

# 3. backup files from cloudinary
if not CLOUDINARY_FOLDER:
    logger.warning('Cloudinary -> Cloudinary URL not provided. Skipping...')
else:
    logger.info('Cloudinary -> Start Sync')
    local_cloudinary_dir = f"{DOWNLOADS_DIR}/cloudinary"
    os.chdir(local_cloudinary_dir)
    cloudinary_command = f"cld sync --pull {local_cloudinary_dir} {CLOUDINARY_FOLDER}"
    logger.info('Cloudinary -> ' + cloudinary_command)
    os.system(cloudinary_command)
    logger.info('Cloudinary -> Finish Sync')

# 3. backup files from S3
if not S3_BUCKET_URL:
    logger.warning('S3 -> S3 Bucket URL not provided. Skipping...')
else:
    logger.info('S3 -> Start Sync')
    local_s3_dir = f"{DOWNLOADS_DIR}/s3"
    os.chdir(local_s3_dir)
    s3_command = f"aws s3 sync {S3_BUCKET_URL} {local_s3_dir}"
    logger.info('S3 -> ' + s3_command)
    os.system(s3_command)
    logger.info('S3 -> Finish Sync')


logger.info('Gzip -> Start')
os.chdir(CURRENT_DIR)
gzip_command = f"tar -czf {BACKUPS_DIR}/aida2_backup_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.tar.gz ./tempbackup"
logger.info('Gzip -> ' + gzip_command)
os.system(gzip_command)
logger.info('Gzip -> Finish')

remove_temp_command = f"rm -rf {TEMP_BACKUP_DIR}"
logger.info('Removing Temp Directory -> ' + remove_temp_command)
os.system(remove_temp_command)

logger.info('AIDA Backup -> Finish')

## Send GET Request to Webhook; Backup Finish
if WEBHOOK_URL_BACKUP_FINISH:
    requests.get(WEBHOOK_URL_BACKUP_FINISH)

## Deleting Extra Backups
for file in os.listdir(BACKUPS_DIR):
    backupfile = BackupFile(directory = BACKUPS_DIR, filename = file)
    if backupfile.has_passed_months_to_keep() or (backupfile.is_older_than_month() and backupfile.is_not_created_on_first_day_of_month()):
        backupfile.remove()
