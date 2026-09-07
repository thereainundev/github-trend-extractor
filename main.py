import asyncio
from apify import Actor
import httpx

async def main():
    async with Actor:
        # 1. Tangkap input dari UI Dashboard Apify pembeli
        actor_input = await Actor.get_input() or {}
        topic = actor_input.get('topic', 'artificial-intelligence')
        max_items = actor_input.get('maxItems', 15)

        Actor.log.info(f"🚀 Menganalisis top {max_items} repositori untuk niche: '{topic}'...")

        # 2. Menggunakan GitHub Search API untuk data premium
        url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page={max_items}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            data = response.json()

        if "items" not in data:
            Actor.log.error("Gagal menarik data. Limit API atau koneksi bermasalah.")
            return

        # 3. Proses Ekstraksi & Pengayaan Data (Data Enrichment)
        insight_dataset = []
        for repo in data["items"]:
            # Kalkulasi sederhana untuk status aktivitas project
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

        # 4. Push ke Dataset Apify
        await Actor.push_data(insight_dataset)
        Actor.log.info(f"✅ Berhasil menyusun {len(insight_dataset)} data intelijen!")
