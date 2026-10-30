from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", thinking_level="low")

def critique(finding):
    sources = "\n".join(finding["sources"]) or "none"
    prompt = (
        "You are a fair research critic. Judge this answer. "
        "Reply OK if it addresses the question and is backed by the listed sources, "
        "even if it admits some details are missing. "
        "Reply WEAK only if it ignores the question or has no sources. "
        "Reply with exactly one line: 'OK - reason' or 'WEAK - reason'.\n\n"
        f"Question: {finding['question']}\n"
        f"Answer: {finding['answer']}\n"
        f"Sources:\n{sources}"
    )
    return llm.invoke(prompt).text.strip()
if __name__ == "__main__":
    test = {"question": "What are the barriers to EVs in Tunisia?",
            "answer": "The sources do not detail this.",
            "sources": []}
    print(critique(test))