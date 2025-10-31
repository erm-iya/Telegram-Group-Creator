# **Telegram Group Creator & Messenger**

Hello\! This is a handy Python script I built to take the boring, repetitive work out of making new Telegram groups.

## **So, what's it do?**

Instead of you having to manually create groups, add people, and change settings one by one, this script does it all for you.

Here's the rundown:

1. **Logs you in:** It'll securely log into your Telegram account.  
2. **Creates Groups:** You tell it "I want 5 groups named 'My Project'," and it'll instantly create "My Project 1", "My Project 2", and so on.  
3. **Sets History:** It automatically makes the group's chat history visible for any new members who join.  
4. **Adds People:** If you want, you can give it a list of usernames, and it'll add all of them to every group it makes.  
5. **Keeps a Log:** It sends a neat little message to you (or any chat you pick) with the new group's name, ID, and invite link.  
6. **Warms them up:** To make the groups look active, it'll post 10 random messages (from a list inside the script) into each new group.

You can also set custom delays (like "wait 5 seconds between making groups") to make sure you don't get flagged by Telegram for moving too fast.

## **⚠️ A Quick (but Important) Security Warning**

To work its magic, this script needs your **API ID** and **API HASH**.

Think of these like a master key to your entire Telegram account. **Never, ever share them with anyone.**

The script will also create a my\_account\_session.session file. This is what keeps you logged in so you don't have to enter a code every time. **Don't share this file either\!** It's just as sensitive.

## **How to Get Started**

You'll need to have Python 3.7 (or newer) on your computer.

### **1\. Get Your "API Keys" from Telegram**

This is a one-time thing.

* Log into Telegram's website: [my.telegram.org](https://my.telegram.org)  
* Click on **"API development tools"**.  
* Fill out the short form (you can put anything for the "App" name, like "My Bot").  
* Telegram will instantly show you your api\_id and api\_hash. Copy these and keep them somewhere safe.

### **2\. Set Up Your Project**

* Make a new folder somewhere on your computer (e.g., telegram\_script).  
* Save the telegram\_group\_creator.py file inside this new folder.

### **3\. Install the "Telethon" Library**

This script depends on a library called "Telethon" to talk to Telegram.

* In that same folder, create a new, empty text file.  
* Name it requirements.txt.  
* Open it and paste this one word into it:  
  telethon

* Now, open your terminal (or Command Prompt) and "navigate" to your new folder:  
  \# Example:  
  cd C:\\Users\\YourName\\Desktop\\telegram\_script

* Once you're "in" the folder, run this command to install the library:  
  pip install \-r requirements.txt

## **Let's Run It\!**

You're all set\!

1. Make sure you're still in your project folder in your terminal.  
2. Run the script by typing:  
   python telegram\_group\_creator.py

The script will start and ask you a few questions. Just follow the prompts\!

* **API ID/HASH:** Paste in the keys you got from Telegram. (Your HASH will be hidden as you type, like a password).  
* **First-Time Login:** The very first time, it'll ask for your phone number, then a login code Telegram sends you (and your 2FA password if you have one).  
* **Groups:** It'll ask *how many* groups to make and what "base name" to use.  
* **Logs:** It'll ask *where* to send the log message (just put your own Telegram username, like @my\_username).  
* **Members:** It'll ask if you want to add people (y/n). If y, just paste in their usernames separated by commas (e.g., @my\_friend, @another\_person).  
* **Delays:** You can just enter small numbers (like 5 or 10\) for the delays.

That's it\! The script will take over and do all the work.
