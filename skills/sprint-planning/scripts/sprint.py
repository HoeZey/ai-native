#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Check a sprint.yaml and render it to a read-only sprint.md.

Usage:
  uv run sprint.py check PATH [PATH ...]
  uv run sprint.py render PATH [PATH ...]

PATH is a sprint.yaml or a folder. A folder is searched for sprint.yaml and
*/sprint.yaml. check exits 1 when anything is flagged and 2 on a schema error.
"""

from __future__ import annotations

import collections
import datetime
import pathlib
import sys

import yaml

DEFAULT_LOAD_LIMIT = 0.8
DONE = {"done", "ready for qa", "ready for acceptance"}
HEADER = "<!-- Generated from sprint.yaml by sprint.py render. Do not edit. -->"
TOP_LEVEL = {
    "sprint", "dates", "merge_by", "jira", "jira_browse", "goal", "load_limit",
    "capacity", "tickets", "pull_in", "not_counted", "open_questions", "changes",
}
TICKET_KEYS = {
    "key", "title", "story", "owner", "points", "status", "ready", "blocked_by", "link",
}
CAPACITY_KEYS = {"person", "pool", "points", "note"}


class SchemaError(Exception):
    pass


def as_date(value, where):
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        raise SchemaError(f"{where}: {value!r} is not a YYYY-MM-DD date") from None


def require(data, field, kind, where):
    if field not in data or data[field] in (None, ""):
        raise SchemaError(f"{where}: missing {field}")
    if not isinstance(data[field], kind):
        raise SchemaError(f"{where}: {field} must be {getattr(kind, '__name__', kind)}")
    return data[field]


def str_list(data, field, where):
    value = data.get(field) or []
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise SchemaError(f"{where}: {field} must be a list of strings")
    return value


def reject_unknown(data, allowed, where):
    unknown = [key for key in data if key not in allowed]
    if unknown:
        raise SchemaError(f"{where}: unknown {', '.join(unknown)}")


def ticket(raw, where, counted):
    if not isinstance(raw, dict):
        raise SchemaError(f"{where}: must be a mapping")
    key = require(raw, "key", str, where)
    where = f"{where} {key}"
    reject_unknown(raw, TICKET_KEYS, where)
    t = {
        "key": key,
        "title": require(raw, "title", str, where),
        "story": raw.get("story", ""),
        "points": require(raw, "points", (int, float), where),
        "blocked_by": str_list(raw, "blocked_by", where),
        "link": raw.get("link", ""),
    }
    if counted:
        t["owner"] = require(raw, "owner", str, where)
        t["status"] = require(raw, "status", str, where)
        t["ready"] = as_date(raw["ready"], f"{where} ready") if raw.get("ready") else None
    return t


def load(path):
    where = str(path)
    raw = yaml.safe_load(path.read_text()) or {}
    if not isinstance(raw, dict):
        raise SchemaError(f"{where}: top level must be a mapping")
    reject_unknown(raw, TOP_LEVEL, where)
    dates = require(raw, "dates", list, where)
    if len(dates) != 2:
        raise SchemaError(f"{where}: dates must be [start, end]")
    sprint = {
        "path": path,
        "name": require(raw, "sprint", str, where),
        "start": as_date(dates[0], f"{where} dates"),
        "end": as_date(dates[1], f"{where} dates"),
        "merge_by": as_date(require(raw, "merge_by", (str, datetime.date), where), f"{where} merge_by"),
        "jira": raw.get("jira", ""),
        "jira_browse": raw.get("jira_browse", ""),
        "goal": require(raw, "goal", str, where),
        "load_limit": float(raw.get("load_limit", DEFAULT_LOAD_LIMIT)),
        "capacity": [],
        "tickets": [ticket(t, f"{where} tickets", True) for t in raw.get("tickets") or []],
        "pull_in": [ticket(t, f"{where} pull_in", False) for t in raw.get("pull_in") or []],
        "not_counted": str_list(raw, "not_counted", where),
        "open_questions": str_list(raw, "open_questions", where),
        "changes": str_list(raw, "changes", where),
    }
    for c in raw.get("capacity") or []:
        w = f"{where} capacity"
        if not isinstance(c, dict):
            raise SchemaError(f"{w}: must be a mapping")
        person = require(c, "person", str, w)
        reject_unknown(c, CAPACITY_KEYS, f"{w} {person}")
        sprint["capacity"].append({
            "person": person,
            "pool": require(c, "pool", str, f"{w} {person}"),
            "points": require(c, "points", (int, float), f"{w} {person}"),
            "note": c.get("note", ""),
        })
    return sprint


def loads(sprint):
    """Return per-person and per-pool load, capacity, and limit."""
    people = {c["person"]: c for c in sprint["capacity"]}
    pool_cap = collections.Counter()
    for c in sprint["capacity"]:
        pool_cap[c["pool"]] += c["points"]
    person_load, pool_load = collections.Counter(), collections.Counter()
    for t in sprint["tickets"]:
        if t["owner"] in people:
            person_load[t["owner"]] += t["points"]
            pool_load[people[t["owner"]]["pool"]] += t["points"]
        elif t["owner"] in pool_cap:
            pool_load[t["owner"]] += t["points"]
    return people, person_load, pool_cap, pool_load


def num(x):
    return f"{x:g}"


def short(day):
    return day.strftime("%a %d.%m") if day else ""


def long(day):
    return day.strftime("%a %d.%m.%Y")


def check(sprint):
    flags = []
    people, person_load, pool_cap, pool_load = loads(sprint)
    limit = sprint["load_limit"]
    by_key = {t["key"]: t for t in sprint["tickets"]}
    for t in sprint["tickets"]:
        if t["owner"] not in people and t["owner"] not in pool_cap:
            flags.append(f"{t['key']} owner {t['owner']} is not in capacity")
        if t["ready"] and t["ready"] > sprint["merge_by"]:
            flags.append(f"{t['key']} ready {short(t['ready'])} is after merge_by {short(sprint['merge_by'])}")
        if t["status"].lower() in DONE:
            continue
        for b in t["blocked_by"]:
            blocker = by_key.get(b)
            if blocker and blocker["ready"] and t["ready"] and blocker["ready"] >= t["ready"]:
                flags.append(f"{t['key']} ready {short(t['ready'])} but its blocker {b} is ready {short(blocker['ready'])}")
    for name, c in people.items():
        cap, used = c["points"], person_load[name]
        if used > cap:
            flags.append(f"{name} is over capacity: {num(used)} of {num(cap)}")
        elif used > cap * limit:
            flags.append(f"{name} is over the {limit:.0%} load limit: {num(used)} of {num(cap * limit)}")
    members = collections.Counter(c["pool"] for c in people.values())
    for pool, cap in pool_cap.items():
        if members[pool] > 1 and pool_load[pool] > cap * limit:
            flags.append(f"Pool {pool} is over the {limit:.0%} load limit: {num(pool_load[pool])} of {num(cap * limit)}")
    for t in sprint["pull_in"]:
        if t["key"] in by_key:
            flags.append(f"{t['key']} is in both tickets and pull_in")
    return flags


def pull_in_fits(sprint):
    """Pull-in items whose blockers are not also waiting, with who has room for them."""
    people, person_load, pool_cap, pool_load = loads(sprint)
    limit = sprint["load_limit"]
    waiting = {t["key"] for t in sprint["pull_in"]}
    fits = []
    for t in sprint["pull_in"]:
        if waiting & set(t["blocked_by"]):
            continue
        who = [n for n, c in people.items() if c["points"] * limit - person_load[n] >= t["points"]]
        if who:
            fits.append((t, who))
    return fits


def check_across(sprints, today):
    flags, where = [], {}
    live = sorted((s for s in sprints if s["end"] >= today), key=lambda s: s["start"])
    rank = {id(s): i for i, s in enumerate(live)}
    for s in live:
        for t in s["tickets"]:
            if t["key"] in where:
                flags.append(f"{t['key']} is in {where[t['key']]['name']} and {s['name']}")
            where.setdefault(t["key"], s)
    waiting = {t["key"]: s for s in live for t in s["pull_in"]}
    for s in live:
        for t in s["tickets"]:
            for b in t["blocked_by"]:
                if b in where and rank[id(where[b])] > rank[id(s)]:
                    flags.append(f"{t['key']} ({s['name']}) is blocked by {b} in later {where[b]['name']}")
                elif b not in where and b in waiting:
                    flags.append(f"{t['key']} ({s['name']}) is blocked by {b}, which is only in "
                                 f"{waiting[b]['name']} pull_in")
    return flags


def link(sprint, key, explicit=""):
    target = explicit or (sprint["jira_browse"] + key if sprint["jira_browse"] and key else "")
    return f"[{key}]({target})" if target else key


def cell(text):
    return str(text).replace("|", "\\|")


def render(sprint):
    people, person_load, pool_cap, pool_load = loads(sprint)
    limit = sprint["load_limit"]
    head = f"{long(sprint['start'])} to {long(sprint['end'])}. Merge by {long(sprint['merge_by'])}."
    if sprint["jira"]:
        head += f" Jira sprint {sprint['jira']}."
    lines = [HEADER, "", f"# {sprint['name']}", "", head + f" Load limit {limit:.0%}.", "",
             f"Goal: {sprint['goal']}", "", "## Capacity", "",
             "| Person | Pool | Capacity | Limit | Load | Room | Use | Note |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, c in people.items():
        cap, used = c["points"], person_load[name]
        use = f"{used / cap:.0%}" if cap else ""
        lines.append(f"| {name} | {c['pool']} | {num(cap)} | {num(cap * limit)} | {num(used)} | "
                     f"{num(cap * limit - used)} | {use} | {cell(c['note'])} |")
    for pool, cap in pool_cap.items():
        lines.append(f"| Pool {pool} | | {num(cap)} | {num(cap * limit)} | {num(pool_load[pool])} | "
                     f"{num(cap * limit - pool_load[pool])} | {pool_load[pool] / cap:.0%} | |")
    lines += ["", "## Tickets", "", "Committed, in review order.", "",
              "| # | Key | Title | Story | Owner | Pts | Status | Review-ready | Blocked by |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for i, t in enumerate(sprint["tickets"], 1):
        lines.append(f"| {i} | {link(sprint, t['key'], t['link'])} | {cell(t['title'])} | "
                     f"{link(sprint, t['story'])} | {t['owner']} | {num(t['points'])} | {t['status']} | "
                     f"{short(t['ready'])} | {', '.join(t['blocked_by'])} |")
    if sprint["pull_in"]:
        lines += ["", "## Pull in next", "", "Ranked. Not counted until pulled in.", "",
                  "| # | Key | Title | Story | Pts | Blocked by |", "| --- | --- | --- | --- | --- | --- |"]
        for i, t in enumerate(sprint["pull_in"], 1):
            lines.append(f"| {i} | {link(sprint, t['key'], t['link'])} | {cell(t['title'])} | "
                         f"{link(sprint, t['story'])} | {num(t['points'])} | {', '.join(t['blocked_by'])} |")
    for title, field in (("Not counted", "not_counted"), ("Open questions", "open_questions"),
                         ("Changes", "changes")):
        if sprint[field]:
            lines += ["", f"## {title}", ""] + [f"- {item}" for item in sprint[field]]
    return "\n".join(lines) + "\n"


def report(sprint):
    people, person_load, pool_cap, pool_load = loads(sprint)
    limit = sprint["load_limit"]
    out = [f"== {sprint['name']}  merge by {short(sprint['merge_by'])}, load limit {limit:.0%}"]
    for name, c in people.items():
        cap = c["points"]
        out.append(f"  {name:28} {num(person_load[name]):>5} of {num(cap):>4}  room {num(cap * limit - person_load[name])}")
    for pool, cap in pool_cap.items():
        out.append(f"  {'Pool ' + pool:28} {num(pool_load[pool]):>5} of {num(cap):>4}  room {num(cap * limit - pool_load[pool])}")
    unassigned = [t for t in sprint["tickets"] if t["owner"] in pool_cap and t["owner"] not in people]
    if unassigned:
        out.append("  Unassigned: " + ", ".join(f"{t['key']} ({t['owner']} {num(t['points'])})" for t in unassigned))
    for t, who in pull_in_fits(sprint):
        after = f", after {', '.join(t['blocked_by'])}" if t["blocked_by"] else ""
        out.append(f"  Can pull in {t['key']} ({num(t['points'])}{after}): room with {', '.join(who)}")
    dated = sorted((t for t in sprint["tickets"] if t["ready"]), key=lambda t: t["ready"])
    for t in dated:
        out.append(f"  {short(t['ready'])}  {t['key']:9} {t['owner']:28} {num(t['points'])}  {t['status']}")
    return out


def find(args):
    paths = []
    for arg in args:
        p = pathlib.Path(arg)
        if p.is_dir():
            paths += sorted(p.glob("sprint.yaml")) + sorted(p.glob("*/sprint.yaml"))
        else:
            paths.append(p)
    return paths


def main(argv, today=None):
    if len(argv) < 2 or argv[0] not in {"check", "render"}:
        print(__doc__)
        return 2
    paths = find(argv[1:])
    if not paths:
        print("No sprint.yaml found.")
        return 2
    try:
        sprints = [load(p) for p in paths]
    except SchemaError as e:
        print(f"Schema error: {e}")
        return 2
    if argv[0] == "render":
        for s in sprints:
            (s["path"].parent / "sprint.md").write_text(render(s))
            print(f"wrote {s['path'].parent / 'sprint.md'}")
        return 0
    flagged = False
    for s in sprints:
        flags = check(s)
        md = s["path"].parent / "sprint.md"
        if not md.exists() or md.read_text() != render(s):
            flags.append("sprint.md is missing or stale: run render")
        print("\n".join(report(s) + [f"  ! {f}" for f in flags]))
        flagged |= bool(flags)
    across = check_across(sprints, today or datetime.date.today())
    if across:
        print("== Across sprints")
        print("\n".join(f"  ! {f}" for f in across))
    return 1 if flagged or across else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
