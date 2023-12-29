This Python script automates sending messages and attachments on WhatsApp using Selenium and Chrome WebDriver.

Prerequisites
Python installed
Chrome browser installed
Chromedriver (automatically installed by chromedriver_autoinstaller)
Setup
Install required packages: pip install pandas selenium chromedriver_autoinstaller
Adjust the file paths and settings in the script:
log_file_path: Path for the log file.
user_data_dir: Chrome user data directory.
folder_path: Path to the folder containing the Excel workbook.
Save your WhatsApp messages, numbers, and attachments in an Excel file with the sheet name "Sheet1".
Run the script.
Script Flow
Initializes log file and redirects stdout and stderr to the log.
Checks and prints the start time of the bot.
Installs Chrome WebDriver and sets user data directory.
Reads Excel sheet data.
Iterates through each number in the Excel sheet.
Opens WhatsApp web for the given number.
Sends up to five messages and an attachment if specified.
Handles interruptions (e.g., manual stop).
Prints stopping time, runtime, and the number of users messaged.
Closes the log file.
Note
The script uses WebDriverWait to ensure elements are present before interacting with them.
A state file (state.txt) is used to save the position in the Excel sheet, avoiding a restart from scratch.
Caution
Ensure compliance with WhatsApp's terms of service to avoid any violations.
Use the script responsibly and ethically.
Disclaimer: This script is provided as-is, and the user is responsible for its usage and any consequences.






