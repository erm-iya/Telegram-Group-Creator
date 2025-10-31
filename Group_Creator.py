#!/usr/bin/env python3
"""
Telegram Group Creator & Messenger
Automates creating groups, adding members, and sending messages.
"""
import asyncio, random, sys
from getpass import getpass
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError, SessionPasswordNeededError

# --- CONFIGURATION ---
SESSION_NAME = 'my_account_session'
RANDOM_WORDS = [
    "سیب", "آلبالو", "cherry", "date", "تاریخ",
    "انگوز", "grape", "honeydew", "kiwi", "lemon",
    "mango", "پرتقال", "orange", "انار", "quince",
    "tangerine", "نارنگی", "tangerine", "توت فرنگی", "watermelon"
]
# --- END CONFIGURATION ---

async def get_delay(prompt):
    """Helper function to get a valid delay time from the user."""
    while True:
        try:
            delay = float(input(prompt))
            if delay >= 0: return delay
            print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 2.5).")

async def main():
    print("--- Telegram Group Creator & Messenger ---")
    
    # --- Login flow (Merged) ---
    try:
        api_id = int(input("Enter your API ID: ").strip())
    except ValueError:
        print("Invalid input. API ID must be a number.", file=sys.stderr)
        return
    api_hash = getpass("Enter your API HASH (will not be visible): ").strip()
    if not api_id or not api_hash:
        print("API ID and API HASH are required. Exiting.", file=sys.stderr)
        return

    async with TelegramClient(SESSION_NAME, api_id, api_hash) as client:
        print("Connecting...")
        # Use robust login flow for first-time use
        try:
            if not await client.is_user_authorized():
                print("First-time login. Enter phone (e.g., +1234567890).")
                phone = input("Enter phone: ")
                await client.send_code_request(phone)
                try:
                    await client.sign_in(phone, input("Enter the code you received: "))
                except SessionPasswordNeededError:
                    await client.sign_in(password=getpass("Enter your 2FA password: "))
            print("Login successful.")
        except Exception as e:
            print(f"Error during login: {e}", file=sys.stderr)
            return
        
        # --- Gather Inputs ---
        while True:
            try:
                num_groups = int(input("Number of groups to create: "))
                if num_groups > 0: break
                print("Please enter a positive number.")
            except ValueError: print("Invalid input. Please enter a number.")
        
        base_name = input("Base name for groups (e.g., 'MyGroup'): ")

        dest_entity = None
        while not dest_entity:
            try:
                peer_str = input("Enter peer ID to send logs to (username, phone, or ID): ")
                dest_entity = await client.get_entity(peer_str)
            except Exception as e:
                print(f"Error: Could not find peer '{peer_str}'. {e}. Try again.")

        member_entities = []
        if input("Add members to these groups? (y/n): ").lower().strip() == 'y':
            member_list_str = input("Enter member peer IDs (usernames, phones, or IDs), separated by commas: ")
            member_ids = [m.strip() for m in member_list_str.split(',')]
            print("Resolving member IDs...")
            for mid in member_ids:
                if not mid: continue
                try:
                    entity = await client.get_entity(mid)
                    member_entities.append(entity)
                    print(f"  > Found user: {getattr(entity, 'username', entity.id)}")
                except Exception as e:
                    print(f"  > Warning: Could not find user '{mid}'. Skipping. Error: {e}")

        print("\n--- Configure Delays (in seconds) ---")
        delay_between_groups = await get_delay("Delay between creating each group: ")
        delay_after_adding = await get_delay("Delay after adding members: ")
        delay_between_messages = await get_delay("Delay between sending each random message: ")

        print(f"\nStarting process... Will create {num_groups} groups.")
        created_groups = []

        # --- LOOP 1: Create Groups ---
        for i in range(1, num_groups + 1):
            group_name = f"{base_name} {i}"
            try:
                print(f"Creating group: '{group_name}'...")
                creation_result = await client(CreateChannelRequest(
                    title=group_name, about="Group created via script.", megagroup=True
                ))
                new_group_entity = await client.get_entity(creation_result.chats[0].id)
                created_groups.append(new_group_entity)
                print(f"  > Group created with ID: {new_group_entity.id}")

                # Make history visible
                try:
                    print("  > Making history visible...")
                    await client(EditChatDefaultBannedRightsRequest(
                        peer=new_group_entity,
                        banned_rights=ChatBannedRights(until_date=None, view_messages=False)
                    ))
                except Exception as e:
                    print(f"  > Warning: Could not set history visibility: {e}")
                
                # Add members
                if member_entities:
                    print(f"  > Adding {len(member_entities)} members...")
                    try:
                        await client(InviteToChannelRequest(channel=new_group_entity, users=member_entities))
                        print("  > Members added.")
                    except UserPrivacyRestrictedError:
                        print("  > Warning: Could not add members due to privacy settings.")
                    except Exception as e:
                        print(f"  > Warning: Error adding members: {e}")
                    
                    print(f"  > Waiting {delay_after_adding} sec...")
                    await asyncio.sleep(delay_after_adding)

                invite_link = (await client(ExportChatInviteRequest(peer=new_group_entity))).link
                print(f"  > Invite link: {invite_link}")

                log_message = (
                    f"**New Group Created**\n"
                    f"**Name:** `{group_name}`\n"
                    f"**Group ID:** `{new_group_entity.id}`\n"
                    f"**Invite Link:** {invite_link}\n"
                    f"**Date:** {datetime.now().strftime('%Y-m-%d %H:%M:%S')}"
                )
                await client.send_message(dest_entity, log_message, parse_mode='md')
                print(f"  > Log message sent to {getattr(dest_entity, 'username', dest_entity.id)}.")
            
            except Exception as e:
                print(f"Error creating group '{group_name}': {e}", file=sys.stderr)
                break
            
            if i < num_groups:
                print(f"Waiting {delay_between_groups} sec...")
                await asyncio.sleep(delay_between_groups)

        print("\n--- Group creation finished. ---")
        
        # --- LOOP 2: Send Messages ---
        if not created_groups:
            print("No groups were created, skipping message sending.")
        else:
            print("Starting to send 10 random messages to all groups...")
            for group_entity in created_groups:
                # Need to get entity again to refresh title, just in case
                group_info = await client.get_entity(group_entity)
                print(f"\nSending to group: '{group_info.title}'")
                try:
                    words_to_send = random.choices(RANDOM_WORDS, k=10)
                    for j, word in enumerate(words_to_send):
                        print(f"  > Sending word {j+1}/10: '{word}'")
                        await client.send_message(group_info, word)
                        if j < 9: await asyncio.sleep(delay_between_messages)
                except Exception as e:
                    print(f"  > Warning: Could not send messages to '{group_info.title}': {e}")

        print("\nScript finished.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
