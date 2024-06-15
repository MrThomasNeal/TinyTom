# File containing all the text dictionaries and lists needed for the program

# Keyboards to match input to an intent as a last resort if classifier, direct matching and more fails
keywords = {
    "add": "Add songs",
    "delete": "Remove songs",
    "remove": "Remove songs",
    "create": "Create playlist",
    "display": "List playlists",
    "list": "List playlists",
    "search": "Search for song",
}

# Training data for the classifier to match intents
training_data = {
    "Add songs": [
        "add a song",
        "put this song",
        "include this song",
        "add a new song",
        "append a song",
        "insert this song",
        "add a fresh song",
    ],
    "Remove songs": [
        "remove a song",
        "delete this song",
        "remove this song",
        "eliminate a song",
        "erase this song",
        "exclude this song",
    ],
    "Create playlist": [
        "create a new playlist",
        "make a playlist for me",
        "generate a playlist",
        "produce a collection",
        "begin a new list of songs",
        "establish an additional playlist",
    ],
    "List playlists": [
        "show my playlists",
        "list my playlists",
        "display playlists",
        "what playlists do I have",
        "show me all my music collections",
        "enumerate my complete collection",
    ],
    "Search for song": [
        "find a song for me",
        "search for a track",
        "locate this tune",
        "whats the title of that song",
        "search my collection for a specific song",
        "is there a song matching this description",
    ],
    "Name set": [
        "my name is",
        "i am",
        "call me",
        "you can call me",
        "they call me",
        "i go by",
        "i respond to",
    ],
    "Request name": [
        "what is my name",
        "can you remember my name",
        "do you know my name",
        "tell me my name",
        "what am i called",
    ],
    "List chatbot capabilities": [
        "what can you do",
        "tell me your capabilities",
        "list your functions",
        "what are your features",
        "what are your abilities",
        "what functionalities do you have",
        "list your capabilities"
    ],
    "Greetings": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "howdy",
        "yo",
    ],
    "Appreciation": [
        "thank you",
        "thanks",
        "much appreciated",
        "i appreciate it",
        "grateful for your help",
        "you've been great",
        "thanks a lot",
        "i'm thankful",
        "much thanks",
        "i owe you one",
        "appreciate your assistance",
        "you've been very helpful",
        "i'm grateful",
        "you're awesome",
        "you're the best",
    ]
}

test_data = {
    "Add songs": [
        "add a new track",
        "insert this melody",
        "include a song in the playlist",
        "append a fresh tune",
        "put this new song",
        "add a track to my collection",
    ],
    "Remove songs": [
        "delete that track",
        "exclude this from the playlist",
        "remove this music",
        "eliminate a song from the list",
        "erase this melody",
        "remove a track from my collection",
    ],
    "Create playlist": [
        "create a playlist for my mood",
        "generate a new music collection",
        "begin a playlist with my favorite songs",
        "make a playlist for the party",
        "establish an additional music collection",
        "produce a new playlist for me",
    ],
    "List playlists": [
        "show my music collections",
        "list my playlists",
        "display my music sets",
        "what playlists do I own",
        "show me all my collections",
        "enumerate my complete music collection",
    ],
    "Search for song": [
        "find a track matching my mood",
        "search for a specific melody",
        "locate this song for me",
        "what's the title of that track",
        "search my collection for a particular song",
        "is there a melody matching this description",
    ],
    "Name set": [
        "my name is John",
        "i am Alice",
        "call me Dave",
        "you can call me Sarah",
        "they call me Alex",
        "i go by Emma",
        "i respond to Michael",
    ],
    "Request name": [
        "what's my name",
        "can you remember my name",
        "do you know my name",
        "tell me my name",
        "what am I called",
        ""
    ],
    "List chatbot capabilities": [
        "what are your features",
        "tell me what you can do",
        "list your functions",
        "what functionalities do you have",
        "tell me about your capabilities",
        "what are your abilities",
    ],
    "Greetings": [
        "hey there",
        "hi",
        "hello",
        "good morning",
        "yo",
        "greetings",
    ],
    "Appreciation": [
        "thank you so much",
        "thanks a bunch",
        "much appreciated",
        "i appreciate it a lot",
        "grateful for your assistance",
        "you're the best",
        "thanks a million",
        "i'm thankful for your help",
        "much thanks to you",
        "i owe you one",
        "appreciate your support",
        "you've been very helpful",
        "i'm grateful for your guidance",
        "you're awesome",
        "thanks a ton",
    ]
}

# A list of responses to a user showing appreciation
appreciation_responses = [
    "You're welcome",
    "No problem, happy to help",
    "It's my pleasure",
    "Anytime",
    "Glad I could assist",
    "You're very kind",
    "No need to thank me",
    "Thank you for your kind words",
    "I appreciate your appreciation"
]

# A list of responses to a user greeting the bot
greeting_responses = [
    "Nice to see you",
    "Hope you are well",
    "It's good to see you",
    "It's a pleasure to see you",
    "TinyTom at your service"
]

# A list of responses to give to the user if they choose to exit
exit_responses = [
    "See you again soon",
    "Have a good rest of your day",
    "Adios",
    "I look forward to seeing you again soon",
    "Goodbye"
]

# A list of responses to give to the user if they choose to cancel the transaction
cancel_responses = [
    "No worries! Let me know if I can assist you elsewhere",
    "No problem! I'm always here if you need more assistance"
    "Groovy! I'll be here if you need anything else",
    "Cool! Let me know if you need anything"
]

# A list of facts to be chosen at random is the user wants a fact
facts = [
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years"
    " old and still perfectly edible.",
    "Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body.",
    "A group of flamingos is called a 'flamboyance.'",
    "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of iron in the heat.",
    "Bananas are berries, but strawberries are not.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered"
    " after 38 minutes.",
    "A day on Venus is longer than a year on Venus. Venus has an extremely slow rotation,"
    " taking about 243 Earth days to complete one rotation, while it only takes 225 Earth days to orbit the Sun.",
    "Cows have best friends and can become stressed when they are separated from them."
]

# A list of jokes to be told to the user if they request a joke
jokes = [
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
    "How do you organize a space party? You 'planet'!",
    "What do you get when you cross a snowman with a vampire? Frostbite.",
    "Why did the bicycle fall over? Because it was two-tired!"
]

# Keyboards to be used for getting confirmation from the user
affirmation_keywords = ['yes', 'yeah', 'sure', 'absolutely', 'ok', 'okay', "ye", "please", "yh"]
negation_keywords = ['no', 'nope', 'not', 'nah']