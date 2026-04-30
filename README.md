📰 Fake News Detection System
🚀 Project Overview

The Fake News Detection System is a Machine Learning and NLP-based application that classifies news articles as True or Fake and provides detailed insights such as:

✅ Confidence Score
✅ Sentiment Analysis
✅ Readability Score
✅ Word Importance Analysis
✅ Word Cloud Visualization

The system supports both real-time single article analysis and batch processing of multiple articles using an interactive Streamlit interface.

🎯 Key Features
🔍 Single Article Analysis
Text input for instant prediction
Confidence score display
Sentiment analysis
Readability score
Word importance visualization
📂 Batch Processing
Upload files (CSV, TXT, XLSX)
Analyze multiple articles at once
Summary statistics:
Total Articles
True News Count
Fake News Count
Graphical visualizations
Detailed results table
🖥️ Application Screenshots
1️⃣ Single Article Input

2️⃣ Prediction Result & Text Analysis

3️⃣ Batch Processing Upload

4️⃣ Batch Analysis Summary

5️⃣ Prediction Distribution

6️⃣ Confidence Score Distribution

7️⃣ Detailed Results Table

8️⃣ Word Cloud

9️⃣ Word Importance Analysis

⚙️ System Architecture
🔹 Text Processing (text_processor.py)
Text cleaning (remove symbols, lowercase)
Tokenization
Stopword removal
Stemming & Lemmatization
🔹 Model Training (train_model.py)
TF-IDF Vectorization
Algorithms used:
Random Forest (Best performing)
Logistic Regression
Evaluation metrics:
Accuracy: 94.59%
Precision, Recall, F1-score
Model saved using joblib
🔹 URL Processing (test_url_functions.py)
URL validation
Web scraping using BeautifulSoup
Metadata extraction (title, author, date)
OCR for image-based text
🔹 Testing (test_url_analysis.py)
Valid & invalid URL testing
Error handling and retry mechanism
🔹 Streamlit Interface (main.py)
User-friendly UI
Real-time prediction
Batch processing support
Interactive charts and visualizations
🛠️ Tech Stack
Language: Python 3.11
Frontend: Streamlit
ML Library: scikit-learn
NLP: NLTK
Web Scraping: BeautifulSoup4
📊 Performance
🎯 Accuracy: 94.59%
🔁 Cross-validation: 5-Fold
⚡ Fast real-time predictions
📦 Efficient batch processing
📁 Project Structure
Fake-News-Detection/
│
├── main.py
├── text_processor.py
├── train_model.py
├── test_url_functions.py
├── test_url_analysis.py
├── model/
├── screenshots/
│   ├── single_input.png
│   ├── prediction_result.png
│   ├── batch_upload.png
│   ├── batch_summary.png
│   ├── prediction_distribution.png
│   ├── confidence_distribution.png
│   ├── detailed_results.png
│   ├── word_cloud.png
│   └── word_importance.png
▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/fake-news-detection.git
cd fake-news-detection
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
streamlit run main.py
🧠 How It Works
Input text or upload file
Text is preprocessed using NLP techniques
TF-IDF converts text into numerical features
Random Forest model predicts True/Fake
Results displayed with:
Confidence score
Sentiment analysis
Visualizations
🔮 Future Improvements
🔹 Add BERT / Deep Learning model
🔹 Improve dataset balancing
🔹 Integrate real-time news APIs
🔹 Deploy on cloud (AWS / Azure)
💡 One-Line Pitch

AI-powered system that detects fake news in real-time with explainable predictions and visual insights.

📌 Author

Yasaswini Sri
