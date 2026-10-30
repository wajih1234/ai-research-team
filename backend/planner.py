from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", thinking_level="low")

def plan(topic):
    prompt = f"Split this topic into 3 short research questions, one per line, no numbering: {topic}"
    return llm.invoke(prompt).text

if __name__ == "__main__":
    print(plan("electric cars in Tunisia"))