import requests
import json

def load_filters():
    try:
        with open('filters.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"title": "", "location": "", "keywords": []}

def scrape_jobs():
    filters = load_filters()

    try:
        response = requests.get("https://remoteok.io/api", headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print("API error:", response.status_code)
            return []
    except Exception as e:
        print("Request failed:", e)
        return []

    data = response.json()
    jobs = []

    for job in data[1:]:  # skip the metadata at index 0
        title = job.get("position", "")
        location = job.get("location", "")
        description = job.get("description", "")

        if filters["title"].lower() not in title.lower():
            continue
        if filters["location"].lower() not in location.lower():
            continue
        if filters["keywords"]:
            if not any(k.lower() in description.lower() for k in filters["keywords"]):
                continue

        jobs.append({
            "title": title,
            "company": job.get("company", ""),
            "location": location,
            "url": job.get("url", "")
        })

    return jobs
