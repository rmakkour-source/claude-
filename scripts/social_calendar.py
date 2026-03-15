#!/usr/bin/env python3
"""
BingeBear 30-Day Sports & Social Calendar Generator
Generates content pillars specifically targeting 40-65 yr old UK/Irish men.
"""
import sys
import json
from datetime import datetime, timedelta

def generate_calendar():
    platforms =["Facebook (Primary)", "WhatsApp Status", "Twitter/X"]
    
    calendar = {
        "target_audience": "UK/Irish Men aged 40-65",
        "core_goal": "Push 24-Hour Free Trials via WhatsApp",
        "content_pillars": {
            "Match Day Hype": "Urgency posts 3 hours before Premier League / GAA matches.",
            "Anti-Sky Rants": "Agitating the pain of expensive contracts and bills.",
            "Setup Simplicity": "Showing how easy it is to install on a Firestick.",
            "Social Proof": "Screenshots of 4.8 Trustpilot reviews and happy WhatsApp chats."
        },
        "hook_formulas":[
            "Sick of paying Sky £100 a month just to watch your team? 🛑",
            "To the 2,843 people streaming the match right now with zero buffering... enjoy! 🍻",
            "Not great with technology? We'll set it up for you on WhatsApp in 5 mins."
        ],
        "schedule": []
    }

    pillar_rotation =["Anti-Sky Rants", "Setup Simplicity", "Match Day Hype", "Social Proof"]
    
    start_date = datetime.now()
    for day in range(30):
        date = start_date + timedelta(days=day)
        pillar = pillar_rotation[day % len(pillar_rotation)]
        
        calendar["schedule"].append({
            "day": day + 1,
            "date": date.strftime("%Y-%m-%d"),
            "focus": pillar,
            "action": f"Post to {platforms[day % 3]} highlighting {pillar}."
        })

    return calendar

if __name__ == "__main__":
    print(json.dumps(generate_calendar(), indent=2))
