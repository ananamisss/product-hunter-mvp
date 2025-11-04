import os, json, gspread, time, requests
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = os.environ["SHEET_ID"]
TELE_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELE_CHAT = os.environ["TELEGRAM_CHAT_ID"]

def auth_gs(json_content):
    creds_dict = json.loads(json_content)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

def append_rows(client, rows):
    sh = client.open_by_key(SHEET_ID)
    ws = sh.worksheet("candidates")
    for r in rows:
        ws.append_row([
            r["id"], r["source"], r["title"], r["url"], r.get("image",""),
            r.get("first_seen",""), r.get("views",0), r.get("favorites",0),
            r.get("orders",0), r.get("score",0), r.get("notes",""), ""
        ])
        time.sleep(0.4)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {"chat_id": TELE_CHAT, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception:
        pass

def publish(items, gservice_json):
    client = auth_gs(gservice_json)
    append_rows(client, items)
    for it in items:
        if it.get("score",0) >= 0.6:
            text = f"🔥 <b>{it['title'][:120]}</b>\nScore: {it['score']}\n{it['url'] or ''}"
            send_telegram(text)
