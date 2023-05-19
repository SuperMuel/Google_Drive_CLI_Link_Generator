# Google Drive CLI Link Generator

This program provides a quick and efficient way to **generate sharable links for files and folders on Google Drive, directly from the command line**. It's designed to **work with any software that mirrors Google Drive files on your machine**, such as [Insync](https://www.insynchq.com/).

 While Insync provides a GUI to share files on Google Drive, it does not provide a way to get a sharable link directly from the command line. This program bridges that gap.

# Usage

To generate a shareable link for a file in your Google Drive, use the following command : 
```bash
gd_link_generator.py <file_path> [OPTIONS]
```
- `<file_path>`: The path to the file or directory in your Google Drive that you want to share.

Options:

- `-a`, `--anyone` - If this option is passed, **anyone with the link can access the file**.

Example : 
```bash
gd_link_generator.py ~/path_to_google_drive/documents/school/notes.pdf -a
```


# Setup

Clone the repository

```bash
git clone https://github.com/SuperMuel/Google_Drive_CLI_Link_Generator.git
cd Google_Drive_CLI_Link_Generator
```

Install the required packages from `requirements.txt` using pip:

```bash
pip install -r requirements.txt
```
## Google Cloud Console Configuration:

- Go to the [Google Cloud Console](https://console.cloud.google.com).

- Create a new project.

- Enable the Google Drive API for your project.

- Create credentials for the Google Drive API. Choose **"Desktop app"** for the type of app.

- **Download the credentials JSON** file

- Place the downloaded file in the project's root directory alongside config.json.

- Rename it **credentials.json**

## Local JSON Configuration:

Edit the JSON file named **config.json** and replace the values with your actual local Google Drive folder path and your email associated with your google drive account.

```json
{
    "gdrive_path": "/path/to/your/local/google/drive/folder",
    "email": "your_email@gmail.com"
}
```

## Adding the Script to the PATH
To make the gd_link_generator.py script accessible from anywhere on your computer, you can add it to your system's PATH variable. Follow the steps below based on your operating system:


### Unix/Linux/Mac

1. Make the script executable:

Inside the `Google_Drive_CLI_Link_Generator` folder, run :
```bash
chmod +x ./bin/gd_link_generator.py
```
2. Open your `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc` file (depending on your shell) using a text editor.

3. Add the following line at the end of the file:

```bash
export PATH=$PATH:~/bin
```
4. Save and close the file.

5. Refresh the terminal by either opening a new terminal window or running:

```
source ~/.bashrc
```
(Make sure to replace `~/.bashrc` with the actual file you opened in step 2)

### Windows

Follow [this stackoverflow answer](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho) to add the `Google_Drive_CLI_Link_Generator/bin` folder of this project to your PATH.



# Development 

This program, in its current state, may have to navigate through a large number of files if the Google Drive directory is large. This can be a performance concern. Future development can consider implementing a caching mechanism to store a mapping of file paths and their respective Google Drive IDs. This could potentially save a significant amount of time in generating shareable links for frequently accessed files.

Another point of consideration is handling files or folders with duplicate names within the Google Drive. Currently, the program may not correctly identify the desired file if there are multiple files with the same name. Future development could address this by enhancing the file lookup mechanism to account for duplicate names.



