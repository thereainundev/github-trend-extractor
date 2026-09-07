import asyncio
from apify import Actor
import httpx

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        topic = actor_input.get('topic', 'artificial-intelligence')
        max_items = actor_input.get('maxItems', 15)

        Actor.log.info(f"🚀 Menganalisis top {max_items} repositori untuk niche: '{topic}'...")

        url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page={max_items}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            data = response.json()

        if "items" not in data:
            Actor.log.error(f"Gagal menarik data: {data}")
            return

        insight_dataset = []
        for repo in data["items"]:
            status_aktif = "Sangat Aktif" if repo.get("open_issues_count", 0) > 50 else "Normal"
            
            insight_dataset.append({
                "Repository Name": repo.get("full_name"),
                "Primary Language": repo.get("language", "N/A"),
                "Stars": repo.get("stargazers_count"),
                "Forks (Adoption Rate)": repo.get("forks_count"),
                "Open Issues (Health)": repo.get("open_issues_count"),
                "Project Status": status_aktif,
                "Tags / Topics": ", ".join(repo.get("topics", [])[:5]), 
                "Last Updated": repo.get("pushed_at"),
                "URL": repo.get("html_url"),
                "Description": repo.get("description")
            })

        await Actor.push_data(insight_dataset)
        Actor.log.info(f"✅ Berhasil menyusun {len(insight_dataset)} data intelijen!")

# INI KUNCI KONTAK YANG SEBELUMNYA TERTINGGAL
if __name__ == '__main__':
    asyncio.run(main())
