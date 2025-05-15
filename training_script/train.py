import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb
from config import NUM_SAMPLES, TEST_SIZE, RANDOM_STATE, PARAM_GRID, MODEL_DIR
from logger import get_logger
from data_generator import generate_synthetic_feedback
from utils import preprocess_text
import joblib


logger = get_logger(__name__)

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    logger.info("Generating synthetic data...")
    df = generate_synthetic_feedback(NUM_SAMPLES)
    logger.info(f"Generated {len(df)} samples")
    logger.info("Preprocessing text...")
    df["clean_text"] = df["text"].apply(preprocess_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["sentiment"], test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    # Vectorize
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Encode labels
    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    y_test_enc = label_encoder.transform(y_test)

    # Model + GridSearch
    model = xgb.XGBClassifier(eval_metric="mlogloss", use_label_encoder=False)
    grid_search = GridSearchCV(model, PARAM_GRID, cv=3, scoring="accuracy", verbose=1)
    grid_search.fit(X_train_tfidf, y_train_enc)

    # Best model
    best_model = grid_search.best_estimator_
    logger.info(f"Best Params: {grid_search.best_params_}")

    # Evaluate
    y_pred = best_model.predict(X_test_tfidf)
    acc = accuracy_score(y_test_enc, y_pred)
    logger.info(f"Test Accuracy: {acc * 100:.2f}%")
    logger.info(
        "\n" + classification_report(y_test_enc, y_pred, target_names=label_encoder.classes_)
    )

    # Save model
    joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.joblib"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.joblib"))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.joblib"))

    logger.info(f"Model and vectorizer saved in '{MODEL_DIR}'")

if __name__ == "__main__":
    main()
