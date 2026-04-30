import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.express as px
import joblib
from text_processor import TextPreprocessor
from lime.lime_text import LimeTextExplainer
import textstat
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import random

# Load model and vectorizer
model = joblib.load('models/best_model.joblib')
vectorizer = joblib.load('models/vectorizer.joblib')
preprocessor = TextPreprocessor()

def analyze_text_complexity(text):
    """Analyze text complexity using various metrics"""
    return {
        'readability_score': textstat.flesch_reading_ease(text),
        'grade_level': textstat.coleman_liau_index(text),
        'sentence_count': textstat.sentence_count(text),
        'syllable_count': textstat.syllable_count(text),
        'complex_word_ratio': len([word for word in text.split() if textstat.syllable_count(word) > 2]) / len(text.split()) if text else 0
    }

def analyze_sentiment(text):
    """Analyze text sentiment using TextBlob"""
    analysis = TextBlob(text)
    return {
        'polarity': analysis.sentiment.polarity,
        'subjectivity': analysis.sentiment.subjectivity
    }

def get_prediction_explanation(text, proba):
    """Get LIME explanation for prediction"""
    explainer = LimeTextExplainer(class_names=['Fake', 'True'])
    
    def predict_proba(texts):
        processed_texts = [preprocessor.clean_text(t) for t in texts]
        vec_texts = vectorizer.transform(processed_texts)
        return model.predict_proba(vec_texts)
    
    exp = explainer.explain_instance(text, predict_proba, num_features=10)
    word_importance = dict(exp.as_list())
    sorted_words = sorted(word_importance.items(), key=lambda x: abs(x[1]), reverse=True)
    
    explanations = []
    for word, importance in sorted_words:
        direction = "supporting" if importance > 0 else "opposing"
        impact = abs(importance)
        explanations.append({
            'word': word,
            'importance': importance,
            'direction': direction,
            'impact_percentage': f"{impact*100:.1f}%"
        })
    
    return explanations

def analyze_batch_predictions(df):
    """Analyze batch prediction results"""
    return {
        'total_articles': len(df),
        'true_predictions': sum(df['prediction'] == 'True'),
        'fake_predictions': sum(df['prediction'] == 'Fake'),
        'avg_confidence': df['confidence'].mean(),
        'high_confidence_count': sum(df['confidence'] >= 0.8)
    }

def make_prediction(text, confidence_threshold=0.5):
    """Make prediction on text with confidence threshold"""
    processed_text = preprocessor.clean_text(text)
    vec_text = vectorizer.transform([processed_text])
    proba = model.predict_proba(vec_text)[0]
    prediction = 'True' if proba[1] >= confidence_threshold else 'Fake'
    confidence = proba[1] if prediction == 'True' else proba[0]
    explanation = get_prediction_explanation(text, proba)
    complexity = analyze_text_complexity(text)
    sentiment = analyze_sentiment(text)
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'explanation': explanation,
        'complexity': complexity,
        'sentiment': sentiment
    }

def process_batch_input(texts, confidence_threshold=0.5):
    """Process batch of texts"""
    results = []
    
    for text in texts:
        if not str(text).strip():
            continue
        result = make_prediction(text, confidence_threshold)
        results.append({
            'text': text[:200] + '...' if len(text) > 200 else text,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'complexity_score': result['complexity']['readability_score'],
            'sentiment_score': result['sentiment']['polarity']
        })
    
    return pd.DataFrame(results)

# Streamlit interface
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Analysis Mode:", ["Single Article Analysis", "Batch Processing"])

confidence_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.50,
    max_value=1.00,
    value=0.70,
    step=0.05,
    help="Adjust the confidence threshold for predictions. Higher values mean stricter classification."
)



if page == "Single Article Analysis":
    st.title("🔍 Fake News Detection - Single Article Analysis")
    
    input_method = st.radio("Choose input method:", ["Text Input"])
    
    if input_method == "Text Input":
        text_input = st.text_area("Enter the news article text:", height=200)
        
        if st.button("Analyze Text"):
            if text_input.strip():
                with st.spinner("Analyzing..."):
                    result = make_prediction(text_input, confidence_threshold)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Prediction Result")
                        if result['prediction'] == 'True':
                            st.success(f"Prediction: {result['prediction']} News")
                        else:
                            st.error(f"Prediction: {result['prediction']} News")
                        st.metric("Confidence Score", f"{result['confidence']*100:.1f}%")
                    
                    with col2:
                        st.subheader("Text Analysis")
                        st.metric("Readability Score", f"{result['complexity']['readability_score']:.1f}")
                        st.metric("Sentiment Score", f"{result['sentiment']['polarity']:.2f}")
                    
                    st.subheader("Word Importance Analysis")
                    
                    word_data = pd.DataFrame(result['explanation'])
                    fig = px.bar(word_data, 
                                x='word', 
                                y='importance',
                                color='direction',
                                title="Word Contributions to Classification",
                                color_discrete_map={'supporting': 'green', 'opposing': 'red'})
                    st.plotly_chart(fig)
                    
                    text_words = text_input.split()
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(text_words))
                    
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    st.pyplot(plt)
                    
            else:
                st.warning("Please enter some text to analyze.")

elif page == "Batch Processing":  # Ensure this is an elif statement
    st.title("📊 Fake News Detection - Batch Processing")

    uploaded_file = st.file_uploader("Upload a file with news articles (CSV, TXT, XLSX)", type=['csv', 'txt', 'xlsx'])

    if uploaded_file is not None:
        try:
            if uploaded_file.type == 'text/csv':
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                df = pd.read_excel(uploaded_file)
            else:
                content = uploaded_file.read().decode()
                texts = content.split('\n')
                df = pd.DataFrame({'text': texts})
            
            text_col = df.select_dtypes(include=['object']).columns[0]
            
            with st.spinner("Processing batch..."):
                results_df = process_batch_input(df[text_col].fillna(''), confidence_threshold)
                
                st.subheader("Batch Analysis Summary")
                
                analysis = analyze_batch_predictions(results_df)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Articles", analysis['total_articles'])
                with col2:
                    st.metric("True News", analysis['true_predictions'])
                with col3:
                    st.metric("Fake News", analysis['fake_predictions'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_pie = px.pie(results_df, 
                                   names='prediction', 
                                   title="Predictions Distribution",
                                   color='prediction',
                                   color_discrete_map={'True': 'green', 'Fake': 'red'})
                    st.plotly_chart(fig_pie)
                
                with col2:
                    fig_hist = px.histogram(results_df, 
                                          x='confidence',
                                          title="Confidence Score Distribution",
                                          nbins=20)
                    st.plotly_chart(fig_hist)
                
                st.subheader("Detailed Results")
                def color_predictions(val):
                    color = 'green' if val == 'True' else 'red'
                    return f'background-color: {color}'

                styled_df = results_df.style.applymap(color_predictions, subset=['prediction'])
                st.dataframe(styled_df)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
