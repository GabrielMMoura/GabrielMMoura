"""Generate a contribution calendar using the public GitHub profile, no token required."""
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import urllib.request

USERNAME = "GabrielMMoura"
ROOT = Path(__file__).resolve().parents[1]

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-date" in attrs and "data-level" in attrs:
            self.days[date.fromisoformat(attrs["data-date"])] = int(attrs["data-level"])

def main():
    request = urllib.request.Request(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "github-profile-calendar"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        source = response.read().decode("utf-8")
    parser = CalendarParser()
    parser.feed(source)
    if len(parser.days) < 300:
        raise RuntimeError("Incomplete GitHub calendar; keeping the previous image.")
    colors = ["#21262d", "#0e4429", "#006d32", "#26a641", "#39d353"]
    first = min(parser.days)
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    heading = re.search(r'<h2\b[^>]*>(.*?)</h2>', source, re.S)
    title = "Contribuições no GitHub"
    if heading:
        raw = re.sub(r"<[^>]+>", "", heading.group(1))
        count = re.search(r"([\d,]+)\s+contributions?", raw)
        if count:
            title = count.group(1).replace(",", ".") + " contribuições no último ano"
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="256" viewBox="0 0 960 256" role="img" aria-label="{escape(title)}">
    <rect width="960" height="256" fill="#0d1117"/>
    <g font-family="Arial, sans-serif"><text x="28" y="39" fill="#c9d1d9" font-size="18">{escape(title)}</text>''']
    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    for day, level in sorted(parser.days.items()):
        if level not in range(5):
            raise ValueError("Unexpected contribution level")
        col = (day - start).days // 7
        row = (day.weekday() + 1) % 7
        x, y = 55 + col * 16, 97 + row * 16
        if day.day == 1:
            parts.append(f'<text x="{x}" y="86" fill="#8b949e" font-size="11">{months[day.month - 1]}</text>')
        parts.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="3" fill="{colors[level]}"><title>{day.isoformat()}: nível de atividade {level}/4</title></rect>')
    for row, label in [(1, "Seg"), (3, "Qua"), (5, "Sex")]:
        parts.append(f'<text x="23" y="{107 + row * 16}" fill="#8b949e" font-size="10">{label}</text>')
    parts.append(f'<text x="28" y="234" fill="#8b949e" font-size="11">Atualizado em {date.today().isoformat()} · Dados: GitHub</text>')
    parts.append('<text x="756" y="234" fill="#8b949e" font-size="11">Menos</text>')
    for i, color in enumerate(colors):
        parts.append(f'<rect x="{795 + i * 16}" y="224" width="12" height="12" rx="3" fill="{color}"/>')
    parts.append('<text x="882" y="234" fill="#8b949e" font-size="11">Mais</text></g></svg>')
    target = ROOT / "assets" / "contributions.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(parts), encoding="utf-8")
    # Split the same year into two chronological rows on narrow screens.
    mobile = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="352" viewBox="0 0 480 352" role="img" aria-label="{escape(title)}">
    <rect width="480" height="352" fill="#0d1117"/>
    <g font-family="Arial, sans-serif"><text x="12" y="24" fill="#c9d1d9" font-size="16">{escape(title)}</text>''']
    for day, level in sorted(parser.days.items()):
        week = (day - start).days // 7
        block, col = divmod(week, 27)
        row = (day.weekday() + 1) % 7
        x, y = 30 + col * 16, 61 + block * 138 + row * 16
        if day.day == 1:
            mobile.append(f'<text x="{x}" y="{y - row * 16 - 9}" fill="#8b949e" font-size="11">{months[day.month - 1]}</text>')
        mobile.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" fill="{colors[level]}"><title>{day.isoformat()}: nível {level}/4</title></rect>')
    mobile.append(f'<text x="12" y="336" fill="#8b949e" font-size="11">{date.today().isoformat()} · Dados: GitHub</text>')
    mobile.append('<text x="300" y="336" fill="#8b949e" font-size="11">Menos</text>')
    for i, color in enumerate(colors):
        mobile.append(f'<rect x="{340 + i * 16}" y="326" width="12" height="12" rx="2" fill="{color}"/>')
    mobile.append('<text x="428" y="336" fill="#8b949e" font-size="11">Mais</text></g></svg>')
    target.with_name("contributions-mobile.svg").write_text("\n".join(mobile), encoding="utf-8")
    print(f"Calendar generated: {len(parser.days)} days")

if __name__ == "__main__":
    main()
