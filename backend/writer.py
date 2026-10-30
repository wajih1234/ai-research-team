from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", thinking_level="low")

def write_report(topic, findings):
    notes = ""
    for f in findings:
        notes += f"\nQuestion: {f['question']}\nFindings: {f['answer']}\nSources: {', '.join(f['sources'])}\n"
    prompt = (
        f"Write a short report in Markdown about: {topic}.\n"
        "Use a title, a one-paragraph summary, then one section per question. "
        "Use only the notes below. Cite sources as numbered links like [1](url). "
        "Do not invent facts.\n"
        f"{notes}"
    )
    return llm.invoke(prompt).text

if __name__ == "__main__":
    test = [{"question": "What are the barriers to EVs in Tunisia?",
             "answer": "Lack of charging stations and limited range are the main barriers.",
             "sources": ["https://example.com/study"]}]
    print(write_report("electric cars in Tunisia", test))