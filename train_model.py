import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
from text_processor import TextPreprocessor
from sklearn.calibration import CalibratedClassifierCV
import joblib
import os

def load_and_prepare_data():
    # Load datasets
    true_news = pd.read_csv('data/True.csv')
    fake_news = pd.read_csv('data/Fake.csv')
    
    # Add labels
    true_news['label'] = 1
    fake_news['label'] = 0
    
    # Combine datasets
    df = pd.concat([true_news, fake_news], ignore_index=True)
    
    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

def train_models():
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Load and prepare data
    df = load_and_prepare_data()
    
    # Initialize text preprocessor
    preprocessor = TextPreprocessor()
    
    # Clean text (using 'Statement' column instead of 'text')
    df['cleaned_text'] = df['Statement'].apply(preprocessor.clean_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['cleaned_text'], df['label'], test_size=0.2, random_state=42
    )
    
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Initialize models
    models = {
        'logistic': LogisticRegression(max_iter=1000),
        'naive_bayes': MultinomialNB(),
        'random_forest': RandomForestClassifier(n_estimators=100),
        'svm': CalibratedClassifierCV(LinearSVC(random_state=42))

    }
    
    # Perform cross-validation for each model
    best_cv_score = 0
    best_model = None
    
    for name, model in models.items():
        print(f"\nPerforming cross-validation for {name.upper()}...")
        cv_scores = cross_val_score(model, X_train_vec, y_train, cv=5)
        print(f'Cross-validation scores: {cv_scores}')
        print(f'Average CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})')
        
        if cv_scores.mean() > best_cv_score:
            best_cv_score = cv_scores.mean()
            best_model = (name, model)
    
    # Train and evaluate models
    print("\nTraining models on full training set...")
    for name, model in models.items():
        print(f"\nTraining {name.upper()}...")
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n{name.upper()} Results:")
        print(classification_report(y_test, y_pred))
    
    # Train the best model (selected from cross-validation)
    print(f"\nSelected best model based on cross-validation: {best_model[0]}")
    final_model = best_model[1]
    final_model.fit(X_train_vec, y_train)
    
    # Save best model and vectorizer
    print("\nSaving models...")
    joblib.dump(final_model, 'models/best_model.joblib')
    joblib.dump(vectorizer, 'models/vectorizer.joblib')
    
    print(f"\nBest model: {best_model[0]} with CV accuracy: {best_cv_score:.4f}")

if __name__ == "__main__":
    train_models()
