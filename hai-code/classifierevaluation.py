from sklearn.metrics import classification_report, accuracy_score
from intentmatcher import train_intent_classifier
from text import training_data, test_data


# Evaluate the classifier used for the chatbot
def evaluate_classifier(test_data, vectorizer, classifier, label_encoder):

    # Lists to store true labels and predicted labels
    y_true = []
    y_pred = []

    # Iterate through each intent and its phrases in the test data
    for intent, phrases in test_data.items():
        for phrase in phrases:

            # Transform text into vectorizer
            x_test = vectorizer.transform([phrase])

            # Append to the true label to the list
            y_true.append(intent)

            # Predict the label for the test phrase
            confidence_score = classifier.predict_proba(x_test)
            y_pred.append(label_encoder.inverse_transform(classifier.predict(x_test))[0])

    # Calculate the accuracy and classification report
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred)

    return accuracy, report


# Call the training function to get the classifier
vectorizer, classifier, label_encoder = train_intent_classifier(training_data)

# Evaluate the classifier on the test data
accuracy, report = evaluate_classifier(test_data, vectorizer, classifier, label_encoder)

# Print the results
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)