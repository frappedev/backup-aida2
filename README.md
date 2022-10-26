# Backup AIDA2

This python script is used to backup the codebase, along with the current resources.

## Pre-requesties:

1. Install required packages:
    - gitpython
    - python-dotenv
    - cloudinary-cli
    - aws-cli
2. Configure Aws-cli:
    - Run `aws configure`
    - follow instructions
3. Configure Cloudinary-cli:
    - Run `export CLOUDINARY_URL={this can be found in cloudinary dashboard}`
    - Check if it is configured by running `cld config`
4. Copy .env.example to .env
    - update with database credentials
5. Now you can run the script by `python backup.py` and you will get a tar.gz file containing backup of everything.
