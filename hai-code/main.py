from intentmatcher import get_intent
from playlistmanagement import perform_intent, get_previous_intent
import sqlite3
from pathlib import Path
from preprocessing import load_typo_corpus
from database import extract_song
import nltk

# Download required NLTK resources
nltk.download('averaged_perceptron_tagger')
nltk.download('names')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('punkt')

if __name__ == '__main__':

    # Set run to true for the user input loop
    run = True

    # Create database if it does not exist
    database_path = Path("playlists.db")
    if not database_path.is_file():
        connection = sqlite3.connect("playlists.db")
        connection.close()

    # Load the corpus into memory that fixes typos
    load_typo_corpus()

    # Initial greeting from the bot
    print("\nYou can exit the chatbot at any time by typing (exit)")
    print("-------------------------------------------------------")
    print("TinyTom: Hello I am Tiny Tom! How may I help you today?")

    # Enter user input loop to allow the chatbot to work
    while run:

        global previous_intent

        # Capture user input
        user_input = input("You: ")

        # Exit chatbot per users request
        if(user_input.lower() == "exit"):
            print(f"TinyTom: See you again soon! :)")
            run = False
        else:
            # Extract song from user input
            song = extract_song(user_input)
            if song:
                if get_previous_intent() != "":
                    # If a song is detected and a previous failed intent exists, perform intent using captured song
                    perform_intent(get_previous_intent(), user_input)
                    continue

            # Get the intent from the user input
            intent = get_intent(user_input)
            # Perform the appropriate actions dependent upon the intent
            perform_intent(intent, user_input)