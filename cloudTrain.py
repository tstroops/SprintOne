import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv("environ.env")  # Load variables from .env file
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def DisplayMenu():
    print("Do you:")
    print("1. Search for a name?")
    print("1. Add a new name?")
    print("3. Update a name?")
    print("4. Delete a name?")
    print("5. Quit")

def Main():
    print("Welcome to the Name Inquiry App!")
    DisplayMenu()
    user_in=input()
    if user_in == "1":
        user_in = input("Enter the name to search for: ")
        response = (supabase.table("test").select("*").execute())

            


Main()