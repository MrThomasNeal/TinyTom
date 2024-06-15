from intentmatcher import get_intent, detect_names
from nltk.tokenize import word_tokenize
from database import *
from text import *
from datetime import datetime
import random

# Global variables
global username
global potential_name_entry
global previous_fail
global previous_intent

# Initialise the global variables
potential_name_entry = False
username = ""
previous_fail = False
previous_intent = ""


# Getter for previous intent
def get_previous_intent():
    return previous_intent


# Given a users input when asked for confirmation, return the users confirmation status
def get_confirmation(user_input):

    # Tokenize the user input
    words_confirmation = word_tokenize(user_input.lower())

    # If any words in user input appear to be affirmation, return yes
    if any(word in affirmation_keywords for word in words_confirmation):
        return "yes"
    # If any words in user input are negation words, return no
    elif any(word in negation_keywords for word in words_confirmation):
        return "no"
    # Else, return unknown
    else:
        return "unknown"


# Remove square brackets and the text within it from an input
def remove_brackets_text(input):

    # Regular expression to remove any song/playlist names from input
    pattern = re.compile(r'\[.*?\]')

    # Remove the song/playlist name from input
    cleaned_input = re.sub(pattern, '', input)

    return cleaned_input



# Check for any potential new intent from a user input
def potential_intent(user_input):

    # Capture if the user wants to cancel the current transaction and return True to cancel
    if(user_input.lower() == "cancel"):
        # Respond to user with a random cancel response
        print("TinyTom: {response}{name}! :)".format(response=random.choice(cancel_responses), name=username))
        return True

    # Capture if the user wants to exit the program and call exit() to cancel
    if(user_input.lower() == "exit"):
        # Respond to user with a random exit response before ending
        print("TinyTom: {response}{name}! :)".format(response=random.choice(exit_responses), name=username))
        exit()

    # Remove any song/playlist names from the input as these can cause issues when not needed
    cleaned_input = remove_brackets_text(user_input)

    # If the input is now empty, return False
    if(len(cleaned_input) == 0):
        return False

    # Check to see if input is a confirmation
    confirmation = get_confirmation(cleaned_input)
    if confirmation != "unknown":
        return False

    # Get the intent of the user_input
    intent = get_intent(cleaned_input)

    # Lists of intents organised into ones that need prompting before change, and no prompting required
    prompt_intents = ["Add songs", "Remove songs", "Create playlists", "List playlists", "Search for song"]
    no_prompt_intents = ["Name set", "Request name", "Appreciation", "Greetings", "List capabilities", "Small talk"]

    # If the intent matches a prompt_intent, prompt the user of a change of intent before performing it
    if (intent in prompt_intents):

        # Get prompt and confirmation of new intent
        print(f"TinyTom: I have detected a new intent of {intent.lower()}, is this correct?")
        confirmation_input = input("You: ")
        confirmation = get_confirmation(confirmation_input)

        # If confirmation returns yes, perform the intent and return True to break out of the other transaction
        if(confirmation == "yes"):
            perform_intent(intent, user_input)
            return True
        # If confirmation returns no, return False to carry on with the previous transaction
        if(confirmation == "no"):
            return False
        # If confirmation returns unknown, tell the user you don't understand and carry on with the previous transaction
        if(confirmation == "unknown"):
            print(f"TinyTom: I don't understand what '{confirmation_input}' means, so I will assume you would like to carry on...")
            return False
    # If the intent matches a no_prompt_intent, perform the intent without getting confirmation first
    elif (intent in no_prompt_intents):
        perform_intent(intent, user_input)
        return True
    # Else, carry on with current transaction
    else:
        return False


# Add songs to database
def add_songs(user_input, username):

    global previous_intent

    # Check user input for song names
    confirmation = ""
    previous_intent = ""

    # Extract song from the input to check if an experienced user has already put it in
    song_in_input = extract_song(user_input)

    if song_in_input:

        # Prompt user for confirmation
        print(f"TinyTom: Would you like to add [{song_in_input}] to your playlist?")
        user_confirmation = input("You: ")

        # Check input for a potential new intent
        if(potential_intent(user_confirmation)):
            return

        # Get confirmation
        confirmation = get_confirmation(user_confirmation)
    else:

        # Prompt for song name input
        print("TinyTom: Enter the name of the song you would like to add in this format [Artist - Title] including "
              "the brackets (or type cancel): ")
        song_input = input("You: ")

        # Check input for potential new intent
        if(potential_intent(song_input)):
            return
        else:

            # Extract song from input
            song_in_input = extract_song(song_input)

            # If song exists in input, confirmation = yes
            if song_in_input:
                confirmation = "yes"
            else:
                print(f"TinyTom: I could not detect a song in the input '{song_input}', perhaps the format was wrong")
                previous_intent = "Add songs"

    # If confirmation from previous code is yes, then a valid song name has been found and the user wants to add it
    if (confirmation == "yes"):

        # Prompt for playlist name entry
        print("TinyTom: Please type the name of the playlist to add it to in the format [playlist name]: ")
        playlist_input = input("You: ")

        # Check input for potential new intent
        if(potential_intent(playlist_input)):
            return

        # Detect playlist name in input
        playlist_name = detect_playlist(playlist_input)

        # If a playlist name has been detected in the input
        if(playlist_name):

            # Check if playlist already exists
            if table_exists(playlist_name):

                # Check if song already exists
                found_song = search_table(song_in_input, playlist_name)

                # If song found, tell user it already exists
                if(found_song):
                    print(f"TinyTom: [{song_in_input}] already exists in the playlist '{playlist_name}'!")
                else:
                    # If song not found, insert it into database
                    insert_song(playlist_name, song_in_input)
                    print(f"TinyTom: I have added [{song_in_input}] to the playlist '{playlist_name}'!")
            else:

                # If table doesn't exist, prompt user if they'd like to create it
                print(f"TinyTom: '{playlist_name}' does not exist, would you like me to create it?")
                create_playlist_confirmation = input("You: ")

                # Check input for potential new intent
                if(potential_intent(create_playlist_confirmation)):
                    return

                # Get confirmation of new playlist creation
                create_playlist = get_confirmation(create_playlist_confirmation)

                # If confirmed, create new table and insert the song into it
                if create_playlist == "yes":
                    create_table(playlist_name)
                    insert_song(playlist_name, song_in_input)
                    print(f"TinyTom: I have added [{song_in_input}] to the playlist '{playlist_name}'")
                if create_playlist == "no":
                    print(f"TinyTom: Okay, no problem{username} :)")
                if create_playlist == "unknown":
                    print(f"TinyTom: Sorry{username}, I don't understand what you are saying :(")
        else:
            print(f"TinyTom: Sorry{username}, I couldn't locate a playlist name inside square brackets :(")

    if (confirmation == "no"):
        print(f"TinyTom: Okay, no worries{username}!")

    if (confirmation == "unknown"):
        print(f"TinyTom: Sorry{username}, I don't understand the input '{user_confirmation}':(")


# Remove songs from database
def remove_songs(user_input, username):

    global previous_intent

    # check user input for song names
    confirmation = ""
    previous_intent = ""

    # Extract song from input as experienced users may already know the format of song names
    song_in_input = extract_song(user_input)
    # If song found, prompt user with confirmation of removing the song
    if song_in_input:

        # Get confirmation from the user
        print(f"TinyTom: Would you like to remove [{song_in_input}] from your playlist?")
        user_confirmation = input("You: ")

        # Check input for potential new intent
        if(potential_intent(user_confirmation)):
            return

        # Get confirmation from user
        confirmation = get_confirmation(user_confirmation)

    else:
        # Prompt user to enter the song to be removed in the correct format
        print("TinyTom: Enter the name of the song you would like to remove in this format [Artist - Title] including "
              "the brackets (or type cancel): ")
        song_input = input("You: ")

        # Check input for any new intents
        if(potential_intent(song_input)):
            return
        else:
            # Find song in input
            song_in_input = extract_song(song_input)

            # If song found, confirmation = yes
            if(song_in_input):
                confirmation = "yes"
            else:
                # If not found, tell the user
                print(f"TinyTom: Sorry, I could not detect a song in your input '{song_input}':(")
                previous_intent = "Remove songs"

    # If confirmation = "yes", valid song has been found and the user wishes to remove it from their playlist
    if (confirmation == "yes"):

        # Search playlists for song
        query_database = search_song_in_db(song_in_input)

        # If song found in db
        if(query_database):

            # Display which playlists it was found in and ask user which ones they'd like to remove it from
            print(f"TinyTom: [{song_in_input}] was found in the following playlists: {', '.join(query_database)}")
            print("TinyTom: Please type the name of the playlists to remove it from below:")
            remove_from_playlists = input("You: ")

            # Check input for potential new intent
            if(potential_intent(remove_from_playlists)):
                return

            # List containing the playlists to have the song removed from
            playlists_to_remove = []

            # Go through the list of playlists the song is found in and take the user input and if any matches are
            # found then add it to the playlists_to_remove list
            for playlist in query_database:
                if playlist.lower() in remove_from_playlists.lower():
                    playlists_to_remove.append(playlist)

            # If there are playlists to remove
            if playlists_to_remove:

                # Tell user which playlists the song will be removed from
                print(f"TinyTom: Removing song from playlists: {', '.join(playlists_to_remove)}")

                # Remove the song from each playlist in the playlists_to_remove list
                for playlist in playlists_to_remove:
                    remove_song(playlist, song_in_input)
            else:
                # If no playlists to remove, tell the user
                print(f"TinyTom: Sorry I couldn't detect any of the following playlists in your reply:"
                      f" {', '.join(query_database)} :(")
        else:
            # If song not found in any playlists, tell the user
            print(f"TinyTom: Sorry{username}, [{song_in_input}] was not found in any of your playlists")

    if (confirmation == "no"):
        print(f"TinyTom: Okay, no worries{username}!")

    if (confirmation == "unknown"):
        print(f"TinyTom: Sorry{username}, I don't understand the input '{user_confirmation}' :(")


# Create playlist (table) in database
def create_playlist(username):

    # Prompt user for confirmation of creating a new playlist
    print("TinyTom: Would you like to create a new playlist?")
    user_confirmation = input("You: ")

    # Check input for potential new intent
    if(potential_intent(user_confirmation)):
        return

    # Get confirmation of new playlist creation
    confirmation = get_confirmation(user_confirmation)

    # If user confirms wanting to create a new playlist
    if (confirmation == "yes"):

        # Prompt user for the name of the playlist to be created between square brackets
        print("TinyTom: Enter the name of the playlist to be created in the format [playlist name] (or type cancel): ")
        playlist_input = input("You: ")

        # Check user input for potential new intent
        if(potential_intent(playlist_input)):
            return

        # Check if playlist exists
        playlist_name = detect_playlist(playlist_input)

        # If it exists, tell the user
        if(table_exists(playlist_name)):
            print(f"TinyTom: A playlist named '{playlist_name}' already exists!")
        else:
            # If it doesn't exist, create the table and tell the user that creation was successful
            create_table(playlist_name)
            print(f"TinyTom: '{playlist_name}' has been created! :)")

    if (confirmation == "no"):
        print(f"TinyTom: My apologies{username}, please rephrase what you would like me to do")

    if (confirmation == "unknown"):
        print(f"TinyTom: Sorry{username}, I don't understand the input '{user_confirmation}' :(")


# Display/list playlists (tables)
def display_playlists(username):

    # Prompt user for confirmation of listing all the tables in the db
    print("TinyTom: Would you like me to list all your playlists?")
    user_confirmation = input("You: ")

    # Check input for potential new intent
    if(potential_intent(user_confirmation)):
        return

    # Get the confirmation from the user's input
    confirmation = get_confirmation(user_confirmation)

    # If confirmed
    if (confirmation == "yes"):

        # Get a list of the tables in the db
        get_playlists = return_tables()

        # If no tables in the db, tell the user
        if get_playlists is None:
            print("TinyTom: You currently have no playlists :(")
        else:
            # If there are tables in the db, list them to the user
            format_tables = ', '.join(get_playlists)
            print(f"TinyTom: Here are your playlists: {format_tables}")

    if (confirmation == "no"):
        print(f"TinyTom: My apologies{username}, please rephrase what you would like me to do")

    if (confirmation == "unknown"):
        print(f"TinyTom: Sorry{username}, I don't understand the input '{user_confirmation}' :( Try rephrasing what "
              f"you said!")


# Search songs in database
def search_for_song(user_input, username):

    global previous_intent

    # Initialise variables
    confirmation = ""
    previous_intent = ""

    # Check initial user input for song names
    song_in_input = extract_song(user_input)

    # If song found in input
    if song_in_input:

        # Prompt user for confirmation of search for song
        print(f"TinyTom: Would you like to search for [{song_in_input}] in your playlists?")
        user_confirmation = input("You: ")

        # Check user input for potential new intent
        if(potential_intent(user_confirmation)):
            return

        # Get the confirmation from the user_confirmation input
        confirmation = get_confirmation(user_confirmation)
    else:

        # Ask user for the song they'd like to search for in the db in the specified format
        print("TinyTom: Enter the name of the song you would like to search in this format [Artist - Title] including "
              "the brackets (or type cancel): ")
        song_input = input("You: ")

        # Check user input for potential new intent
        if(potential_intent(song_input)):
            return
        else:

            # Extract song from input
            song_in_input = extract_song(song_input)

            # If song is found in input, set confirmation to yes
            if(song_in_input):
                confirmation = "yes"
            else:
                # If no song was found, tell the user
                print(f"TinyTom: Sorry{username}, I couldn't detect a song in your input :(")
                previous_intent = "Search for song"

    # If confirmation is yes, valid song has been extracted from input and is ready to be searched
    if (confirmation == "yes"):

        # Search song in db and a list of tables where the song is found is returned
        found_song = search_song_in_db(song_in_input)

        # If song found nowhere in the db, tell the user
        if found_song is None:
            print(f"TinyTom: The song [{song_in_input}] does not exist in any of your playlists")
        else:
            # If song was found in the db, tell the user which playlists it was found in
            print(f"TinyTom: [{song_in_input}] was found in the following playlists: {', '.join(found_song)}")

    if (confirmation == "no"):
        print(f"TinyTom: My apologies{username}, please rephrase what you would like me to do")

    if (confirmation == "unknown"):
        print(f"TinyTom: Sorry{username}, I don't understand the input '{user_confirmation}' :(")


# Perform an intent based on the intent parameter given and the user input parameter
def perform_intent(intent, user_input):

    # Use global variables for tracking name context
    global potential_name_entry
    global username
    global previous_fail

    # If bot has prompted user for name entry, potential_name_entry is true to capture it
    if potential_name_entry:

        # Set variable back to False, so it is not attempting to capture name when user not prompted
        potential_name_entry = False

        # If a name is detected in the user, save it as new_name
        new_name = detect_names(user_input)

        # If new name detected, set the global username variable to the new name and greet the user personally
        if new_name:
            username = new_name
            print(f"TinyTom: Nice to meet you{username}!")
            return

    # If user is wanting to set their name
    if (intent == "Name set"):

        # Detect a new name and assign it to new_name
        new_name = detect_names(user_input)

        # If a new name has been found, assign it to the global variable (username) and greet the user personally
        if new_name:
            username = new_name
            print(f"TinyTom: Nice to meet you{username}!")
        else:
            print("TinyTom: Sorry, I couldn't detect your name! :(")

    # If user is requesting their name
    if (intent == "Request name"):

        # If a name for the user has already been captured
        if (username != ""):
            # Tell the user their name
            print(f"TinyTom: Your name is{username}!")
        else:
            print("TinyTom: You haven't told me yet! What is your name?")

            # Set potential_name_entry to True due to name prompt and tell program to look for it in the next input
            potential_name_entry = True

    # If user is showing appreciation
    if (intent == "Appreciation"):

        # Respond to the user with a random appreciation response and their name for personalisation
        print(f"TinyTom: {random.choice(appreciation_responses)}{username}! :) ")

    # If user is greeting the bot
    if (intent == "Greetings"):

        # Get the current hour for the user
        current_hour = datetime.now().hour

        # Depending on the time of day, formulate a greeting response
        if 5 <= current_hour < 12:
            greeting_time = "Good morning"
        elif 12 <= current_hour < 18:
            greeting_time = "Good afternoon"
        else:
            greeting_time = "Good evening"

        # If username has been captured
        if (username != ""):
            # Greet the user using a personalised response with name
            print(f"TinyTom: {greeting_time}{username}! {random.choice(greeting_responses)}!")
        else:
            # Greet the user using a personalised response and prompt user for their name
            print(f"TinyTom: {greeting_time}! {random.choice(greeting_responses)}! What is your name?")

            # Set potential_name_entry to True due to name prompt and tell program to look for it in the next input
            potential_name_entry = True

    # If the user is wanting to find out what the chatbot can do, tell them
    if (intent == "List chatbot capabilities"):
        print(f"TinyTom: I am here to help you manage your playlists. I can create and delete playlists"
              " for you, as well as add/remove/search for songs of your choice in these playlists. I'm also here"
              " to chat with you and answer questions :)")

    # If the user is wanting to add a song to their playlist
    if (intent == "Add songs"):
        # Start the add songs transaction
        add_songs(user_input, username)

    # If the user is wanting to remove a song from their playlists
    if (intent == "Remove songs"):
        # Start the remove songs transaction
        remove_songs(user_input, username)

    # If the user is wanting to create a new playlist
    if (intent == "Create playlist"):
        # Start the create playlist transaction
        create_playlist(username)

    # If the user is wanting their playlists to be listed/displayed
    if (intent == "List playlists"):
        # Start the list playlists transaction
        display_playlists(username)

    # If the user is wanting to search for a song in the database
    if (intent == "Search for song"):
        # Start the search for song transaction
        search_for_song(user_input, username)

    # If no intent is found
    if intent is None:
        # Tell the user that what they are saying is not understood and rephrasing is prompted
        if previous_fail == True:
            print(f"TinyTom: Hey{username}, you seem stuck! Let me tell you how I am able to assist you: ")
            perform_intent("List chatbot capabilities", "")
        else:
            print(f"TinyTom: Sorry{username}, I am unsure of what '{user_input}' means, my apologies!"
                f" Try rephrasing what you said :(")
            previous_fail = True

    if intent != None:
        previous_fail = False

    # Debug
    # print("Detected Intent: {intent}".format(intent=intent))


