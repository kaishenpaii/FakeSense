import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv('fake_or_real_news.csv')

# Features and labels
X = df['text']
y = df['label'].apply(lambda x: 1 if x == 'REAL' else 0)  # Convert labels to binary

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with TfidfVectorizer and LogisticRegression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_df=0.7, stop_words='english')),
    ('lr', LogisticRegression())
])

# Train the model
pipeline.fit(X_train, y_train)

# Calculate the accuracy
accuracy = accuracy_score(y_test, pipeline.predict(X_test))

# Save the model and the accuracy
joblib.dump((pipeline, accuracy), 'fake_news_detector.pkl')
print(f"Model saved as fake_news_detector.pkl with accuracy: {accuracy:.2f}")
