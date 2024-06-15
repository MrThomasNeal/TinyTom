from intentmatcher import load_csv, preprocess_text
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Cosine similarity function for csv files
def find_most_similar_row(input_text):

    # Initialise variables
    highest_sim = 0
    answer = None

    # Preprocess text for an input vector
    input_vector = preprocess_text(input_text, "vector")

    # Vectorise the input text
    x_input = vectorizer.fit_transform([input_vector])

    # Store cosine similarities between the input and each row
    similarity_scores = []

    # Iterate through the rows in the csv
    for row in data:

        # Preprocess the row
        row_vector = preprocess_text(row[1], "vector")

        # Vectorise the current row
        x_row = vectorizer.transform([row_vector])

        # Compute cosine similarity
        cosine_sim = cosine_similarity(x_input, x_row)
        current_sim_score = cosine_sim[0][0]
        similarity_scores.append(current_sim_score)

        # Keep track of highest similarity
        if current_sim_score > highest_sim:
            highest_sim = current_sim_score
            answer = row[2]

    return answer


# Evaluate the question-answering system
def evaluate_qa_system(test_data):

    # Initialise variables
    correct_predictions = 0
    total_questions = len(test_data)

    # Iterate through test_data
    for input_question, expected_answer in test_data:

        # Call cosine similarity function to get answer to question
        predicted_answer = find_most_similar_row(input_question)

        # Check if the predicted answer matches the expected answer
        if predicted_answer == expected_answer:
            correct_predictions += 1

    # Calculate accuracy
    accuracy = correct_predictions / total_questions
    return accuracy


# Get a random selection of QA pairs from csv file
def get_random_qa_pairs(data, num_pairs):

    # Ensure that the number of requested pairs is not greater than the available data
    num_pairs = min(num_pairs, len(data))

    # Randomly shuffle the data and select the first num_pairs
    random.shuffle(data)

    # Extract only columns 2 and 3 for the selected pairs
    selected_pairs = [(row[1], row[2]) for row in data[:num_pairs]]

    return selected_pairs


# File name of csv to use
filename = "QA.csv"

# Load csv into data variable
data = load_csv(filename)

# Initialise vectorizer
vectorizer = CountVectorizer()

# Get a random selection of QA pairs from the csv
random_qa_pairs = get_random_qa_pairs(data, 30)

# Message to show code is working and not just frozen
print("Calculating...")

# Call the evaluator and pass the random selection of QA pairs
accuracy = evaluate_qa_system(random_qa_pairs)

# Output the accuracy
print("Accuracy:", accuracy)