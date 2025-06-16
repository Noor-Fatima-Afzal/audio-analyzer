import os
from groq import Groq

# Set your Groq API key as an environment variable
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

def call_groq_api(user_input):
    # Initialize the Groq client
    client = Groq()

    # Create the chat completion request
    try:
        completion = client.chat.completions.create(
            model="llama-3.2-1b-preview",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Collect the response chunks
        response_content = ""
        for chunk in completion:
            response_content += chunk.choices[0].delta.content or ""

        return {"response": response_content}  # Return the final response
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {"error": str(e)}  # Return error information
