import os
from pathlib import Path

# Get the file types, update file types accordingly
folder_names = {
    "Audio": {'aif','cda','mid','midi','mp3','mpa','ogg','wav','wma','m4a', 'aac'},
    "Compressed":{'7z','deb','pkg','rar','rpm', 'tar.gz','z', 'zip'},
    'Code':{'js','jsp','html','ipynb','py','java','css','mhtml','htm','ics','asm', 'circ','csv', 'cms','sql','seb','sh','asc','md','cpp'},
    'Documents':{'ppt','pptx','pdf','xls', 'xlsx','doc','docx','txt', 'tex', 'epub'},
    'Images':{'bmp','gif.ico','jpeg','jpg','png','jfif','svg','tif','tiff','HEIC','JPG','gif','ico','webp'},
    'Softwares':{'apk','bat','bin', 'exe','jar','msi', 'dmg','iso','pyc','stamp'},
    'Videos':{'3gp','avi','flv','h264','mkv','mov','mp4','mpg','mpeg','wmv', 'drp'},
    'Others': {'NONE'}
}

# Extract list of files/folders
downloads_path = r'C:\Users\Asus\Downloads'

onlyfiles = [os.path.join(downloads_path, file) 
             for file in os.listdir(downloads_path) 
             if os.path.isfile(os.path.join(downloads_path, file))]

onlyfolders = [os.path.join(downloads_path, file) 
               for file in os.listdir(downloads_path) 
               if not os.path.isfile(os.path.join(downloads_path, file))]

extension_filetype_map = {extension: fileType 
                          for fileType, extensions in folder_names.items() 
                          for extension in extensions }

# Create folders
folder_paths = [os.path.join(downloads_path, folder_name) 
                for folder_name in folder_names.keys()]
folders_directory = os.path.join(downloads_path, 'Folders')

#For Re-Cluttering Unknown files
# others_directory = os.path.join(downloads_path, 'Others')


# Make folders if they do not exist
[os.mkdir(folderPath) 
 for folderPath in folder_paths if not os.path.exists(folderPath)]
if not os.path.exists(folders_directory):
    os.mkdir(folders_directory)

#For Re-Cluttering Unknown files
# if not os.path.exists(others_directory):
#     os.mkdir(others_directory)


# Move files to categorized folders
def new_path(old_path):
    extension = str(old_path).split('.')[-1]
    amplified_folder = extension_filetype_map.get(extension, 'Others')
    final_path = os.path.join(downloads_path, amplified_folder, str(old_path).split('\\')[-1])
    return final_path
[Path(eachfile).rename(new_path(eachfile)) for eachfile in onlyfiles]


#For Re-Cluttering Unknown files
# Recheck files in 'Others' folder and move them to the correct folders
# others_files = [os.path.join(others_directory, file) 
#                 for file in os.listdir(others_directory) 
#                 if os.path.isfile(os.path.join(others_directory, file))]

# [Path(eachfile).rename(new_path(eachfile)) for eachfile in others_files]


# Move existing folders to 'Folders' directory
for onlyfolder in onlyfolders:
    folder_name = str(onlyfolder).split('\\')[-1]
    destination_folder = os.path.join(folders_directory, folder_name)
    
    # Skip if the folder is 'Folders' directory itself or in predefined folder names
    if onlyfolder == folders_directory or folder_name in folder_names.keys():
        continue
    
    if not os.path.exists(destination_folder):
        try:
            Path(onlyfolder).rename(destination_folder)
        except PermissionError as e:
            print(f"PermissionError: {e}")
    else:
        # If the destination folder already exists, merge the contents
        try:
            for sub_file in os.listdir(onlyfolder):
                Path(os.path.join(onlyfolder, sub_file)).rename(os.path.join(destination_folder, sub_file))
            os.rmdir(onlyfolder)
        except PermissionError as e:
            print(f"PermissionError: {e}")
