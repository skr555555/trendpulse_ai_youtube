# TrendPulse AI (YouTube Edition) 📈

TrendPulse AI is a dynamic analytics platform to monitor, analyze, and predict trends from **YouTube** using user-defined keywords. It analyzes video comments, tracks popular channels, and identifies trending topics.

## MLOps Features
- **Containerization:** Packaged with Docker for consistent deployment.
- **CI/CD:** Automated testing and linting with GitHub Actions.
- **Multilingual Cleaning:** Handles stopwords and characters for multiple languages.
- **Experiment Tracking:** Uses MLflow to track model training runs.

## Setup Instructions

1.  **Clone the repository and navigate into it.**

2.  **Enable the YouTube Data API v3:**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Go to "APIs & Services" > "Library".
    - Search for and enable the **"YouTube Data API v3"**.
    - Go to "APIs & Services" > "Credentials".
    - Click "Create Credentials" > "API key". Copy the key.

3.  **Configure API Key:**
    - Open `config.py` and paste your API key.

4.  **Install dependencies (local setup):**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Download NLTK data:**
    In a Python shell, run:
    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    ```

## How to Run

### Local Development
1.  Ensure a MongoDB instance is accessible.
2.  Run the Streamlit app: `streamlit run app.py`

### Running with Docker (Recommended)
1.  Build and run: `docker-compose up --build`
2.  Open your browser to `http://localhost:8501`.

### Experiment Tracking
1.  Train a model: `python src/training/train_model.py`
2.  Launch UI: `mlflow ui` (view at `http://localhost:5000`)