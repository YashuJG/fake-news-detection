📰 Fake News Detection System
<div align="center">
Show Image
Show Image
Show Image
Show Image
Show Image
An AI-powered system that detects fake news in real-time with explainable predictions and visual insights.
</div>

🚀 Overview
The Fake News Detection System is a Machine Learning and NLP-based application that classifies news articles as True or Fake and provides detailed insights including confidence scores, sentiment analysis, readability metrics, word importance analysis, and word cloud visualizations.
The system supports both real-time single article analysis and batch processing of multiple articles through an interactive Streamlit interface.

✨ Key Features
🔍 Single Article Analysis

Instant text prediction with confidence score
Sentiment analysis (Positive / Negative / Neutral)
Readability score
Word importance visualization

📂 Batch Processing

Upload CSV, TXT, or XLSX files
Analyze multiple articles simultaneously
Summary statistics: total articles, true count, fake count
Graphical visualizations and detailed results table


🖥️ Application Screenshots
Home ScreenPrediction ResultShow ImageShow Image
Batch Analysis SummaryBatch URL AnalysisShow ImageShow Image
Word CloudWord Importance AnalysisShow ImageShow Image
Detailed ResultsShow Image

⚙️ System Architecture
Fake-News-Detection/
│
├── main.py                  # Streamlit UI & application entry point
├── text_processor.py        # NLP text preprocessing pipeline
├── train_model.py           # Model training & evaluation
├── test_url_functions.py    # URL validation & web scraping
├── test_url_analysis.py     # URL-based testing & error handling
│
├── model/                   # Saved trained model (joblib)
│
├── screenshots/
│   ├── Home screen.png
│   ├── fake or news.png
│   ├── batch analysis.png
│   ├── batch url analysis summary.png
│   ├── word cloud.png
│   ├── Word Importance Analysis.png
│   └── Detailed results.png
│
└── requirements.txt

🔬 Component Details
🧹 Text Processing — text_processor.py

Text cleaning (remove symbols, lowercase conversion)
Tokenization
Stopword removal
Stemming & Lemmatization

🤖 Model Training — train_model.py

Vectorization: TF-IDF
Algorithms Used:

✅ Random Forest (Best performing)
Logistic Regression


Evaluation Metrics: Accuracy, Precision, Recall, F1-Score
Cross-Validation: 5-Fold
Model persistence via joblib

🌐 URL Processing — test_url_functions.py

URL validation
Web scraping using BeautifulSoup
Metadata extraction (title, author, publish date)
OCR support for image-based text

🧪 Testing — test_url_analysis.py

Valid & invalid URL test cases
Error handling and retry mechanism

🖥️ Streamlit Interface — main.py

User-friendly, responsive UI
Real-time prediction results
Interactive charts and visualizations
Batch processing support


🛠️ Tech Stack
CategoryTechnologyLanguagePython 3.11FrontendStreamlitML Libraryscikit-learnNLPNLTKWeb ScrapingBeautifulSoup4Model Persistencejoblib

📊 Performance
MetricResult🎯 Accuracy94.59%🔁 Cross-Validation5-Fold⚡ InferenceReal-time📦 Batch Support✅ Yes

🧠 How It Works
Input Text / File Upload
        ↓
Text Preprocessing (cleaning, tokenization, stopword removal, stemming)
        ↓
TF-IDF Vectorization
        ↓
Random Forest Classification
        ↓
Results: Label + Confidence + Sentiment + Readability + Visualizations

▶️ Getting Started
1. Clone the Repository
bashgit clone https://github.com/your-username/fake-news-detection.git
cd fake-news-detection
2. Install Dependencies
bashpip install -r requirements.txt
3. Run the Application
bashstreamlit run main.py

🔮 Future Improvements

 Integrate BERT / Deep Learning models for higher accuracy
 Improve dataset balancing techniques
 Add real-time news API integration
 Deploy on cloud (AWS / Azure / GCP)
 Support multilingual news detection


👩‍💻 Author
Yasaswini Srigive
Feel free to ⭐ this repository if you found it useful!

<div align="center">
Made with ❤️ using Python & Streamlit
</div>
