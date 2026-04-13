#!/usr/bin/env python3
# =============================================================
# SENTINEL INTELLIGENCE NETWORK — Fase 3
# JT SecureConsult | Bevelvoerder: SENTINEL-1
# Agente: PHANTOM | HAWK | JACKAL | MAMBA | AGITATOR | EAR
#         CONDOR | TRITON
# =============================================================

import os
import requests
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
OPENSKY_CLIENT_ID = os.environ.get("OPENSKY_CLIENT_ID")
OPENSKY_CLIENT_SECRET = os.environ.get("OPENSKY_CLIENT_SECRET")

REALTIME_INTERVAL = 1800

SA_LAT_MIN = -35.0
SA_LAT_MAX = -22.0
SA_LON_MIN = 16.0
SA_LON_MAX = 33.0

SALDANHA_LAT_MIN = -33.5
SALDANHA_LAT_MAX = -32.5
SALDANHA_LON_MIN = 17.5
SALDANHA_LON_MAX = 18.5

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
# PHANTOM — Cyber Intel
# =============================================================

def phantom_otx():
    try:
        requests.get(
            "https://otx.alienvault.com/api/v1/pulses/subscribed",
            headers={"X-OTX-KEY": "public"}, timeout=10)
        return "🔴 OTX Threat Feed: Aktief"
    except:
        return "⚫ OTX Threat Feed: Onbeskikbaar"

def phantom_cisa():
    try:
        r = requests.get(
            "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            timeout=10)
        vulns = r.json()['vulnerabilities'][:3]
        lines = ["⚠️ CISA KEV (Top 3):"]
        for v in vulns:
            lines.append(f"  • {v['cveID']}: {v['vulnerabilityName']}")
        return "\n".join(lines)
    except:
        return "⚫ CISA KEV: Onbeskikbaar"

def phantom_sa_csirt():
    try:
        feed = feedparser.parse("https://www.gov.za/rss.xml")
        keywords = ['cyber', 'security', 'breach', 'hack', 'ransomware', 'vulnerability']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "🇿🇦 SA Cyber Intel:\n" + "\n".join(items) if items else "🇿🇦 SA Cyber Intel: Geen nuwe insidente"
    except:
        return "🇿🇦 SA Cyber Intel: Feed onbeskikbaar"

def run_phantom():
    return "\n".join(["💻 PHANTOM — Cyber Intel", "─────────────────────────",
                      phantom_otx(), "", phantom_cisa(), "", phantom_sa_csirt()])

# =============================================================
# HAWK — Algemene Misdaad & Onrus
# =============================================================

def hawk_news24():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        keywords = ['crime','murder','shooting','robbery','arrested','protest','taxi',
                    'violence','unrest','hijack','cape town','western cape','wes-kaap',
                    'langebaan','saldanha','riot','attack']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:30]
                 if any(k in e.get('title','').lower() for k in keywords)][:5]
        return "📰 News24:\n" + "\n".join(items) if items else "📰 News24: Geen relevante insidente"
    except:
        return "📰 News24: Feed onbeskikbaar"

def hawk_saps():
    try:
        feed = feedparser.parse("https://www.saps.gov.za/newsroom/rss.php")
        items = [f"  • {e.get('title','')}" for e in feed.entries[:3]]
        return "🚔 SAPS Media:\n" + "\n".join(items) if items else "🚔 SAPS: Geen aankondigings"
    except:
        return "🚔 SAPS: Feed onbeskikbaar"

def hawk_arrive_alive():
    try:
        feed = feedparser.parse("https://www.arrivealive.mobi/rss/news")
        keywords = ['western cape','cape town','langebaan','saldanha','n7','n1',
                    'road closure','protest','blocked','accident','crash']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "🚗 Arrive Alive (WK):\n" + "\n".join(items) if items else "🚗 Arrive Alive: Geen WK insidente"
    except:
        return "🚗 Arrive Alive: Feed onbeskikbaar"

def run_hawk():
    return "\n".join(["🦅 HAWK — Misdaad & Onrus Intel", "─────────────────────────────────",
                      hawk_news24(), "", hawk_saps(), "", hawk_arrive_alive()])

# =============================================================
# JACKAL — Bendegeweld Spesialis
# =============================================================

def jackal_gangs():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        keywords = ['gang','bendes','anti-gang','nyanga','mitchells plain','delft',
                    'manenberg','hanover park','lavender hill','cape flats']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:30]
                 if any(k in e.get('title','').lower() for k in keywords)][:5]
        return "🔫 Bendegeweld Intel:\n" + "\n".join(items) if items else "🔫 Bendegeweld: Geen nuwe insidente"
    except:
        return "🔫 Bendegeweld: Feed onbeskikbaar"

def jackal_groundup():
    try:
        feed = feedparser.parse("https://groundup.org.za/feed/")
        keywords = ['gang','shooting','murder','violence','cape flats','western cape']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "📡 GroundUp:\n" + "\n".join(items) if items else "📡 GroundUp: Geen insidente"
    except:
        return "📡 GroundUp: Feed onbeskikbaar"

def run_jackal():
    return "\n".join(["🐺 JACKAL — Bendegeweld Spesialis", "───────────────────────────────────",
                      jackal_gangs(), "", jackal_groundup()])

# =============================================================
# MAMBA — Taxi Geweld Spesialis
# =============================================================

def mamba_taxi():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        keywords = ['taxi','minibus','santaco','taxi violence','taxi war',
                    'taxi strike','taxi protest','taxi shooting','taxi rank']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:30]
                 if any(k in e.get('title','').lower() for k in keywords)][:5]
        return "🚕 Taxi Geweld Intel:\n" + "\n".join(items) if items else "🚕 Taxi: Geen nuwe insidente"
    except:
        return "🚕 Taxi Intel: Feed onbeskikbaar"

def mamba_timeslive():
    try:
        feed = feedparser.parse("https://www.timeslive.co.za/rss/")
        keywords = ['taxi','strike','protest','western cape','cape town','road block']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "📰 TimesLive:\n" + "\n".join(items) if items else "📰 TimesLive: Geen taxi insidente"
    except:
        return "📰 TimesLive: Feed onbeskikbaar"

def run_mamba():
    return "\n".join(["🐍 MAMBA — Taxi Geweld Spesialis", "──────────────────────────────────",
                      mamba_taxi(), "", mamba_timeslive()])

# =============================================================
# AGITATOR — Politieke Onrus
# =============================================================

def agitator_protests():
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        keywords = ['protest','optog','march','unrest','shutdown','strike','eff',
                    'riot','looting','service delivery','toyi-toyi','destabiliz']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:30]
                 if any(k in e.get('title','').lower() for k in keywords)][:5]
        return "⚠️ Politieke Onrus:\n" + "\n".join(items) if items else "⚠️ Politieke Onrus: Geen aktiewe insidente"
    except:
        return "⚠️ Politieke Onrus: Feed onbeskikbaar"

def agitator_maverick():
    try:
        feed = feedparser.parse("https://www.dailymaverick.co.za/feed/")
        keywords = ['protest','unrest','strike','march','shutdown','western cape','riot']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "📡 Daily Maverick:\n" + "\n".join(items) if items else "📡 Daily Maverick: Geen onrus insidente"
    except:
        return "📡 Daily Maverick: Feed onbeskikbaar"

def run_agitator():
    return "\n".join(["🔥 AGITATOR — Politieke Onrus & Destabilisering",
                      "──────────────────────────────────────────────────",
                      agitator_protests(), "", agitator_maverick()])

# =============================================================
# EAR — Gemeenskap Intel
# =============================================================

def ear_community():
    try:
        feed = feedparser.parse("https://www.westerncape.gov.za/rss.xml")
        keywords = ['crime','safety','community','watch','police','cpf',
                    'langebaan','saldanha','vredenburg']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "👂 WK Gemeenskap:\n" + "\n".join(items) if items else "👂 Gemeenskap: Geen nuwe alerts"
    except:
        return "👂 Gemeenskap Intel: Feed onbeskikbaar"

def ear_mybroadband():
    try:
        feed = feedparser.parse("https://mybroadband.co.za/news/feed")
        keywords = ['crime','security','south africa','western cape','protest','strike']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "📡 MyBroadband:\n" + "\n".join(items) if items else "📡 MyBroadband: Geen insidente"
    except:
        return "📡 MyBroadband: Feed onbeskikbaar"

def run_ear():
    return "\n".join(["👂 EAR — Gemeenskap Intel", "──────────────────────────",
                      ear_community(), "", ear_mybroadband()])

# =============================================================
# CONDOR — Lugvaart Spesialis (OpenSky Network)
# =============================================================

def condor_get_token():
    try:
        r = requests.post(
            "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token",
            data={"grant_type": "client_credentials",
                  "client_id": OPENSKY_CLIENT_ID,
                  "client_secret": OPENSKY_CLIENT_SECRET},
            timeout=10)
        return r.json().get("access_token")
    except:
        return None

def condor_sa_flights():
    try:
        token = condor_get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.get(
            f"https://opensky-network.org/api/states/all"
            f"?lamin={SA_LAT_MIN}&lomin={SA_LON_MIN}"
            f"&lamax={SA_LAT_MAX}&lomax={SA_LON_MAX}",
            headers=headers, timeout=15)
        states = r.json().get('states', [])
        if not states:
            return "✈️ SA Lugvaart: Geen aktiewe vliegtuie"

        critical = []
        warnings = []
        total = len(states)

        for s in states:
            if not s:
                continue
            callsign = str(s[1]).strip() if s[1] else "Onbekend"
            squawk = str(s[14]) if len(s) > 14 and s[14] else ""
            lat = s[6]
            lon = s[5]
            altitude = s[7] or 0

            if squawk == "7500":
                critical.append(f"  🔴 KAPING: {callsign} | Squawk 7500")
            elif squawk == "7700":
                critical.append(f"  🔴 NOODGEVAL: {callsign} | Squawk 7700")
            elif squawk == "7600":
                warnings.append(f"  🟠 KOMMS VERLIES: {callsign} | Squawk 7600")

            if lat and lon:
                if SALDANHA_LAT_MIN <= lat <= SALDANHA_LAT_MAX and \
                   SALDANHA_LON_MIN <= lon <= SALDANHA_LON_MAX:
                    warnings.append(f"  🟡 FALA AREA: {callsign} | Alt: {int(altitude)}m")

        lines = [f"✈️ SA Lugvaart: {total} aktiewe vliegtuie"]
        if critical:
            lines.append("🔴 KRITIEKE ALERTS:")
            lines.extend(critical)
        if warnings:
            lines.append("🟠 WAARSKUWINGS:")
            lines.extend(warnings[:3])
        if not critical and not warnings:
            lines.append("  ✅ Geen abnormale aktiwiteit")
        return "\n".join(lines)
    except Exception as e:
        return f"✈️ Lugvaart data: Onbeskikbaar"

def condor_aviation_news():
    try:
        feed = feedparser.parse("https://www.avcom.co.za/phpBB3/feed.php")
        keywords = ['incident','accident','emergency','crash','south africa',
                    'cape town','langebaan','hijack','divert','mayday']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "📰 Lugvaart Nuus:\n" + "\n".join(items) if items else "📰 Lugvaart Nuus: Geen insidente"
    except:
        return "📰 Lugvaart Nuus: Feed onbeskikbaar"

def run_condor():
    return "\n".join(["✈️ CONDOR — Lugvaart Spesialis", "────────────────────────────────",
                      condor_sa_flights(), "", condor_aviation_news()])

# =============================================================
# TRITON — Marine & Kus Spesialis
# =============================================================

def triton_vessel_finder():
    try:
        feed = feedparser.parse("https://www.marinetraffic.com/rss/latest_vessels.rss")
        keywords = ['saldanha','cape town','south africa','distress','mayday',
                    'emergency','missing','aground','collision','sinking',
                    'drug','smuggling','trafficking']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() or
                        k in e.get('summary','').lower() for k in keywords)][:5]
        return "⚓ MarineTraffic:\n" + "\n".join(items) if items else "⚓ MarineTraffic: Geen insidente"
    except:
        return "⚓ MarineTraffic: Feed onbeskikbaar"

def triton_saldanha_monitor():
    try:
        token = condor_get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.get(
            f"https://opensky-network.org/api/states/all"
            f"?lamin={SALDANHA_LAT_MIN}&lomin={SALDANHA_LON_MIN}"
            f"&lamax={SALDANHA_LAT_MAX}&lomax={SALDANHA_LON_MAX}",
            headers=headers, timeout=15)
        states = r.json().get('states', [])
        if states:
            return f"🌊 Saldanha/Langebaan: {len(states)} lugvaart aktiwiteite"
        return "🌊 Saldanha/Langebaan: Geen abnormale aktiwiteit"
    except:
        return "🌊 Saldanha Area: Monitor onbeskikbaar"

def triton_marine_news():
    try:
        feed = feedparser.parse("https://www.portnews.ru/rss/")
        keywords = ['south africa','saldanha','cape town','distress',
                    'rescue','incident','drug','smuggling','trafficking']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "📰 Marine Nuus:\n" + "\n".join(items) if items else "📰 Marine Nuus: Geen SA insidente"
    except:
        return "📰 Marine Nuus: Feed onbeskikbaar"

def triton_mrcc():
    try:
        feed = feedparser.parse("https://www.transport.gov.za/rss.xml")
        keywords = ['maritime','vessel','ship','coast','sea','rescue',
                    'distress','mrcc','navy','marine']
        items = [f"  • {e.get('title','')}" for e in feed.entries[:20]
                 if any(k in e.get('title','').lower() for k in keywords)][:3]
        return "🆘 MRCC / Transport:\n" + "\n".join(items) if items else "🆘 MRCC: Geen noodseine"
    except:
        return "🆘 MRCC: Feed onbeskikbaar"

def run_triton():
    return "\n".join(["⚓ TRITON — Marine & Kus Spesialis",
                      "─────────────────────────────────────",
                      triton_vessel_finder(), "",
                      triton_saldanha_monitor(), "",
                      triton_marine_news(), "",
                      triton_mrcc()])

# =============================================================
# REAL-TIME KRITIEKE ALERT MONITOR
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
        'taxi blockade', 'mayday', 'vessel distress',
        'squawk 7500', 'squawk 7700', 'aircraft emergency'
    ]
    try:
        feed = feedparser.parse("https://feeds.news24.com/articles/news24/TopStories/rss")
        for entry in feed.entries[:20]:
            title = entry.get('title', '')
            entry_id = entry.get('id', title)
            if any(kw in title.lower() for kw in critical_keywords):
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
        except Exception as e:
            print(f"Monitor fout: {e}")
        time.sleep(REALTIME_INTERVAL)

# =============================================================
# SENTINEL-1 — VOLLEDIGE BRIEFING
# =============================================================

def compile_briefing():
    agente = ["PHANTOM", "HAWK", "JACKAL", "MAMBA", "AGITATOR", "EAR", "CONDOR", "TRITON"]
    sections = [
        sentinel_header(),
        run_phantom(), "",
        run_hawk(), "",
        run_jackal(), "",
        run_mamba(), "",
        run_agitator(), "",
        run_ear(), "",
        run_condor(), "",
        run_triton(),
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
        alert_msg = "🔴 SENTINEL — KRITIEKE ALERT\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
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

    print("✅ SENTINEL Fase 3 briefing gestuur!")

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
