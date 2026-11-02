"""'Did this bus turn up?' — a daily guessing game in the profile README.

    python scripts/game.py new                 pick today's departure (daily)
    python scripts/game.py answer "<title>"    score a guess sent as an issue title

Each puzzle is a real Sheffield departure from the latest judged day of
Ghost Bus Detector. A guess is an issue titled  ghostbus:<puzzle id>:ran
or  ghostbus:<puzzle id>:ghost ; the workflow replies with this script's
output, updates the scoreboard and closes the issue.
"""
import csv
import gzip
import hashlib
import io
import json
import os
import random
import re
import sys
import urllib.request
from datetime import datetime
from urllib.parse import quote

REPO = "Mohammed-890/Mohammed-890"
DATA = "https://raw.githubusercontent.com/Mohammed-890/ghost-bus/"
STATE = "game/state.json"
START, END = "<!-- game:start -->", "<!-- game:end -->"


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def load():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"puzzle": None, "previous": None, "plays": 0, "correct": 0}


def save(st):
    os.makedirs("game", exist_ok=True)
    json.dump(st, open(STATE, "w"), indent=1)


def hhmm(secs):
    secs = int(secs) % 86400
    return f"{secs // 3600:02d}:{secs % 3600 // 60:02d}"


def nice_day(d):
    return datetime.fromisoformat(d).strftime("%A %-d %B")


def digest(pid, answer):
    return hashlib.sha256(f"{pid}:{answer}".encode()).hexdigest()[:16]


def pick(seed=None):
    summary = json.loads(fetch(DATA + "main/docs/data/summary.json"))
    day = summary.get("last_day")
    if not day:
        return None, summary
    rows = list(csv.DictReader(io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(fetch(DATA + f"data/results/{day}.csv.gz"))), "utf-8")))
    judged = [r for r in rows if r["verdict"] in ("ghost", "ran_tracked", "ran_matched") and r.get("from_stop") and r.get("to_stop")]
    ghosts = [r for r in judged if r["verdict"] == "ghost"]
    ran = [r for r in judged if r["verdict"] != "ghost"]
    rnd = random.Random(seed or day)
    pool = ghosts if ghosts and rnd.random() < 0.5 else ran
    r = rnd.choice(pool)
    answer = "ghost" if r["verdict"] == "ghost" else "ran"
    pid = hashlib.sha256(f"{day}{r['trip_id']}".encode()).hexdigest()[:6]
    return {
        "id": pid, "day": day, "route": r["route"], "operator": r["operator"], "time": hhmm(r["start_secs"]),
        "from": r["from_stop"], "to": r["to_stop"], "check": digest(pid, answer), "answer": None,
        "plays": 0, "correct": 0, "ghosts_that_day": len(ghosts), "judged_that_day": len(judged),
    }, summary


def reveal(p):
    for a in ("ran", "ghost"):
        if digest(p["id"], a) == p["check"]:
            return a
    return None


def badge(label, color, answer, pid):
    title = quote(f"ghostbus:{pid}:{answer}")
    body = quote("Just press **Submit new issue**. A bot replies with the real answer in about a minute, "
                 "adds you to the scoreboard and closes this issue.")
    return (f'<a href="https://github.com/{REPO}/issues/new?title={title}&body={body}">'
            f'<img src="https://img.shields.io/badge/{quote(label)}-{color}?style=for-the-badge" alt="{label}"></a>')


def section(st):
    p = st["puzzle"]
    lines = [START, "## Play: did this bus turn up?", ""]
    if not p:
        lines += ["The game starts once Ghost Bus Detector has judged its first full day. Check back tomorrow.", END]
        return "\n".join(lines)
    lines += [
        f"Every day this asks about a **real departure** from Sheffield, checked by [Ghost Bus Detector](https://github.com/Mohammed-890/ghost-bus) against live GPS.",
        "",
        f"> **Route {p['route']}** ({p['operator']}), **{p['time']}** on **{nice_day(p['day'])}**",
        f"> from {p['from']} to {p['to']}",
        "",
        "Did a bus actually run it?",
        "",
        '<p align="left">' + badge("It ran", "1aa38c", "ran", p["id"]) + " &nbsp; " + badge("It never came", "7b5cff", "ghost", p["id"]) + "</p>",
        "",
    ]
    today = f"{p['plays']} guess{'es' if p['plays'] != 1 else ''} today" + (f", {round(100 * p['correct'] / p['plays'])}% right" if p["plays"] else "")
    total = f"{st['plays']} guess{'es' if st['plays'] != 1 else ''} in total" + (f", {round(100 * st['correct'] / st['plays'])}% right" if st["plays"] else "")
    lines.append(f"<sub>{today} · {total}</sub>")
    prev = st.get("previous")
    if prev:
        word = "it never came" if prev["answer"] == "ghost" else "it ran"
        lines += ["", f"<sub>Yesterday's bus (route {prev['route']} at {prev['time']}): **{word}**. "
                      f"{prev['correct']} of {prev['plays']} guessed right.</sub>"]
    lines.append(END)
    return "\n".join(lines)


def write_readme(st):
    readme = open("README.md", encoding="utf-8").read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: section(st), readme, flags=re.S)
    open("README.md", "w", encoding="utf-8").write(new)


def cmd_new():
    st = load()
    p, _ = pick()
    if p is None:
        write_readme(st)
        return
    if st["puzzle"] and st["puzzle"]["day"] == p["day"]:
        write_readme(st)
        print("no new day yet")
        return
    if st["puzzle"]:
        old = st["puzzle"]
        old["answer"] = reveal(old)
        st["previous"] = {k: old[k] for k in ("route", "time", "answer", "plays", "correct")}
    st["puzzle"] = p
    save(st)
    write_readme(st)
    print("new puzzle", p["id"], p["route"], p["time"])


def cmd_answer(title):
    st = load()
    m = re.match(r"\s*ghostbus:([0-9a-f]{6}):(ran|ghost)\s*$", title or "")
    p = st["puzzle"]
    if not m:
        print("That doesn't look like a guess. Use the **It ran** or **It never came** buttons on the profile.")
        return
    if not p or m.group(1) != p["id"]:
        print("That puzzle has closed. Today's bus is on the [profile](https://github.com/Mohammed-890), have another go.")
        return
    guess, truth = m.group(2), reveal(p)
    right = guess == truth
    p["plays"] += 1
    st["plays"] += 1
    if right:
        p["correct"] += 1
        st["correct"] += 1
    save(st)
    write_readme(st)
    what = ("**never came**. No bus was seen on the route while the live feed and the operator were both reporting"
            if truth == "ghost" else "**ran**. A bus was tracked doing this trip")
    pct = round(100 * p["correct"] / p["plays"])
    print(f"{'Correct!' if right else 'Not this time.'} Route {p['route']} at {p['time']} on {nice_day(p['day'])} {what}.\n\n"
          f"That day {p['ghosts_that_day']} of the {p['judged_that_day']} departures that could be checked never turned up. "
          f"So far {pct}% of players got today's bus right.\n\n"
          f"The data comes from [Ghost Bus Detector](https://mohammed-890.github.io/ghost-bus/), which matches every Sheffield bus "
          f"against the timetable using the government's live GPS feed. A new bus is picked every day.")


if __name__ == "__main__":
    if sys.argv[1] == "new":
        cmd_new()
    else:
        cmd_answer(sys.argv[2] if len(sys.argv) > 2 else "")
