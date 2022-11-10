from datetime import datetime
import os
from dateutil.relativedelta import relativedelta

class BackupFile():
    filepath = None
    directory = None
    filename = None
    file_created_at = None
    months_to_keep = None
    def __init__(self, directory, filename, months_to_keep=None):
        self.directory = directory
        self.filename = filename
        self.filepath = self.directory + '/' + self.filename
        self.file_created_at = datetime.fromtimestamp(os.path.getmtime(self.filepath))
        if months_to_keep:
            self.months_to_keep = int(months_to_keep)    

    def remove(self):
        if self._pre_remove_check():
            print(f"Deleting {self.filepath}")
            os.system(f'rm {self.filepath}')

    def is_older_than_month(self):
        one_month_ago = datetime.today() - relativedelta(months=1)
        return self.file_created_at < one_month_ago
    
    def is_not_created_on_first_day_of_month(self):
        return self.file_created_at.date() != self.file_created_at.replace(day=1).date()
    
    def has_passed_months_to_keep(self):
        if self.months_to_keep is None or self.months_to_keep == 0:
            return False
        
        date_months_ago = datetime.today() - relativedelta(months=self.months_to_keep)
        return self.file_created_at < date_months_ago

    def _pre_remove_check(self):
        # Safety Check: To make sure the file being removed is a aida2 backup file and not any other file
        if self.filename[:12] == 'aida2_backup' and self.filename[-6:] == 'tar.gz':
            return True
        return False