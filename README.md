# **Telegram Group Creator**

This Python script allows you to automatically create multiple Telegram supergroups (private) in bulk. It will prompt you for all necessary information, including how many groups to create, what to name them, and who to add.

For each group successfully created, it generates an invite link and sends a log message to a Telegram chat of your choice.

## **Requirements**

* Python 3.7+  
* The telethon library

## **Installation**

1. Make sure you have Python installed.  
2. Install the required library (telethon) using pip:  
   pip install telethon

## **How to Use**

This script is fully interactive. You do **not** need to edit the .py file.

### **Step 1: Get API Credentials**

1. Log in to your Telegram account at [my.telegram.org](https://my.telegram.org).  
2. Go to "API development tools" and create a new application.  
3. You will be given your api\_id and api\_hash. Keep these ready.

### **Step 2: Run the Script**

1. Open your terminal or command prompt.  
2. Navigate to the directory where group\_creator.py is saved.  
3. Run the script:  
   python group\_creator.py

4. The script will guide you through the following prompts:  
   1. **Enter your API ID:** (Paste the value from my.telegram.org)  
   2. **Enter your API Hash:** (Paste the value from my.telegram.org)  
   3. **Enter phone (e.g., \+1234567890):** (Only if it's your first time logging in)  
   4. **Enter the code you received:** (Check your Telegram app for the login code)  
   5. **Enter your 2FA password:** (If you have two-factor authentication enabled)  
   6. **Enter the number of group chats to create:** (e.g., 5\)  
   7. **Enter the base name for the groups:** (e.g., My Test Group. The script will create My Test Group 1, My Test Group 2, etc.)  
   8. **Enter the peer ID (username, phone, or ID) to send logs:** (This is where the script will send its reports. You can use your own username, e.g., @myusername, or the username of a bot or channel).  
   9. **Do you want to add members...? (y/n):**  
   10. **Enter member peer IDs... separated by commas:** (If you typed y. e.g., @username1, @username2, \+1234567890)  
5. The script will then start the creation process, pausing for 5 seconds between each group to avoid API limits.  
6. Check the "log" chat you specified. You will see messages appearing with the details for each new group.
