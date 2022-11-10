# Backup AIDA2

This python script is used to backup the codebase, along with the current resources.

## Pre-requesties:
1. Install required linux package(s):
    - aws-cli
2. Configure aws-cli:
    - Run `aws configure`
    - follow instructions
3. Install python packages
    - pip install -r requirements.txt
4. Copy `.env.example` to `.env`
    - update .env with appropriate credentials
5. Now you can run the script by `python backup.py` and you will get a tar.gz file containing backup of everything.
    - Also if a backup is either "a month old & wasn't created on first of a month"
        or "a backup which was `x` months old will be deleted"; `x` is integer value configurable in .env