import asyncio
import json
import os
import httpx

try:
    from apify import Actor
    HAS_APIFY = True
except ImportError:
    HAS_APIFY = False

async def main():
    keyword = os.getenv("KEYWORD", "artificial-intelligence")
    print(f"Mengambil data tren real-time dari GitHub untuk topik: {keyword}...")
    
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc"
    headers = {
        "User-Agent": "TermuxApifyActor/1.0",
        "Accept": "application/vnd.github.v3+json"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error {response.status_code}: Gagal mengambil data.")
            return

        data = response.json()

    results = []
    items = data.get("items", [])[:5]

    for item in items:
        results.append({
            "title": item.get("name"),
            "url": item.get("html_url"),
            "stars": item.get("stargazers_count"),
            "description": item.get("description"),
            "language": item.get("language")
        })

    if HAS_APIFY:
        async with Actor:
            await Actor.push_data(results)
            print(f"Berhasil push {len(results)} data ke Apify Dataset!")
    else:
        os.makedirs("storage/datasets/default", exist_ok=True)
        with open("storage/datasets/default/results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"Berhasil! {len(results)} data tersimpan di storage/datasets/default/results.json")

if __name__ == "__main__":
    asyncio.run(main())
