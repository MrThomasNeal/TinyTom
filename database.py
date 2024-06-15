import sqlite3
import re


# Given an input, find the song in form [Artist - Title] within the input and return 'Artist - Title'
def extract_song(input):

    # Initialise reformat variable
    reformat = ""

    # Find any matches in the input for the format [Artist - Title]
    matches = re.findall(r'\[(.*?)\]', input)

    # Split matches up into artist and title variables
    for content in matches:
        parts = content.split('-')
        artist = parts[0].strip()
        title = parts[1].strip() if len(parts) > 1 else ''

        # Return the reformatted song name
        reformat = f"{artist} - {title}"

    # If reformat exists and isn't empty
    if reformat and reformat != " - ":
        return reformat
    return None


# Given an input find a playlist name somewhere within the input in square brackets and return just its name
def detect_playlist(user_input):

    # Search for any input within square brackets that may contain a playlist name
    pattern = r'\[([^\[\]]+)\]'
    match = re.search(pattern, user_input)

    # If found, return the playlist name without brackets
    if match:
        return match.group(1)
    else:
        return None


# Check if a table name given in input exists within the database
def table_exists(table_name):

    # Replace any spaces in the table_name with underscores to allow for multiple words to be input into the database
    table_name = table_name.replace(" ", "_")

    # Connect to db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Query db for any tables matching table_name
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=? COLLATE NOCASE", (table_name,))
    table = cursor.fetchone()

    # Close the db connection
    connection.close()

    # Return the table name if it exists
    return table is not None


# Create a table in the database using the name passed to the function (table_name)
def create_table(table_name):

    # Replace any spaces in the table_name with underscores to allow for multiple words to be input into the database
    table_name = table_name.replace(" ", "_")

    # Connect to the db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Query the db to create a table with the columns Artist and Title with the given table_name parameter as its name
    query = f"CREATE TABLE {table_name.lower()} (Artist TEXT, Title TEXT)"
    cursor.execute(query)

    # Commit the transaction
    connection.commit()

    # Close the connection
    connection.close()


# Inserts a song into the given table_name into the playlist database
def insert_song(table_name, song):

    # Split the song name into artist and title variables
    artist, title = map(str.strip, song.split('-'))

    # Replace any spaces in the table_name with underscores to allow for multiple words to be input into the database
    table_name = table_name.replace(" ", "_")

    # Connect to the db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Query the db to insert Artist and Title values into the table_name table within the db
    insert_query = f"INSERT INTO {table_name} (Artist, Title) VALUES (?, ?)"
    cursor.execute(insert_query, (artist, title))

    # Commit the transaction
    connection.commit()

    # Close the connection
    connection.close()


# Removes a song from the given table_name from the playlist database
def remove_song(table_name, song):

    # Split the song name into artist and title variables
    artist, title = map(str.strip, song.split('-'))

    # Replace any spaces in the table_name with underscores to allow for multiple words to be input into the database
    table_name = table_name.replace(" ", "_")

    # Connect to the db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Query the db to remove a song from table_name where the relevant Artist and Title are found from song param
    remove_query = f"DELETE FROM {table_name} WHERE Artist = ? COLLATE NOCASE AND Title = ? COLLATE NOCASE"
    cursor.execute(remove_query, (artist, title))

    # Commit the transaction
    connection.commit()

    # Close the connection
    connection.close()


# Search if song_name exists within the database in any of the tables
def search_song_in_db(song_name):

    # Split the song name into artist and title variables
    artist, title = map(str.strip, song_name.split('-'))

    # Connect to the db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Query the db to get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    # List for containing all the tables that song_name was found in
    found_tables = []

    # Iterate through each table
    for table_info in tables:
        table_name = table_info[0]

        # Query the current table for matches on the song name
        search_query = f"SELECT * FROM {table_name} WHERE Artist = ? COLLATE NOCASE AND Title = ? COLLATE NOCASE"
        cursor.execute(search_query, (artist, title))

        # If found a match, add the table it was found in to the found_tables list
        if cursor.fetchone() is not None:
            # Replace underscore with space for readability on the user's end
            found_tables.append(table_name.replace("_", " "))

    # Close the connection
    connection.close()

    # If the song exists in any tables, return the list containing which ones
    if found_tables:
        return found_tables
    else:
        return None


# Search a specific table (table_name) for a song (song_name) to see if it exists
def search_table(song_name, table_name):

    # Split the song name into artist and title variables
    artist, title = map(str.strip, song_name.split('-'))

    # Replace any spaces in the table_name with underscores to allow for multiple words to be input into the database
    table_name = table_name.replace(" ", "_")

    # Connect to the db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Search for the song in the specified table
    search_query = f"SELECT * FROM {table_name} WHERE Artist = ? COLLATE NOCASE AND Title = ? COLLATE NOCASE"
    cursor.execute(search_query, (artist, title))

    # If the song is found, close the connection and return True
    if cursor.fetchone() is not None:
        connection.close()
        return True

    # Else, close the connection and return False
    connection.close()
    return False


# Return all the tables which exist within the database
def return_tables():

    # Connect to the db
    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    # Query the db for tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    # Replace underscores with spaces for user readability
    table_names = [table[0].replace("_", " ") for table in tables]

    # Close the connection
    connection.close()

    # If no table names, return None
    if not table_names:
        return None

    # Else, return the table names that exist within the db
    return table_names