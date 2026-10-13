"""Regenerate earnings.ics from Yahoo Finance earnings dates."""
import datetime
import hashlib

import yfinance as yf

# label -> Yahoo Finance symbol
TICKERS = {
    "AMD": "AMD", "INTC": "INTC", "MU": "MU", "NVDA": "NVDA", "AVGO": "AVGO",
    "MRVL": "MRVL", "ADI": "ADI", "AMAT": "AMAT", "KLAC": "KLAC", "TXN": "TXN",
    "LRCX": "LRCX", "QCOM": "QCOM", "MPWR": "MPWR", "TER": "TER", "TSM": "TSM",
    "NXPI": "NXPI", "SKHY": "000660.KS", "ALAB": "ALAB", "MCHP": "MCHP",
    "CRDO": "CRDO", "ON": "ON", "ASML": "ASML", "ENTG": "ENTG", "TSEM": "TSEM",
    "MTSI": "MTSI", "ASX": "ASX", "CBRS": "CBRS", "UMC": "UMC", "ARM": "ARM",
    "STM": "STM", "NOK": "NOK", "WDC": "WDC", "SNDK": "SNDK", "STX": "STX",
    "LITE": "LITE", "COHR": "COHR", "META": "META", "HIMS": "HIMS",
    "MSFT": "MSFT", "GOOG": "GOOGL", "AMZN": "AMZN",
}

NAMES = {
    "AMD": "AMD", "INTC": "Intel", "MU": "Micron", "NVDA": "NVIDIA",
    "AVGO": "Broadcom", "MRVL": "Marvell", "ADI": "Analog Devices",
    "AMAT": "Applied Materials", "KLAC": "KLA", "TXN": "Texas Instruments",
    "LRCX": "Lam Research", "QCOM": "Qualcomm", "MPWR": "Monolithic Power",
    "TER": "Teradyne", "TSM": "TSMC", "NXPI": "NXP", "SKHY": "SK Hynix",
    "ALAB": "Astera Labs", "MCHP": "Microchip", "CRDO": "Credo",
    "ON": "ON Semi", "ASML": "ASML", "ENTG": "Entegris", "TSEM": "Tower Semi",
    "MTSI": "MACOM", "ASX": "ASE", "CBRS": "Cerebras", "UMC": "UMC",
    "ARM": "Arm", "STM": "STMicro", "NOK": "Nokia", "WDC": "Western Digital",
    "SNDK": "Sandisk", "STX": "Seagate", "LITE": "Lumentum",
    "COHR": "Coherent", "META": "Meta", "HIMS": "Hims & Hers",
    "MSFT": "Microsoft", "GOOG": "Google", "AMZN": "Amazon",
}


def next_earnings(symbol):
    try:
        ed = yf.Ticker(symbol).earnings_dates
    except Exception as e:
        print(f"{symbol}: fetch failed: {e}")
        return None
    if ed is None or ed.empty:
        return None
    today = datetime.date.today()
    for d in sorted(ed.index):
        dd = d.date() if hasattr(d, "date") else d
        if dd >= today:
            return str(dd)
    return None


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def main():
    items = []
    for label, sym in TICKERS.items():
        d = next_earnings(sym)
        print(f"{label} ({sym}) -> {d}")
        if d:
            items.append((label, d))
    items.sort(key=lambda kv: kv[1])

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//yujun//earnings-calendar//EN",
        "X-WR-CALNAME:Earnings — 财报日历",
        "CALSCALE:GREGORIAN",
    ]
    dtstamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for label, date in items:
        cname = NAMES.get(label, label)
        uid = hashlib.md5(f"{label}-{date}-finch".encode()).hexdigest() + "@finch.earnings"
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;VALUE=DATE:{date.replace('-', '')}",
            f"SUMMARY:{esc(label)} {esc(cname)} 财报",
            f"DESCRIPTION:{esc(label)} ({esc(cname)}) 预计发布财报。数据来源 Yahoo Finance，日期可能调整，以公司公告为准。",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    with open("earnings.ics", "w") as f:
        f.write("\r\n".join(lines) + "\r\n")
    print(f"Wrote earnings.ics with {len(items)} events")


if __name__ == "__main__":
    main()
