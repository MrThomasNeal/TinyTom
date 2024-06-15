from nltk.corpus import wordnet
import re

# Dictionary for replacing common typos with their proper spelling
typo_corpus = {}


# Replaces contradictions in an input to allow for a higher chance of input recognition
def replace_contradictions(input):

    # Dictionary containing contradictions and their replacements
    contractions = {
        "i'm": "i am", "i'd": "i would", "you're": "you are", "he's": "he is", "she's": "she is", "it's": "it is", "we're": "we are",
        "they're": "they are", "i've": "i have", "you've": "you have", "we've": "we have", "they've": "they have",
        "i'll": "i will", "you'll": "you will", "he'll": "he will", "she'll": "she will", "it'll": "it will",
        "we'll": "we will", "they'll": "they will", "isn't": "is not", "aren't": "are not", "wasn't": "was not",
        "weren't": "were not", "haven't": "have not", "hasn't": "has not", "hadn't": "had not", "won't": "will not",
        "wouldn't": "would not", "don't": "do not", "doesn't": "does not", "didn't": "did not", "can't": "cannot",
        "couldn't": "could not", "shouldn't": "should not", "mightn't": "might not", "mustn't": "must not",
        "what's": "what is", "whats": "what is",
    }

    expanded_text = input

    # Iterate over each contradiction and replace it in the input text
    for contraction, expanded in contractions.items():
        expanded_text = expanded_text.replace(contraction, expanded)

    # Return the expanded text
    return expanded_text


# Takes a word and returns its synonyms
def get_synonyms(word):

    # Initialise an empty list of synonyms
    synonyms = []

    # Iterate through each synonym set for the given word
    for syn in wordnet.synsets(word):
        # Iterate through each lemma in the synset
        for lemma in syn.lemmas():
            # Add synonym to the list
            synonyms.append(lemma.name())

    # Return the list of synonyms for the given word
    return synonyms


# Preprocesses text
def preprocess_text(input, text_type):

    # Remove any unnecessary spaces in the input
    remove_spaces = re.sub(r'\s+', ' ', input)

    # Replace any contradictions in the input with their expanded form
    expanded_user_input = replace_contradictions(remove_spaces.strip().lower())

    # Remove any punctuation from the input
    no_punctuation = re.sub(r'[^\w\s]', '', expanded_user_input)

    # If the text being preprocessed is NOT for the classifier vectors
    if(text_type != "vector"):
        # Correct typos using the typo corpus
        correct_typos = correct_typo_in_text(no_punctuation)
        # Return the preprocessed text
        return correct_typos.lower()
    else:
        # If the text is a vector for classifiers, don't correct typos as it's not needed and slows down the program
        return no_punctuation.lower()


# Load the typo corpus into memory
def load_typo_corpus():

    # Open the misspellings.txt file for reading
    with open("misspellings.txt", 'r') as file:

        # Initialise a variable to keep track of the current correct spelling
        current_correct_spelling = None

        # Iterate through each line in the file
        for line in file:
            # Check if line starts with a $, indicating it's the correct spelling
            if line.startswith('$'):
                # Extract the correct spelling from the line removing the $
                current_correct_spelling = line[1:].strip()
                # Initialise an empty list for the misspellings associated with the correct spelling
                typo_corpus[current_correct_spelling] = []
            else:
                # If the line does not start with a $, it contains a misspelling, extract it and strip whitespace
                misspelling = line.strip()
                # Add the misspelling to the list
                typo_corpus[current_correct_spelling].append(misspelling)


def correct_typo(word):

    # Iterate through the typo corpus
    for correct_word, misspellings in typo_corpus.items():
        # If the given word is found in the misspellings
        if word.lower() in [misspelling.lower() for misspelling in misspellings]:
            # Return the correct word
            return correct_word
    # If not found in corpus, return given word
    return word


def correct_typo_in_text(input_text):

    # Split the input text into words
    words = input_text.split()
    # Correct each word in the words list using the correct_typo() function
    corrected_words = [correct_typo(word) for word in words]
    # Join the corrected words back together
    corrected_text = ' '.join(corrected_words)
    # Return the corrected text
    return corrected_text