#!/usr/bin/env python3
# =============================================================
# SENTINEL INTELLIGENCE NETWORK — Fase 2
# JT SecureConsult | Bevelvoerder: SENTINEL-1
# Agente: PHANTOM | HAWK | JACKAL | MAMBA | AGITATOR | EAR
# =============================================================

import os
import feedparser
import asyncio
import threading
import time
from datetime import datetime
from telegram import Bot

# =============================================================
# KONFIGURASIE
# =============================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = "1049427763"

# Real-time monitor interval (sekondes) — elke 30 minute
REALTIME_INTERVAL = 1800

# =============================================================
# SENTINEL-1 — BEVELVOERDER
# =============================================================

def sentinel_header():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    return (
        "🛡️ SENTINEL INTELLIGENCE NETWORK\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎖️ SENTINEL-1 — Bevelvoerder\n"
        f"📅 {now} SAST\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    )

def sentinel_footer(agente):
    agent_str = " | ".join([f"{a} aktief" for a in agente])
    return (
        "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ SENTINEL-1 — Operasioneel\n"
        f"🤖 {agent_str}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

# =============================================================
# PHANTOM — Cyber Intel Agent
# =============================================================

def phantom_otx():
    try:
        r = requests.get(
            "https://otx.alienvault.com/api/v1/pulses/subscribed",
            headers={"X-OTX-KEY": "public"},
            timeout=10
        )
        return "🔴 OTX Threat Feed: Aktief"
    except:
        return "⚫ OTX Threat Feed: Onbeskikbaar"

def phantom_cisa():
    try:
        r = requests.get(
            "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            timeout=10
        )
        data = r.json()
        vulns = data['vulnerabilities'][:3]
        lines = ["⚠️ CISA KEV (Top 3):"]
        for v in vulns:
            lines.append(f"  • {v['cveID']}: {v['vulnerabilityName']}")
        return "\n".join(lines)
    except:
        return "⚫ CISA KEV: Onbeskikbaar"

def phantom_sa_csirt():
    try:
        feed = feedparser.parse("https://www.gov.za/rss.xml")
        items = []
        keywords = ['cyber', 'security', 'breach', 'hack', 'ransomware', 'vulnerability']
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "🇿🇦 SA Cyber Intel:\n" + "\n".join(items)
        else:
            return "🇿🇦 SA Cyber Intel: Geen nuwe insidente"
    except:
        return "🇿🇦 SA Cyber Intel: Feed onbeskikbaar"

def run_phantom():
    return "\n".join([
        "💻 PHANTOM — Cyber Intel",
        "─────────────────────────",
        phantom_otx(),
        "",
        phantom_cisa(),
        "",
        phantom_sa_csirt(),
    ])

# =============================================================
# HAWK — Algemene Misdaad & Onrus
# =============================================================

def hawk_news24():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        items = []
        keywords = [
            'crime', 'murder', 'shooting', 'robbery', 'arrested',
            'protest', 'taxi', 'violence', 'unrest', 'hijack',
            'cape town', 'western cape', 'wes-kaap', 'langebaan',
            'saldanha', 'riot', 'attack', 'aanval', 'misdaad'
        ]
        count = 0
        for entry in feed.entries[:30]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 5:
                break
        if items:
            return "📰 News24:\n" + "\n".join(items)
        else:
            return "📰 News24: Geen relevante insidente"
    except:
        return "📰 News24: Feed onbeskikbaar"

def hawk_saps():
    try:
        feed = feedparser.parse("https://www.saps.gov.za/newsroom/rss.php")
        items = []
        count = 0
        for entry in feed.entries[:10]:
            items.append(f"  • {entry.get('title', 'Onbekend')}")
            count += 1
            if count >= 3:
                break
        if items:
            return "🚔 SAPS Media:\n" + "\n".join(items)
        else:
            return "🚔 SAPS: Geen nuwe aankondigings"
    except:
        return "🚔 SAPS: Feed onbeskikbaar"

def hawk_arrive_alive():
    try:
        feed = feedparser.parse("https://www.arrivealive.mobi/rss/news")
        items = []
        keywords = [
            'western cape', 'cape town', 'wes-kaap', 'langebaan',
            'saldanha', 'n7', 'n1', 'road closure', 'protest',
            'blocked', 'accident', 'crash'
        ]
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "🚗 Arrive Alive (WK):\n" + "\n".join(items)
        else:
            return "🚗 Arrive Alive: Geen WK insidente"
    except:
        return "🚗 Arrive Alive: Feed onbeskikbaar"

def run_hawk():
    return "\n".join([
        "🦅 HAWK — Misdaad & Onrus Intel",
        "─────────────────────────────────",
        hawk_news24(),
        "",
        hawk_saps(),
        "",
        hawk_arrive_alive(),
    ])

# =============================================================
# JACKAL — Bendegeweld Spesialis
# =============================================================

def jackal_gangs():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        items = []
        keywords = [
            'gang', 'bendes', 'bende', 'anti-gang', 'nyanga',
            'mitchells plain', 'delft', 'manenberg', 'hanover park',
            'lavender hill', 'steenberg', 'philippi', 'gang shooting',
            'cape flats', 'kaapse vlakte'
        ]
        count = 0
        for entry in feed.entries[:30]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 5:
                break
        if items:
            return "🔫 Bendegeweld Intel:\n" + "\n".join(items)
        else:
            return "🔫 Bendegeweld: Geen nuwe insidente"
    except:
        return "🔫 Bendegeweld: Feed onbeskikbaar"

def jackal_groundup():
    try:
        feed = feedparser.parse("https://groundup.org.za/feed/")
        items = []
        keywords = [
            'gang', 'shooting', 'murder', 'violence', 'cape flats',
            'western cape', 'anti-gang unit', 'police'
        ]
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "📡 GroundUp:\n" + "\n".join(items)
        else:
            return "📡 GroundUp: Geen relevante insidente"
    except:
        return "📡 GroundUp: Feed onbeskikbaar"

def run_jackal():
    return "\n".join([
        "🐺 JACKAL — Bendegeweld Spesialis",
        "───────────────────────────────────",
        jackal_gangs(),
        "",
        jackal_groundup(),
    ])

# =============================================================
# MAMBA — Taxi Geweld Spesialis
# =============================================================

def mamba_taxi():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        items = []
        keywords = [
            'taxi', 'minibus', 'santaco', 'taxi violence',
            'taxi war', 'taxi strike', 'taxi protest',
            'taxi association', 'taxi shooting', 'taxi rank',
            'taxi conflict', 'taxi route', 'taxi industry'
        ]
        count = 0
        for entry in feed.entries[:30]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 5:
                break
        if items:
            return "🚕 Taxi Geweld Intel:\n" + "\n".join(items)
        else:
            return "🚕 Taxi Sektor: Geen nuwe insidente"
    except:
        return "🚕 Taxi Intel: Feed onbeskikbaar"

def mamba_timeslive():
    try:
        feed = feedparser.parse("https://www.timeslive.co.za/rss/")
        items = []
        keywords = [
            'taxi', 'strike', 'protest', 'western cape',
            'cape town', 'road block', 'padafsluiting'
        ]
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "📰 TimesLive (Taxi):\n" + "\n".join(items)
        else:
            return "📰 TimesLive: Geen taxi insidente"
    except:
        return "📰 TimesLive: Feed onbeskikbaar"

def run_mamba():
    return "\n".join([
        "🐍 MAMBA — Taxi Geweld Spesialis",
        "──────────────────────────────────",
        mamba_taxi(),
        "",
        mamba_timeslive(),
    ])

# =============================================================
# AGITATOR — Politieke Onrus & Destabilisering
# =============================================================

def agitator_protests():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        items = []
        keywords = [
            'protest', 'optog', 'march', 'demonstration', 'unrest',
            'shutdown', 'strike', 'staking', 'eff', 'riot', 'looting',
            'community protest', 'service delivery', 'toyi-toyi',
            'western cape protest', 'cape town protest', 'destabiliz'
        ]
        count = 0
        for entry in feed.entries[:30]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 5:
                break
        if items:
            return "⚠️ Politieke Onrus Intel:\n" + "\n".join(items)
        else:
            return "⚠️ Politieke Onrus: Geen aktiewe insidente"
    except:
        return "⚠️ Politieke Onrus: Feed onbeskikbaar"

def agitator_maverick():
    try:
        feed = feedparser.parse("https://www.dailymaverick.co.za/feed/")
        items = []
        keywords = [
            'protest', 'unrest', 'strike', 'march', 'shutdown',
            'western cape', 'cape town', 'destabiliz', 'riot'
        ]
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "📡 Daily Maverick:\n" + "\n".join(items)
        else:
            return "📡 Daily Maverick: Geen onrus insidente"
    except:
        return "📡 Daily Maverick: Feed onbeskikbaar"

def run_agitator():
    return "\n".join([
        "🔥 AGITATOR — Politieke Onrus & Destabilisering",
        "──────────────────────────────────────────────────",
        agitator_protests(),
        "",
        agitator_maverick(),
    ])

# =============================================================
# EAR — Gemeenskap Intel Agent
# =============================================================

def ear_community():
    try:
        feed = feedparser.parse("https://www.westerncape.gov.za/rss.xml")
        items = []
        keywords = [
            'crime', 'safety', 'community', 'neighbourhood',
            'watch', 'police', 'cpf', 'security', 'alert',
            'langebaan', 'saldanha', 'vredenburg', 'western cape'
        ]
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "👂 WK Gemeenskap Intel:\n" + "\n".join(items)
        else:
            return "👂 Gemeenskap: Geen nuwe alerts"
    except:
        return "👂 Gemeenskap Intel: Feed onbeskikbaar"

def ear_mybroadband():
    try:
        feed = feedparser.parse("https://mybroadband.co.za/news/feed")
        items = []
        keywords = [
            'crime', 'security', 'south africa', 'western cape',
            'protest', 'strike', 'unrest', 'loadshedding'
        ]
        count = 0
        for entry in feed.entries[:20]:
            title = entry.get('title', '').lower()
            if any(kw in title for kw in keywords):
                items.append(f"  • {entry.get('title', 'Onbekend')}")
                count += 1
            if count >= 3:
                break
        if items:
            return "📡 MyBroadband:\n" + "\n".join(items)
        else:
            return "📡 MyBroadband: Geen relevante insidente"
    except:
        return "📡 MyBroadband: Feed onbeskikbaar"

def run_ear():
    return "\n".join([
        "👂 EAR — Gemeenskap Intel",
        "──────────────────────────",
        ear_community(),
        "",
        ear_mybroadband(),
    ])

# =============================================================
# REAL-TIME KRITIEKE ALERT MONITOR
# Loop elke 30 minute
# =============================================================

sent_alerts = set()

def check_critical_alerts():
    alerts = []
    critical_keywords = [
        'langebaan', 'saldanha', 'vredenburg',
        'western cape shooting', 'cape town riot',
        'taxi violence western cape', 'protest n7',
        'gang western cape', 'bomb', 'explosion',
        'hostage', 'mass shooting', 'terrorist',
        'road closure western cape', 'n7 closed',
        'taxi blockade', 'padafsluiting wes-kaap'
    ]
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        for entry in feed.entries[:20]:
            title = entry.get('title', '')
            title_lower = title.lower()
            entry_id = entry.get('id', title)
            if any(kw in title_lower for kw in critical_keywords):
                if entry_id not in sent_alerts:
                    alerts.append(title)
                    sent_alerts.add(entry_id)
    except:
        pass
    return alerts

async def send_critical_alert(alert_list):
    bot = Bot(token=TELEGRAM_TOKEN)
    msg = (
        "🔴 SENTINEL — KRITIEKE ALERT\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ {datetime.now().strftime('%H:%M')} SAST\n"
    )
    for a in alert_list:
        msg += f"⚠️ {a}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    await bot.send_message(chat_id=CHAT_ID, text=msg)

def realtime_monitor_loop():
    print("🔴 Real-time monitor geaktiveer...")
    while True:
        try:
            alerts = check_critical_alerts()
            if alerts:
                asyncio.run(send_critical_alert(alerts))
                print(f"⚠️ Kritieke alert gestuur: {len(alerts)} insidente")
        except Exception as e:
            print(f"Real-time monitor fout: {e}")
        time.sleep(REALTIME_INTERVAL)

# =============================================================
# SENTINEL-1 — VOLLEDIGE BRIEFING
# =============================================================

def compile_briefing():
    agente = ["PHANTOM", "HAWK", "JACKAL", "MAMBA", "AGITATOR", "EAR"]
    sections = [
        sentinel_header(),
        run_phantom(),
        "",
        run_hawk(),
        "",
        run_jackal(),
        "",
        run_mamba(),
        "",
        run_agitator(),
        "",
        run_ear(),
        sentinel_footer(agente)
    ]
    return "\n".join(sections)

# =============================================================
# TELEGRAM UITSTUUR
# =============================================================

async def send_briefing():
    bot = Bot(token=TELEGRAM_TOKEN)

    alerts = check_critical_alerts()
    if alerts:
        alert_msg = (
            "🔴 SENTINEL — KRITIEKE ALERT\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        for a in alerts:
            alert_msg += f"⚠️ {a}\n"
        alert_msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        await bot.send_message(chat_id=CHAT_ID, text=alert_msg)

    message = compile_briefing()

    if len(message) > 4096:
        parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
        for part in parts:
            await bot.send_message(chat_id=CHAT_ID, text=part)
            await asyncio.sleep(1)
    else:
        await bot.send_message(chat_id=CHAT_ID, text=message)

    print("✅ SENTINEL Fase 2 briefing gestuur!")

# =============================================================
# HOOF UITVOERING
# =============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        print("🛡️ SENTINEL Real-time Monitor — Aktief")
        monitor_thread = threading.Thread(target=realtime_monitor_loop, daemon=True)
        monitor_thread.start()
        while True:
            time.sleep(60)
    else:
        asyncio.run(send_briefing())
