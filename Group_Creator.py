import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError, SessionPasswordNeededError
from datetime import datetime
import sys

async def main():
    print("--- Telegram Group Creator ---")
    print("You will need your API credentials from my.telegram.org\n")
    
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API Hash: ")
    session_name = 'my_group_creator_session'

    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("Connecting and logging in...")
        await client.connect()
        
        if not await client.is_user_authorized():
            print("First-time login. Please enter your phone number.")
            phone = input("Enter phone (e.g., +1234567890): ")
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input("Enter the code you received: "))
            except SessionPasswordNeededError:
                await client.sign_in(password=input("Enter your 2FA password: "))
            print("Login successful!")
        else:
            print("Client already logged in.")

        while True:
            try:
                num_groups = int(input("Enter the number of group chats to create: "))
                if num_groups > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        base_name = input("Enter the base name for the groups (e.g., 'MyGroup'): ")

        dest_entity = None
        while not dest_entity:
            try:
                dest_peer_str = input("Enter the peer ID (username, phone, or ID) to send logs: ")
                dest_entity = await client.get_entity(dest_peer_str)
            except Exception as e:
                print(f"Error: Could not find peer '{dest_peer_str}'. {e}. Please try again.")

        add_members = input("Do you want to add members to these groups? (y/n): ").lower().strip()
        
        member_entities = []
        if add_members == 'y':
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

        print(f"\nStarting process... Will create {num_groups} groups.")
        
        for i in range(1, num_groups + 1):
            group_name = f"{base_name} {i}"
            
            try:
                print(f"Creating group: '{group_name}'...")
                
                creation_result = await client(CreateChannelRequest(
                    title=group_name,
                    about="Group created via script.",
                    megagroup=True
                ))
                
                new_group = creation_result.chats[0]
                new_group_entity = await client.get_entity(new_group.id)
                print(f"  > Group created with ID: {new_group.id}")

                if member_entities:
                    print(f"  > Adding {len(member_entities)} members...")
                    try:
                        await client(InviteToChannelRequest(
                            channel=new_group_entity,
                            users=member_entities
                        ))
                        print("  > Members added successfully.")
                    except UserPrivacyRestrictedError:
                        print("  > Warning: Could not add members. Their privacy settings prevent it.")
                    except Exception as e:
                        print(f"  > Warning: An error occurred while adding members: {e}")

                invite_link_result = await client(ExportChatInviteRequest(peer=new_group_entity))
                invite_link = invite_link_result.link
                print(f"  > Invite link: {invite_link}")

                creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_message = (
                    f"**New Group Created**\n\n"
                    f"**Name:** `{group_name}`\n"
                    f"**Group ID:** `{new_group.id}`\n"
                    f"**Invite Link:** {invite_link}\n"
                    f"**Date:** {creation_date}"
                )

                await client.send_message(dest_entity, log_message, parse_mode='md')
                print(f"  > Log message sent to {getattr(dest_entity, 'username', dest_entity.id)}.")

            except Exception as e:
                print(f"Error creating group '{group_name}': {e}")
                print("Aborting remaining groups.")
                break
            
            if i < num_groups:
                print("Waiting 5 seconds before creating the next group...")
                await asyncio.sleep(5)

        print("\nScript finished.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
