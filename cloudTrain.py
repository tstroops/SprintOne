import os
from enum import Enum
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv("environ.env")  # Load variables from .env file
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

TABLE_NAME= "Inventory: weapon"
INPUT_ERROR = "We didn't get that! Please pick a valid option!"

def DisplayMenu():
    print("Do you:")
    print("1. Search for a weapon")
    print("2. Add a new weapon")
    print("3. Update a weapon")
    print("4. Delete a weapon")
    print("5. Get aggregate data")
    print("6. Quit.")

def Main():
    done = False
    print("Welcome to Weapon Manager")
    while not done:
        DisplayMenu()
        user_in=input()
        if user_in == "1":
            search = input("Enter a weapon to search for: ").lower()
            response = (
                supabase.table(TABLE_NAME)
                .select("*")
                .ilike("name", f"%{search}%")
                .execute()
            )
            if len(response.data) > 0: print(response.data)
            else: print(f"We couldn't find '{search}'.")

        elif user_in=="2":

            insert = input("Enter the weapon name: ").lower()
            dmg = int(input("Enter the weapon's damage: "))
            price = int(input("Enter the weapon's value: "))

            check = (
                supabase.table(TABLE_NAME)
                .select("*")
                .eq("name", insert)
                .execute()
                )
            
            if len(check.data) > 0: print("An item already has that name. Did you mean to update an item?")
            else:
                response = (supabase.table(TABLE_NAME).insert({'name': insert, 'damage': dmg, 'value': price}).execute())
                print(f"Creation of '{insert}' sucessful!")

        elif user_in =="3":
            item = input("What is the name of the item you want to update: ").lower()
            stat_type = input("Update NAME, DAMAGE, PRICE, or ALL: ").lower()

            if stat_type=="name":
                new_stat = input(f"Enter the item's new {stat_type}: ")
                response = (
                    supabase.table(TABLE_NAME)
                    .update({stat_type: new_stat})
                    .eq("name", item)
                    .execute()
                )
                print(f"Updated {item}'s {stat_type} to {new_stat}.")

            elif stat_type =="damage" or stat_type == "price":
                new_stat = int(input(f"Enter the item's new {stat_type}: "))
                response = (
                    supabase.table(TABLE_NAME)
                    .update({stat_type: new_stat})
                    .eq("name", item)
                    .execute()
                )
                print(f"Updated {item}'s {stat_type} to {new_stat}.")

            elif stat_type == "all":
                new_name = input("Enter the item's new name: ")
                new_dmg = int(input("Enter the item's new damage: "))
                new_price = int(input("Enter the item's new price: "))

                response = (
                    supabase.table(TABLE_NAME)
                    .update({"name": new_name, "damage": new_dmg, "price": new_price})
                    .eq("name", item)
                    .execute()
                )
                print(f"Updated {item} to {response.data}")

            else: print(INPUT_ERROR)



        elif user_in == "4":
            delete = input("Enter the name of the item to delete: ")
            response = (
                supabase.table(TABLE_NAME)
                .delete()
                .eq("name", delete)
                .execute()
            )
            print(f"Deleted '{delete}'!")

        elif user_in=="5":
            #ai assisted with the implementation of the aggregation
            response=(
                supabase.table(TABLE_NAME)
                .select("damage")
                .execute()
            )
            sum_damage = sum(
                item.get('damage', 0) 
                for item in response.data 
                if item.get("damage")
                )
            print(sum_damage)

        elif user_in =="6":
            done=True

        else: print(INPUT_ERROR)

Main()