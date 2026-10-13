# -*- coding: utf-8 -*-
"""Programmatic calendar expansion (Oct 2026): per-Bundesland Feiertage, Brückentage
and Arbeitstage across 2025/2026/2027 + national year hubs. Data from holidays_de.

Keyword-gap targets (KD 0-2, weak SERPs): feiertage <land> <jahr> (e.g. NRW 2026 ~194k,
Bayern 2026 ~144k), brückentage <land> <jahr>, arbeitstage <land> <jahr>, feiertage 2027, etc.
"""
import datetime as dt
from holidays_de import (LAENDER, LNAME, WT, MONATE, all_holidays, feiertage, easter,
                         arbeitstage_monat, arbeitstage_jahr, fmt, brueckentage)
# reuse the shared renderers/constants from the main content module (one-way import)
from pages_content import (month_table, hol_list, bridge_table, wd_hols, n_hols,
                           land_opts, AT_UI, AT_JS, FT)

# Years to generate. 2026 arbeitstage-state + national hubs already exist in pages_content.
FT_YEARS = [2025, 2026, 2027]   # per-state Feiertage pages
BT_YEARS = [2026, 2027]         # per-state Brückentage pages
AT_YEARS = [2025, 2027]         # per-state Arbeitstage pages (2026 already built)
FT_HUB_YEARS = [2025, 2027]     # national Feiertage hubs (2026 = FT26)
BT_HUB_YEARS = [2027]           # national Brückentage hubs (2026 = BT26)
AT_HUB_YEARS = [2025, 2027]     # national Arbeitstage hubs (2026 = AT_HUB)

TODAY_Y = 2026  # pages for this year or later get the live "nächster Feiertag" widget


def gd(d):
    return f"{d.day}. {MONATE[d.month - 1]} {d.year}"


def ostern_str(y):
    E = easter(y)
    return f"Ostersonntag ist am {gd(E)}, Karfreitag am {gd(E - dt.timedelta(days=2))}, Ostermontag am {gd(E + dt.timedelta(days=1))}"


def at_ui_year(sel, y):
    return AT_UI.format(opts=land_opts(sel), y=y)


def naechster_ft_widget(sel):
    return (f'<div class="calc"><h2>Nächster Feiertag</h2>'
            f'<div class="grid"><div><label for="land">Bundesland</label><select id="land">{land_opts(sel)}</select></div></div>'
            f'<div class="result" aria-live="polite"><div class="big" id="nx">–</div><div class="sub" id="nxd"></div></div></div>')


NAECHSTER_FT_JS = FT + r"""
(function(){function c(){var L=document.getElementById('land').value,t=new Date();t.setHours(12,0,0,0);var A=[];[t.getFullYear(),t.getFullYear()+1].forEach(function(y){var F=ftDE(y,L);Object.keys(F).sort().forEach(function(k){A.push([k,F[k]])})});
for(var i=0;i<A.length;i++){var d=new Date(A[i][0]+'T12:00:00');if(d>=t){var n=Math.round((d-t)/864e5);document.getElementById('nx').textContent=n===0?'Heute ist Feiertag!':'noch '+n+(n===1?' Tag':' Tage');document.getElementById('nxd').textContent='bis '+A[i][1]+' – '+d.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'long',year:'numeric'});break}}}
document.getElementById('land').addEventListener('input',c);c()})();"""


def _bt_link(y, slug):
    yy = y if y in BT_YEARS else 2026
    return f"/brueckentage-{yy}-{slug}/"


def _ft_hub_link(y):
    return f"/feiertage-{y}/"


# ---------------------------------------------------------------- Feiertage <state> <year>
def ft_state_page(y, c, name, slug):
    hols = sorted(feiertage(y, c).items())
    nh = n_hols(y, c)
    wdh = wd_hols(y, c)
    weekend = [n for d, n in hols if d.weekday() >= 5 and n not in ("Ostersonntag", "Pfingstsonntag")]
    special = [n for d, n, s in all_holidays(y) if s and c in s and n not in ("Ostersonntag", "Pfingstsonntag")]
    live = y >= TODAY_Y
    first_future = None
    nxt = [(d, n) for d, n in hols if d >= dt.date(TODAY_Y, 1, 1)]
    if nxt:
        first_future = nxt[0]
    widget = naechster_ft_widget(c) if live else ""
    special_txt = (f"Landesspezifische Feiertage in {name}: {', '.join(special)}." if special
                   else f"{name} hat ausschließlich die neun bundeseinheitlichen Feiertage.")
    weekend_txt = (f" {y} fallen folgende Feiertage auf ein Wochenende: {', '.join(weekend)}." if weekend else "")
    return {
        "path": f"/feiertage-{y}-{slug}/", "short": f"Feiertage {y} {name}", "group": "kal",
        "tool": live, "prio": "0.8" if live else "0.6",
        "card": f"Alle gesetzlichen Feiertage {y} in {name} mit Datum und Wochentag.",
        "title": f"Feiertage {y} {name} – Termine & Wochentage",
        "desc": f"Feiertage {y} in {name}: alle {nh} gesetzlichen Termine mit Datum und Wochentag – und welche nur hier gelten.",
        "h1": f"Feiertage {y} in {name}",
        "lead": f"{name} hat {y} <strong>{nh} gesetzliche Feiertage</strong>; davon fallen {wdh} auf einen Werktag "
                f"(Montag bis Freitag). {ostern_str(y)}. Hier findest du alle Termine mit Wochentag.",
        "sources": ["ftgesetze"],
        "body": widget + f"""
<h2>Alle Feiertage {y} in {name}</h2>
{hol_list(y, c)}
<p>{special_txt}{weekend_txt}</p>
<h2>Feiertage {y} in {name} clever nutzen</h2>
<p>Mit den richtigen Brückentagen holst du aus den {wdh} Feiertagen, die {y} auf einen Werktag fallen, deutlich
mehr freie Tage heraus. Die konkreten Kombinationen für {name} stehen auf der Seite
<a href="{_bt_link(y, slug)}">Brückentage {y if y in BT_YEARS else 2026} {name}</a>. Wie viele Arbeitstage
{y} übrig bleiben, zeigt <a href="/arbeitstage-{y}-{slug}/">Arbeitstage {y} {name}</a>.</p>
<p>Alle Bundesländer im Überblick: <a href="{_ft_hub_link(y)}">Feiertage {y} in Deutschland</a>. Einen Countdown
zu einem eigenen Datum liefert der <a href="/tagerechner/">Tagerechner</a>, Zeitspannen in Stunden der
<a href="/zeitrechner/">Zeitrechner</a>.</p>
""",
        "faq": [
            (f"Wie viele Feiertage hat {name} {y}?",
             f"{nh} gesetzliche Feiertage; davon fallen {wdh} auf Montag bis Freitag und sind damit arbeitsfreie Werktage."),
            (f"Wann ist Ostern {y}?", f"{ostern_str(y)}."),
            (f"Welche Feiertage gelten {y} nur in {name}?",
             (f"{', '.join(special)}." if special else f"Keine – {name} hat ausschließlich die bundesweiten Feiertage.")),
            (f"Welcher Feiertag ist {y} der nächste in {name}?",
             (f"{first_future[1]} am {gd(first_future[0])}." if first_future else "Siehe die Tabelle oben für alle Termine.")),
        ],
        "js": NAECHSTER_FT_JS if live else "",
    }


# ---------------------------------------------------------------- Brückentage <state> <year>
def bt_state_page(y, c, name, slug):
    rows = brueckentage(y, c)
    best = max(rows, key=lambda r: r[5]) if rows else None
    cheap = [r for r in rows if len(r[2]) == 1]
    cheap_txt = ""
    if cheap:
        r = max(cheap, key=lambda x: x[5])
        cheap_txt = (f"Schon mit einem einzigen Urlaubstag ({fmt(r[2][0])}) rund um {r[1]} "
                     f"({WT[r[0].weekday()]}, {fmt(r[0])}) bekommst du {r[5]} freie Tage am Stück.")
    best_txt = ""
    if best and best[2]:
        best_txt = (f"Die größte Brücke bildet {best[1]}: mit {len(best[2])} Urlaubstagen "
                    f"({', '.join(fmt(x) for x in best[2])}) sind {best[5]} Tage am Stück frei "
                    f"({fmt(best[3])} bis {fmt(best[4])}).")
    return {
        "path": f"/brueckentage-{y}-{slug}/", "short": f"Brückentage {y} {name}", "group": "kal", "prio": "0.7",
        "card": f"Brückentage {y} in {name}: mit wenig Urlaub maximal frei.",
        "title": f"Brückentage {y} {name} – mit wenig Urlaub maximal frei",
        "desc": f"Brückentage {y} in {name}: für jeden Feiertag die kürzeste Brücke und die beste Urlaubswoche – maximal frei mit wenig Urlaub.",
        "h1": f"Brückentage {y} in {name}",
        "lead": f"So nutzt du die Feiertage {y} in {name} optimal. {cheap_txt or best_txt} Die Tabelle zeigt für "
                f"jeden Feiertag die kürzeste Brücke und die Variante mit einer ganzen Urlaubswoche.",
        "sources": ["ftgesetze"],
        "body": f"""
<h2>Alle Brückentage {y} in {name}</h2>
<p>Jede Zeile nennt einen Feiertag, die dafür nötigen Urlaubstage und wie viele freie Tage am Stück daraus
entstehen. {best_txt}</p>
{bridge_table(y, c)}
<p class="hint">Grundlage sind die {y} in {name} geltenden gesetzlichen Feiertage. Ostersonntag und
Pfingstsonntag sind nur in Brandenburg gesetzliche Feiertage.</p>
<h2>Tipps zur Urlaubsplanung {y}</h2>
<ul>
<li>Urlaubsanträge für Brückentage früh stellen – die Tage sind beliebt und schnell vergeben.</li>
<li>Prüfe, ob dein Betrieb an Brückentagen ohnehin Betriebsurlaub macht; das wird auf den Jahresurlaub angerechnet.</li>
<li>Wie viele Urlaubstage dir zustehen, berechnet der <a href="/urlaubsrechner/">Urlaubsrechner</a>.</li>
</ul>
<p>Alle Termine im Überblick: <a href="/feiertage-{y}-{slug}/">Feiertage {y} {name}</a> und
<a href="/arbeitstage-{y}-{slug}/">Arbeitstage {y} {name}</a>.</p>
""",
        "faq": [
            (f"Welche Brückentage gibt es {y} in {name}?",
             (f"{best[1]} bietet die längste Brücke ({best[5]} freie Tage mit {len(best[2])} Urlaubstagen)."
              if best and best[2] else "Siehe die Tabelle oben für alle Feiertage und Brücken.")),
            ("Was ist ein Brückentag?",
             "Ein Arbeitstag zwischen einem Feiertag und dem Wochenende. Wer ihn freinimmt, verlängert das "
             "Wochenende mit nur einem Urlaubstag auf mindestens vier freie Tage."),
            (f"Wie bekomme ich {y} mit wenig Urlaub viel frei?",
             (cheap_txt or "Lege deine Urlaubstage direkt neben Feiertage, die auf einen Dienstag oder Donnerstag fallen.")),
        ],
    }


# ---------------------------------------------------------------- Arbeitstage <state> <year>
def at_state_page_year(y, c, name, slug):
    tot = arbeitstage_jahr(y, c)
    nh = n_hols(y, c)
    wdh = wd_hols(y, c)
    special = [n for d, n, s in all_holidays(y) if s and c in s and n not in ("Ostersonntag", "Pfingstsonntag")]
    hours = tot * 8
    # most/least working-day months
    per_m = [(m, arbeitstage_monat(y, m, c)) for m in range(1, 13)]
    mmax = max(per_m, key=lambda x: x[1])
    mmin = min(per_m, key=lambda x: x[1])
    return {
        "path": f"/arbeitstage-{y}-{slug}/", "short": f"Arbeitstage {y} {name}", "group": "land", "prio": "0.7",
        "card": f"{tot} Arbeitstage {y} in {name}.",
        "title": f"Arbeitstage {y} {name} – pro Monat, Feiertage & Stunden",
        "desc": f"{name} hat {y} {tot} Arbeitstage (Mo–Fr). Arbeitstage und Stunden pro Monat, alle {nh} Feiertage und die besten Brückentage.",
        "h1": f"Arbeitstage {y} in {name}",
        "lead": f"{name} hat {y} <strong>{tot} Arbeitstage</strong> von Montag bis Freitag. Von den {nh} "
                f"gesetzlichen Feiertagen fallen {wdh} auf einen Werktag. Bei einer 40-Stunden-Woche ergibt das "
                f"{hours:,} Sollstunden.".replace(",", "."),
        "sources": ["ftgesetze"],
        "body": f"""
<h2>Arbeitstage {y} {name} pro Monat</h2>
{month_table(y, c)}
<h2>Feiertage {y} in {name}</h2>
{hol_list(y, c)}
<p>{"Landesspezifische Feiertage: " + ", ".join(special) + "." if special else name + " hat nur die bundeseinheitlichen Feiertage."} Alle Termine mit Erklärung stehen unter <a href="/feiertage-{y}-{slug}/">Feiertage {y} {name}</a>.</p>
<h2>Brückentage {y} in {name}</h2>
<p>Mit wenigen Urlaubstagen lassen sich lange freie Zeiträume herausholen. Die Tabelle zeigt für jeden Feiertag
die kürzeste Brücke und die Variante mit einer ganzen Urlaubswoche.</p>
{bridge_table(y, c)}
""" + at_ui_year(c, y) + f"""
<p>Alle Länder im Vergleich: <a href="/arbeitstage-{y}/">Arbeitstage {y} nach Bundesland</a>. Deinen
Urlaubsanspruch rechnest du mit dem <a href="/urlaubsrechner/">Urlaubsrechner</a> aus, Monatsstunden mit dem
<a href="/stundenrechner/">Stundenrechner</a>.</p>
""",
        "faq": [
            (f"Wie viele Arbeitstage hat {name} {y}?",
             f"{tot} Arbeitstage von Montag bis Freitag, nach Abzug der {wdh} Feiertage, die auf einen Werktag fallen."),
            (f"Wie viele Arbeitsstunden hat {y} in {name}?",
             f"Bei 8 Stunden pro Tag {hours:,} Stunden, bei 7,7 Stunden (38,5-Stunden-Woche) rund {round(tot*7.7):,} Stunden – vor Abzug von Urlaub und Krankheit.".replace(",", ".")),
            (f"Welcher Monat hat {y} in {name} die meisten Arbeitstage?",
             f"Der {MONATE[mmax[0]-1]} mit {mmax[1]} Arbeitstagen; die wenigsten hat der {MONATE[mmin[0]-1]} mit {mmin[1]}."),
        ],
        "js": AT_JS,
    }


# ---------------------------------------------------------------- national hubs for other years
def _state_list(y, kind):
    """kind: 'ft' | 'bt' | 'at' -> UL of per-state links."""
    if kind == "ft":
        return "".join(f'<li><a href="/feiertage-{y}-{slug}/">Feiertage {y} {n}</a> – {n_hols(y, c)} Feiertage</li>' for c, n, slug in LAENDER)
    if kind == "bt":
        return "".join(f'<li><a href="/brueckentage-{y}-{slug}/">Brückentage {y} {n}</a></li>' for c, n, slug in LAENDER)
    return "".join(f'<li><a href="/arbeitstage-{y}-{slug}/">Arbeitstage {y} {n}</a> – {arbeitstage_jahr(y, c)} Tage</li>' for c, n, slug in LAENDER)


def _ft_table_year(y):
    rows = ""
    for d, n, s in all_holidays(y):
        if n in ("Ostersonntag", "Pfingstsonntag"):
            continue
        where = "bundesweit" if s is None else ", ".join(LNAME[x] for x in s)
        if n == "Mariä Himmelfahrt":
            where = "Saarland, Bayern (überwiegend katholische Gemeinden)"
        rows += f'<tr><td>{fmt(d)}</td><td>{WT[d.weekday()]}</td><td>{n}</td><td>{where}</td></tr>'
    return f'<div class="tw"><table class="t"><thead><tr><th>Datum</th><th>Wochentag</th><th>Feiertag</th><th>Gültig in</th></tr></thead><tbody>{rows}</tbody></table></div>'


def ft_hub(y):
    live = y >= TODAY_Y
    lo = min(n_hols(y, c) for c, _, _ in LAENDER)
    hi = max(n_hols(y, c) for c, _, _ in LAENDER)
    return {
        "path": f"/feiertage-{y}/", "short": f"Feiertage {y}", "group": "kal", "tool": live, "prio": "0.8" if live else "0.6",
        "card": f"Alle gesetzlichen Feiertage {y} mit Wochentag und Bundesländern.",
        "title": f"Feiertage {y} – alle gesetzlichen Feiertage nach Bundesland",
        "desc": f"Alle gesetzlichen Feiertage {y} in Deutschland: Datum, Wochentag und Bundesländer. {ostern_str(y).split(',')[0]}.",
        "h1": f"Feiertage {y} in Deutschland",
        "lead": f"Bundesweit gibt es 9 gesetzliche Feiertage, je nach Bundesland kommen weitere dazu – {y} sind es "
                f"zwischen {lo} und {hi} pro Land. {ostern_str(y)}.",
        "sources": ["ftgesetze"],
        "body": (naechster_ft_widget("NW") if live else "") + f"""
<h2>Alle Feiertage {y}</h2>
{_ft_table_year(y)}
<h2>Feiertage {y} nach Bundesland</h2>
<ul class="cols2">{_state_list(y, 'ft')}</ul>
<h2>Feiertage {y} planen</h2>
<p>Die besten Kombinationen aus Feiertagen und Urlaub findest du unter Brückentage, die verbleibenden
Arbeitstage unter <a href="/arbeitstage-{y}/">Arbeitstage {y}</a>. Einen Countdown zu einem eigenen Termin
liefert der <a href="/tagerechner/">Tagerechner</a>.</p>
""",
        "faq": [
            (f"Wann ist Ostern {y}?", f"{ostern_str(y)}."),
            (f"Wie viele Feiertage gibt es {y}?", f"Bundesweit 9 gesetzliche Feiertage; je nach Bundesland {lo} bis {hi}."),
            (f"Welche Bundesländer haben {y} die meisten Feiertage?", "Bayern und Baden-Württemberg; in Augsburg kommt das Friedensfest (8. August) hinzu."),
        ],
        "js": NAECHSTER_FT_JS if live else "",
    }


def at_hub(y):
    lo = min(arbeitstage_jahr(y, c) for c, _, _ in LAENDER)
    hi = max(arbeitstage_jahr(y, c) for c, _, _ in LAENDER)
    head = "".join(f"<th style='text-align:right'>{m[:3]}</th>" for m in MONATE)
    rows = ""
    for c, n, slug in LAENDER:
        cells = "".join(f'<td class="num">{arbeitstage_monat(y, m, c)}</td>' for m in range(1, 13))
        rows += f'<tr><td><a href="/arbeitstage-{y}-{slug}/">{n}</a></td>{cells}<td class="num"><strong>{arbeitstage_jahr(y, c)}</strong></td></tr>'
    table = f'<div class="tw"><table class="t sm"><thead><tr><th>Bundesland</th>{head}<th style="text-align:right">Jahr</th></tr></thead><tbody>{rows}</tbody></table></div>'
    return {
        "path": f"/arbeitstage-{y}/", "short": f"Arbeitstage {y}", "group": "kal", "tool": True, "prio": "0.8",
        "card": f"Arbeitstage {y} pro Monat und Bundesland – mit Rechner.",
        "title": f"Arbeitstage {y} – pro Monat und Bundesland (mit Rechner)",
        "desc": f"Wie viele Arbeitstage hat {y}? Tabelle pro Monat für alle 16 Bundesländer plus Rechner für jeden Zeitraum.",
        "h1": f"Arbeitstage {y} – pro Monat und Bundesland",
        "lead": f"{y} hat je nach Bundesland zwischen {lo} und {hi} Arbeitstage (Montag bis Freitag, abzüglich "
                f"gesetzlicher Feiertage). Unten findest du die Zahlen pro Monat und einen Rechner für jeden Zeitraum.",
        "sources": ["ftgesetze"],
        "body": at_ui_year("NW", y) + f"""
<h2>Arbeitstage {y} pro Monat nach Bundesland</h2>
{table}
<h2>Arbeitstage {y} für dein Bundesland</h2>
<ul class="cols2">{_state_list(y, 'at')}</ul>
<p>Alle Feiertage stehen unter <a href="/feiertage-{y}/">Feiertage {y}</a>, Urlaubstipps liefert die
Brückentage-Planung. Monatsstunden für Lohn und Überstunden ermittelst du mit dem
<a href="/stundenrechner/">Stundenrechner</a>.</p>
""",
        "faq": [
            (f"Wie viele Arbeitstage hat {y}?", f"Zwischen {lo} und {hi} – abhängig von den Feiertagen im Bundesland."),
            ("Zählt der Samstag als Arbeitstag?", "Bei einer 5-Tage-Woche nicht. Als Werktag zählt der Samstag aber im Arbeitsrecht, etwa beim Urlaubsanspruch."),
            (f"Wie viele Arbeitsstunden hat {y}?", f"Bei 8 Stunden pro Tag rund {lo*8:,} bis {hi*8:,} Stunden – vor Abzug von Urlaub und Krankheit.".replace(",", ".")),
        ],
        "js": AT_JS,
    }


def bt_hub(y):
    return {
        "path": f"/brueckentage-{y}/", "short": f"Brückentage {y}", "group": "kal", "prio": "0.7",
        "card": f"Brückentage {y}: mit wenigen Urlaubstagen maximal frei – alle Bundesländer.",
        "title": f"Brückentage {y} – mit wenig Urlaub maximal frei (alle Bundesländer)",
        "desc": f"Brückentage {y} clever nutzen: für jedes Bundesland die besten Kombinationen aus Feiertagen und Urlaub – maximal frei.",
        "h1": f"Brückentage {y}: die besten Urlaubstipps",
        "lead": f"Mit den richtigen Brückentagen holst du {y} aus wenigen Urlaubstagen lange Freizeiten heraus. "
                f"Wähle dein Bundesland für die genaue Tabelle mit Feiertagen, nötigen Urlaubstagen und freien Tagen am Stück.",
        "sources": ["ftgesetze"],
        "body": f"""
<h2>Brückentage {y} bundesweit</h2>
<p>Die folgende Tabelle zeigt die bundesweit einheitlichen Feiertage {y} und die passenden Brücken. Zusätzliche
Brückentage durch landesspezifische Feiertage (z. B. Fronleichnam, Heilige Drei Könige, Buß- und Bettag) findest
du auf den Länderseiten unten.</p>
{bridge_table(y, "HH")}
<h2>Brückentage {y} nach Bundesland</h2>
<ul class="cols2">{_state_list(y, 'bt')}</ul>
<p>Alle Termine im Überblick: <a href="/feiertage-{y}/">Feiertage {y}</a>. Deinen Urlaubsanspruch berechnet der
<a href="/urlaubsrechner/">Urlaubsrechner</a>, die verbleibenden Arbeitstage zeigt
<a href="/arbeitstage-{y}/">Arbeitstage {y}</a>.</p>
""",
        "faq": [
            ("Was ist ein Brückentag?", "Ein Arbeitstag zwischen einem Feiertag und dem Wochenende. Freigenommen verlängert er das Wochenende mit nur einem Urlaubstag auf mindestens vier Tage."),
            (f"Wo gibt es {y} die meisten Brückentage?", "In Ländern mit vielen werktäglichen Feiertagen wie Bayern, Baden-Württemberg und Nordrhein-Westfalen (Fronleichnam) sowie Sachsen (Buß- und Bettag)."),
            ("Wie plane ich Brückentage am besten?", "Lege Urlaubstage neben Feiertage, die auf Dienstag oder Donnerstag fallen – so entsteht aus einem Urlaubstag ein langes Wochenende."),
        ],
    }


# ---------------------------------------------------------------- assemble
CAL = []
for y in FT_YEARS:
    CAL += [ft_state_page(y, c, n, s) for c, n, s in LAENDER]
for y in BT_YEARS:
    CAL += [bt_state_page(y, c, n, s) for c, n, s in LAENDER]
for y in AT_YEARS:
    CAL += [at_state_page_year(y, c, n, s) for c, n, s in LAENDER]
for y in FT_HUB_YEARS:
    CAL.append(ft_hub(y))
for y in BT_HUB_YEARS:
    CAL.append(bt_hub(y))
for y in AT_HUB_YEARS:
    CAL.append(at_hub(y))
