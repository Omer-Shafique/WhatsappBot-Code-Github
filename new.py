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


log_file_path = "log_file.txt"

# Open the log file in append mode (append mode is basically use to open the log file without removing the content)
log_file = open(log_file_path, "a")

# Save the original stdout and stderr
original_stdout = sys.stdout
original_stderr = sys.stderr

# Redirect stdout and stderr to the log file
sys.stdout = log_file
sys.stderr = log_file

#check and print the starting time of the bot
start_time = datetime.now()
print(f"Bot started at: {start_time}")


#install all the desired drivers
install()

# Webdriver Collect The Browser Data
options = webdriver.ChromeOptions()
user_data_dir = "C:/Users/" + os.getlogin() + "/AppData/Local/Google/Chrome/User Data"
options.add_argument(f"user-data-dir={user_data_dir}")

#Create The New Profile When Run For The First Time
options.add_argument("profile-directory=NewProfile")

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# web driver page load delay
wait = WebDriverWait(driver, 40)

# excel sheet data
folder_path = "C:/Users/Developer/Desktop/whatsapp-bot(EXCEL)"
excel_read = pd.read_excel(
    os.getcwd().replace("/", "//") + "//excel-workbook.xlsx", sheet_name="Sheet1"
)
numbers = excel_read["Number"].tolist()
message_1 = excel_read["Message-1"].tolist()
message_2 = excel_read["Message-2"].tolist()
message_3 = excel_read["Message-3"].tolist()
message_4 = excel_read["Message-4"].tolist()
message_5 = excel_read["Message-5"].tolist()
attachments = excel_read["Attachment"].tolist()
count = 0


# automation looping
for number in numbers:
    try:
        print(" ")
        print(" ")
        print(f"Preparing Data For {number}")
        
        #opening whatsapps web in loop
        driver.get("https://web.whatsapp.com/send?phone=" + str(number) + "&text= ")

        # type + send message in WhatsApp
        message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))

        # First to fifth message
        for i, message in enumerate([message_1, message_2, message_3, message_4, message_5]):
            if str(message[count]) != str("nan"):
                print(f"Sending message {i+1}: {message[count]}")
                message_box.send_keys(message[count] + Keys.ENTER)
                time.sleep(1)

        # Click attachment icon
        if str(attachments[count]) != str("nan"):
            print(f"Uploading attachment: {attachments[count]}")
            attachment_path = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
            attachment = wait.until(EC.presence_of_element_located((By.XPATH, attachment_path)))
            ActionChains(driver).move_to_element(attachment).click().perform()

            # Locate the file input element and wait for the attachment to load
            file_input_path = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, file_input_path)))


            # Set the file path dynamically from Excel sheet
            file_path = os.path.abspath(attachments[count])
            file_input.send_keys(file_path)

            # Wait for the file to be uploaded
            time.sleep(5)

            # Locate and click send icon using a complex XPath
            send_icon_xpath = '//div[@aria-label="Send" and @role="button"]/span[@data-icon="send"]'
            send_icon = wait.until(EC.element_to_be_clickable((By.XPATH, send_icon_xpath)))

            # Click the send icon using ActionChains (imported on the top of the code)
            ActionChains(driver).move_to_element(send_icon).click().perform()

            #printing the attachment status on the log
            print(f"Attachment with caption sent to {number}")
            print(" ")
            print(" ")

    #this codesnippet will be execute when user stop the bot manually
    except KeyboardInterrupt:
        print("Script interrupted by the user.")
        break

    # Increment for excel rows and moving the bot to new line
    count += 1
    time.sleep(3)

    #save the position of the bot at certain cell. to avoid the restart of the bot from the scratch
    state_file_path = "state.txt"
    with open(state_file_path, "w") as state_file:
      state_file.write(str(count))


#print the bot stopping time
end_time = datetime.now()
print(f"Bot closed at: {end_time}")

# Calculate the runtime of the bot
runtime = end_time - start_time
print(f"Bot ran for: {runtime}")

# Print the number of messages sent
print(f"Number Of Users messaged by the bot: {count}")

#Verify that bot ain't working
print("Bot Is Now Stopped")


#close the log file.
log_file.close()
sys.stdout = original_stdout
sys.stderr = original_stderr







