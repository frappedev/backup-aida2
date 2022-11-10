# Backup AIDA2

This python script is used to backup the codebase, along with the current resources.

## Pre-requesties:
1. Install required linux package(s):
    - **mysql client**; For MacOS: https://formulae.brew.sh/formula/mysql-client
    - **aws cli**
        - For All OS: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
        - For MacOS (easiest): https://formulae.brew.sh/formula/awscli
2. Configure aws-cli:
    - Run `aws configure`
    - That will ask following info, so keep it ready.
        - **AWS Access Key ID** & **AWS Secret Access Key** (which you can find these in your aws console under security credentials)
        - **Default region name** (in our case its `eu-north-1`)
3. Install python packages
    - Run `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`
    - Run  `cp .env.example .env`
    - update .env with appropriate credentials
5. Now you can take backups 
    - Run `python backup.py` and you will get a tar.gz file containing backup of everything.
    - Also if a backup is either "a month old & wasn't created on first of a month"
        or "a backup which was `x` months old" will be deleted; `x` is integer value configurable in .env