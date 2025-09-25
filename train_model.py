from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# tiny sample dataset (replace with real dataset later)
texts = [
    "I love this product, it's amazing!",
    "This is wonderful and excellent.",
    "I am so happy with the service.",
    "This is the worst purchase I ever made.",
    "Terrible experience, I hate it.",
    "Very disappointed and unhappy."
]
labels = [1, 1, 1, 0, 0, 0]  # 1 = positive, 0 = negative

# train/test split
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.33, random_state=42)

# pipeline
pipeline = make_pipeline(
    TfidfVectorizer(ngram_range=(1,2), max_features=5000),
    LogisticRegression(max_iter=1000)
)

pipeline.fit(X_train, y_train)

# evaluate
preds = pipeline.predict(X_test)
print(classification_report(y_test, preds))

# save both parts (pipeline includes vectorizer + model)
joblib.dump(pipeline, "model.joblib")
print("Saved model.joblib")
