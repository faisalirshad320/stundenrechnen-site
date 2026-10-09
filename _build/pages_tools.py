# -*- coding: utf-8 -*-
AD = ''  # AdSense Auto Ads (head script) places ads; no manual units

DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

# ---------------------------------------------------------------- HOME: Arbeitszeitrechner
rows = "".join(
    f'<tr><td><span class="dl">{d}</span><span class="ds">{d[:2]}</span></td><td><input type="time" id="s{i}" value="{"08:00" if i < 5 else ""}" aria-label="{d} Beginn"></td>'
    f'<td><input type="time" id="e{i}" value="{"16:30" if i < 5 else ""}" aria-label="{d} Ende"></td>'
    f'<td><input type="number" id="p{i}" value="{30 if i < 5 else 0}" min="0" step="5" aria-label="{d} Pause in Minuten"></td>'
    f'<td class="num" id="r{i}">–</td></tr>' for i, d in enumerate(DAYS))

HOME = {
    "path": "/", "short": "Arbeitszeitrechner", "tool": True,
    "card": "Beginn, Ende und Pause eingeben – Netto-Arbeitszeit pro Tag und Woche.",
    "title": "Arbeitszeitrechner – Arbeitszeit mit Pause berechnen (kostenlos)",
    "desc": "Arbeitszeitrechner online: Arbeitsbeginn, Arbeitsende und Pause eingeben und die Netto-Arbeitszeit pro Tag und Woche in Stunden:Minuten und Dezimal berechnen. Kostenlos, ohne Anmeldung.",
    "h1": "Arbeitszeitrechner – Arbeitszeit abzüglich Pausen berechnen",
    "lead": "Trage Arbeitsbeginn, Arbeitsende und Pause ein. Der Rechner zeigt die Netto-Arbeitszeit pro Tag und die Wochensumme – als Stunden:Minuten und als Dezimalzahl für die Zeiterfassung.",
    "body": f"""
<div class="calc">
<h2>Arbeitszeit pro Woche berechnen</h2>
<div class="tw"><table class="t"><thead><tr><th>Tag</th><th>Beginn</th><th>Ende</th><th>Pause (Min.)</th><th style="text-align:right">Netto</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="actions"><button class="btn" id="go">Arbeitszeit berechnen</button><button class="btn ghost" id="reset">Zurücksetzen</button><label style="margin:0;display:flex;align-items:center;gap:8px;font-weight:500">Soll-Stunden/Woche <input type="number" id="soll" value="40" step="0.5" min="0" style="width:90px;min-height:38px;padding:6px 8px"></label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">0:00 Std.</div><div class="sub" id="totd">0,00 Stunden (dezimal)</div>
<dl><dt>Soll (Woche)</dt><dd id="sollv">40,00 Std.</dd><dt>Differenz</dt><dd id="diff">–</dd><dt>Ø pro Arbeitstag</dt><dd id="avg">–</dd></dl>
<div class="actions"><button class="btn sm ghost" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Nachtschichten über Mitternacht werden erkannt (z. B. 22:00 bis 06:00). Pausen werden in Minuten abgezogen.</p>
</div>
{AD}
<h2>So funktioniert der Arbeitszeitrechner</h2>
<p>Der Arbeitszeitrechner zieht von der Zeitspanne zwischen Arbeitsbeginn und Arbeitsende die Pausenzeit ab. Das Ergebnis ist die <strong>Netto-Arbeitszeit</strong>, also die Zeit, die tatsächlich als Arbeitszeit zählt. Für eine Schicht von 8:00 bis 16:30 Uhr mit 30 Minuten Pause ergibt das 8 Stunden – als Dezimalzahl 8,00.</p>
<p>Die Dezimalangabe ist für Zeiterfassungssysteme, Stundenzettel und Lohnabrechnungen wichtig: 7 Stunden und 45 Minuten entsprechen 7,75 Stunden, nicht 7,45. Der Rechner zeigt beide Schreibweisen nebeneinander, damit du nichts umrechnen musst. Wer nur die Umrechnung braucht, findet sie im <a href="/dezimal-rechner/">Dezimal-Rechner</a>.</p>
<h2>Gesetzliche Regeln zur Arbeitszeit in Deutschland</h2>
<ul>
<li><strong>Höchstarbeitszeit:</strong> Nach § 3 Arbeitszeitgesetz (ArbZG) darf die werktägliche Arbeitszeit 8 Stunden nicht überschreiten. Sie kann auf bis zu 10 Stunden verlängert werden, wenn innerhalb von 6 Monaten im Durchschnitt 8 Stunden werktäglich nicht überschritten werden.</li>
<li><strong>Pausen:</strong> Bei mehr als 6 Stunden Arbeit sind mindestens 30 Minuten Pause vorgeschrieben, bei mehr als 9 Stunden mindestens 45 Minuten (§ 4 ArbZG). Der <a href="/pausenrechner/">Pausenrechner</a> ermittelt die Mindestpause automatisch.</li>
<li><strong>Ruhezeit:</strong> Zwischen zwei Arbeitstagen müssen mindestens 11 Stunden ununterbrochene Ruhezeit liegen (§ 5 ArbZG).</li>
<li><strong>Pausen zählen nicht als Arbeitszeit.</strong> Sie werden deshalb von der Anwesenheitszeit abgezogen.</li>
</ul>
<h2>Arbeitszeit pro Monat berechnen</h2>
<p>Die monatliche Arbeitszeit ergibt sich aus der Wochenarbeitszeit multipliziert mit dem Faktor 4,33 (durchschnittliche Wochen pro Monat: 52 ÷ 12). Bei 40 Wochenstunden sind das rechnerisch 173,33 Stunden im Monat; bei 38,5 Stunden 166,83 Stunden. Für die genaue Zahl der Arbeitstage in einem bestimmten Monat hilft der <a href="/tagerechner/">Tagerechner</a> mit Werktagsfunktion.</p>
<div class="note">Mehrarbeit über die vertraglich vereinbarte Zeit hinaus kannst du mit dem <a href="/ueberstunden-rechner/">Überstunden-Rechner</a> bewerten – inklusive der möglichen Auszahlung nach Stundenlohn.</div>
""",
    "faq": [
        ("Wie berechnet man die Arbeitszeit mit Pause?", "Arbeitsende minus Arbeitsbeginn ergibt die Anwesenheitszeit. Davon wird die Pause abgezogen. Beispiel: 8:00 bis 16:30 Uhr sind 8,5 Stunden; abzüglich 30 Minuten Pause bleiben 8 Stunden Netto-Arbeitszeit."),
        ("Zählt die Pause zur Arbeitszeit?", "Nein. Gesetzliche Ruhepausen nach § 4 ArbZG sind keine Arbeitszeit und werden nicht bezahlt, sofern Tarif- oder Arbeitsvertrag nichts anderes regeln."),
        ("Wie rechnet man Stunden und Minuten in Dezimalstunden um?", "Minuten durch 60 teilen: 45 Minuten = 0,75 Stunden, 20 Minuten = 0,33 Stunden. 7 Stunden 45 Minuten sind also 7,75 Dezimalstunden."),
        ("Wie viele Stunden sind 40 Wochenstunden im Monat?", "40 Stunden × 4,33 Wochen = 173,33 Stunden pro Monat. Diesen Wert nutzen viele Arbeitgeber zur Berechnung des Stundenlohns aus dem Monatsgehalt."),
        ("Werden meine Daten gespeichert?", "Nein. Alle Berechnungen laufen in deinem Browser. Es wird nichts an einen Server gesendet und nichts gespeichert."),
    ],
    "js": r"""
(function(){
function calc(){var tot=0,days=0;for(var i=0;i<7;i++){var s=tmin(document.getElementById('s'+i).value),e=tmin(document.getElementById('e'+i).value),p=parseFloat(document.getElementById('p'+i).value)||0,c=document.getElementById('r'+i);
if(s===null||e===null){c.textContent='–';continue}var d=e-s;if(d<0)d+=1440;d-=p;if(d<0)d=0;tot+=d;days++;c.textContent=fmtHM(d)+' ('+fmtDec(d)+')'}
document.getElementById('tot').textContent=fmtHM(tot)+' Std.';document.getElementById('totd').textContent=fmtDec(tot)+' Stunden (dezimal)';
var soll=parseFloat(document.getElementById('soll').value)||0;document.getElementById('sollv').textContent=soll.toLocaleString('de-DE',{minimumFractionDigits:2})+' Std.';
var diff=tot-soll*60;document.getElementById('diff').textContent=(diff>=0?'+':'')+fmtHM(diff)+' Std. ('+(diff>=0?'Überstunden':'Minusstunden')+')';
document.getElementById('avg').textContent=days?fmtHM(tot/days)+' Std.':'–'}
document.getElementById('go').onclick=calc;document.getElementById('soll').oninput=calc;
document.getElementById('reset').onclick=function(){for(var i=0;i<7;i++){document.getElementById('s'+i).value='';document.getElementById('e'+i).value='';document.getElementById('p'+i).value=0}calc()};
document.querySelectorAll('table.t input').forEach(function(x){x.addEventListener('change',calc)});calc();
})();"""
}

# ---------------------------------------------------------------- Stundenrechner
STUNDEN = {
    "path": "/stundenrechner/", "short": "Stundenrechner", "tool": True,
    "card": "Stunden und Minuten addieren oder subtrahieren – Summe in h:mm und dezimal.",
    "title": "Stundenrechner – Stunden und Minuten addieren & zusammenrechnen",
    "desc": "Stundenrechner online: Stunden und Minuten addieren, subtrahieren und zusammenrechnen. Ergebnis in Stunden:Minuten und Dezimalstunden. Ideal für Stundenzettel und Arbeitszeiten.",
    "h1": "Stundenrechner – Stunden und Minuten zusammenrechnen",
    "lead": "Gib beliebig viele Zeiten als Stunden und Minuten ein. Der Stundenrechner addiert (oder subtrahiert) sie und zeigt die Summe als Stunden:Minuten und als Dezimalstunden.",
    "body": f"""
<div class="calc">
<h2>Stunden addieren</h2>
<div class="rows" id="rows"></div>
<div class="actions"><button class="btn ghost sm" id="add">+ Zeile hinzufügen</button><button class="btn" id="go">Summe berechnen</button><button class="btn ghost" id="reset">Leeren</button></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">0:00</div><div class="sub" id="totd">0,00 Dezimalstunden · 0 Minuten</div>
<div class="actions"><button class="btn sm ghost" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Vorzeichen „–“ wählen, um eine Zeit abzuziehen. Minutenwerte über 59 werden automatisch in Stunden umgerechnet.</p>
</div>
<div class="calc">
<h2>Stunden zwischen zwei Uhrzeiten</h2>
<div class="grid"><div><label for="a">Von (Uhrzeit)</label><input type="time" id="a" value="09:00"></div><div><label for="b">Bis (Uhrzeit)</label><input type="time" id="b" value="17:30"></div><div><label for="pz">Pause (Minuten)</label><input type="number" id="pz" value="0" min="0" step="5"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">8:30</div><div class="sub" id="t2d">8,50 Stunden</div></div>
</div>
{AD}
<h2>Wofür braucht man einen Stundenrechner?</h2>
<p>Ein Stundenrechner addiert Zeitspannen, die in Stunden und Minuten vorliegen. Das klingt einfach, ist aber fehleranfällig, weil Minuten im 60er-System laufen: 2:45 + 1:30 sind nicht 3:75, sondern 4:15. Genau diesen Übertrag übernimmt der Rechner. Typische Anwendungen sind der Stundenzettel am Monatsende, die Abrechnung von Projektzeiten, das Zusammenrechnen von Überstunden oder die Summe mehrerer Fahrzeiten.</p>
<h2>Stunden richtig addieren – die Rechenregel</h2>
<ol>
<li>Alle Stunden addieren und alle Minuten addieren.</li>
<li>Die Minutensumme durch 60 teilen: der ganzzahlige Teil wird zu den Stunden addiert, der Rest bleibt als Minuten.</li>
<li>Beispiel: 3:50 + 2:40 → Stunden 5, Minuten 90 → 90 ÷ 60 = 1 Rest 30 → Ergebnis 6:30.</li>
</ol>
<p>Für die Lohnabrechnung wird meist die Dezimalschreibweise benötigt. 6:30 Stunden sind 6,50 Dezimalstunden. Die Umrechnungstabelle für alle Minutenwerte findest du im <a href="/dezimal-rechner/">Dezimal-Rechner</a>.</p>
<h2>Stundenrechner für die Arbeitszeit</h2>
<p>Wenn du mehrere Arbeitstage mit Beginn, Ende und Pause erfassen willst, ist der <a href="/">Arbeitszeitrechner</a> die bessere Wahl: Er berechnet die Netto-Arbeitszeit pro Tag und vergleicht die Wochensumme mit deinen Soll-Stunden. Den reinen Zeitabstand zwischen zwei Uhrzeiten – auch über Mitternacht – liefert der <a href="/zeitrechner/">Zeitrechner</a>.</p>
""",
    "faq": [
        ("Wie rechnet man Stunden und Minuten zusammen?", "Stunden und Minuten getrennt addieren, dann die Minuten durch 60 teilen. Jede volle 60 Minuten ergeben eine zusätzliche Stunde. 2:45 + 1:30 = 3 Stunden und 75 Minuten = 4:15."),
        ("Was ist der Unterschied zwischen 7:30 und 7,30 Stunden?", "7:30 bedeutet 7 Stunden und 30 Minuten (= 7,50 Dezimalstunden). 7,30 Dezimalstunden sind dagegen 7 Stunden und 18 Minuten. Für Abrechnungen ist die Dezimalform üblich."),
        ("Kann der Stundenrechner auch subtrahieren?", "Ja. Wähle bei einer Zeile das Minuszeichen, dann wird diese Zeit von der Summe abgezogen – zum Beispiel für Pausen oder Fehlzeiten."),
        ("Wie viele Minuten sind 1,75 Stunden?", "1,75 × 60 = 105 Minuten, also 1 Stunde und 45 Minuten."),
    ],
    "js": r"""
(function(){var R=document.getElementById('rows'),n=0;
function row(h,m){n++;var d=document.createElement('div');d.className='row';d.innerHTML='<div><label>Vorzeichen / Stunden</label><div style="display:flex;gap:6px"><select aria-label="Vorzeichen" style="width:64px"><option value="1">+</option><option value="-1">–</option></select><input type="number" min="0" placeholder="Std." value="'+(h||'')+'" aria-label="Stunden"></div></div><div><label>Minuten</label><input type="number" min="0" placeholder="Min." value="'+(m||'')+'" aria-label="Minuten"></div><button class="btn ghost sm" type="button" aria-label="Zeile entfernen" style="margin-bottom:2px">×</button>';
d.querySelector('button').onclick=function(){d.remove();calc()};d.querySelectorAll('input,select').forEach(function(x){x.addEventListener('input',calc)});R.appendChild(d)}
function calc(){var t=0;R.querySelectorAll('.row').forEach(function(r){var s=parseInt(r.querySelector('select').value),i=r.querySelectorAll('input');t+=s*((parseFloat(i[0].value)||0)*60+(parseFloat(i[1].value)||0))});
document.getElementById('tot').textContent=fmtHM(t);document.getElementById('totd').textContent=fmtDec(t)+' Dezimalstunden · '+Math.round(t).toLocaleString('de-DE')+' Minuten'}
document.getElementById('add').onclick=function(){row()};document.getElementById('go').onclick=calc;document.getElementById('reset').onclick=function(){R.innerHTML='';row();row();row();calc()};
row(2,45);row(1,30);row(3,50);calc();
function c2(){var a=tmin(document.getElementById('a').value),b=tmin(document.getElementById('b').value),p=parseFloat(document.getElementById('pz').value)||0;if(a===null||b===null)return;var d=b-a;if(d<0)d+=1440;d-=p;if(d<0)d=0;document.getElementById('t2').textContent=fmtHM(d);document.getElementById('t2d').textContent=fmtDec(d)+' Stunden'}
['a','b','pz'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c2();
})();"""
}

# ---------------------------------------------------------------- Zeitrechner
ZEIT = {
    "path": "/zeitrechner/", "short": "Zeitrechner", "tool": True,
    "card": "Zeitspanne zwischen zwei Uhrzeiten – auch über Mitternacht – und Uhrzeit plus/minus Dauer.",
    "title": "Zeitrechner – Zeitspanne zwischen zwei Uhrzeiten berechnen",
    "desc": "Zeitrechner online: Zeit von–bis berechnen, Stunden und Minuten zwischen zwei Uhrzeiten ermitteln (auch über Mitternacht) und zu einer Uhrzeit eine Dauer addieren oder abziehen.",
    "h1": "Zeitrechner – Zeitspanne von Uhrzeit bis Uhrzeit",
    "lead": "Wie lange ist es von 22:15 bis 06:40 Uhr? Welche Uhrzeit ist 3 Stunden 20 Minuten nach 14:50? Der Zeitrechner beantwortet beides – mit Übergang über Mitternacht.",
    "body": f"""
<div class="calc">
<h2>Zeit von – bis</h2>
<div class="grid"><div><label for="a">Von</label><input type="time" id="a" value="22:15"></div><div><label for="b">Bis</label><input type="time" id="b" value="06:40"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">8:25</div><div class="sub" id="td">8,42 Stunden · 505 Minuten</div></div>
</div>
<div class="calc">
<h2>Uhrzeit plus / minus Dauer</h2>
<div class="grid"><div><label for="u">Uhrzeit</label><input type="time" id="u" value="14:50"></div><div><label for="op">Rechenart</label><select id="op"><option value="1">+ addieren</option><option value="-1">– abziehen</option></select></div><div><label for="h">Stunden</label><input type="number" id="h" value="3" min="0"></div><div><label for="m">Minuten</label><input type="number" id="m" value="20" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">18:10 Uhr</div><div class="sub" id="t2d">am selben Tag</div></div>
</div>
{AD}
<h2>Zeitspanne berechnen – so geht es per Hand</h2>
<p>Wandle beide Uhrzeiten in Minuten seit Mitternacht um (Stunden × 60 + Minuten) und bilde die Differenz. Ist das Ergebnis negativ, liegt die Endzeit am nächsten Tag: Addiere 1440 Minuten (24 Stunden). Beispiel 22:15 bis 06:40: 400 − 1335 = −935, plus 1440 = 505 Minuten = 8 Stunden 25 Minuten.</p>
<h2>Typische Anwendungen</h2>
<ul>
<li><strong>Nachtschicht:</strong> Beginn am Abend, Ende am Morgen – der Rechner erkennt den Tageswechsel automatisch.</li>
<li><strong>Fahrzeiten und Reisen:</strong> Abfahrt und Ankunft eingeben, Reisedauer ablesen.</li>
<li><strong>Zeiterfassung:</strong> Kommen- und Gehen-Zeiten in Netto-Stunden umrechnen – mit Pausen im <a href="/">Arbeitszeitrechner</a>.</li>
<li><strong>Termine planen:</strong> Welche Uhrzeit ist 90 Minuten vor 8:00? 6:30 Uhr.</li>
</ul>
<p>Mehrere Zeitspannen summierst du anschließend im <a href="/stundenrechner/">Stundenrechner</a>. Zeitabstände in Tagen statt Stunden berechnet der <a href="/tagerechner/">Tagerechner</a>.</p>
""",
    "faq": [
        ("Wie berechne ich die Zeit zwischen zwei Uhrzeiten?", "Beide Zeiten in Minuten umrechnen und subtrahieren. Bei einem negativen Ergebnis 24 Stunden (1440 Minuten) addieren, weil die Endzeit am Folgetag liegt."),
        ("Wie viele Stunden sind von 22 Uhr bis 6 Uhr?", "8 Stunden. Von 22:00 bis 24:00 sind es 2 Stunden, von 0:00 bis 6:00 weitere 6 Stunden."),
        ("Rechnet der Zeitrechner mit Sekunden?", "Nein, der Rechner arbeitet mit Stunden und Minuten. Das reicht für Arbeitszeit, Fahrzeiten und Terminplanung aus."),
    ],
    "js": r"""
(function(){function c1(){var a=tmin(document.getElementById('a').value),b=tmin(document.getElementById('b').value);if(a===null||b===null)return;var d=b-a;if(d<0)d+=1440;document.getElementById('t').textContent=fmtHM(d);document.getElementById('td').textContent=fmtDec(d)+' Stunden · '+d+' Minuten'+(b<a?' · Ende am Folgetag':'')}
function c2(){var u=tmin(document.getElementById('u').value);if(u===null)return;var s=parseInt(document.getElementById('op').value),d=(parseFloat(document.getElementById('h').value)||0)*60+(parseFloat(document.getElementById('m').value)||0),r=u+s*d,days=Math.floor(r/1440);r=((r%1440)+1440)%1440;document.getElementById('t2').textContent=pad(Math.floor(r/60))+':'+pad(r%60)+' Uhr';document.getElementById('t2d').textContent=days===0?'am selben Tag':(days>0?days+' Tag(e) später':Math.abs(days)+' Tag(e) früher')}
['a','b'].forEach(function(i){document.getElementById(i).addEventListener('input',c1)});['u','op','h','m'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c1();c2()})();"""
}

# ---------------------------------------------------------------- Tagerechner
TAGE = {
    "path": "/tagerechner/", "short": "Tagerechner", "tool": True,
    "card": "Tage zwischen zwei Daten zählen, Werktage ermitteln, Datum plus/minus Tage.",
    "title": "Tagerechner – Tage zwischen zwei Daten berechnen (inkl. Werktage)",
    "desc": "Tagerechner online: Anzahl der Tage zwischen zwei Daten zählen, Werktage (Mo–Fr) berechnen und ein Datum plus oder minus X Tage ermitteln. Kostenlos und ohne Anmeldung.",
    "h1": "Tagerechner – Tage zwischen zwei Daten zählen",
    "lead": "Wie viele Tage liegen zwischen zwei Daten? Wie viele davon sind Werktage? Und welches Datum ist in 90 Tagen? Der Tagerechner beantwortet alle drei Fragen.",
    "body": f"""
<div class="calc">
<h2>Tage zwischen zwei Daten</h2>
<div class="grid"><div><label for="d1">Startdatum</label><input type="date" id="d1"></div><div><label for="d2">Enddatum</label><input type="date" id="d2"></div><div><label for="inc">Enddatum mitzählen</label><select id="inc"><option value="0">Nein (Differenz)</option><option value="1">Ja (beide Tage zählen)</option></select></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">– Tage</div><div class="sub" id="td"></div>
<dl><dt>Werktage (Mo–Fr)</dt><dd id="wd">–</dd><dt>Wochenendtage</dt><dd id="we">–</dd><dt>Wochen</dt><dd id="wk">–</dd></dl></div>
<p class="hint">Gesetzliche Feiertage sind bundeslandabhängig und werden nicht abgezogen.</p>
</div>
<div class="calc">
<h2>Datum plus / minus Tage</h2>
<div class="grid"><div><label for="d3">Ausgangsdatum</label><input type="date" id="d3"></div><div><label for="op">Rechenart</label><select id="op"><option value="1">+ Tage addieren</option><option value="-1">– Tage abziehen</option></select></div><div><label for="n">Anzahl Tage</label><input type="number" id="n" value="90" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">–</div><div class="sub" id="t2d"></div></div>
</div>
{AD}
<h2>Tage zählen: Differenz oder inklusive?</h2>
<p>Zwischen dem 1. und dem 10. März liegen 9 Tage Differenz – zählt man beide Tage mit, sind es 10 Tage. Welche Variante richtig ist, hängt vom Zweck ab: Für Fristen zählt meist die Differenz (der Tag des Ereignisses selbst zählt nicht mit, § 187 BGB), für Urlaubs- oder Krankheitstage werden Anfangs- und Endtag mitgezählt. Der Rechner bietet beide Optionen.</p>
<h2>Werktage und Arbeitstage</h2>
<p>Der Tagerechner zählt Werktage als Montag bis Freitag. Juristisch sind Werktage allerdings Montag bis Samstag; die Arbeitstage Mo–Fr werden in der Praxis trotzdem meist so bezeichnet. Feiertage unterscheiden sich je nach Bundesland (Bayern hat bis zu 13, Berlin 10) und müssen bei Bedarf von Hand abgezogen werden. Für die monatliche Arbeitszeit multiplizierst du die Arbeitstage mit den täglichen Stunden aus dem <a href="/">Arbeitszeitrechner</a>.</p>
<h2>Häufige Fristen und Zeiträume</h2>
<ul>
<li><strong>6 Wochen Lohnfortzahlung</strong> im Krankheitsfall = 42 Kalendertage ab dem ersten Krankheitstag.</li>
<li><strong>Kündigungsfrist 4 Wochen</strong> zum 15. oder Monatsende (§ 622 BGB) – Zugang der Kündigung plus 28 Tage, dann der nächste zulässige Termin.</li>
<li><strong>Probezeit 6 Monate</strong>, <strong>Elternzeit</strong>, <strong>Mutterschutz 6 Wochen vor / 8 Wochen nach</strong> der Geburt – alle lassen sich mit „Datum plus Tage“ terminieren.</li>
</ul>
""",
    "faq": [
        ("Wie viele Tage hat ein Jahr?", "Ein normales Jahr hat 365 Tage, ein Schaltjahr 366 Tage. 2028 ist das nächste Schaltjahr. Der Rechner berücksichtigt Schaltjahre automatisch."),
        ("Wie berechnet man Werktage zwischen zwei Daten?", "Alle Tage zählen und die Samstage und Sonntage abziehen. Feiertage müssen zusätzlich abgezogen werden, da sie je nach Bundesland verschieden sind."),
        ("Wie viele Wochen sind 90 Tage?", "90 ÷ 7 = 12,86 Wochen, also 12 Wochen und 6 Tage."),
        ("Zählt der Starttag mit?", "Das lässt sich einstellen. Bei „Nein“ wird die reine Differenz berechnet (Fristenlogik), bei „Ja“ werden Start- und Endtag mitgezählt (z. B. für Urlaubstage)."),
    ],
    "js": r"""
(function(){var fmt=function(d){return d.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'long',year:'numeric'})};var today=new Date();var iso=function(d){return d.toISOString().slice(0,10)};
document.getElementById('d1').value=iso(today);var e=new Date(today);e.setDate(e.getDate()+30);document.getElementById('d2').value=iso(e);document.getElementById('d3').value=iso(today);
function c1(){var a=document.getElementById('d1').value,b=document.getElementById('d2').value;if(!a||!b)return;var A=new Date(a+'T00:00:00'),B=new Date(b+'T00:00:00'),inc=document.getElementById('inc').value==='1';var sign=B<A?-1:1;if(B<A){var x=A;A=B;B=x}var days=Math.round((B-A)/864e5);var wd=0,we=0;var cur=new Date(A);var total=days+(inc?1:0);for(var i=0;i<total;i++){var dow=cur.getDay();if(dow===0||dow===6)we++;else wd++;cur.setDate(cur.getDate()+1)}
document.getElementById('t').textContent=(sign<0?'−':'')+total.toLocaleString('de-DE')+' Tage';document.getElementById('td').textContent=fmt(A)+' bis '+fmt(B)+(sign<0?' (Enddatum liegt vor Startdatum)':'');
document.getElementById('wd').textContent=wd;document.getElementById('we').textContent=we;document.getElementById('wk').textContent=Math.floor(total/7)+' Wochen, '+(total%7)+' Tage'}
function c2(){var a=document.getElementById('d3').value;if(!a)return;var A=new Date(a+'T00:00:00'),n=parseInt(document.getElementById('n').value)||0,s=parseInt(document.getElementById('op').value);A.setDate(A.getDate()+s*n);document.getElementById('t2').textContent=A.toLocaleDateString('de-DE');document.getElementById('t2d').textContent=fmt(A)}
['d1','d2','inc'].forEach(function(i){document.getElementById(i).addEventListener('input',c1)});['d3','op','n'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c1();c2()})();"""
}

# ---------------------------------------------------------------- Überstunden
UEBER = {
    "path": "/ueberstunden-rechner/", "short": "Überstunden-Rechner", "tool": True,
    "card": "Überstunden berechnen und Auszahlung nach Stundenlohn und Zuschlag ermitteln.",
    "title": "Überstunden-Rechner – Überstunden berechnen & Auszahlung ermitteln",
    "desc": "Überstunden-Rechner: Mehrarbeit aus Soll- und Ist-Stunden berechnen und die Auszahlung der Überstunden mit Stundenlohn und Zuschlag (25 %, 50 %) ermitteln. Kostenlos online.",
    "h1": "Überstunden-Rechner – Überstunden und Auszahlung berechnen",
    "lead": "Wie viele Überstunden hast du gemacht und was sind sie wert? Gib Vertragsstunden, geleistete Stunden, Monatsgehalt und Zuschlag ein – der Rechner zeigt Überstunden und Brutto-Auszahlung.",
    "body": f"""
<div class="calc">
<h2>Überstunden berechnen</h2>
<div class="grid"><div><label for="soll">Vertragliche Stunden pro Woche</label><input type="number" id="soll" value="40" step="0.5" min="0"></div><div><label for="ist">Tatsächlich gearbeitet (Stunden)</label><input type="number" id="ist" value="46.5" step="0.25" min="0"></div><div><label for="per">Zeitraum</label><select id="per"><option value="1">1 Woche</option><option value="4.33">1 Monat</option></select></div></div>
<h3 style="margin-top:18px">Auszahlung (optional)</h3>
<div class="grid"><div><label for="gehalt">Monatsgehalt brutto (€)</label><input type="number" id="gehalt" value="3400" step="50" min="0"></div><div><label for="z">Zuschlag</label><select id="z"><option value="0">0 % (kein Zuschlag)</option><option value="25" selected>25 %</option><option value="50">50 %</option><option value="100">100 %</option></select></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="ot">6:30 Überstunden</div><div class="sub" id="otd"></div>
<dl><dt>Stundenlohn brutto</dt><dd id="sl">–</dd><dt>Überstundensatz (inkl. Zuschlag)</dt><dd id="sz">–</dd><dt>Auszahlung brutto</dt><dd id="pay">–</dd></dl>
<div class="actions"><button class="btn sm ghost" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
<p class="hint">Stundenlohn = Monatsgehalt ÷ (Wochenstunden × 4,33). Die Auszahlung ist ein Bruttobetrag; Steuern und Sozialabgaben werden abgezogen.</p>
</div>
{AD}
<h2>Wann sind Überstunden zu bezahlen?</h2>
<p>Überstunden sind Arbeitsstunden über die vertraglich vereinbarte Arbeitszeit hinaus. Ein <strong>gesetzlicher Anspruch auf einen Zuschlag</strong> besteht nicht; er ergibt sich nur aus Tarifvertrag, Betriebsvereinbarung oder Arbeitsvertrag. Üblich sind 25 % für normale Überstunden und 50 % an Sonn- und Feiertagen oder in der Nacht. Die Grundvergütung der Überstunde selbst steht dir dagegen in der Regel zu (§ 612 BGB), sofern sie vom Arbeitgeber angeordnet oder geduldet wurde.</p>
<h2>Pauschale Abgeltung im Arbeitsvertrag</h2>
<p>Klauseln wie „Überstunden sind mit dem Gehalt abgegolten“ sind nur wirksam, wenn der Umfang klar begrenzt ist (z. B. „bis zu 10 Stunden im Monat“). Pauschale Formulierungen ohne Obergrenze hat das Bundesarbeitsgericht für unwirksam erklärt – außer bei Gehältern über der Beitragsbemessungsgrenze der Rentenversicherung.</p>
<h2>Überstunden auszahlen oder abfeiern?</h2>
<p>Viele Betriebe führen ein Arbeitszeitkonto. Dann werden Überstunden als Freizeitausgleich genommen, statt ausgezahlt. Bei der Auszahlung fallen Lohnsteuer und Sozialversicherung an – der Nettobetrag liegt daher je nach Steuerklasse bei rund 55–70 % der Bruttosumme. Für die genaue Nettoberechnung ist ein Brutto-Netto-Rechner mit deiner Steuerklasse nötig.</p>
<p>Die geleisteten Stunden pro Woche erfasst du am einfachsten im <a href="/">Arbeitszeitrechner</a>; den Stundenlohn allein berechnet der <a href="/stundenlohnrechner/">Stundenlohnrechner</a>.</p>
""",
    "faq": [
        ("Wie berechnet man Überstunden?", "Tatsächlich geleistete Stunden minus vertraglich vereinbarte Stunden im selben Zeitraum. Bei 40 Wochenstunden und 46,5 gearbeiteten Stunden sind es 6,5 Überstunden."),
        ("Wie hoch ist der Überstundenzuschlag?", "Es gibt keinen gesetzlichen Zuschlag. Tarifverträge sehen häufig 25 % vor, für Nacht-, Sonn- und Feiertagsarbeit 50 % oder mehr. Maßgeblich ist dein Tarif- oder Arbeitsvertrag."),
        ("Wie berechnet man den Stundenlohn aus dem Monatsgehalt?", "Monatsgehalt ÷ (Wochenstunden × 4,33). Bei 3.400 € und 40 Stunden: 3.400 ÷ 173,33 = 19,62 € pro Stunde."),
        ("Verfallen Überstunden?", "Ansprüche verjähren nach drei Jahren (§ 195 BGB). Arbeitsverträge enthalten oft kürzere Ausschlussfristen von drei Monaten – dann müssen Überstunden innerhalb dieser Frist schriftlich geltend gemacht werden."),
    ],
    "js": r"""
(function(){function c(){var soll=parseFloat(document.getElementById('soll').value)||0,ist=parseFloat(document.getElementById('ist').value)||0,per=parseFloat(document.getElementById('per').value),g=parseFloat(document.getElementById('gehalt').value)||0,z=parseFloat(document.getElementById('z').value)||0;
var ot=ist-soll*per;document.getElementById('ot').textContent=fmtHM(ot*60)+(ot>=0?' Überstunden':' Minusstunden');document.getElementById('otd').textContent=ot.toLocaleString('de-DE',{minimumFractionDigits:2,maximumFractionDigits:2})+' Stunden (dezimal) bei '+(soll*per).toLocaleString('de-DE',{maximumFractionDigits:2})+' Soll-Stunden';
if(g>0&&soll>0){var sl=g/(soll*4.33),sz=sl*(1+z/100);document.getElementById('sl').textContent=eur(sl);document.getElementById('sz').textContent=eur(sz);document.getElementById('pay').textContent=ot>0?eur(sz*ot):'–'}else{['sl','sz','pay'].forEach(function(i){document.getElementById(i).textContent='–'})}}
['soll','ist','per','gehalt','z'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""
}

# ---------------------------------------------------------------- Pausenrechner
PAUSE = {
    "path": "/pausenrechner/", "short": "Pausenrechner", "tool": True,
    "card": "Gesetzliche Mindestpause nach § 4 ArbZG und Netto-Arbeitszeit berechnen.",
    "title": "Pausenrechner – gesetzliche Pause bei 6, 8 oder 10 Stunden Arbeit",
    "desc": "Pausenrechner nach § 4 Arbeitszeitgesetz: Wie viel Pause steht mir bei 6, 8, 9 oder 10 Stunden Arbeit zu? Arbeitsbeginn und -ende eingeben, Mindestpause und Netto-Arbeitszeit berechnen.",
    "h1": "Pausenrechner – gesetzliche Pause und Arbeitszeit berechnen",
    "lead": "Bei mehr als 6 Stunden Arbeit sind 30 Minuten Pause Pflicht, bei mehr als 9 Stunden 45 Minuten. Der Pausenrechner zeigt die Mindestpause für deine Schicht und die verbleibende Netto-Arbeitszeit.",
    "body": f"""
<div class="calc">
<h2>Pause nach Arbeitszeitgesetz</h2>
<div class="grid"><div><label for="a">Arbeitsbeginn</label><input type="time" id="a" value="07:30"></div><div><label for="b">Arbeitsende</label><input type="time" id="b" value="17:15"></div><div><label for="p">Geplante Pause (Minuten)</label><input type="number" id="p" value="30" min="0" step="5"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div>
<dl><dt>Anwesenheit</dt><dd id="an">–</dd><dt>Gesetzliche Mindestpause</dt><dd id="mp">–</dd><dt>Netto-Arbeitszeit</dt><dd id="net">–</dd><dt>Höchstarbeitszeit (10 Std.)</dt><dd id="max">–</dd></dl></div>
</div>
{AD}
<h2>Pausenregelung nach § 4 ArbZG</h2>
<table class="t"><thead><tr><th>Arbeitszeit</th><th>Mindestpause</th><th>Aufteilung möglich</th></tr></thead><tbody>
<tr><td>bis 6 Stunden</td><td>keine Pflicht</td><td>–</td></tr>
<tr><td>mehr als 6 bis 9 Stunden</td><td>30 Minuten</td><td>in Abschnitte von je mindestens 15 Minuten</td></tr>
<tr><td>mehr als 9 Stunden</td><td>45 Minuten</td><td>in Abschnitte von je mindestens 15 Minuten</td></tr>
</tbody></table>
<p>Wichtig: Die Pause muss <strong>im Voraus feststehen</strong> und darf nicht am Anfang oder Ende der Schicht liegen. Länger als 6 Stunden ohne Pause zu arbeiten, ist nicht erlaubt. Für Jugendliche unter 18 gilt das Jugendarbeitsschutzgesetz mit strengeren Regeln: 30 Minuten bei mehr als 4,5 Stunden, 60 Minuten bei mehr als 6 Stunden.</p>
<h2>Zählt die Pause zur Arbeitszeit?</h2>
<p>Nein. Ruhepausen sind unbezahlte Unterbrechungen, in denen du frei über deine Zeit verfügst. Anders ist es bei <em>Arbeitsbereitschaft</em> oder <em>Bereitschaftsdienst</em> – diese zählen als Arbeitszeit. Kurzpausen wie der Gang zur Toilette oder ein Kaffee am Platz sind keine Pausen im Sinne des Gesetzes und werden nicht abgezogen.</p>
<p>Die Pause wird im <a href="/">Arbeitszeitrechner</a> direkt von der Anwesenheitszeit abgezogen. Wer in Dezimalstunden abrechnet, findet die Umrechnung im <a href="/dezimal-rechner/">Dezimal-Rechner</a>.</p>
""",
    "faq": [
        ("Wie viel Pause bei 8 Stunden Arbeit?", "Mindestens 30 Minuten. Die Regel gilt ab mehr als 6 Stunden Arbeitszeit bis einschließlich 9 Stunden."),
        ("Wie viel Pause bei 10 Stunden?", "Mindestens 45 Minuten, da die Arbeitszeit mehr als 9 Stunden beträgt. 10 Stunden sind zugleich die tägliche Höchstarbeitszeit."),
        ("Wie viel Pause bei 6 Stunden?", "Bei genau 6 Stunden ist keine Pause vorgeschrieben. Erst ab 6 Stunden und 1 Minute gelten 30 Minuten."),
        ("Darf die Pause aufgeteilt werden?", "Ja, in Abschnitte von jeweils mindestens 15 Minuten. Zwei Pausen à 15 Minuten erfüllen also die 30-Minuten-Pflicht."),
        ("Muss die Pause bezahlt werden?", "Gesetzliche Ruhepausen sind unbezahlt, es sei denn, Tarifvertrag oder Arbeitsvertrag sehen etwas anderes vor."),
    ],
    "js": r"""
(function(){function c(){var a=tmin(document.getElementById('a').value),b=tmin(document.getElementById('b').value),p=parseFloat(document.getElementById('p').value)||0;if(a===null||b===null)return;var an=b-a;if(an<0)an+=1440;
var net=an-p;var mp=net>540?45:(net>360?30:0);if(an-mp>540&&mp<45)mp=45;var ok=p>=mp;
document.getElementById('an').textContent=fmtHM(an)+' Std.';document.getElementById('mp').textContent=mp+' Minuten';document.getElementById('net').textContent=fmtHM(net)+' Std. ('+fmtDec(net)+')';
document.getElementById('max').textContent=net>600?'überschritten um '+fmtHM(net-600):'eingehalten';
document.getElementById('t').textContent=ok?'Pause ausreichend ✓':'Pause zu kurz: mindestens '+mp+' Min.';document.getElementById('td').textContent=ok?'Deine Pause von '+p+' Minuten erfüllt § 4 ArbZG.':'Es fehlen '+(mp-p)+' Minuten Pause.'}
['a','b','p'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""
}

# ---------------------------------------------------------------- Dezimal
tbl = "".join(f"<tr><td>{m} Min.</td><td class=\"num\">{m/60:.2f}".replace(".", ",") + "</td><td>" + f"{m+30 if m+30<60 else ''}" + "</td></tr>" for m in [])
dez_rows = "".join(
    f'<tr><td>{m}</td><td class="num">{str(round(m/60,2)).replace(".",",")}</td><td>{m+30}</td><td class="num">{str(round((m+30)/60,2)).replace(".",",")}</td></tr>'
    for m in range(0, 30, 1))
DEZ = {
    "path": "/dezimal-rechner/", "short": "Dezimal-Rechner", "tool": True,
    "card": "Stunden:Minuten in Dezimalstunden umrechnen und zurück – mit Industrieminuten-Tabelle.",
    "title": "Stunden in Dezimal umrechnen – Dezimal-Rechner & Industrieminuten-Tabelle",
    "desc": "Stunden und Minuten in Dezimalstunden umrechnen (und zurück): 7:45 = 7,75. Dezimal-Rechner mit Umrechnungstabelle für Industrieminuten – für Zeiterfassung und Lohnabrechnung.",
    "h1": "Dezimal-Rechner – Stunden und Minuten in Dezimalstunden",
    "lead": "7 Stunden 45 Minuten sind 7,75 Dezimalstunden. Der Rechner wandelt in beide Richtungen um und zeigt die Industrieminuten-Tabelle für die Zeiterfassung.",
    "body": f"""
<div class="calc">
<h2>Stunden:Minuten → Dezimal</h2>
<div class="grid"><div><label for="h">Stunden</label><input type="number" id="h" value="7" min="0"></div><div><label for="m">Minuten</label><input type="number" id="m" value="45" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">7,75</div><div class="sub" id="td">Dezimalstunden · 465 Minuten · 775 Industrieminuten</div></div>
</div>
<div class="calc">
<h2>Dezimal → Stunden:Minuten</h2>
<div class="grid"><div><label for="d">Dezimalstunden</label><input type="number" id="d" value="3.3" step="0.01" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">3:18</div><div class="sub" id="t2d">3 Stunden und 18 Minuten</div></div>
</div>
{AD}
<h2>Umrechnungstabelle Minuten in Dezimalstunden</h2>
<table class="t"><thead><tr><th>Minuten</th><th style="text-align:right">Dezimal</th><th>Minuten</th><th style="text-align:right">Dezimal</th></tr></thead><tbody>{dez_rows}</tbody></table>
<h2>Was sind Industrieminuten?</h2>
<p>Industrieminuten (auch Dezimalminuten) teilen die Stunde in 100 statt 60 Einheiten. 1 Industrieminute = 0,6 normale Minuten; 1 normale Minute = 1,667 Industrieminuten. Zeiterfassungssysteme rechnen intern fast immer dezimal, weil sich Dezimalzahlen direkt mit dem Stundenlohn multiplizieren lassen: 7,75 Stunden × 20 € = 155 €. Mit 7:45 ginge das nicht.</p>
<h2>Formel</h2>
<ul>
<li><strong>Minuten → Dezimal:</strong> Minuten ÷ 60. Beispiel 45 ÷ 60 = 0,75.</li>
<li><strong>Dezimal → Minuten:</strong> Nachkommastellen × 60. Beispiel 0,3 × 60 = 18 Minuten.</li>
<li><strong>Industrieminuten:</strong> normale Minuten × 1,667 (oder Dezimalstunden × 100).</li>
</ul>
<p>Die Umrechnung ist der letzte Schritt nach dem <a href="/">Arbeitszeitrechner</a> oder dem <a href="/stundenrechner/">Stundenrechner</a>, wenn Werte in den Stundenzettel übertragen werden.</p>
""",
    "faq": [
        ("Wie viel ist 7,5 Stunden in Stunden und Minuten?", "7 Stunden und 30 Minuten (0,5 × 60 = 30)."),
        ("Was sind 1,75 Stunden?", "1 Stunde und 45 Minuten."),
        ("Wie rechne ich 8:20 in Dezimal um?", "20 ÷ 60 = 0,333. Ergebnis: 8,33 Dezimalstunden."),
        ("Warum verwenden Zeiterfassungssysteme Dezimalstunden?", "Weil sich Dezimalzahlen direkt mit dem Stundenlohn multiplizieren und addieren lassen, ohne den 60er-Übertrag der Minuten."),
    ],
    "js": r"""
(function(){function c1(){var h=parseFloat(document.getElementById('h').value)||0,m=parseFloat(document.getElementById('m').value)||0,t=h*60+m;document.getElementById('t').textContent=fmtDec(t);document.getElementById('td').textContent='Dezimalstunden · '+Math.round(t)+' Minuten · '+Math.round(t/60*100)+' Industrieminuten'}
function c2(){var d=parseFloat(document.getElementById('d').value)||0,t=Math.round(d*60);document.getElementById('t2').textContent=fmtHM(t);document.getElementById('t2d').textContent=Math.floor(t/60)+' Stunden und '+(t%60)+' Minuten'}
['h','m'].forEach(function(i){document.getElementById(i).addEventListener('input',c1)});document.getElementById('d').addEventListener('input',c2);c1();c2()})();"""
}

# ---------------------------------------------------------------- MwSt
MWST = {
    "path": "/mwst-rechner/", "short": "MwSt-Rechner", "tool": True,
    "card": "Mehrwertsteuer berechnen: Netto ↔ Brutto bei 19 % und 7 %.",
    "title": "MwSt-Rechner – Mehrwertsteuer berechnen (19 % & 7 %, Netto ↔ Brutto)",
    "desc": "MwSt-Rechner: Mehrwertsteuer aus Netto oder Brutto berechnen – 19 %, 7 % oder eigener Satz. Netto zu Brutto, Brutto zu Netto und Steuerbetrag in einem Schritt. Kostenlos online.",
    "h1": "MwSt-Rechner – Mehrwertsteuer aus Netto oder Brutto berechnen",
    "lead": "Betrag eingeben, Steuersatz wählen, fertig: Der Mehrwertsteuer-Rechner zeigt Netto, Brutto und den MwSt-Betrag bei 19 %, 7 % oder einem eigenen Satz.",
    "body": f"""
<div class="calc">
<h2>Mehrwertsteuer berechnen</h2>
<div class="grid"><div><label for="amt">Betrag (€)</label><input type="number" id="amt" value="100" step="0.01" min="0"></div><div><label for="kind">Der Betrag ist</label><select id="kind"><option value="n">Netto (ohne MwSt)</option><option value="b">Brutto (mit MwSt)</option></select></div><div><label for="rate">Steuersatz</label><select id="rate"><option value="19">19 % (Regelsatz)</option><option value="7">7 % (ermäßigt)</option><option value="0">0 %</option><option value="x">Eigener Satz</option></select></div><div id="cw" style="display:none"><label for="custom">Eigener Satz (%)</label><input type="number" id="custom" value="20" step="0.1" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">119,00 €</div><div class="sub" id="td">Brutto</div>
<dl><dt>Netto</dt><dd id="n">100,00 €</dd><dt>MwSt-Betrag</dt><dd id="v">19,00 €</dd><dt>Brutto</dt><dd id="b">119,00 €</dd></dl>
<div class="actions"><button class="btn sm ghost" onclick="copyRes('res',this)">Ergebnis kopieren</button></div></div>
</div>
{AD}
<h2>Mehrwertsteuer in Deutschland: 19 % und 7 %</h2>
<p>Der Regelsteuersatz der Umsatzsteuer (umgangssprachlich Mehrwertsteuer) beträgt in Deutschland 19 %. Der ermäßigte Satz von 7 % gilt unter anderem für Lebensmittel, Bücher, Zeitungen, den öffentlichen Nahverkehr und ab 2026 wieder für Speisen in der Gastronomie. Einige Leistungen sind steuerfrei (0 %), etwa ärztliche Behandlungen, Vermietung von Wohnraum und innergemeinschaftliche Lieferungen.</p>
<h2>Formeln für die MwSt-Berechnung</h2>
<ul>
<li><strong>Netto → Brutto:</strong> Netto × 1,19 (bei 19 %) bzw. × 1,07 (bei 7 %).</li>
<li><strong>Brutto → Netto:</strong> Brutto ÷ 1,19 bzw. ÷ 1,07. Nicht Brutto × 0,81 – das ist ein häufiger Fehler.</li>
<li><strong>MwSt aus Brutto herausrechnen:</strong> Brutto ÷ 1,19 × 0,19 – oder einfacher Brutto × 19 ÷ 119 (= Brutto × 0,1597).</li>
</ul>
<p>Beispiel: Ein Bruttopreis von 238 € enthält 238 ÷ 1,19 = 200 € Netto und 38 € Mehrwertsteuer.</p>
<h2>Wer braucht den MwSt-Rechner?</h2>
<p>Selbstständige und Kleinunternehmer beim Schreiben von Rechnungen, Käufer, die den Nettopreis für die Vorsteuer wissen wollen, und alle, die einen Bruttopreis schnell auf den Nettobetrag zurückrechnen müssen. Kleinunternehmer nach § 19 UStG weisen keine Umsatzsteuer aus – für sie gilt der Satz 0 %.</p>
<p>Stundenbasierte Rechnungen entstehen oft aus dem <a href="/stundenrechner/">Stundenrechner</a>: Stunden × Stundensatz = Netto, dann hier die MwSt aufschlagen.</p>
""",
    "faq": [
        ("Wie rechne ich 19 % MwSt aus dem Bruttobetrag heraus?", "Bruttobetrag ÷ 1,19 ergibt den Nettobetrag; die Differenz ist die Mehrwertsteuer. 119 € ÷ 1,19 = 100 € Netto, 19 € MwSt."),
        ("Wie berechne ich den Bruttopreis aus dem Nettopreis?", "Nettopreis × 1,19 bei 19 % oder × 1,07 bei 7 %. 250 € Netto × 1,19 = 297,50 € Brutto."),
        ("Was ist der Unterschied zwischen Mehrwertsteuer und Umsatzsteuer?", "Keiner im Alltag: Das Gesetz heißt Umsatzsteuergesetz, auf Rechnungen und im Sprachgebrauch wird meist Mehrwertsteuer gesagt. Gemeint ist dieselbe Steuer."),
        ("Welche Produkte haben 7 % Mehrwertsteuer?", "Grundnahrungsmittel, Bücher, Zeitschriften, Hotelübernachtungen, der Nahverkehr, Kunstgegenstände und ab 2026 Speisen in Restaurants."),
    ],
    "js": r"""
(function(){function c(){var a=parseFloat(document.getElementById('amt').value)||0,k=document.getElementById('kind').value,rs=document.getElementById('rate').value;document.getElementById('cw').style.display=rs==='x'?'block':'none';var r=rs==='x'?(parseFloat(document.getElementById('custom').value)||0):parseFloat(rs);
var n,b;if(k==='n'){n=a;b=a*(1+r/100)}else{b=a;n=a/(1+r/100)}var v=b-n;
document.getElementById('n').textContent=eur(n);document.getElementById('v').textContent=eur(v)+' ('+r.toLocaleString('de-DE')+' %)';document.getElementById('b').textContent=eur(b);
document.getElementById('t').textContent=k==='n'?eur(b):eur(n);document.getElementById('td').textContent=k==='n'?'Brutto (inkl. MwSt)':'Netto (ohne MwSt)'}
['amt','kind','rate','custom'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""
}

# ---------------------------------------------------------------- Stundenlohn
LOHN = {
    "path": "/stundenlohnrechner/", "short": "Stundenlohnrechner", "tool": True,
    "card": "Stundenlohn aus Monatsgehalt berechnen – oder Monatslohn aus Stundenlohn.",
    "title": "Stundenlohnrechner – Stundenlohn aus Monatsgehalt berechnen",
    "desc": "Stundenlohnrechner: Brutto-Stundenlohn aus Monatsgehalt und Wochenstunden berechnen oder Monatslohn aus Stundenlohn ermitteln. Mit Mindestlohn 2026 und Minijob-Grenze.",
    "h1": "Stundenlohnrechner – Stundenlohn und Monatslohn umrechnen",
    "lead": "Was verdienst du pro Stunde? Monatsgehalt und Wochenstunden eingeben – oder umgekehrt aus Stundenlohn und Stunden den Monatslohn berechnen.",
    "body": f"""
<div class="calc">
<h2>Stundenlohn aus Monatsgehalt</h2>
<div class="grid"><div><label for="g">Monatsgehalt brutto (€)</label><input type="number" id="g" value="3200" step="50" min="0"></div><div><label for="w">Wochenstunden</label><input type="number" id="w" value="40" step="0.5" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">18,46 €</div><div class="sub" id="td">brutto pro Stunde bei 173,33 Monatsstunden</div>
<dl><dt>Jahresgehalt</dt><dd id="y">–</dd><dt>Vergleich Mindestlohn 2026 (13,90 €)</dt><dd id="ml">–</dd></dl></div>
</div>
<div class="calc">
<h2>Monatslohn aus Stundenlohn</h2>
<div class="grid"><div><label for="sl">Stundenlohn brutto (€)</label><input type="number" id="sl" value="15" step="0.5" min="0"></div><div><label for="hs">Stunden pro Woche</label><input type="number" id="hs" value="20" step="0.5" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">1.299,00 €</div><div class="sub" id="t2d">brutto pro Monat (86,6 Stunden)</div>
<dl><dt>Minijob-Grenze 2026 (603 €)</dt><dd id="mj">–</dd></dl></div>
</div>
{AD}
<h2>So wird der Stundenlohn berechnet</h2>
<p>Die gängige Formel lautet: <strong>Stundenlohn = Monatsgehalt ÷ (Wochenstunden × 4,33)</strong>. Der Faktor 4,33 ist die durchschnittliche Zahl der Wochen pro Monat (52 ÷ 12 = 4,333). Bei 3.200 € und 40 Stunden ergibt das 3.200 ÷ 173,33 = 18,46 € brutto pro Stunde. Manche Tarifverträge verwenden den Faktor 4,35 oder rechnen mit 4,348 Wochen – die Abweichung liegt im Cent-Bereich.</p>
<h2>Mindestlohn und Minijob</h2>
<p>Der gesetzliche Mindestlohn beträgt seit dem 1. Januar 2026 <strong>13,90 € brutto pro Stunde</strong> (2027: 14,60 €). Die Minijob-Grenze ist an den Mindestlohn gekoppelt und liegt 2026 bei <strong>603 € pro Monat</strong> – das entspricht etwa 10 Wochenstunden zum Mindestlohn. Wer mehr verdient, rutscht in den Übergangsbereich (Midijob) mit reduzierten Sozialabgaben bis 2.000 €.</p>
<h2>Brutto ist nicht netto</h2>
<p>Alle Werte hier sind Bruttobeträge. Vom Bruttolohn gehen Lohnsteuer, Solidaritätszuschlag (meist entfallen), gegebenenfalls Kirchensteuer und die Sozialversicherungsbeiträge (rund 20–21 % Arbeitnehmeranteil) ab. Der Nettolohn liegt je nach Steuerklasse bei etwa 60–75 % des Brutto.</p>
<p>Mehrarbeit bewertest du mit dem <a href="/ueberstunden-rechner/">Überstunden-Rechner</a>, die tatsächlich geleisteten Stunden erfasst der <a href="/">Arbeitszeitrechner</a>.</p>
""",
    "faq": [
        ("Wie berechnet man den Stundenlohn aus dem Gehalt?", "Monatsgehalt ÷ (Wochenstunden × 4,33). Bei 2.800 € und 38,5 Stunden: 2.800 ÷ 166,7 = 16,80 € pro Stunde."),
        ("Wie hoch ist der Mindestlohn 2026?", "13,90 € brutto pro Stunde seit dem 1. Januar 2026. Zum 1. Januar 2027 steigt er auf 14,60 €."),
        ("Wie viele Stunden darf ich im Minijob arbeiten?", "Die Grenze ist der Verdienst, nicht die Stundenzahl: 603 € im Monat (2026). Zum Mindestlohn sind das rund 43 Stunden im Monat bzw. 10 Stunden pro Woche."),
        ("Warum rechnet man mit 4,33 Wochen pro Monat?", "Ein Jahr hat 52 Wochen und 12 Monate. 52 ÷ 12 = 4,33 Wochen je Monat im Durchschnitt."),
    ],
    "js": r"""
(function(){var ML=13.90,MJ=603;function c1(){var g=parseFloat(document.getElementById('g').value)||0,w=parseFloat(document.getElementById('w').value)||0;if(!w){return}var mh=w*4.33,sl=g/mh;document.getElementById('t').textContent=eur(sl);document.getElementById('td').textContent='brutto pro Stunde bei '+mh.toLocaleString('de-DE',{maximumFractionDigits:2})+' Monatsstunden';document.getElementById('y').textContent=eur(g*12);document.getElementById('ml').textContent=sl>=ML?'über Mindestlohn (+'+eur(sl-ML)+')':'UNTER Mindestlohn (−'+eur(ML-sl)+')'}
function c2(){var sl=parseFloat(document.getElementById('sl').value)||0,h=parseFloat(document.getElementById('hs').value)||0,mh=h*4.33,m=sl*mh;document.getElementById('t2').textContent=eur(m);document.getElementById('t2d').textContent='brutto pro Monat ('+mh.toLocaleString('de-DE',{maximumFractionDigits:1})+' Stunden)';document.getElementById('mj').textContent=m<=MJ?'Minijob möglich (noch '+eur(MJ-m)+' Spielraum)':'über Minijob-Grenze – sozialversicherungspflichtig'}
['g','w'].forEach(function(i){document.getElementById(i).addEventListener('input',c1)});['sl','hs'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c1();c2()})();"""
}

TOOLS = [HOME, STUNDEN, ZEIT, TAGE, UEBER, PAUSE, DEZ, MWST, LOHN]
