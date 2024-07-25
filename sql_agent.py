from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv, find_dotenv
import os
import warnings

# Filtering the warnings
warnings.filterwarnings("ignore")

load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Initialilze database
db = SQLDatabase.from_uri("sqlite:///employee_database.db")

# function to get schema
def get_schema(_):
    return db.get_table_info()

# function to run query
def run_query(query):
    return db.run(query)

def get_final_query(query):
    print(query)
    return query.replace("`","").replace("sql", "")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=GOOGLE_API_KEY)

# Update the template based on the type of SQL Database like MySQL, Microsoft SQL Server and so on
template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""

# Creating a prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Given an input question, convert it to a SQL query. No pre-amble. Only return the query."),
        ("human", template),
    ]
)

# Creating a chain for the SQL query response
sql_response = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
    | RunnableLambda(get_final_query)
)

    
# Chain to answer
template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""

# Creating a prompt for generating natural language response
prompt_response = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question and SQL response, convert it to a natural language answer. No pre-amble.",
        ),
        ("human", template),
    ]
)

# Adding both the chains to create a full chain
full_chain = (
    RunnablePassthrough.assign(query=sql_response)
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response
    | llm
    | StrOutputParser()
)

# print(full_chain.invoke({"question": "What are the top 5 salaries? I want their names, position, department and salary."}))



