import time
from ddgs import DDGS

def search(query, n=3):
    for attempt in range(3):
        try:
            results = DDGS().text(query, max_results=n)
            return [{"title": r["title"], "url": r["href"], "snippet": r["body"]} for r in results]
        except Exception:
            time.sleep(2)
    return []

if __name__ == "__main__":
    for r in search("electric vehicles Tunisia"):
        print(r["title"], "-", r["url"])