from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from search_tool import search

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", thinking_level="low")

def research(question):
    sources = search(question, n=3)
    if not sources:
        return {"question": question, "answer": "No sources found for this question.", "sources": []}
    context = "\n".join(f"- {s['title']}: {s['snippet']}" for s in sources)
    prompt = f"Answer in 3 sentences using only these sources.\n\nQuestion: {question}\n\nSources:\n{context}"
    answer = llm.invoke(prompt).text
    return {"question": question, "answer": answer, "sources": [s["url"] for s in sources]}

if __name__ == "__main__":
    print(research("What are the barriers to electric vehicle adoption in Tunisia?"))