import asyncio
from apify import Actor
import httpx
import os
from datetime import datetime, timezone

async def send_telegram_alert(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        Actor.log.warning("⚠️ Telegram credentials not found in environment variables.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            Actor.log.info("🔥 [ENTERNEURAL] Telegram alpha briefing dispatched successfully.")
        else:
            Actor.log.error(f"❌ Failed to send Telegram alert: {response.text}")

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

        if master_intelligence_stream:
            sorted_alpha = sorted(master_intelligence_stream, key=lambda x: x["Growth Velocity (Stars/Day)"], reverse=True)[:3]
            msg = "🔥 *[ENTERNEURAL] Sovereign Alpha Briefing*\n\n"
            for i, repo in enumerate(sorted_alpha, 1):
                msg += f"*{i}. {repo['Repository Identifier']}*\n"
                msg += f"• Vector: `{repo['Entity Vector']}`\n"
                msg += f"• Velocity: `{repo['Growth Velocity (Stars/Day)']}` stars/day\n"
                msg += f"• Status: {repo['Vector Status']}\n"
                msg += f"• [View Repository]({repo['Repository URL']})\n\n"
            msg += "⚡ *System autonomous execution complete.*"
            await send_telegram_alert(msg)

if __name__ == '__main__':
    asyncio.run(main())
