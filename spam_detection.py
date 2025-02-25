import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from wordcloud import WordCloud
from sklearn.model_selection import GridSearchCV

# Data Loading and Initial Cleaning
print("Loading and cleaning data...")
df = pd.read_csv('spam.csv', encoding='latin-1')

# Document data cleaning steps
print(f"Initial dataset size: {len(df)}")
print(f"Number of null values:\n{df.isnull().sum()}")

# Preprocess the data
df = df[['v1', 'v2']].copy()  # Only keep relevant columns
df.columns = ['label', 'message']
print(f"Cleaned dataset size: {len(df)}")

# Convert labels to binary values (ham = 0, spam = 1)
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Print class distribution
print("\nClass distribution:")
print(df['label'].value_counts(normalize=True) * 100)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], 
                                                    test_size=0.2, random_state=42)

# Feature extraction using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Model training with hyperparameter tuning
classifier = MultinomialNB()
param_grid = {'alpha': [0.1, 0.5, 1.0, 1.5]}
grid_search = GridSearchCV(classifier, param_grid, cv=5, scoring='f1')
grid_search.fit(X_train_vectorized, y_train)

# Best model evaluation
best_classifier = grid_search.best_estimator_
y_pred = best_classifier.predict(X_test_vectorized)

# Print evaluation metrics
print("\nModel Performance Metrics:")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nDetailed Classification Report:")
report = classification_report(y_test, y_pred, output_dict=True)

# Convert classification report metrics to percentage
for label, metrics in report.items():
    if isinstance(metrics, dict):
        metrics['precision'] *= 100
        metrics['recall'] *= 100
        metrics['f1-score'] *= 100

# Print the modified classification report
print("\nClassification Report (in percentages):")
print(f"{'Label':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support':<10}")
for label, metrics in report.items():
    if isinstance(metrics, dict):
        print(f"{label:<10} {metrics['precision']:<10.2f} {metrics['recall']:<10.2f} {metrics['f1-score']:<10.2f} {metrics['support']:<10}")

# Visualization
plt.figure(figsize=(10, 6))
wordcloud = WordCloud(width=800, height=400, 
                     background_color='white').generate(' '.join(df['message']))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Messages')
plt.show()
