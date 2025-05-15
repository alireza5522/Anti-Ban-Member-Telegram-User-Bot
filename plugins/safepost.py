from plugins.functions import *
from .functions import *
import asyncio
from keys import OPEN_AI_API_KEY,LOG_PATH
import json
import aiohttp
import asyncio
import json

async def check_post(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
        "X-Title": "<YOUR_SITE_NAME>",  # Optional
    }

    data = {
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [
            {
                "role": "user",
                "content": f"""
You are a security guard for my Telegram channel. Each time, I will provide you with a post that an admin has submitted, and you must check it against the following rules:

1. The channel is serious, and no profanity or rude language should be present in the post.
2. Any promotion of other channels or groups is strictly prohibited. The channel's name is "sefrooyekk," and if the post contains any external advertisements, it must be removed.
3. The channel focuses on computers and cybersecurity. If a post contains a GitHub link or a source reference, and you determine it's not an advertisement, do NOT remove it.
4. The channel is about cybersecurity. If the post discusses hacking, security, or malware development, do NOT delete it—it is allowed.
5. Any form of defamation against the channel "sefrooyekk," its admins, or false accusations about them violates the rules, and the post must be removed.

Now, based on these rules, I will provide you with a post. If you determine the post should be removed, respond with **False**. If the post is acceptable, respond with **True**. Your response should be **ONLY** "True" or "False"—nothing else.

Post: {text}
"""
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()

            # Save the response to a file
            with open(f"{application_path}{LOG_PATH}", 'a+', encoding='utf-8') as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

            return result["choices"][0]["message"]["content"],result
        
