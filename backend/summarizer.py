import os
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Load environment variables from .env file if it exists
load_dotenv()

# Set your API key
os.environ['GROQ_API_KEY'] = "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"
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize the GROQ client with the API key
client = Groq(api_key=groq_api_key)

# Initialize the ChatGroq model
llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma-7b-It")

def summarize_text(text):
    # Prepare the chat message for summarization
    chat_message = [
        SystemMessage(content="You are an expert with expertise in summarizing text"),
        HumanMessage(content=f"Please provide a short and concise summary of the following text and give me a summary in a way that it should start with general phrase not like in this vedio or article etc.  :\n Text:{text}")
    ]
    
    # Get and return the summary
    return llm(chat_message).content
