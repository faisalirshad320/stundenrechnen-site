# -*- coding: utf-8 -*-
"""Tier-2 converter/answer pages (Oct 2026): high-volume KD-0 gaps not covered by
existing tools. minuten-in-stunden, stunden-umrechnen, wie-viele-stunden-hat-ein-monat,
40-stunden-woche, kalenderwoche. (stunden↔dezimal and monatslohn↔stundenlohn are already
covered by /dezimal-rechner/ and /stundenlohnrechner/.)"""
import calendar
import datetime as dt
from pages_tools import AD

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
WT = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def de(n, d=2):
    return f"{n:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------- 1) Minuten in Stunden
def _min_rows():
    vals = [15, 30, 45, 60, 75, 90, 108, 120, 135, 150, 180, 200, 210, 240, 300, 360, 420, 480, 540, 600, 720, 1000]
    half = (len(vals) + 1) // 2
    cols = list(zip(vals[:half], vals[half:] + [None]))
    rows = ""
    for a, b in cols:
        def cell(v):
            if v is None:
                return "<td></td><td></td>"
            h, m = divmod(v, 60)
            return f'<td class="num">{v}</td><td class="num">{h}:{m:02d} ({de(v/60)})</td>'
        rows += f"<tr>{cell(a)}{cell(b)}</tr>"
    return rows


MINUTEN = {
    "path": "/minuten-in-stunden/", "short": "Minuten in Stunden", "tool": True, "group": "zeit",
    "card": "Minuten in Stunden umrechnen – Rechner und Tabelle (z. B. 90 Minuten = 1,5 Stunden).",
    "title": "Minuten in Stunden umrechnen – Rechner & Tabelle",
    "desc": "Minuten in Stunden umrechnen: 90 Minuten sind 1,5 Stunden. Rechner in beide Richtungen plus Umrechnungstabelle von 15 bis 1000 Minuten.",
    "h1": "Minuten in Stunden umrechnen",
    "lead": "Wie viele Stunden sind 90, 150 oder 200 Minuten? Gib die Minuten ein – der Rechner zeigt das Ergebnis als Stunden:Minuten und als Dezimalstunde. Darunter findest du die komplette Umrechnungstabelle.",
    "body": f"""
<div class="calc">
<h2>Minuten → Stunden</h2>
<div class="grid"><div><label for="min">Minuten</label><input type="number" id="min" value="150" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">2:30</div><div class="sub" id="td">2 Stunden und 30 Minuten · 2,5 Dezimalstunden</div></div>
</div>
<div class="calc">
<h2>Stunden → Minuten</h2>
<div class="grid"><div><label for="h">Stunden</label><input type="number" id="h" value="2" min="0"></div><div><label for="m">Minuten</label><input type="number" id="m" value="30" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">150</div><div class="sub">Minuten</div></div>
</div>
{AD}
<h2>Umrechnungstabelle: Minuten in Stunden</h2>
<div class="tw"><table class="t sm"><thead><tr><th>Minuten</th><th style="text-align:right">Stunden</th><th>Minuten</th><th style="text-align:right">Stunden</th></tr></thead><tbody>{_min_rows()}</tbody></table></div>
<h2>So rechnest du Minuten in Stunden um</h2>
<div class="formula">Stunden = Minuten ÷ 60</div>
<p>Teile die Minuten durch 60. Der ganzzahlige Teil sind die vollen Stunden, der Rest sind die restlichen Minuten.
Beispiel: 150 ÷ 60 = 2 Rest 30, also <strong>2 Stunden und 30 Minuten</strong>. Als Dezimalzahl: 150 ÷ 60 = 2,5 Stunden.</p>
<p>Für die Zeiterfassung brauchst du oft die Dezimalschreibweise (z. B. 2,5 statt 2:30). Diese Umrechnung inklusive
Industrieminuten übernimmt der <a href="/dezimal-rechner/">Dezimal-Rechner</a>. Mehrere Zeiten addierst du mit dem
<a href="/stundenrechner/">Stundenrechner</a>.</p>
""",
    "faq": [
        ("Wie viele Stunden sind 90 Minuten?", "1,5 Stunden, also 1 Stunde und 30 Minuten (90 ÷ 60 = 1,5)."),
        ("Wie viele Stunden sind 150 Minuten?", "2,5 Stunden bzw. 2 Stunden und 30 Minuten."),
        ("Wie rechne ich 200 Minuten in Stunden um?", "200 ÷ 60 = 3,33 Stunden, also 3 Stunden und 20 Minuten."),
        ("Wie viele Stunden sind 1000 Minuten?", "16,67 Stunden, also 16 Stunden und 40 Minuten."),
    ],
    "js": r"""
(function(){function c1(){var v=parseFloat(document.getElementById('min').value)||0,h=Math.floor(v/60),m=Math.round(v-h*60);document.getElementById('t').textContent=h+':'+pad(m);document.getElementById('td').textContent=h+' Stunden und '+m+' Minuten · '+fmtDec(v)+' Dezimalstunden'}
function c2(){var h=parseFloat(document.getElementById('h').value)||0,m=parseFloat(document.getElementById('m').value)||0;document.getElementById('t2').textContent=Math.round(h*60+m).toLocaleString('de-DE')}
document.getElementById('min').addEventListener('input',c1);['h','m'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c1();c2()})();""",
}


# ---------------------------------------------------------------- 2) Stunden umrechnen (Min/Sek/Tage)
def _std_rows():
    vals = [1, 2, 4, 6, 8, 12, 24, 36, 48, 72, 96, 100, 168, 500, 1000]
    rows = ""
    for h in vals:
        rows += (f'<tr><td class="num">{h}</td><td class="num">{h*60:,}</td>'
                 f'<td class="num">{h*3600:,}</td><td class="num">{de(h/24)}</td></tr>').replace(",", ".")
    return rows


STDUM = {
    "path": "/stunden-umrechnen/", "short": "Stunden umrechnen", "tool": True, "group": "zeit",
    "card": "Stunden in Minuten, Sekunden und Tage umrechnen – Rechner und Tabelle.",
    "title": "Stunden umrechnen – in Minuten, Sekunden und Tage",
    "desc": "Stunden umrechnen in Minuten, Sekunden und Tage. Wie viele Tage sind 72 Stunden? Rechner in alle Richtungen plus Umrechnungstabelle.",
    "h1": "Stunden umrechnen: Minuten, Sekunden und Tage",
    "lead": "Wie viele Sekunden hat eine Stunde, wie viele Tage sind 72 Stunden? Gib einen Wert ein – der Rechner zeigt die Stunden sofort in Minuten, Sekunden und Tagen an.",
    "body": f"""
<div class="calc">
<h2>Stunden umrechnen</h2>
<div class="grid"><div><label for="val">Wert</label><input type="number" id="val" value="72" step="0.5" min="0"></div><div><label for="unit">Einheit</label><select id="unit"><option value="h" selected>Stunden</option><option value="min">Minuten</option><option value="s">Sekunden</option><option value="d">Tage</option></select></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">3 Tage</div><div class="sub" id="td"></div>
<dl><dt>Stunden</dt><dd id="rh">–</dd><dt>Minuten</dt><dd id="rm">–</dd><dt>Sekunden</dt><dd id="rs">–</dd><dt>Tage</dt><dd id="rd">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
</div>
{AD}
<h2>Umrechnungstabelle Stunden</h2>
<div class="tw"><table class="t sm"><thead><tr><th>Stunden</th><th style="text-align:right">Minuten</th><th style="text-align:right">Sekunden</th><th style="text-align:right">Tage</th></tr></thead><tbody>{_std_rows()}</tbody></table></div>
<h2>Die Umrechnungen im Überblick</h2>
<ul>
<li><strong>Stunden → Minuten:</strong> × 60. Eine Stunde hat 60 Minuten.</li>
<li><strong>Stunden → Sekunden:</strong> × 3.600. Eine Stunde hat 60 × 60 = 3.600 Sekunden.</li>
<li><strong>Stunden → Tage:</strong> ÷ 24. 72 Stunden sind 72 ÷ 24 = 3 Tage.</li>
</ul>
<p>Beispiel: 100 Stunden sind 6.000 Minuten, 360.000 Sekunden oder rund 4,17 Tage. Für Zeitspannen zwischen zwei
Uhrzeiten nutze den <a href="/zeitrechner/">Zeitrechner</a>, für Tage zwischen zwei Daten den
<a href="/tagerechner/">Tagerechner</a>.</p>
""",
    "faq": [
        ("Wie viele Tage sind 72 Stunden?", "Genau 3 Tage (72 ÷ 24 = 3)."),
        ("Wie viele Sekunden hat eine Stunde?", "3.600 Sekunden (60 Minuten × 60 Sekunden)."),
        ("Wie viele Tage sind 1000 Stunden?", "Rund 41,7 Tage (1000 ÷ 24 = 41,67)."),
        ("Wie viele Minuten hat ein Tag?", "1.440 Minuten (24 Stunden × 60)."),
    ],
    "js": r"""
(function(){function toH(){var v=parseFloat(document.getElementById('val').value)||0,u=document.getElementById('unit').value;return u==='h'?v:u==='min'?v/60:u==='s'?v/3600:v*24}
function c(){var h=toH();document.getElementById('rh').textContent=h.toLocaleString('de-DE',{maximumFractionDigits:4})+' h';document.getElementById('rm').textContent=(h*60).toLocaleString('de-DE',{maximumFractionDigits:2})+' min';document.getElementById('rs').textContent=Math.round(h*3600).toLocaleString('de-DE')+' s';document.getElementById('rd').textContent=(h/24).toLocaleString('de-DE',{maximumFractionDigits:3})+' Tage';
var dd=h/24,big=dd>=1?(Math.round(dd*100)/100).toLocaleString('de-DE')+' Tage':(Math.round(h*60))+' Minuten';document.getElementById('t').textContent=big;document.getElementById('td').textContent=h.toLocaleString('de-DE',{maximumFractionDigits:2})+' Stunden'}
['val','unit'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}


# ---------------------------------------------------------------- 3) Wie viele Stunden hat ein Monat
def _monat_rows(y=2026):
    rows = ""
    tot = 0
    for m in range(1, 13):
        days = calendar.monthrange(y, m)[1]
        h = days * 24
        tot += h
        rows += f'<tr><td>{MONATE[m-1]} {y}</td><td class="num">{days}</td><td class="num">{h}</td></tr>'
    rows += f'<tr><td><strong>Gesamt {y}</strong></td><td class="num">{"366" if calendar.isleap(y) else "365"}</td><td class="num">{tot}</td></tr>'
    return rows


MONAT = {
    "path": "/wie-viele-stunden-hat-ein-monat/", "short": "Stunden pro Monat", "tool": True, "group": "kal",
    "card": "Wie viele Stunden hat ein Monat? Kalenderstunden und Arbeitsstunden pro Monat.",
    "title": "Wie viele Stunden hat ein Monat? – Tabelle & Rechner",
    "desc": "Wie viele Stunden hat ein Monat? 672 bis 744 Kalenderstunden, im Schnitt 730,5 – plus die Arbeitsstunden bei einer 40-Stunden-Woche.",
    "h1": "Wie viele Stunden hat ein Monat?",
    "lead": "Ein Monat hat je nach Länge <strong>672 bis 744 Kalenderstunden</strong> – im Durchschnitt 730,5 Stunden. Als Arbeitszeit sind es bei einer 40-Stunden-Woche dagegen nur rund 173 Stunden. Beide Werte findest du hier.",
    "body": f"""
<div class="calc">
<h2>Stunden pro Monat berechnen</h2>
<div class="grid"><div><label for="mon">Monat</label><select id="mon"></select></div><div><label for="jahr">Jahr</label><input type="number" id="jahr" value="2026" min="1900" max="2100"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div>
<dl><dt>Kalendertage</dt><dd id="kt">–</dd><dt>Kalenderstunden</dt><dd id="kh">–</dd><dt>Arbeitsstunden (40-h-Woche, ca.)</dt><dd id="ah">–</dd></dl></div>
</div>
{AD}
<h2>Kalenderstunden pro Monat {2026}</h2>
<div class="tw"><table class="t"><thead><tr><th>Monat</th><th style="text-align:right">Tage</th><th style="text-align:right">Stunden</th></tr></thead><tbody>{_monat_rows(2026)}</tbody></table></div>
<h2>Kalenderstunden oder Arbeitsstunden?</h2>
<p>Es gibt zwei Antworten, je nachdem was du meinst:</p>
<ul>
<li><strong>Kalenderstunden</strong> – alle Stunden des Monats: Tage × 24. Ein 30-Tage-Monat hat 720 Stunden, ein
31-Tage-Monat 744, der Februar 672 (im Schaltjahr 696). Im Jahresdurchschnitt sind es 730,5 Stunden (365,25 × 24 ÷ 12).</li>
<li><strong>Arbeitsstunden</strong> – die bezahlte Arbeitszeit: Bei einer 40-Stunden-Woche rechnet man mit
40 × 4,33 = rund <strong>173,33 Stunden pro Monat</strong>. Bei 38,5 Stunden sind es 166,8, bei 35 Stunden 151,7.
Mehr dazu auf der Seite <a href="/40-stunden-woche/">40-Stunden-Woche</a>.</li>
</ul>
<p>Die genaue Zahl der <a href="/arbeitstage-2026/">Arbeitstage pro Monat</a> hängt vom Bundesland und den
Feiertagen ab. Deine tatsächliche Arbeitszeit erfasst der <a href="/">Arbeitszeitrechner</a>.</p>
""",
    "faq": [
        ("Wie viele Stunden hat ein Monat?", "Zwischen 672 (Februar) und 744 Stunden (Monate mit 31 Tagen). Im Durchschnitt hat ein Monat 730,5 Kalenderstunden."),
        ("Wie viele Arbeitsstunden hat ein Monat?", "Bei einer 40-Stunden-Woche rund 173,33 Stunden (40 × 4,33). Das ist unabhängig von der Monatslänge der Standardwert für die Lohnabrechnung."),
        ("Wie viele Stunden hat der Februar?", "Der Februar hat 28 × 24 = 672 Stunden, im Schaltjahr 29 × 24 = 696 Stunden."),
        ("Warum rechnet man mit 173,33 Arbeitsstunden?", "Weil ein Monat im Schnitt 4,33 Wochen hat (52 ÷ 12). 40 Wochenstunden × 4,33 = 173,33 Monatsstunden."),
    ],
    "js": r"""
(function(){var M=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'],s=document.getElementById('mon');M.forEach(function(n,i){s.add(new Option(n,i+1))});var now=new Date();s.value=now.getMonth()+1;
function c(){var m=+s.value,y=parseInt(document.getElementById('jahr').value,10)||2026,days=new Date(y,m,0).getDate(),kh=days*24,ah=40*4.3333;
document.getElementById('t').textContent=kh+' Stunden';document.getElementById('td').textContent=M[m-1]+' '+y+' · '+days+' Tage';
document.getElementById('kt').textContent=days;document.getElementById('kh').textContent=kh+' Stunden';document.getElementById('ah').textContent=ah.toLocaleString('de-DE',{maximumFractionDigits:2})+' Stunden'}
['mon','jahr'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}


# ---------------------------------------------------------------- 4) 40-Stunden-Woche
def _woche_rows():
    rows = ""
    for w in [20, 25, 30, 35, 38.5, 40, 42]:
        rows += (f'<tr><td class="num">{de(w,1).rstrip("0").rstrip(",")}</td><td class="num">{de(w/5,2)}</td>'
                 f'<td class="num">{de(w*4.3333,1)}</td><td class="num">{de(w*52,0)}</td></tr>')
    return rows


WOCHE = {
    "path": "/40-stunden-woche/", "short": "40-Stunden-Woche", "tool": True, "group": "arb",
    "card": "40-Stunden-Woche: Stunden pro Tag, Monat und Jahr – mit Rechner für jede Wochenstundenzahl.",
    "title": "40-Stunden-Woche – Stunden pro Monat, Jahr & Tag",
    "desc": "40-Stunden-Woche: 8 Stunden pro Tag, 173,33 pro Monat, 2.080 pro Jahr. Rechner und Tabelle für 20, 30, 35, 38,5 und 40 Wochenstunden.",
    "h1": "40-Stunden-Woche: Stunden pro Monat, Jahr und Tag",
    "lead": "Die 40-Stunden-Woche bedeutet 8 Stunden an 5 Tagen, <strong>173,33 Stunden pro Monat</strong> und 2.080 Stunden im Jahr. Mit dem Rechner ermittelst du die Werte für jede Wochenstundenzahl – auch für die 30- oder 35-Stunden-Woche.",
    "body": f"""
<div class="calc">
<h2>Wochenstunden in Monat und Jahr umrechnen</h2>
<div class="grid"><div><label for="ws">Stunden pro Woche</label><input type="number" id="ws" value="40" step="0.5" min="0"></div><div><label for="at">Arbeitstage pro Woche</label><input type="number" id="at" value="5" step="0.5" min="1" max="7"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">173,33 h</div><div class="sub">Stunden pro Monat</div>
<dl><dt>Pro Tag</dt><dd id="pd">–</dd><dt>Pro Monat (× 4,33)</dt><dd id="pm">–</dd><dt>Pro Jahr (× 52)</dt><dd id="pj">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
</div>
{AD}
<h2>Tabelle: Wochenstunden in Monats- und Jahresstunden</h2>
<div class="tw"><table class="t"><thead><tr><th>Stunden/Woche</th><th style="text-align:right">Pro Tag (5 Tage)</th><th style="text-align:right">Pro Monat</th><th style="text-align:right">Pro Jahr</th></tr></thead><tbody>{_woche_rows()}</tbody></table></div>
<h2>Wie viele Stunden hat die 40-Stunden-Woche im Monat?</h2>
<p>Für die Lohnabrechnung rechnet man mit durchschnittlich 4,33 Wochen pro Monat (52 Wochen ÷ 12 Monate). Damit
ergibt die 40-Stunden-Woche <strong>40 × 4,33 = 173,33 Stunden pro Monat</strong> und 40 × 52 = 2.080 Stunden pro
Jahr. Pro Tag sind es bei 5 Tagen 8 Stunden.</p>
<h2>30-Stunden-Woche und 35-Stunden-Woche</h2>
<p>Die gleiche Formel gilt für jede Teilzeit: Die <strong>30-Stunden-Woche</strong> ergibt 30 × 4,33 = 130 Stunden
im Monat (6 Stunden pro Tag bei 5 Tagen), die <strong>35-Stunden-Woche</strong> 151,7 Stunden und die
<strong>38,5-Stunden-Woche</strong> 166,8 Stunden. Was du dabei verdienst, zeigt der
<a href="/teilzeitrechner/">Teilzeitrechner</a>.</p>
<h2>Was ist erlaubt?</h2>
<p>Das Arbeitszeitgesetz erlaubt werktäglich maximal 8 Stunden, vorübergehend bis zu 10 Stunden, wenn im
Durchschnitt von sechs Monaten 8 Stunden nicht überschritten werden – also höchstens 48 Stunden pro Woche
(§ 3 ArbZG). Vollzeit liegt in Deutschland meist zwischen 35 und 40 Wochenstunden. Deinen Stundenlohn aus dem
Monatsgehalt berechnet der <a href="/stundenlohnrechner/">Stundenlohnrechner</a>.</p>
""",
    "sources": ["arbzg"],
    "faq": [
        ("Wie viele Stunden hat die 40-Stunden-Woche im Monat?", "173,33 Stunden (40 × 4,33). Pro Jahr sind es 2.080 Stunden, pro Tag 8 Stunden bei 5 Arbeitstagen."),
        ("Wie viele Stunden sind eine 30-Stunden-Woche im Monat?", "130 Stunden (30 × 4,33), also 6 Stunden an 5 Tagen pro Woche."),
        ("Wie viele Stunden pro Jahr sind 40 Stunden pro Woche?", "2.080 Stunden (40 × 52) – vor Abzug von Urlaub und Feiertagen."),
        ("Wie viele Stunden am Tag sind eine 40-Stunden-Woche?", "8 Stunden pro Tag bei einer 5-Tage-Woche, 6,67 Stunden bei 6 Tagen."),
        ("Wie viele Stunden darf man pro Woche maximal arbeiten?", "Höchstens 48 Stunden (8 Stunden an 6 Werktagen); vorübergehend bis 60, wenn der Sechs-Monats-Schnitt bei 48 bleibt (§ 3 ArbZG)."),
    ],
    "js": r"""
(function(){function c(){var w=parseFloat(document.getElementById('ws').value)||0,t=parseFloat(document.getElementById('at').value)||5,pm=w*4.3333,pj=w*52,pd=t?w/t:0;
document.getElementById('t').textContent=pm.toLocaleString('de-DE',{maximumFractionDigits:2})+' h';
document.getElementById('pd').textContent=pd.toLocaleString('de-DE',{maximumFractionDigits:2})+' Stunden';
document.getElementById('pm').textContent=pm.toLocaleString('de-DE',{maximumFractionDigits:2})+' Stunden';
document.getElementById('pj').textContent=pj.toLocaleString('de-DE',{maximumFractionDigits:0})+' Stunden'}
['ws','at'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}


# ---------------------------------------------------------------- 5) Kalenderwoche
def _kw_rows(y=2026):
    rows = ""
    w = 1
    while True:
        try:
            mon = dt.date.fromisocalendar(y, w, 1)
        except ValueError:
            break
        sun = mon + dt.timedelta(days=6)
        rows += (f'<tr><td class="num">KW {w}</td>'
                 f'<td>{mon.day:02d}.{mon.month:02d}. – {sun.day:02d}.{sun.month:02d}.{sun.year}</td></tr>')
        w += 1
    return rows


KW = {
    "path": "/kalenderwoche/", "short": "Kalenderwoche", "tool": True, "group": "kal",
    "card": "Welche Kalenderwoche haben wir heute? KW berechnen und KW-Tabelle 2026.",
    "title": "Welche Kalenderwoche haben wir heute? – KW-Rechner 2026",
    "desc": "Welche Kalenderwoche ist heute? Der KW-Rechner zeigt die aktuelle KW, rechnet jedes Datum um und nennt den Zeitraum – mit KW-Tabelle 2026.",
    "h1": "Welche Kalenderwoche haben wir heute?",
    "lead": "Die aktuelle Kalenderwoche siehst du sofort unten. Darunter rechnest du jedes beliebige Datum in seine Kalenderwoche um oder lässt dir den Zeitraum einer KW anzeigen – nach der ISO-8601-Norm, die in Deutschland gilt.",
    "body": f"""
<div class="calc"><h2>Aktuelle Kalenderwoche</h2>
<div class="result" aria-live="polite"><div class="big" id="now">–</div><div class="sub" id="nowd"></div></div></div>
<div class="calc">
<h2>Datum → Kalenderwoche</h2>
<div class="grid"><div><label for="d">Datum</label><input type="date" id="d"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div></div>
</div>
<div class="calc">
<h2>Kalenderwoche → Zeitraum</h2>
<div class="grid"><div><label for="kw">Kalenderwoche</label><input type="number" id="kw" value="1" min="1" max="53"></div><div><label for="ky">Jahr</label><input type="number" id="ky" value="2026" min="1900" max="2100"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">–</div><div class="sub" id="t2d"></div></div>
</div>
{AD}
<h2>Kalenderwochen 2026 im Überblick</h2>
<div class="tw"><table class="t sm"><thead><tr><th>Kalenderwoche</th><th>Zeitraum (Mo–So)</th></tr></thead><tbody>{_kw_rows(2026)}</tbody></table></div>
<h2>Wie wird die Kalenderwoche gezählt?</h2>
<p>In Deutschland und der EU gilt die Norm ISO 8601: Eine Woche beginnt am <strong>Montag</strong>, und die
<strong>erste Kalenderwoche</strong> eines Jahres ist die Woche, die den ersten Donnerstag enthält – gleichbedeutend
mit der Woche, in die der 4. Januar fällt. Dadurch kann der Jahresanfang noch zur letzten KW des Vorjahres gehören
und ein Jahr 52 oder 53 Kalenderwochen haben. 2026 hat 53 Kalenderwochen.</p>
<p>Den Abstand zwischen zwei Daten in Tagen berechnet der <a href="/tagerechner/">Tagerechner</a>, alle freien Tage
stehen unter <a href="/feiertage-2026/">Feiertage 2026</a>.</p>
""",
    "faq": [
        ("Welche Kalenderwoche haben wir heute?", "Die aktuelle Kalenderwoche wird oben auf dieser Seite automatisch angezeigt – nach der in Deutschland gültigen ISO-8601-Zählung."),
        ("Wie wird die Kalenderwoche berechnet?", "Nach ISO 8601: Die Woche beginnt am Montag, und die erste KW ist die Woche mit dem ersten Donnerstag des Jahres (die Woche, in die der 4. Januar fällt)."),
        ("Wie viele Kalenderwochen hat 2026?", "2026 hat 53 Kalenderwochen, weil der 31. Dezember 2026 (ein Donnerstag) noch zur KW 53 gehört."),
        ("Wann beginnt die Kalenderwoche – Montag oder Sonntag?", "In Deutschland und Europa am Montag (ISO 8601). In den USA beginnt die Woche dagegen am Sonntag, dort wird anders gezählt."),
    ],
    "js": r"""
(function(){function isoWeek(dt){var d=new Date(Date.UTC(dt.getFullYear(),dt.getMonth(),dt.getDate()));var day=d.getUTCDay()||7;d.setUTCDate(d.getUTCDate()+4-day);var ys=new Date(Date.UTC(d.getUTCFullYear(),0,1));var w=Math.ceil(((d-ys)/864e5+1)/7);return[w,d.getUTCFullYear()]}
function mondayOf(y,w){var simple=new Date(Date.UTC(y,0,1+(w-1)*7));var dow=simple.getUTCDay()||7;var mon=new Date(simple);mon.setUTCDate(simple.getUTCDate()-dow+1);return mon}
function fmtU(d){return pad(d.getUTCDate())+'.'+pad(d.getUTCMonth()+1)+'.'+d.getUTCFullYear()}
var t=new Date();var nw=isoWeek(t);document.getElementById('now').textContent='KW '+nw[0];document.getElementById('nowd').textContent=t.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'long',year:'numeric'});
var di=document.getElementById('d');di.value=t.getFullYear()+'-'+pad(t.getMonth()+1)+'-'+pad(t.getDate());
function cD(){var v=di.value;if(!v)return;var p=v.split('-'),dd=new Date(p[0],p[1]-1,p[2]),r=isoWeek(dd);document.getElementById('t').textContent='KW '+r[0];document.getElementById('td').textContent=dd.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'long',year:'numeric'})+(r[1]!=p[0]?' (KW-Jahr '+r[1]+')':'')}
function cK(){var w=parseInt(document.getElementById('kw').value,10)||1,y=parseInt(document.getElementById('ky').value,10)||2026,mon=mondayOf(y,w),sun=new Date(mon);sun.setUTCDate(mon.getUTCDate()+6);document.getElementById('t2').textContent=fmtU(mon)+' – '+fmtU(sun);document.getElementById('t2d').textContent='Montag bis Sonntag der KW '+w+' '+y}
di.addEventListener('input',cD);['kw','ky'].forEach(function(i){document.getElementById(i).addEventListener('input',cK)});cD();cK()})();""",
}

TIER2 = [MINUTEN, STDUM, MONAT, WOCHE, KW]
