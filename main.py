import asyncio
from apify import Actor
import httpx
from datetime import datetime, timezone

async def main():
    async with Actor:
        # 1. Autonomous Context Ingestion (Dynamic Market Targeting)
        actor_input = await Actor.get_input() or {}
        topic = actor_input.get('topic', 'artificial-intelligence')
        max_items = actor_input.get('maxItems', 20)

        Actor.log.info(f"⚡ [NEXUS-CORE] Initializing sovereign scan for sector: '{topic}' (Depth: {max_items})")

        url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page={max_items}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            data = response.json()

        if "items" not in data:
            Actor.log.error(f"❌ [NEXUS-CORE] Telemetry failure: {data}")
            return

        now = datetime.now(timezone.utc)
        intelligence_stream = []

        # 2. Autonomous Heuristic Analysis & Scoring Engine
        for repo in data["items"]:
            created_at_str = repo.get("created_at")
            pushed_at_str = repo.get("pushed_at")
            
            # Calculate repository age in days
            age_days = 1
            if created_at_str:
                created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                age_days = max(1, (now - created_at).days)

            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            open_issues = repo.get("open_issues_count", 0)

            # Heuristic Alpha Calculations
            velocity_score = round(stars / age_days, 2) # Stars gained per day
            adoption_ratio = round((forks / max(1, stars)) * 100, 2) # Fork-to-Star percentage
            
            # Autonomous Health & Market Valuation Logic
            if open_issues > 50 and velocity_score > 5:
                project_status = "🔥 Viral & High-Demand"
                commercial_alpha = "Tier-1 (Venture Fundable / High Utility)"
            elif velocity_score > 2:
                project_status = "🚀 Momentum Accelerating"
                commercial_alpha = "Tier-2 (Strong Community Growth)"
            else:
                project_status = "⚖️ Stable / Mature"
                commercial_alpha = "Tier-3 (Established Infrastructure)"

            intelligence_stream.append({
                "Repository Identifier": repo.get("full_name"),
                "Primary Stack": repo.get("language", "Multi-Language / Config"),
                "Total Stars": stars,
                "Growth Velocity (Stars/Day)": velocity_score,
                "Adoption Ratio (%)": adoption_ratio,
                "Open Issues (Community Load)": open_issues,
                "Core Project Status": project_status,
                "Commercial Alpha Rating": commercial_alpha,
                "Key Topics": ", ".join(repo.get("topics", [])[:6]),
                "Last Active Timestamp": pushed_at_str,
                "Repository Direct URL": repo.get("html_url"),
                "Executive Summary": repo.get("description") or "No executive summary provided by maintainers."
            })

        # 3. Secure Autonomous Delivery to Dataset Matrix
        await Actor.push_data(intelligence_stream)
        Actor.log.info(f"✅ [NEXUS-CORE] Successfully synthesized and deployed {len(intelligence_stream)} high-alpha intelligence vectors.")

if __name__ == '__main__':
    asyncio.run(main())
