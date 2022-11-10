# Backup AIDA2

This python script is used to backup the codebase, along with the current resources.

## Pre-requesties:

1. Install required linux packages:
    - cloudinary-cli
    - aws-cli
2. Configure aws-cli:
    - Run `aws configure`
    - follow instructions
3. Configure cloudinary-cli:
    - Run `export CLOUDINARY_URL={this can be found in cloudinary dashboard}`
    - Check if it is configured by running `cld config`
4. Install python packages
    - pip install -r requirements.txt
5. Copy `.env.example` to `.env`
    - update with database credentials
5. Now you can run the script by `python backup.py` and you will get a tar.gz file containing backup of everything.