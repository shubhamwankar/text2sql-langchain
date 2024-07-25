# Text 2 SQL LLM App

![Text2SQL Bot](/text2sqlbot.jpg)
This project implements a natural language interface for querying SQL databases using advanced language models and AI technologies.

## Technologies Used

- Gemini 1.5 Flash LLM
- Langchain
- SQLAlchemy
- Streamlit

## Project Structure

![Text2SQL Process Flow](/Text2SQL%20App%20Process%20Flow.png)

The project consists of three main files:

1. `dummy_db.py`: Creates a dummy SQLite database using SQLAlchemy.
2. `sql_agent.py`: Contains the main logic for converting natural language questions to SQL queries, executing them, and generating natural language responses.
3. `app.py`: Implements a Streamlit-based chat interface for interacting with the SQL agent.

## File Descriptions

### dummy_db.py

This script sets up a sample SQLite database using SQLAlchemy. It creates tables and populates them with dummy data for testing and demonstration purposes.

### sql_agent.py

The core of the application, this file uses Langchain to:

- Convert user questions into SQL queries using the Gemini 1.5 Flash LLM
- Execute the generated SQL queries against the database
- Transform the query results back into natural language responses using the Gemini LLM

### app.py

A Streamlit application that provides a user-friendly chat interface for interacting with the SQL agent. Users can input questions in natural language and receive responses based on the database content.

## Setup and Usage

1. Clone the repo using the following command.

```git
github.com/shubhamwankar/text2sql_langchain.git
```

2. Install the dependencies using the following command.

```pip
pip install -r requirements.txt
```

3. [Setup your own Google API Key](https://ai.google.dev/gemini-api/docs/api-key) for using Gemini API. (it's free)
4. Create .env variable and add the GOOGLE_API_KEY for reference.

```terminal
touch .env
```

Inside .env file add the following

```.env
GOOGLE_API_KEY="enter_your_api_key"
```

3. Run the following command in terminal to create a dummy database. [Optional]

```bash
python dummy_db.py
```

4. Run the below command to start the LLM app.

```streamlit
streamlit run app.py
```
