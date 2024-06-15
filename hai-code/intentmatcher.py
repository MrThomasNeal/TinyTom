import random
from nltk import pos_tag
from nltk.corpus import names
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import numpy as np
from nltk.tokenize import word_tokenize
import re
import csv
import datetime
import urllib.request
import json
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from text import *
from preprocessing import get_synonyms, preprocess_text

# API key for weather functions
api_key = "859a92e5838a4d3fad2183747230611"


# Detects names in an input
def detect_names(userInput):

    full_name = ""
    tokenized_text = word_tokenize(userInput)
    tagged_tokens = pos_tag(tokenized_text)

    # Go through each word in user input and detect a name (and surname) and add it to full_name
    detected_names = [word for word, pos in tagged_tokens if pos == "NNP" or word.title() in names.words()]
    if detected_names:
        for name in detected_names:
            full_name += " "
            full_name += name
    return full_name


# Takes in user input and returns its predicted intent
def get_intent(user_input):
    return predict_intent(user_input.lower(), vectorizer, classifier, label_encoder, 0.7)


# Loads the data from a csv file
def load_csv(filename):

    data = []

    with open(filename, newline='', encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

# Given the input text, find the most similar row in the given csv file
def find_most_similar_row(csv_filename, input_text):

    # Holds the highest similarity score
    highest_sim = 0

    # Load data into "data" variable
    data = load_csv(csv_filename)

    # Preprocess text for an input vector
    input_vector = preprocess_text(input_text, "vector")

    # Initialise vectorizer
    vectorizer = CountVectorizer()

    # Vectorise the input text
    x_input = vectorizer.fit_transform([input_vector])

    # Store cosine similarities between the input and each row
    similarity_scores = []

    # Iterate through the rows in the csv file
    for row in data:
        row_vector = preprocess_text(row[1], "vector")

        # Vectorise the current row
        x_row = vectorizer.transform([row_vector])

        # Compute cosine similarity
        cosine_sim = cosine_similarity(x_input, x_row)
        current_sim_score = cosine_sim[0][0]
        similarity_scores.append(current_sim_score)

        # Keep track of highest similarity
        if(current_sim_score > highest_sim):
            highest_sim = current_sim_score

    # Find the index of the most similar row
    most_similar_index = np.argmax(similarity_scores)
    most_similar_row = data[most_similar_index]
    answer = most_similar_row[2]

    # If confidence score of highest similarity > 0.8, perform actions based on the answer found to the input
    if(highest_sim > 0.87):

        # Respond to the user with a random fact
        if (answer == "facts"):
            answer = random.choice(facts)

        # Respond with the date today
        if (answer == "date"):
            date = datetime.date.today()
            answer = "The date is {today_date}".format(today_date=date)

        # Asks user for their location then provides their weather forecast for the day
        if (answer == "weather"):
            print("TinyTom: What city are you in?")
            city_input = input("You: ")
            url = "http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}".format(api_key=api_key, city=
            city_input)
            try:
                response = urllib.request.urlopen(url)
                data = response.read().decode("utf-8")
                weather_data = json.loads(data)
                current = weather_data['current']
                condition = f"{current['condition']['text']}"
                temperature = f"{current['temp_c']}°C"
                feels_like = f"{current['feelslike_c']}°C"
                wind_speed = f"{current['wind_kph']} km/h"
                answer = ("It is a {condition} day today in {city}. The temperature is {temp}, but feels like"
                          " {feels_like} with wind speeds of {wind_speed}".format(condition=condition.lower(),
                                                                                  city=city_input,
                                                                                  temp=temperature,
                                                                                  feels_like=feels_like,
                                                                                  wind_speed=wind_speed))
            except Exception:
                answer = "I had en error fetching the weather data :("

        # Respond to the user with a random joke
        if (answer == "jokes"):
            answer = random.choice(jokes)

        # Tell the user the current time
        if (answer == "time"):
            time = datetime.datetime.now().time()
            formatted_time = time.strftime("%H:%M:%S")
            answer = "The time is {current_time}".format(current_time=formatted_time)

        print("TinyTom: {answer}".format(answer=answer))
        return True
    else:
        return False


# Train the intent classifier to allow for intent predicitons
def train_intent_classifier(training_data):

    # Initialise the vectorizer, classifier and label encoder
    vectorizer = CountVectorizer()
    classifier = MultinomialNB()
    label_encoder = LabelEncoder()

    # Lists to store text data and corresponding intents
    texts = []
    intents = []

    # Iterate through training data, adding phrases and intents to the lists appropriately
    for intent, phrases in training_data.items():
        texts.extend(phrases)
        intents.extend([intent] * len(phrases))

    # Convert text data into matrix of token counts
    x = vectorizer.fit_transform(texts)
    # Encode target labels into numerical values
    y = label_encoder.fit_transform(intents)
    # Train classifier using x and y
    classifier.fit(x, y)

    return vectorizer, classifier, label_encoder

def predict_intent(user_input, vectorizer, classifier, label_encoder, threshold):

    # Preprocess user input
    user_input = preprocess_text(user_input, "input")

    if user_input == "":
        return None

    # If not, predict intent using a classifier
    x = vectorizer.transform([user_input])
    y_pred = classifier.predict(x)

    # Confidence scores
    confidence_score = classifier.predict_proba(x)
    max_confidence = np.max(confidence_score)

    # Debug
    # print("Confidence of user input: {v}".format(v=max_confidence))

    # Predict intent from the classifier
    intent = label_encoder.inverse_transform(y_pred)[0]

    # If the confidence score for the match from the classifier is not accurate enough, run backup processes
    if max_confidence < threshold:

        # Checks if the users input is small talk
        if (find_most_similar_row("smalltalk.csv", user_input)):
            return "Small talk"

        # Initially check if users input is QA
        if (find_most_similar_row("QA.csv", user_input)):
            return "QA"

        # Initially check for direct phrase matching
        for intent, phrases in training_data.items():
            for phrase in phrases:
                pattern = r'\b' + re.escape(phrase) + r'\b'
                if re.search(pattern, user_input, re.I):
                    return intent

        # If no luck, check for keywords and their synonyms within the user input
        user_input = user_input.lower()

        for keyword, intent in keywords.items():
            if keyword in user_input:
                return intent

        # Also check for keywords synonyms in the input
        for keyword, intent in keywords.items():
            keyword_synonyms = get_synonyms(keyword)
            for synonym in keyword_synonyms:
                if synonym in user_input:
                    return intent
    else:
        return intent


# Train the intent classifier
vectorizer, classifier, label_encoder = train_intent_classifier(training_data)
