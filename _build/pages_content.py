# -*- coding: utf-8 -*-
"""Content expansion (Oct 2026): Arbeitstage 2026 (hub + 16 Länder), Feiertage, Brückentage, Urlaub, Teilzeit, Minijob, Alter."""
import datetime as dt
from holidays_de import (LAENDER, LNAME, WT, MONATE, all_holidays, feiertage, arbeitstage_monat, arbeitstage_jahr,
                         fmt, brueckentage, ft_js)

Y = 2026
FT = ft_js()
LAND_OPTS = "".join(f'<option value="{c}"{" selected" if c == "NW" else ""}>{n}</option>' for c, n, _ in LAENDER)


def land_opts(sel):
    return "".join(f'<option value="{c}"{" selected" if c == sel else ""}>{n}</option>' for c, n, _ in LAENDER)


def wd_hols(y, land):
    return sum(1 for d in feiertage(y, land) if d.weekday() < 5)


def n_hols(y, land):
    return sum(1 for d, n in feiertage(y, land).items() if n not in ("Ostersonntag", "Pfingstsonntag"))


def month_table(y, land):
    rows = ""
    for m in range(1, 13):
        a = arbeitstage_monat(y, m, land)
        rows += f'<tr><td>{MONATE[m-1]}</td><td class="num">{a}</td><td class="num">{a*8} h</td><td class="num">{str(round(a*7.7, 1)).replace(".", ",")} h</td></tr>'
    t = arbeitstage_jahr(y, land)
    rows += f'<tr><td><strong>Gesamt {y}</strong></td><td class="num">{t}</td><td class="num">{t*8} h</td><td class="num">{str(round(t*7.7, 1)).replace(".", ",")} h</td></tr>'
    return f'<div class="tw"><table class="t"><thead><tr><th>Monat</th><th style="text-align:right">Arbeitstage</th><th style="text-align:right">Stunden (40-h-Woche)</th><th style="text-align:right">Stunden (38,5-h-Woche)</th></tr></thead><tbody>{rows}</tbody></table></div>'


def hol_list(y, land):
    out = ""
    for d, n in sorted(feiertage(y, land).items()):
        we = d.weekday() >= 5
        out += f'<tr><td>{fmt(d)}</td><td>{WT[d.weekday()]}</td><td>{n}</td><td>{"fällt aufs Wochenende" if we else "arbeitsfrei"}</td></tr>'
    return f'<div class="tw"><table class="t"><thead><tr><th>Datum</th><th>Wochentag</th><th>Feiertag</th><th>Wirkung</th></tr></thead><tbody>{out}</tbody></table></div>'


def bridge_table(y, land, only_short=False):
    rows = ""
    for d, n, vac, a, b, free in brueckentage(y, land):
        if only_short and len(vac) > 2:
            continue
        if a.year < y:
            continue
        v = f"{len(vac)} ({', '.join(f'{x.day:02d}.{x.month:02d}.' for x in vac)})" if vac else "0"
        rows += f'<tr><td>{n}<br><span class="hint" style="margin:0">{WT[d.weekday()]}, {fmt(d)}</span></td><td class="num">{v}</td><td class="num">{free}</td><td>{a.day:02d}.{a.month:02d}. – {b.day:02d}.{b.month:02d}.{b.year}</td></tr>'
    # Silvester / Neujahr y+1 combination
    for d, n, vac, a, b, free in brueckentage(y + 1, land):
        if d.month == 1 and d.day == 1 and vac and all(x.year == y for x in vac):
            rows += f'<tr><td>Neujahr {y+1}<br><span class="hint" style="margin:0">{WT[d.weekday()]}, {fmt(d)}</span></td><td class="num">{len(vac)} ({", ".join(f"{x.day:02d}.{x.month:02d}." for x in vac)})</td><td class="num">{free}</td><td>{a.day:02d}.{a.month:02d}.{a.year} – {b.day:02d}.{b.month:02d}.{b.year}</td></tr>'
    return f'<div class="tw"><table class="t"><thead><tr><th>Feiertag</th><th style="text-align:right">Urlaubstage</th><th style="text-align:right">Freie Tage am Stück</th><th>Zeitraum</th></tr></thead><tbody>{rows}</tbody></table></div>'


AT_UI = """
<div class="calc">
<h2>Arbeitstage zwischen zwei Daten</h2>
<div class="grid"><div><label for="land">Bundesland</label><select id="land">{opts}</select></div><div><label for="d1">Von</label><input type="date" id="d1" value="{y}-01-01"></div><div><label for="d2">Bis</label><input type="date" id="d2" value="{y}-12-31"></div><div><label for="hpt">Stunden pro Tag</label><input type="number" id="hpt" value="8" step="0.1" min="0"></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="sa"> Samstag ist Arbeitstag</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div>
<dl><dt>Kalendertage</dt><dd id="kt">–</dd><dt>Wochenendtage</dt><dd id="wt">–</dd><dt>Feiertage (Mo–Fr)</dt><dd id="ft">–</dd><dt>Arbeitsstunden</dt><dd id="ah">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Gesetzliche Feiertage des gewählten Bundeslands sind berücksichtigt. Regionale Feiertage (z. B. Augsburger Friedensfest, Fronleichnam in Teilen Sachsens und Thüringens) bitte selbst abziehen.</p>
</div>"""

AT_JS = FT + r"""
(function(){function c(){var a=document.getElementById('d1').value,b=document.getElementById('d2').value;if(!a||!b)return;var A=new Date(a+'T12:00:00'),B=new Date(b+'T12:00:00');if(B<A){var x=A;A=B;B=x}
var L=document.getElementById('land').value,r=atZaehlen(A,B,L,document.getElementById('sa').checked),h=parseFloat(String(document.getElementById('hpt').value).replace(',','.'))||0;
document.getElementById('t').textContent=r.u+' Arbeitstage';document.getElementById('td').textContent=A.toLocaleDateString('de-DE')+' bis '+B.toLocaleDateString('de-DE')+' · '+document.getElementById('land').selectedOptions[0].text;
document.getElementById('kt').textContent=r.t;document.getElementById('wt').textContent=r.w;document.getElementById('ft').textContent=r.f?r.f+' – '+r.n.join(' · '):'keine';document.getElementById('ah').textContent=(r.u*h).toLocaleString('de-DE',{maximumFractionDigits:1})+' Stunden'}
['land','d1','d2','hpt','sa'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""


def at_ui(sel):
    return AT_UI.format(opts=land_opts(sel), y=Y)


# ---------------------------------------------------------------- Hub: Arbeitstage 2026
def _hub_table():
    head = "".join(f"<th style='text-align:right'>{m[:3]}</th>" for m in MONATE)
    rows = ""
    for c, n, slug in LAENDER:
        cells = "".join(f'<td class="num">{arbeitstage_monat(Y, m, c)}</td>' for m in range(1, 13))
        rows += f'<tr><td><a href="/arbeitstage-{Y}-{slug}/">{n}</a></td>{cells}<td class="num"><strong>{arbeitstage_jahr(Y, c)}</strong></td></tr>'
    return f'<div class="tw"><table class="t sm"><thead><tr><th>Bundesland</th>{head}<th style="text-align:right">Jahr</th></tr></thead><tbody>{rows}</tbody></table></div>'


AT_HUB = {
    "path": f"/arbeitstage-{Y}/", "short": f"Arbeitstage {Y}", "tool": True, "group": "kal",
    "card": f"Arbeitstage {Y} pro Monat und Bundesland – mit Rechner für jeden Zeitraum.",
    "title": f"Arbeitstage {Y} – pro Monat und Bundesland (mit Rechner)",
    "desc": f"Wie viele Arbeitstage hat {Y}? Tabelle mit den Arbeitstagen pro Monat für alle 16 Bundesländer, Arbeitsstunden bei 40 und 38,5 Stunden sowie Rechner für beliebige Zeiträume.",
    "h1": f"Arbeitstage {Y} – pro Monat und Bundesland",
    "lead": f"{Y} hat je nach Bundesland zwischen {min(arbeitstage_jahr(Y, c) for c, _, _ in LAENDER)} und {max(arbeitstage_jahr(Y, c) for c, _, _ in LAENDER)} Arbeitstage (Montag bis Freitag, abzüglich gesetzlicher Feiertage). Viele Feiertage fallen {Y} aufs Wochenende – daher gibt es mehr Arbeitstage als 2025.",
    "sources": ["ftgesetze"],
    "body": at_ui("NW") + f"""
<h2>Arbeitstage {Y} pro Monat nach Bundesland</h2>
{_hub_table()}
<p class="hint">Montag bis Freitag abzüglich der landesweiten gesetzlichen Feiertage. In Bayern ist Mariä Himmelfahrt (15.08.) nur in Gemeinden mit überwiegend katholischer Bevölkerung frei – {Y} fällt der Tag ohnehin auf einen Samstag.</p>
<h2>Warum {Y} so viele Arbeitstage hat</h2>
<p>{Y} fallen mehrere Feiertage auf Samstag oder Sonntag: der Tag der Deutschen Einheit (3. Oktober, Samstag), der 2. Weihnachtstag (Samstag), Reformationstag (31. Oktober, Samstag) und Allerheiligen (1. November, Sonntag). Auch der Frauentag in Berlin und Mecklenburg-Vorpommern (8. März) und der Weltkindertag in Thüringen (20. September) liegen auf einem Sonntag. Bundesweit sind nur 7 der 9 einheitlichen Feiertage arbeitsfrei.</p>
<h2>Arbeitstage für dein Bundesland</h2>
<ul class="cols2">{"".join(f'<li><a href="/arbeitstage-{Y}-{slug}/">Arbeitstage {Y} {n}</a> – {arbeitstage_jahr(Y, c)} Tage</li>' for c, n, slug in LAENDER)}</ul>
<h2>Arbeitstage richtig zählen</h2>
<p>Arbeitstage sind in der Praxis Montag bis Freitag. Juristisch zählen als <strong>Werktage</strong> alle Tage außer Sonn- und Feiertage, also auch der Samstag (z. B. beim gesetzlichen Mindesturlaub von 24 Werktagen). Für Urlaubsplanung siehe <a href="/brueckentage-{Y}/">Brückentage {Y}</a>, alle Termine findest du unter <a href="/feiertage-{Y}/">Feiertage {Y}</a>. Monatsstunden für Lohn und Überstunden ermittelst du mit dem <a href="/stundenrechner/">Stundenrechner</a>.</p>
""",
    "faq": [
        (f"Wie viele Arbeitstage hat {Y}?", f"Zwischen {min(arbeitstage_jahr(Y, c) for c, _, _ in LAENDER)} (Baden-Württemberg, Bayern) und {max(arbeitstage_jahr(Y, c) for c, _, _ in LAENDER)} (u. a. Berlin, Hamburg, Niedersachsen) – abhängig von den Feiertagen im Bundesland."),
        ("Wie viele Arbeitstage hat ein Monat im Durchschnitt?", f"Rund 21 Arbeitstage. {Y} reicht die Spanne von 18 Tagen (Mai) bis 23 Tagen (Juli)."),
        (f"Wie viele Arbeitsstunden hat {Y}?", f"Bei 8 Stunden pro Tag und 254 Arbeitstagen sind es 2.032 Stunden, in Bayern und Baden-Württemberg (252 Tage) 2.016 Stunden – vor Abzug von Urlaub und Krankheit."),
        ("Zählt der Samstag als Arbeitstag?", "Bei einer 5-Tage-Woche nicht. Als Werktag zählt der Samstag aber im Arbeitsrecht, etwa beim Urlaubsanspruch nach dem Bundesurlaubsgesetz."),
        (f"Welcher Monat {Y} hat die wenigsten Arbeitstage?", "Der Mai mit 18 Arbeitstagen: Tag der Arbeit, Christi Himmelfahrt und Pfingstmontag fallen alle auf Werktage."),
    ],
    "js": AT_JS,
}


# ---------------------------------------------------------------- 16 Länder pages
def state_page(code, name, slug):
    tot = arbeitstage_jahr(Y, code)
    nh = n_hols(Y, code)
    wdh = wd_hols(Y, code)
    weekend = [n for d, n in feiertage(Y, code).items() if d.weekday() >= 5 and n not in ("Ostersonntag", "Pfingstsonntag")]
    special = [n for d, n, s in all_holidays(Y) if s and code in s and n not in ("Ostersonntag", "Pfingstsonntag")]
    extra = {
        "BY": "In Bayern ist Mariä Himmelfahrt (15.08.) nur in Gemeinden mit überwiegend katholischer Bevölkerung gesetzlicher Feiertag; in Augsburg kommt das Augsburger Friedensfest (08.08.) hinzu. {Y} fallen beide Tage auf einen Samstag.",
        "SN": "In einigen katholisch geprägten Gemeinden der Oberlausitz ist zusätzlich Fronleichnam (04.06.{Y}) arbeitsfrei.",
        "TH": "In Teilen des Eichsfelds ist zusätzlich Fronleichnam (04.06.{Y}) gesetzlicher Feiertag.",
        "BB": "Brandenburg kennt als einziges Land Ostersonntag und Pfingstsonntag als gesetzliche Feiertage; sie fallen naturgemäß auf einen Sonntag.",
        "BE": "Berlin hat seit 2019 den Internationalen Frauentag (08.03.) als Feiertag – {Y} fällt er auf einen Sonntag.",
        "MV": "Mecklenburg-Vorpommern hat seit 2023 den Internationalen Frauentag (08.03.) als Feiertag – {Y} fällt er auf einen Sonntag.",
    }.get(code, "").format(Y=Y)
    hours = tot * 8
    return {
        "path": f"/arbeitstage-{Y}-{slug}/", "short": f"Arbeitstage {Y} {name}", "group": "land", "prio": "0.7",
        "card": f"{tot} Arbeitstage in {name}.",
        "title": f"Arbeitstage {Y} {name} – pro Monat, Feiertage & Stunden",
        "desc": f"{name} hat {Y} {tot} Arbeitstage (Mo–Fr). Tabelle mit Arbeitstagen und Arbeitsstunden pro Monat, allen {nh} Feiertagen in {name} und den besten Brückentagen.",
        "h1": f"Arbeitstage {Y} in {name}",
        "lead": f"{name} hat {Y} <strong>{tot} Arbeitstage</strong> von Montag bis Freitag. Von den {nh} gesetzlichen Feiertagen fallen {wdh} auf einen Werktag. Bei einer 40-Stunden-Woche ergibt das {hours:,} Sollstunden.".replace(",", "."),
        "sources": ["ftgesetze"],
        "body": f"""
<h2>Arbeitstage {Y} {name} pro Monat</h2>
{month_table(Y, code)}
<h2>Feiertage {Y} in {name}</h2>
{hol_list(Y, code)}
<p>{"Landesspezifische Feiertage in " + name + ": " + ", ".join(special) + "." if special else name + " hat ausschließlich die bundeseinheitlichen Feiertage."}{(" Auf ein Wochenende fallen " + Y.__str__() + ": " + ", ".join(weekend) + ".") if weekend else ""} {extra}</p>
<h2>Brückentage {Y} in {name}</h2>
<p>Mit wenigen Urlaubstagen lassen sich lange Freizeiten herausholen. Die Tabelle zeigt für jeden Feiertag die kürzeste Brücke und die Variante mit einer ganzen Urlaubswoche.</p>
{bridge_table(Y, code)}
""" + at_ui(code) + f"""
<p>Alle Länder im Vergleich: <a href="/arbeitstage-{Y}/">Arbeitstage {Y} nach Bundesland</a>. Deinen Urlaubsanspruch rechnest du mit dem <a href="/urlaubsrechner/">Urlaubsrechner</a> aus, Teilzeit-Stunden mit dem <a href="/teilzeitrechner/">Teilzeitrechner</a>.</p>
""",
        "faq": [
            (f"Wie viele Arbeitstage hat {name} {Y}?", f"{tot} Arbeitstage von Montag bis Freitag, nach Abzug der {wdh} Feiertage, die auf einen Werktag fallen."),
            (f"Wie viele Feiertage hat {name} {Y}?", f"{nh} gesetzliche Feiertage; davon fallen {wdh} auf Montag bis Freitag."),
            (f"Wie viele Arbeitsstunden hat {Y} in {name}?", f"Bei 8 Stunden pro Tag {hours:,} Stunden, bei 7,7 Stunden (38,5-Stunden-Woche) rund {round(tot*7.7):,} Stunden.".replace(",", ".")),
            (f"Welcher Monat hat {Y} in {name} die meisten Arbeitstage?", f"Der Juli mit {arbeitstage_monat(Y, 7, code)} Arbeitstagen; die wenigsten hat der Mai mit {arbeitstage_monat(Y, 5, code)}."),
        ],
        "js": AT_JS,
    }


STATES = [state_page(c, n, s) for c, n, s in LAENDER]


# ---------------------------------------------------------------- Feiertage 2026
def _ft_table():
    rows = ""
    for d, n, s in all_holidays(Y):
        if n in ("Ostersonntag", "Pfingstsonntag"):
            continue
        where = "bundesweit" if s is None else ", ".join(LNAME[x] for x in s)
        if n == "Mariä Himmelfahrt":
            where = "Saarland, Bayern (überwiegend katholische Gemeinden)"
        rows += f'<tr><td>{fmt(d)}</td><td>{WT[d.weekday()]}</td><td>{n}</td><td>{where}</td></tr>'
    return f'<div class="tw"><table class="t"><thead><tr><th>Datum</th><th>Wochentag</th><th>Feiertag</th><th>Gültig in</th></tr></thead><tbody>{rows}</tbody></table></div>'


def _count_table():
    rows = "".join(f'<tr><td><a href="/arbeitstage-{Y}-{s}/">{n}</a></td><td class="num">{n_hols(Y, c)}</td><td class="num">{wd_hols(Y, c)}</td></tr>' for c, n, s in LAENDER)
    return f'<div class="tw"><table class="t"><thead><tr><th>Bundesland</th><th style="text-align:right">Feiertage</th><th style="text-align:right">davon Mo–Fr</th></tr></thead><tbody>{rows}</tbody></table></div>'


FT26 = {
    "path": f"/feiertage-{Y}/", "short": f"Feiertage {Y}", "tool": True, "group": "kal",
    "card": f"Alle gesetzlichen Feiertage {Y} mit Wochentag und Bundesländern.",
    "title": f"Feiertage {Y} – alle gesetzlichen Feiertage nach Bundesland",
    "desc": f"Gesetzliche Feiertage {Y} in Deutschland: Datum, Wochentag und in welchen Bundesländern sie gelten. Mit Countdown zum nächsten Feiertag und Anzahl der Feiertage pro Land.",
    "h1": f"Feiertage {Y} in Deutschland",
    "lead": f"Bundesweit gibt es 9 gesetzliche Feiertage, dazu kommen je nach Bundesland bis zu 5 weitere. Ostern ist {Y} am 5. April. Hier findest du alle Termine und den nächsten Feiertag in deinem Bundesland.",
    "sources": ["ftgesetze"],
    "body": f"""
<div class="calc"><h2>Nächster Feiertag</h2>
<div class="grid"><div><label for="land">Bundesland</label><select id="land">{land_opts("NW")}</select></div></div>
<div class="result" aria-live="polite"><div class="big" id="nx">–</div><div class="sub" id="nxd"></div></div></div>
<h2>Alle Feiertage {Y}</h2>
{_ft_table()}
<h2>Anzahl der Feiertage {Y} pro Bundesland</h2>
{_count_table()}
<p>Die meisten Feiertage haben Bayern und Baden-Württemberg; Augsburg kommt mit dem Friedensfest (8. August) sogar auf 14. Weil {Y} der Tag der Deutschen Einheit, der 2. Weihnachtstag, der Reformationstag und Allerheiligen auf ein Wochenende fallen, bleiben weniger freie Werktage als üblich.</p>
<h2>Feiertage planen</h2>
<p>Die besten Kombinationen aus Feiertagen und Urlaub zeigt die Seite <a href="/brueckentage-{Y}/">Brückentage {Y}</a>. Wie viele Arbeitstage übrig bleiben, steht unter <a href="/arbeitstage-{Y}/">Arbeitstage {Y}</a>. Für einen Countdown zu einem eigenen Datum nutze den <a href="/tagerechner/">Tagerechner</a>.</p>
""",
    "faq": [
        (f"Wann ist Ostern {Y}?", f"Ostersonntag ist am 5. April {Y}. Karfreitag ist der 3. April, Ostermontag der 6. April."),
        (f"Wie viele Feiertage gibt es {Y}?", "Bundesweit 9 gesetzliche Feiertage. Je nach Bundesland sind es 10 bis 13 (Bayern, Baden-Württemberg haben die meisten)."),
        (f"Auf welchen Tag fällt der 3. Oktober {Y}?", "Der Tag der Deutschen Einheit fällt 2026 auf einen Samstag."),
        (f"Wann ist Christi Himmelfahrt {Y}?", "Am Donnerstag, 14. Mai 2026. Pfingstmontag ist am 25. Mai, Fronleichnam am 4. Juni."),
        ("Ist Heiligabend ein Feiertag?", "Nein, der 24. Dezember ist kein gesetzlicher Feiertag. Viele Arbeitgeber geben ihn ganz oder halb frei; das regelt der Arbeits- oder Tarifvertrag."),
        ("Ist der Buß- und Bettag ein Feiertag?", f"Nur in Sachsen. {Y} fällt er auf Mittwoch, den 18. November."),
    ],
    "js": FT + r"""
(function(){function c(){var L=document.getElementById('land').value,t=new Date();t.setHours(12,0,0,0);var A=[];[t.getFullYear(),t.getFullYear()+1].forEach(function(y){var F=ftDE(y,L);Object.keys(F).sort().forEach(function(k){A.push([k,F[k]])})});
for(var i=0;i<A.length;i++){var d=new Date(A[i][0]+'T12:00:00');if(d>=t){var n=Math.round((d-t)/864e5);document.getElementById('nx').textContent=n===0?'Heute ist Feiertag!':'noch '+n+(n===1?' Tag':' Tage');document.getElementById('nxd').textContent='bis '+A[i][1]+' – '+d.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'long',year:'numeric'});break}}}
document.getElementById('land').addEventListener('input',c);c()})();""",
}

# ---------------------------------------------------------------- Brückentage 2026
BT26 = {
    "path": f"/brueckentage-{Y}/", "short": f"Brückentage {Y}", "tool": True, "group": "kal",
    "card": f"Brückentage {Y}: mit wenigen Urlaubstagen das Maximum an Freizeit.",
    "title": f"Brückentage {Y} – mit wenig Urlaub maximal frei (alle Bundesländer)",
    "desc": f"Brückentage {Y} clever nutzen: Mit 8 Urlaubstagen zu Ostern 16 Tage frei, mit 1 Tag an Himmelfahrt 4 Tage. Alle Brückentage {Y} bundesweit und nach Bundesland.",
    "h1": f"Brückentage {Y}: die besten Urlaubstipps",
    "lead": f"{Y} ist kein gutes Brückentagsjahr – viele Feiertage fallen aufs Wochenende. Trotzdem lässt sich einiges herausholen: Ostern bringt mit 8 Urlaubstagen 16 freie Tage am Stück, Christi Himmelfahrt mit nur einem Brückentag ein 4-Tage-Wochenende.",
    "sources": ["ftgesetze"],
    "body": f"""
<h2>Die Top-Brückentage {Y} (bundesweit)</h2>
<ol>
<li><strong>Ostern:</strong> 30.03.–02.04. und 07.–10.04. Urlaub (8 Tage) = <strong>16 Tage frei</strong> vom 28.03. bis 12.04.</li>
<li><strong>Christi Himmelfahrt:</strong> Freitag, 15.05. als Brückentag = 4 Tage frei (14.–17.05.).</li>
<li><strong>Neujahr:</strong> Freitag, 02.01. = 4 Tage frei (01.–04.01.).</li>
<li><strong>Weihnachten/Silvester:</strong> 21.–24.12. und 28.–31.12. Urlaub (8 Tage) = <strong>16 Tage frei</strong> vom 19.12.{Y} bis 03.01.{Y+1}.</li>
<li><strong>Tag der Arbeit</strong> (Freitag) und <strong>Pfingstmontag</strong>: lange Wochenenden ohne Urlaub; mit je 4 Urlaubstagen 9 Tage frei.</li>
</ol>
<h2>Alle Brückentage {Y} bundesweit</h2>
{bridge_table(Y, "HH")}
<p class="hint">Basis: die bundesweit einheitlichen Feiertage (Beispiel Hamburg, das nur zusätzlich den Reformationstag kennt, der {Y} auf einen Samstag fällt).</p>
<h2>Zusätzliche Brückentage nach Bundesland</h2>
<ul>
<li><strong>Heilige Drei Könige</strong> (Dienstag, 06.01.) – Baden-Württemberg, Bayern, Sachsen-Anhalt: Brückentag Montag 05.01. = 4 Tage frei (03.–06.01.).</li>
<li><strong>Fronleichnam</strong> (Donnerstag, 04.06.) – Baden-Württemberg, Bayern, Hessen, Nordrhein-Westfalen, Rheinland-Pfalz, Saarland: Brückentag Freitag 05.06. = 4 Tage frei (04.–07.06.).</li>
<li><strong>Buß- und Bettag</strong> (Mittwoch, 18.11.) – Sachsen: Donnerstag und Freitag frei nehmen = 5 Tage frei (18.–22.11.).</li>
<li>Frauentag (Berlin, Mecklenburg-Vorpommern), Weltkindertag (Thüringen), Reformationstag, Allerheiligen und Mariä Himmelfahrt fallen {Y} aufs Wochenende – hier gibt es keine Brücken.</li>
</ul>
<p>Die genaue Tabelle für dein Land findest du auf den Länderseiten, z. B. <a href="/arbeitstage-{Y}-bayern/">Bayern</a>, <a href="/arbeitstage-{Y}-nrw/">NRW</a>, <a href="/arbeitstage-{Y}-baden-wuerttemberg/">Baden-Württemberg</a>, <a href="/arbeitstage-{Y}-sachsen/">Sachsen</a> oder <a href="/arbeitstage-{Y}-hessen/">Hessen</a>.</p>
<h2>Tipps für die Urlaubsplanung</h2>
<ul>
<li>Urlaubsanträge für Brückentage früh stellen – Kollegen haben dieselbe Idee.</li>
<li>Viele Betriebe machen an Brückentagen ohnehin Betriebsurlaub; das wird auf den Jahresurlaub angerechnet.</li>
<li>Wie viele Urlaubstage dir zustehen, berechnet der <a href="/urlaubsrechner/">Urlaubsrechner</a>; alle Termine stehen unter <a href="/feiertage-{Y}/">Feiertage {Y}</a>.</li>
</ul>
""",
    "faq": [
        (f"Welche Brückentage gibt es {Y}?", "Bundesweit: 2. Januar (nach Neujahr) und 15. Mai (nach Christi Himmelfahrt). Regional zusätzlich 5. Januar (Heilige Drei Könige), 5. Juni (Fronleichnam) sowie 19./20. November in Sachsen (Buß- und Bettag)."),
        (f"Wie bekomme ich {Y} mit wenig Urlaub am meisten frei?", "Ostern: 8 Urlaubstage ergeben 16 freie Tage. Weihnachten/Silvester: ebenfalls 8 Urlaubstage für 16 freie Tage."),
        ("Was ist ein Brückentag?", "Ein Arbeitstag zwischen einem Feiertag und dem Wochenende. Wer ihn freinimmt, verlängert das Wochenende mit nur einem Urlaubstag auf vier Tage."),
        (f"Warum ist {Y} ein schlechtes Brückentagsjahr?", "Tag der Deutschen Einheit, 2. Weihnachtstag, Reformationstag und Allerheiligen fallen auf ein Wochenende und bringen keinen freien Werktag."),
    ],
}

# ---------------------------------------------------------------- Urlaubsrechner
URLAUB = {
    "path": "/urlaubsrechner/", "short": "Urlaubsrechner", "tool": True, "group": "arb",
    "card": "Urlaubsanspruch bei Teilzeit, Jobwechsel und unterjährigem Eintritt berechnen.",
    "title": "Urlaubsrechner – Urlaubsanspruch berechnen (Teilzeit, Jobwechsel)",
    "desc": "Urlaubsanspruch berechnen: Urlaubstage bei Teilzeit, anteiliger Urlaub bei Eintritt oder Austritt im Laufe des Jahres und gesetzlicher Mindesturlaub nach dem Bundesurlaubsgesetz (BUrlG).",
    "h1": "Urlaubsrechner: Urlaubsanspruch berechnen",
    "lead": "Wie viele Urlaubstage stehen dir zu? Trage den Jahresurlaub laut Vertrag, deine Arbeitstage pro Woche und den Beschäftigungszeitraum ein – der Rechner ermittelt den anteiligen Anspruch nach dem Bundesurlaubsgesetz.",
    "sources": ["burlg", "sgb9"],
    "body": """
<div class="calc">
<h2>Urlaubsanspruch berechnen</h2>
<div class="grid"><div><label for="ju">Jahresurlaub Vollzeit (Tage)</label><input type="number" id="ju" value="30" min="0"></div><div><label for="vt">Arbeitstage/Woche Vollzeit</label><input type="number" id="vt" value="5" min="1" max="6"></div><div><label for="et">Deine Arbeitstage/Woche</label><input type="number" id="et" value="5" min="0" max="6" step="0.5"></div></div>
<div class="grid" style="margin-top:12px"><div><label for="von">Beschäftigt ab Monat</label><select id="von"></select></div><div><label for="bis">bis Monat</label><select id="bis"></select></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="sb"> Schwerbehindert (+5 Tage, § 208 SGB IX)</label><label class="chk"><input type="checkbox" id="wz"> Wartezeit (6 Monate) erfüllt, Austritt nach dem 30.06.</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div>
<dl><dt>Voller Jahresanspruch</dt><dd id="vj">–</dd><dt>Gesetzlicher Mindesturlaub</dt><dd id="mu">–</dd><dt>Berechnung</dt><dd id="be">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Bruchteile ab einem halben Tag werden beim Teilurlaub aufgerundet (§ 5 Abs. 2 BUrlG). Tarif- und Arbeitsverträge können günstigere Regeln enthalten.</p>
</div>
<h2>So wird der Urlaubsanspruch berechnet</h2>
<div class="formula">Urlaubstage = Jahresurlaub × eigene Arbeitstage pro Woche ÷ Arbeitstage Vollzeit</div>
<p>Beispiel: 30 Tage Urlaub bei Vollzeit (5-Tage-Woche), du arbeitest 3 Tage pro Woche: 30 × 3 ÷ 5 = <strong>18 Urlaubstage</strong>. Damit hast du genauso viele Wochen frei wie Vollzeitkräfte – nämlich 6.</p>
<h2>Gesetzlicher Mindesturlaub</h2>
<ul>
<li><strong>24 Werktage</strong> pro Jahr bei einer 6-Tage-Woche (§ 3 BUrlG), das entspricht <strong>20 Arbeitstagen</strong> bei 5 Tagen pro Woche – also 4 Wochen.</li>
<li><strong>Wartezeit:</strong> Der volle Anspruch entsteht erstmals nach 6 Monaten Beschäftigung (§ 4 BUrlG).</li>
<li><strong>Teilurlaub:</strong> 1/12 des Jahresurlaubs pro vollem Monat, wenn die Wartezeit im Kalenderjahr nicht erfüllt wird oder du in der ersten Jahreshälfte ausscheidest (§ 5 BUrlG). Wer nach erfüllter Wartezeit in der zweiten Jahreshälfte ausscheidet, behält den vollen gesetzlichen Mindesturlaub.</li>
<li><strong>Schwerbehinderte Menschen</strong> erhalten 5 zusätzliche Arbeitstage (§ 208 SGB IX), bei weniger Arbeitstagen anteilig.</li>
<li><strong>Jugendliche</strong>: 25 bis 30 Werktage je nach Alter (§ 19 JArbSchG).</li>
<li><strong>Übertragung:</strong> Resturlaub muss grundsätzlich bis 31. März des Folgejahres genommen werden (§ 7 Abs. 3 BUrlG); er verfällt nur, wenn der Arbeitgeber rechtzeitig auf den drohenden Verfall hingewiesen hat.</li>
</ul>
<p>Die passenden Urlaubstermine findest du bei den <a href="/brueckentage-2026/">Brückentagen 2026</a>. Bei Teilzeit hilft auch der <a href="/teilzeitrechner/">Teilzeitrechner</a>.</p>
""",
    "faq": [
        ("Wie viel Urlaub steht mir bei Teilzeit zu?", "Jahresurlaub × eigene Arbeitstage pro Woche ÷ Arbeitstage bei Vollzeit. Bei 30 Tagen Vollzeiturlaub und 3 Arbeitstagen sind es 18 Tage."),
        ("Wie viel Urlaub bekomme ich, wenn ich im Laufe des Jahres anfange?", "Im Eintrittsjahr ohne erfüllte Wartezeit 1/12 des Jahresurlaubs pro vollem Beschäftigungsmonat, z. B. 30 × 5/12 = 12,5, aufgerundet 13 Tage bei Beginn am 1. August."),
        ("Wie hoch ist der gesetzliche Mindesturlaub?", "24 Werktage bei einer 6-Tage-Woche, also 20 Arbeitstage bei einer 5-Tage-Woche (§ 3 BUrlG)."),
        ("Verfällt Resturlaub am 31. März?", "Nur, wenn der Arbeitgeber dich vorher konkret aufgefordert hat, den Urlaub zu nehmen, und auf den Verfall hingewiesen hat (EuGH und BAG seit 2019)."),
        ("Werden halbe Urlaubstage aufgerundet?", "Beim Teilurlaub nach § 5 BUrlG werden Bruchteile von mindestens einem halben Tag auf einen vollen Tag aufgerundet."),
    ],
    "js": r"""
(function(){var M=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'],v=document.getElementById('von'),b=document.getElementById('bis');M.forEach(function(m,i){v.add(new Option(m,i+1));b.add(new Option(m,i+1))});b.value=12;
function n(id){return parseFloat(String(document.getElementById(id).value).replace(',','.'))||0}
function c(){var ju=n('ju'),vt=n('vt'),et=n('et'),f=+v.value,t=+b.value,mo=Math.max(0,t-f+1),full=vt?ju*et/vt:0;if(document.getElementById('sb').checked)full+=5*et/5;
var wz=document.getElementById('wz').checked,anteil=mo>=12||(wz&&t>6)?full:full*mo/12,r=mo>=12?anteil:(anteil%1>=.5?Math.ceil(anteil):Math.floor(anteil)),mind=20*et/5;
if(wz&&t>6&&mo<12){r=Math.max(Math.round(full*mo/12),Math.ceil(mind))}
document.getElementById('t').textContent=(Math.round(r*10)/10).toLocaleString('de-DE')+' Urlaubstage';document.getElementById('td').textContent=mo>=12?'voller Jahresanspruch':'anteilig für '+mo+' Monat(e)';
document.getElementById('vj').textContent=(Math.round(full*10)/10).toLocaleString('de-DE')+' Tage';document.getElementById('mu').textContent=(Math.round(mind*10)/10).toLocaleString('de-DE')+' Tage (24 Werktage)';
document.getElementById('be').textContent=ju+' × '+et+' ÷ '+vt+(mo<12?' × '+mo+'/12':'')}
['ju','vt','et','von','bis','sb','wz'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

# ---------------------------------------------------------------- Teilzeitrechner
TEILZ = {
    "path": "/teilzeitrechner/", "short": "Teilzeitrechner", "tool": True, "group": "arb",
    "card": "Teilzeitgehalt, Stunden pro Tag, Teilzeitquote und Urlaubstage berechnen.",
    "title": "Teilzeitrechner – Teilzeitgehalt und Stunden berechnen (2026)",
    "desc": "Teilzeitrechner: Aus Vollzeitgehalt und Wochenstunden das Teilzeitgehalt brutto, den Stundenlohn, die Teilzeitquote in Prozent, die Stunden pro Tag und die Urlaubstage berechnen.",
    "h1": "Teilzeitrechner: Gehalt, Stunden und Urlaub bei Teilzeit",
    "lead": "Wie viel verdienst du bei 20, 25 oder 30 Stunden? Gib Vollzeitgehalt und -stunden ein, dann deine gewünschten Teilzeitstunden. Der Rechner zeigt Bruttogehalt, Teilzeitquote, tägliche Arbeitszeit und Urlaubsanspruch.",
    "sources": ["tzbfg", "burlg"],
    "body": """
<div class="calc">
<h2>Teilzeit berechnen</h2>
<div class="grid"><div><label for="vg">Vollzeitgehalt brutto (€/Monat)</label><input type="number" id="vg" value="3800" step="50" min="0"></div><div><label for="vs">Vollzeit Stunden/Woche</label><input type="number" id="vs" value="40" step="0.5" min="1"></div><div><label for="ts">Teilzeit Stunden/Woche</label><input type="number" id="ts" value="25" step="0.5" min="0"></div></div>
<div class="grid" style="margin-top:12px"><div><label for="td_">Arbeitstage/Woche (Teilzeit)</label><input type="number" id="td_" value="5" step="0.5" min="0.5" max="6"></div><div><label for="vu">Urlaub Vollzeit (Tage, 5-Tage-Woche)</label><input type="number" id="vu" value="30" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub">Teilzeitgehalt brutto pro Monat</div>
<dl><dt>Teilzeitquote</dt><dd id="q">–</dd><dt>Stundenlohn brutto</dt><dd id="sl">–</dd><dt>Stunden pro Arbeitstag</dt><dd id="hd">–</dd><dt>Stunden pro Monat</dt><dd id="hm">–</dd><dt>Urlaubstage</dt><dd id="u">–</dd><dt>Jahresgehalt brutto</dt><dd id="jg">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Bruttowerte. Durch den progressiven Steuertarif sinkt das Netto bei Teilzeit meist weniger stark als das Brutto. Liegt das Gehalt zwischen 603,01 € und 2.000 €, gelten die reduzierten Arbeitnehmerbeiträge im Übergangsbereich (Midijob).</p>
</div>
<h2>Formeln</h2>
<div class="formula">Teilzeitgehalt = Vollzeitgehalt × Teilzeitstunden ÷ Vollzeitstunden &nbsp;·&nbsp; Urlaub = Vollzeiturlaub × Arbeitstage ÷ 5</div>
<p>Beispiel: 3.800 € bei 40 Stunden, Teilzeit mit 25 Stunden an 5 Tagen: 3.800 × 25 ÷ 40 = <strong>2.375 € brutto</strong> (62,5 %), 5 Stunden pro Tag, weiterhin 30 Urlaubstage. Wer die 25 Stunden auf 3 Tage verteilt, arbeitet 8,33 Stunden pro Tag und hat 18 Urlaubstage – die Zahl der freien Wochen bleibt gleich.</p>
<h2>Anspruch auf Teilzeit</h2>
<ul>
<li><strong>Allgemeiner Teilzeitanspruch</strong> (§ 8 TzBfG): nach 6 Monaten Beschäftigung in Betrieben mit mehr als 15 Beschäftigten; Antrag spätestens 3 Monate vor Beginn in Textform.</li>
<li><strong>Brückenteilzeit</strong> (§ 9a TzBfG): befristet für 1 bis 5 Jahre mit Rückkehrrecht in Vollzeit, in Betrieben mit mehr als 45 Beschäftigten.</li>
<li><strong>Elternzeit</strong>: Teilzeit von 15 bis 32 Wochenstunden (§ 15 BEEG).</li>
<li><strong>Diskriminierungsverbot:</strong> Teilzeitkräfte dürfen nicht schlechter behandelt werden; Lohn und Sonderzahlungen stehen ihnen anteilig zu (§ 4 TzBfG).</li>
</ul>
<p>Den genauen Urlaubsanspruch bei Eintritt im Laufe des Jahres liefert der <a href="/urlaubsrechner/">Urlaubsrechner</a>, den Stundenlohn der <a href="/stundenlohnrechner/">Stundenlohnrechner</a>. Für Jobs bis 603 € siehe den <a href="/minijob-rechner/">Minijob-Rechner</a>.</p>
""",
    "faq": [
        ("Wie berechne ich mein Teilzeitgehalt?", "Vollzeitgehalt × Teilzeitstunden ÷ Vollzeitstunden. Bei 4.000 € und 30 von 40 Stunden: 4.000 × 30 ÷ 40 = 3.000 € brutto."),
        ("Wie viel Prozent sind 30 Stunden bei 40 Stunden Vollzeit?", "75 %. 20 Stunden sind 50 %, 25 Stunden 62,5 %, 32 Stunden 80 %."),
        ("Bekomme ich bei Teilzeit weniger Urlaub?", "Nur wenn du an weniger Tagen pro Woche arbeitest. Bei gleich vielen Arbeitstagen (z. B. 5 kürzere Tage) bleibt der Urlaubsanspruch in Tagen gleich."),
        ("Wann habe ich Anspruch auf Teilzeit?", "Nach 6 Monaten im Betrieb, wenn der Arbeitgeber regelmäßig mehr als 15 Arbeitnehmer beschäftigt (§ 8 TzBfG). Der Antrag muss 3 Monate vor Beginn gestellt werden."),
    ],
    "js": r"""
(function(){function n(id){return parseFloat(String(document.getElementById(id).value).replace(',','.'))||0}
function c(){var vg=n('vg'),vs=n('vs'),ts=n('ts'),td=n('td_'),vu=n('vu'),q=vs?ts/vs:0,g=vg*q,hm=ts*52/12;
document.getElementById('t').textContent=eur(g);document.getElementById('q').textContent=(q*100).toLocaleString('de-DE',{maximumFractionDigits:1})+' %';document.getElementById('sl').textContent=eur(hm?g/hm:0);
document.getElementById('hd').textContent=td?fmtHM(ts/td*60)+' h ('+(ts/td).toLocaleString('de-DE',{maximumFractionDigits:2})+')':'–';document.getElementById('hm').textContent=hm.toLocaleString('de-DE',{maximumFractionDigits:1})+' h';
document.getElementById('u').textContent=(Math.round(vu*td/5*10)/10).toLocaleString('de-DE')+' Tage';document.getElementById('jg').textContent=eur(g*12)}
['vg','vs','ts','td_','vu'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

# ---------------------------------------------------------------- Minijob-Rechner
MINI = {
    "path": "/minijob-rechner/", "short": "Minijob-Rechner", "tool": True, "group": "arb",
    "card": "Minijob 2026: 603-€-Grenze, maximale Stunden, Abgaben und Netto.",
    "title": "Minijob-Rechner 2026 – Stunden, 603-€-Grenze und Abgaben",
    "desc": "Minijob-Rechner 2026: Monatsverdienst aus Stundenlohn und Stunden, Prüfung der 603-€-Grenze, maximale Stunden zum Mindestlohn (13,90 €), Rentenbeitrag, Netto und Arbeitgeberkosten.",
    "h1": "Minijob-Rechner 2026",
    "lead": "Bleibst du unter 603 € im Monat? Gib Stundenlohn und Arbeitsstunden ein: Der Rechner zeigt den Monatsverdienst, wie viele Stunden du maximal arbeiten darfst, dein Netto mit oder ohne Rentenversicherung und was der Minijob den Arbeitgeber kostet.",
    "sources": ["minijob", "milog"],
    "body": """
<div class="calc">
<h2>Minijob berechnen</h2>
<div class="grid"><div><label for="sl">Stundenlohn (€)</label><input type="number" id="sl" value="13.90" step="0.05" min="0"></div><div><label for="h">Stunden</label><input type="number" id="h" value="10" step="0.5" min="0"></div><div><label for="per">Zeitraum</label><select id="per"><option value="w" selected>pro Woche</option><option value="m">pro Monat</option></select></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="rv" checked> Rentenversicherungspflicht (keine Befreiung beantragt)</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div>
<dl><dt>Monatsverdienst brutto</dt><dd id="mv">–</dd><dt>Max. Stunden/Monat bei diesem Lohn</dt><dd id="mx">–</dd><dt>Dein Rentenbeitrag (3,6 %)</dt><dd id="rb">–</dd><dt>Netto</dt><dd id="ne">–</dd><dt>Arbeitgeberkosten (ca.)</dt><dd id="ag">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Gewerblicher Minijob: Arbeitgeber zahlt pauschal 13 % Krankenversicherung, 15 % Rentenversicherung und 2 % Pauschsteuer plus Umlagen (U1, U2, Insolvenzgeld, zusammen ca. 1,2 %) und Unfallversicherung. Im Privathaushalt gelten niedrigere Pauschalen.</p>
</div>
<h2>Minijob-Grenze 2026: 603 €</h2>
<p>Seit 2024 ist die Verdienstgrenze an den Mindestlohn gekoppelt: Mindestlohn × 130 ÷ 3, aufgerundet. Mit <strong>13,90 €</strong> ergibt das <strong>603 € pro Monat</strong> bzw. 7.236 € im Jahr. Zum 1. Januar 2027 steigt der Mindestlohn auf 14,60 €, die Grenze damit auf <strong>633 €</strong>.</p>
<div class="formula">Max. Stunden pro Monat = 603 € ÷ Stundenlohn &nbsp;·&nbsp; zum Mindestlohn: 603 ÷ 13,90 = 43,4 Stunden (rund 10 Stunden pro Woche)</div>
<h2>Wichtige Regeln</h2>
<ul>
<li><strong>Durchschnitt zählt:</strong> Maßgeblich ist das regelmäßige Entgelt im Jahresdurchschnitt. Ein unvorhersehbares Überschreiten ist in bis zu 2 Monaten pro Jahr erlaubt, jeweils bis zum Doppelten der Grenze.</li>
<li><strong>Rentenversicherung:</strong> Minijobber sind grundsätzlich rentenversicherungspflichtig und zahlen die Differenz zum vollen Beitrag (18,6 % − 15 % = 3,6 %). Eine Befreiung ist auf Antrag möglich.</li>
<li><strong>Mehrere Minijobs</strong> werden zusammengerechnet. Neben einem Hauptjob ist ein Minijob abgabenfrei für den Arbeitnehmer möglich.</li>
<li><strong>Mindestlohn, Urlaub, Lohnfortzahlung:</strong> gelten auch im Minijob.</li>
<li><strong>Über 603 €:</strong> Ab 603,01 € beginnt der Übergangsbereich (Midijob) bis 2.000 € mit reduzierten Arbeitnehmerbeiträgen.</li>
</ul>
<p>Stunden zusammenrechnen kannst du mit dem <a href="/stundenrechner/">Stundenrechner</a>, den Lohn pro Stunde prüft der <a href="/stundenlohnrechner/">Stundenlohnrechner</a>. Mehr Stunden geplant? Dann hilft der <a href="/teilzeitrechner/">Teilzeitrechner</a>.</p>
""",
    "faq": [
        ("Wie viel darf ich 2026 im Minijob verdienen?", "603 € pro Monat bzw. 7.236 € im Jahr. Ab 2027 sind es 633 €, weil der Mindestlohn auf 14,60 € steigt."),
        ("Wie viele Stunden darf ich im Minijob arbeiten?", "Es gibt keine feste Stundengrenze, nur die Verdienstgrenze. Zum Mindestlohn von 13,90 € sind es maximal 43,4 Stunden im Monat, also rund 10 Stunden pro Woche."),
        ("Was bleibt netto vom Minijob?", "Ohne Befreiung von der Rentenversicherung zahlst du 3,6 % Rentenbeitrag: Von 603 € bleiben 581,29 €. Mit Befreiung erhältst du den vollen Betrag."),
        ("Was kostet ein Minijob den Arbeitgeber?", "Rund 31 % Abgaben zusätzlich zum Lohn: 13 % Kranken-, 15 % Rentenversicherung, 2 % Pauschsteuer und etwa 1,2 % Umlagen, dazu der Beitrag zur Unfallversicherung."),
        ("Darf ich den Minijob-Verdienst einmal überschreiten?", "Ja, gelegentlich und unvorhersehbar in bis zu 2 Kalendermonaten pro Jahr, jeweils höchstens bis zum doppelten Grenzbetrag."),
    ],
    "js": r"""
(function(){var G=603;function n(id){return parseFloat(String(document.getElementById(id).value).replace(',','.'))||0}
function c(){var sl=n('sl'),h=n('h'),m=document.getElementById('per').value==='w'?h*52/12:h,mv=sl*m,rv=document.getElementById('rv').checked,rb=rv?Math.round(mv*.036*100)/100:0;
var ok=mv<=G;document.getElementById('t').textContent=ok?'Minijob ✓':'über 603 €';document.getElementById('td').textContent=ok?'noch '+eur(G-mv)+' Spielraum bis zur Grenze':'Übergangsbereich (Midijob) – sozialversicherungspflichtig';
document.getElementById('mv').textContent=eur(mv)+' ('+m.toLocaleString('de-DE',{maximumFractionDigits:1})+' h)';document.getElementById('mx').textContent=sl?(G/sl).toLocaleString('de-DE',{maximumFractionDigits:1})+' h ('+(G/sl*12/52).toLocaleString('de-DE',{maximumFractionDigits:1})+' h/Woche)':'–';
document.getElementById('rb').textContent=ok?'− '+eur(rb):'–';document.getElementById('ne').textContent=ok?eur(mv-rb):'–';document.getElementById('ag').textContent=ok?eur(mv*1.3117)+' (Lohn + ca. 31,2 %)':'–'}
['sl','h','per','rv'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

# ---------------------------------------------------------------- Altersrechner
ALTER = {
    "path": "/altersrechner/", "short": "Altersrechner", "tool": True, "group": "kal",
    "card": "Alter exakt in Jahren, Monaten und Tagen – plus Tage bis zum Geburtstag.",
    "title": "Altersrechner – Alter berechnen in Jahren, Monaten und Tagen",
    "desc": "Alter berechnen: Geburtsdatum eingeben und das genaue Alter in Jahren, Monaten und Tagen sehen, dazu gelebte Tage und Wochen, Wochentag der Geburt und Tage bis zum nächsten Geburtstag.",
    "h1": "Altersrechner: Alter berechnen",
    "lead": "Gib dein Geburtsdatum ein, um dein exaktes Alter in Jahren, Monaten und Tagen zu berechnen – oder das Alter an einem bestimmten Stichtag, etwa für Rente, Führerschein oder Bewerbungsfristen.",
    "sources": [],
    "body": """
<div class="calc">
<h2>Alter berechnen</h2>
<div class="grid"><div><label for="geb">Geburtsdatum</label><input type="date" id="geb" value="1990-05-15"></div><div><label for="st">Alter am Stichtag</label><input type="date" id="st"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div>
<dl><dt>Monate gesamt</dt><dd id="mg">–</dd><dt>Wochen gesamt</dt><dd id="wg">–</dd><dt>Tage gesamt</dt><dd id="tg">–</dd><dt>Geboren an einem</dt><dd id="wt">–</dd><dt>Nächster Geburtstag</dt><dd id="ng">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
</div>
<h2>So berechnest du das Alter</h2>
<p>Ziehe das Geburtsjahr vom aktuellen Jahr ab. Hattest du dieses Jahr noch nicht Geburtstag, ziehe 1 ab. Monate und Tage zählt man ab dem letzten Geburtstag weiter. Beispiel: Wer am 15.05.1990 geboren ist, ist am 10.10.2026 <strong>36 Jahre, 4 Monate und 25 Tage</strong> alt.</p>
<h2>Altersgrenzen im Alltag</h2>
<ul>
<li><strong>Volljährigkeit:</strong> 18 Jahre (§ 2 BGB).</li>
<li><strong>Regelaltersrente:</strong> steigt schrittweise auf 67 Jahre; für den Jahrgang 1964 und jünger gilt 67 (§ 235 SGB VI).</li>
<li><strong>Jugendarbeitsschutz:</strong> Beschäftigung grundsätzlich ab 15 Jahren; Jugendliche unter 18 haben mehr Urlaub und kürzere Arbeitszeiten (JArbSchG).</li>
<li><strong>Führerschein B:</strong> ab 18, begleitetes Fahren ab 17 Jahren.</li>
</ul>
<p>Die Differenz zwischen zwei beliebigen Daten berechnet der <a href="/tagerechner/">Tagerechner</a>; Zeitspannen in Stunden und Minuten der <a href="/zeitrechner/">Zeitrechner</a>.</p>
""",
    "faq": [
        ("Wie berechne ich mein genaues Alter?", "Geburtsdatum eingeben – der Altersrechner zeigt das Alter in Jahren, Monaten und Tagen sowie die Gesamtzahl der gelebten Tage."),
        ("Wie viele Tage bin ich alt?", "Der Rechner zählt alle Kalendertage vom Geburtstag bis heute oder bis zum gewählten Stichtag."),
        ("Wann habe ich am 29. Februar Geburtstag?", "In Nicht-Schaltjahren gilt rechtlich der Ablauf des 28. Februar als Vollendung des Lebensjahres; der Rechner zählt bis zum 1. März als nächstem Geburtstag."),
        ("Wie berechne ich das Alter an einem bestimmten Datum?", "Trage den Stichtag in das zweite Feld ein, z. B. den Rentenbeginn oder eine Bewerbungsfrist."),
    ],
    "js": r"""
(function(){var t=new Date();document.getElementById('st').value=t.getFullYear()+'-'+pad(t.getMonth()+1)+'-'+pad(t.getDate());
function c(){var a=document.getElementById('geb').value,b=document.getElementById('st').value;if(!a||!b)return;var A=new Date(a+'T12:00:00'),B=new Date(b+'T12:00:00');if(B<A){document.getElementById('t').textContent='Ungültiges Datum';return}
var y=B.getFullYear()-A.getFullYear(),m=B.getMonth()-A.getMonth(),d=B.getDate()-A.getDate();if(d<0){m--;d+=new Date(B.getFullYear(),B.getMonth(),0).getDate()}if(m<0){y--;m+=12}
var tot=Math.round((B-A)/864e5),N=new Date(B.getFullYear(),A.getMonth(),A.getDate(),12);if(N<=B)N=new Date(B.getFullYear()+1,A.getMonth(),A.getDate(),12);var f=Math.round((N-B)/864e5);
document.getElementById('t').textContent=y+' Jahre';document.getElementById('td').textContent=m+' Monat(e) und '+d+' Tag(e)';document.getElementById('mg').textContent=(y*12+m).toLocaleString('de-DE');
document.getElementById('wg').textContent=Math.floor(tot/7).toLocaleString('de-DE');document.getElementById('tg').textContent=tot.toLocaleString('de-DE');document.getElementById('wt').textContent=A.toLocaleDateString('de-DE',{weekday:'long'});
document.getElementById('ng').textContent=N.toLocaleDateString('de-DE')+' – noch '+f+' Tag(e), dann '+(N.getFullYear()-A.getFullYear())+' Jahre'}
['geb','st'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

CONTENT = [AT_HUB, FT26, BT26, URLAUB, TEILZ, MINI, ALTER] + STATES
