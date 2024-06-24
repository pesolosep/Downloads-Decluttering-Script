

## Download Sorter Script

This script is designed to organize files and folders in your "Downloads" directory by categorizing them into specific subdirectories based on their file types.

### Features

- Categorizes files based on their extensions.
- Creates categorized folders if they do not already exist.
- Moves files to their respective categorized folders.
- Moves existing folders to a designated "Folders" directory.
- Ensures folders are not moved into themselves or other categorized folders.

### How It Works

1. **Define File Types**:
   The `folder_names` dictionary maps folder names to sets of file extensions. This categorizes various file types by their extensions.

   ```python
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
   ```

2. **Extract List of Files and Folders**:
   The script retrieves all files and folders in the "Downloads" directory.

   ```python
   downloads_path = r'C:\Users\Asus\Downloads'
   
   onlyfiles = [os.path.join(downloads_path, file) 
                for file in os.listdir(downloads_path) 
                if os.path.isfile(os.path.join(downloads_path, file))]

   onlyfolders = [os.path.join(downloads_path, file) 
                  for file in os.listdir(downloads_path) 
                  if not os.path.isfile(os.path.join(downloads_path, file))]
   ```

3. **Map File Extensions to Folder Names**:
   The `extension_filetype_map` dictionary is created to map each file extension to its corresponding folder name based on the `folder_names` dictionary.

   ```python
   extension_filetype_map = {extension: fileType 
                             for fileType, extensions in folder_names.items() 
                             for extension in extensions }
   ```

4. **Create Destination Folders**:
   The script generates the full paths for each category folder and creates them if they do not already exist.

   ```python
   folder_paths = [os.path.join(downloads_path, folder_name) 
                   for folder_name in folder_names.keys()]
   folders_directory = os.path.join(downloads_path, 'Folders')

   [os.mkdir(folderPath) 
    for folderPath in folder_paths if not os.path.exists(folderPath)]
   if not os.path.exists(folders_directory):
       os.mkdir(folders_directory)
   ```

5. **Move Files to Categorized Folders**:
   The `new_path` function determines the new path for each file based on its extension. It constructs the new path within the appropriate folder in the "Downloads" directory and moves the file to its new path.

   ```python
   def new_path(old_path):
       extension = str(old_path).split('.')[-1]
       amplified_folder = extension_filetype_map.get(extension, 'Others')
       final_path = os.path.join(downloads_path, amplified_folder, str(old_path).split('\\')[-1])
       return final_path

   [Path(eachfile).rename(new_path(eachfile)) for eachfile in onlyfiles]
   ```

6. **Move Existing Folders to 'Folders' Directory**:
   The script moves each existing folder in the "Downloads" directory to the "Folders" directory, except for predefined folders. If a destination folder already exists, it merges the contents.

   ```python
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
   ```


 ### **To automate the execution of your script using Task Scheduler and run it weekly, follow these steps:**

### Step-by-Step Guide

1. **Create the Batch Script**:
   Ensure your batch script (`script.bat`) contains the following lines and is saved in the specified folder:
   ```batch
   "C:\Users\Asus\Documents\Vacation Projects\Download Sorter\Download Sorter.py"
   pause
   ```

2. **Open Task Scheduler**:
   - Press `Win + R` to open the Run dialog box.
   - Type `taskschd.msc` and press Enter. This opens the Task Scheduler.

3. **Create a New Task**:
   - In the Task Scheduler window, click on `Create Task` in the Actions pane on the right.

4. **General Settings**:
   - In the `General` tab, provide a name for your task (e.g., "Download Sorter Weekly").
   - Optionally, add a description.
   - Choose `Run whether user is logged on or not` if you want the task to run even when you're not logged in.
   - Check `Run with highest privileges` to ensure the task runs with administrator permissions.

5. **Trigger Settings**:
   - Go to the `Triggers` tab.
   - Click `New` to create a new trigger.
   - In the `New Trigger` window, select `Weekly`.
   - Choose the day(s) of the week you want the task to run.
   - Set the start time for the task.
   - Click `OK` to save the trigger.

6. **Action Settings**:
   - Go to the `Actions` tab.
   - Click `New` to create a new action.
   - In the `New Action` window, set the action to `Start a program`.
   - In the `Program/script` field, browse to and select your batch script (`script.bat`).
   - Click `OK` to save the action.

7. **Conditions and Settings**:
   - Optionally, you can configure additional conditions in the `Conditions` tab and settings in the `Settings` tab according to your preferences.
   - For instance, you might want the task to run only if the computer is idle or to stop the task if it runs longer than a specified duration.

8. **Save and Test the Task**:
   - Click `OK` to save the task.
   - You may be prompted to enter your user password to confirm.
   - Once the task is created, you can manually run it by right-clicking on the task in the Task Scheduler library and selecting `Run` to ensure it works as expected.

### Summary

1. **Batch Script**: Ensure your `script.bat` file contains the correct commands.
2. **Task Scheduler**: Use Task Scheduler to create a new task that runs weekly, pointing to your `script.bat` file.


### Notes

- **Re-Cluttering Unknown Files**:
  The commented-out sections of the code indicate additional functionality for rechecking and re-categorizing files in the "Others" directory. If you want to enable this functionality, uncomment the relevant sections.

  ```python
  # For Re-Cluttering Unknown files
  # others_directory = os.path.join(downloads_path, 'Others')
  # if not os.path.exists(others_directory):
  #     os.mkdir(others_directory)

  # Recheck files in 'Others' folder and move them to the correct folders
  # others_files = [os.path.join(others_directory, file) 
  #                 for file in os.listdir(others_directory) 
  #                 if os.path.isfile(os.path.join(others_directory, file))]

  # [Path(eachfile).rename(new_path(eachfile)) for eachfile in others_files]
  ```

This script helps maintain an organized "Downloads" directory by ensuring all files and folders are sorted into appropriate categories based on their types.



- **Ensure the path to the Python executable is correct**.
- **Make sure that Task Scheduler has the necessary permissions to run the task**.
- **If the script requires administrator privileges, make sure to check the `Run with highest privileges` option**.

This setup will automate the execution of your Python script weekly, keeping your Downloads folder organized without manual intervention.