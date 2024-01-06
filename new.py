import os
import sys
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from chromedriver_autoinstaller import install
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window (it will be hidden)
root = tk.Tk()
root.withdraw()

# Open a file dialog for the user to select the Excel file
file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xlsx;*.xls")])

# Check if the user selected a file
if file_path:
    # Get sheet names from the selected Excel file
    sheet_names = pd.ExcelFile(file_path).sheet_names

    # Automatic selection of the first sheet
    selected_index = 0
    selected_sheet_name = sheet_names[selected_index]

    # Use the selected sheet for reading Excel data
    excel_read = pd.read_excel(file_path, sheet_name=selected_sheet_name)

    # Open the log file in append mode
    log_file_path = "log_file.txt"
    log_file = open(log_file_path, "a")

    # Save the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout and stderr to the log file
    sys.stdout = log_file
    sys.stderr = log_file

    # Check and print the starting time of the bot
    start_time = datetime.now()
    print(f"Bot started at: {start_time}")

    # Install all the desired drivers
    install()

    # Webdriver Collect The Browser Data
    options = webdriver.ChromeOptions()
    user_data_dir = "C:/Users/" + os.getlogin() + "/AppData/Local/Google/Chrome/User Data"
    options.add_argument(f"user-data-dir={user_data_dir}")

    # Create The New Profile When Run For The First Time
    options.add_argument("profile-directory=NewProfile")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    # Web driver page load delay
    wait = WebDriverWait(driver, 40)

    # Excel sheet data
    try:
        numbers = excel_read.iloc[:, 0].tolist()
        message_1 = excel_read.iloc[:, 1].tolist()
        message_2 = excel_read.iloc[:, 2].tolist()
        attachments = excel_read.iloc[:, 3].tolist()

        count = 0

        # Automation looping
        for index, number in enumerate(numbers):
            try:
                print(" ")
                print(" ")
                print(f"Preparing Data For {number}")

                # Opening WhatsApp web in a loop
                driver.get("https://web.whatsapp.com/send?phone=" + str(number) + "&text= ")

                # Type + send message in WhatsApp
                message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
                message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))

                # First and second messages
                for i, message in enumerate([message_1, message_2]):
                    if str(message[index]) != str("nan"):
                        print(f"Sending message {i + 1}: {message[index]}")
                        message_box.send_keys(message[index] + Keys.ENTER)
                        time.sleep(1)

                # Click attachment icon
                if str(attachments[index]) != str("nan"):
                    print(f"Uploading attachment: {attachments[index]}")
                    attachment_path = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
                    attachment = wait.until(EC.presence_of_element_located((By.XPATH, attachment_path)))
                    ActionChains(driver).move_to_element(attachment).click().perform()

                    # Locate the file input element and wait for the attachment to load
                    file_input_path = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
                    file_input = wait.until(EC.presence_of_element_located((By.XPATH, file_input_path)))

                    # Set the file path dynamically from Excel sheet
                    file_path = os.path.abspath(attachments[index])
                    file_input.send_keys(file_path)

                    # Wait for the file to be uploaded
                    time.sleep(5)

                    # Locate and click send icon using a complex XPath
                    send_icon_xpath = '//div[@aria-label="Send" and @role="button"]/span[@data-icon="send"]'
                    send_icon = wait.until(EC.element_to_be_clickable((By.XPATH, send_icon_xpath)))

                    # Click the send icon using ActionChains (imported on the top of the code)
                    ActionChains(driver).move_to_element(send_icon).click().perform()

                    # Printing the attachment status on the log
                    print(f"Attachment with caption sent to {number}")
                    print(" ")
                    print(" ")

            # This code snippet will be executed when the user stops the bot manually
            except KeyboardInterrupt:
                print("Script interrupted by the user.")
                break

            except Exception as e:
                print(f"An error occurred in row {index + 1}: {e}")

            # Increment for Excel rows and move the bot to a new line
            count += 1
            time.sleep(3)

            # Save the position of the bot at a certain cell to avoid the restart of the bot from scratch
            state_file_path = "state.txt"
            with open(state_file_path, "w") as state_file:
                state_file.write(str(count))

    finally:
        # Print the bot stopping time
        end_time = datetime.now()
        print(f"Bot closed at: {end_time}")

        # Calculate the runtime of the bot
        runtime = end_time - start_time
        print(f"Bot ran for: {runtime}")

        # Print the number of messages sent
        print(f"Number Of Users messaged by the bot: {count}")

        # Verify that the bot isn't working
        print("Bot Is Now Stopped")

        # Close the log file.
        log_file.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr

else:
    print("No file selected. Exiting the program.")