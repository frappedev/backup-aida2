import os
from BackupFile import BackupFile

os.system('touch -t 202211081005 backups/aida2_backup_current.tar.gz')
os.system('touch -t 202211111240 backups/aida2_backup_almost_month_ago.tar.gz')
os.system('touch -t 202210110005 backups/aida2_backup_month_ago.tar.gz')
os.system('touch -t 202210100900 backups/aida2_backup_month_ago_1.tar.gz')
os.system('touch -t 202210090900 backups/aida2_backup_month_ago_2.tar.gz')
os.system('touch -t 202209091000 backups/aida2_backup_month_ago_3.tar.gz')
os.system('touch -t 202209091000 backups/aida2_backup_month_ago_4.tar.gz')
os.system('touch -t 202211010090 backups/aida2_backup_first_day.tar.gz')
os.system('touch -t 202210011200 backups/aida2_backup_first_day_1.tar.gz')
os.system('touch -t 202209011800 backups/aida2_backup_first_day_2.tar.gz')
os.system('touch -t 202111011800 backups/aida2_backup_first_day_last_year.tar.gz')

backups = os.listdir('backups')
backups.sort()

for file in backups:
    backupfile = BackupFile(directory= 'backups', filename = file, months_to_keep=8)
    print(f"{file} is months_to_keep_passed: {backupfile.has_passed_months_to_keep()} | older_than_month: {backupfile.is_older_than_month()} | first_day_of_month: {not backupfile.is_not_created_on_first_day_of_month()}")
    if backupfile.has_passed_months_to_keep() or (backupfile.is_older_than_month() and backupfile.is_not_created_on_first_day_of_month()):
        backupfile.remove()