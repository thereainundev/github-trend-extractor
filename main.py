import asyncio
from apify import Actor
import httpx
from datetime import datetime, timezone

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        topics = actor_input.get('topics', ['artificial-intelligence', 'agentic-workflows', 'distributed-systems'])
        max_items_per_topic = actor_input.get('maxItemsPerTopic', 10)

        Actor.log.info(f"🧠 [ENTERNEURAL] Activating multi-vector sovereign matrix across topics: {topics}")

        async with httpx.AsyncClient() as client:
            master_intelligence_stream = []

            for topic in topics:
                url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page={max_items_per_topic}"
                headers = {"Accept": "application/vnd.github.v3+json"}
                
                response = await client.get(url, headers=headers)
                data = response.json()

                if "items" not in data:
                    Actor.log.warning(f"⚠️ [ENTERNEURAL] Telemetry disruption on vector '{topic}': {data.get('message', 'Unknown error')}")
                    continue

                now = datetime.now(timezone.utc)

                for repo in data["items"]:
                    created_at_str = repo.get("created_at")
                    pushed_at_str = repo.get("pushed_at")
                    
                    age_days = 1
                    if created_at_str:
                        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                        age_days = max(1, (now - created_at).days)

                    stars = repo.get("stargazers_count", 0)
                    forks = repo.get("forks_count", 0)
                    open_issues = repo.get("open_issues_count", 0)

                    velocity_score = round(stars / age_days, 2)
                    adoption_ratio = round((forks / max(1, stars)) * 100, 2)
                    
                    if open_issues > 40 and velocity_score > 4:
                        vector_status = "🔥 Hyper-Growth Vector"
                        commercial_alpha = "Tier-1 (Venture Institutional Grade)"
                    elif velocity_score > 1.5:
                        vector_status = "🚀 Momentum Accelerating"
                        commercial_alpha = "Tier-2 (Strong Developer Adoption)"
                    else:
                        vector_status = "⚖️ Stable Infrastructure"
                        commercial_alpha = "Tier-3 (Core Utility)"

                    master_intelligence_stream.append({
                        "Entity Vector": topic,
                        "Repository Identifier": repo.get("full_name"),
                        "Primary Stack": repo.get("language", "Config/Multi"),
                        "Total Stars": stars,
                        "Growth Velocity (Stars/Day)": velocity_score,
                        "Adoption Ratio (%)": adoption_ratio,
                        "Open Issues Load": open_issues,
                        "Vector Status": vector_status,
                        "Commercial Alpha Rating": commercial_alpha,
                        "Key Technical Tags": ", ".join(repo.get("topics", [])[:5]),
                        "Last Active Timestamp": pushed_at_str,
                        "Repository URL": repo.get("html_url"),
                        "Executive Summary": repo.get("description") or "No description provided."
                    })

        await Actor.push_data(master_intelligence_stream)
        Actor.log.info(f"⚡ [ENTERNEURAL] Synchronization complete. Deployed {len(master_intelligence_stream)} alpha vectors into dataset matrix.")

if __name__ == '__main__':
    asyncio.run(main())
