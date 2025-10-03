'''
Author: Mark Sikder
Date: 2025-08-26
'''

import pandas as pd

class Anomaly:
    def __init__(self):
        pass

    # read the files and concat them into one
    def read_files(self, files, sheet):
        all_files = [pd.read_excel(file, sheet_name=sheet) for file in files]
        all_combined_files = pd.concat(all_files, ignore_index=True)
        return all_combined_files

    # trim whitespaces from the columns
    def trim(self, file, col):
        file[col] = file[col].str.strip()
        return file
    
    # MAIN FUNCTION
    def find_anomalies(self, file1, file2, colf1, colf2):
        try:
            # trim the files
            tfile1 = self.trim(file1, colf1)
            tfile2 = self.trim(file2, colf2)
            # missing in File 1 Data
            missing_in_File1 = tfile1[~tfile1[colf1].isin(tfile2[colf2])]
            # missing in File 2  Data
            missing_in_File2 = tfile2[~tfile2[colf2].isin(tfile1[colf1])]
            

            return missing_in_File1, missing_in_File2
        except Exception as e:
            print("Failed to find anomalies.")
