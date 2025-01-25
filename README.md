# Tweet Sentiment Analysis Application

This repository contains a Flask-based web application that performs sentiment analysis on Twitter text extracted via a URL. The project uses a pre-trained sentiment classifier, text preprocessing techniques, and integrates with a PostgreSQL database to store and display analysis results.

## Features

- **Sentiment Analysis**: Predicts whether the sentiment of the input text is positive or negative.
- **Text Preprocessing**: Cleans the text by removing noise, lemmatizing words, and filtering stopwords.
- **Twitter URL Parsing**: Extracts tweets from the provided Twitter URL.
- **Data Storage**: Saves analysis results in a PostgreSQL database.
- **Visualization**: Generates a bar chart summarizing the text analysis.
- **Admin Panel**: Displays stored analysis data with password-protected access.

---

## Prerequisites

1. **Python**: Make sure Python is installed (version 3.7 or higher).
2. **PostgreSQL**: Install and configure PostgreSQL.
3. **Dependencies**: Install the required Python libraries (see [Requirements](#requirements)).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up PostgreSQL**:
   - Create a database named `country_5aym`.
   - Add a user `amit` with the password `J6O5kkf7wCcsGeN7XAgKWbL4rsMves0W`.
   - Ensure the database connection matches the settings in the code.

4. **Download NLTK Resources**:
   - NLTK resources like `stopwords`, `averaged_perceptron_tagger`, `wordnet`, and `opinion_lexicon` will be downloaded automatically when the app runs.

---

## Configuration

### Database Schema

The PostgreSQL table `analysis_results` is created with the following schema:
```sql
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    text TEXT,
    cleaned_text TEXT,
    total_words INT,
    total_sentences INT,
    positive_words INT,
    negative_words INT,
    sentiment VARCHAR(10)
);
```

---

## Usage

1. **Start the Flask App**:
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

2. **Perform Sentiment Analysis**:
   - Navigate to the home page.
   - Enter a Twitter URL and your name.
   - Submit the form to see the sentiment analysis results.

3. **Admin Panel**:
   - Navigate to `/admin`.
   - Enter the password (`amit`) to view stored analysis data.

---

## File Structure

```
.
|-- app.py                # Main Flask application
|-- templates/            # HTML templates for the web interface
|   |-- index.html        # Home page
|   |-- result.html       # Result display page
|   |-- admin.html        # Admin login page
|   |-- detail.html       # Table view for admin data
|-- static/               # Static files (CSS, JS, etc.)
|-- sentiment_classifier.pickle # Pre-trained sentiment analysis model
```

---

## Requirements

Install the required dependencies using:
```bash
pip install -r requirements.txt
```
**Dependencies:**
- Flask
- NLTK
- psycopg2
- matplotlib
- selenium

---

## Security Notes

1. **Database Credentials**:
   Ensure that sensitive information like database credentials is stored securely. Consider using environment variables or a configuration management tool.
2. **Admin Password**:
   The admin password should be hashed and stored securely, not hardcoded in the application.

---

## Future Improvements

- Add better error handling for database connections and input validation.
- Use a more advanced sentiment analysis model.
- Implement secure authentication for the admin panel.
- Optimize text processing for performance.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

