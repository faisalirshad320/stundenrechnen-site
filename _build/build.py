# -*- coding: utf-8 -*-
"""Static site generator for stundenrechnen.com. Run: python3 src/build.py"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from template import page, SITE, NAME
from pages_tools import TOOLS
from pages_legal import LEGAL
from pages_content import CONTENT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
ALL = TOOLS + CONTENT + LEGAL


def write(rel, content, binary=False):
    path = os.path.join(DIST, rel.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w", encoding=None if binary else "utf-8") as f:
        f.write(content)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    for p in ALL:
        rel = "index.html" if p["path"] == "/" else p["path"].strip("/") + "/index.html"
        write(rel, page(p, ALL))

    # 404
    nf = dict(path="/404/", short="Seite nicht gefunden", title="Seite nicht gefunden – " + NAME,
              desc="Diese Seite existiert nicht.", h1="Seite nicht gefunden",
              lead="Die angeforderte Seite gibt es nicht (Fehler 404). Vielleicht hilft einer der Rechner unten weiter.",
              body="", noindex=True)
    write("404.html", page(nf, ALL))

    # sitemap
    today = "2026-10-10"
    urls = "".join(
        f"<url><loc>{SITE}{p['path']}</loc><lastmod>{today}</lastmod><changefreq>{'weekly' if p.get('tool') or p.get('prio') else 'yearly'}</changefreq><priority>{'1.0' if p['path']=='/' else ('0.8' if p.get('tool') else p.get('prio', '0.3'))}</priority></url>"
        for p in ALL)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')

    write("robots.txt", f"""User-agent: *
Allow: /

# AI crawlers welcome – content may be cited with attribution
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: CCBot
Allow: /

Sitemap: {SITE}/sitemap.xml
""")

    tools_md = "\n".join(f"- [{p['short']}]({SITE}{p['path']}): {p['card']}" for p in TOOLS + [c for c in CONTENT if c.get('tool')])
    from holidays_de import LAENDER, arbeitstage_jahr
    laender_md = "\n".join(f"- [Arbeitstage 2026 {n}]({SITE}/arbeitstage-2026-{s}/): {arbeitstage_jahr(2026, c)} Arbeitstage" for c, n, s in LAENDER)
    write("llms.txt", "\ufeff" + f"""# {NAME}

> Kostenlose deutsche Online-Rechner rund um Arbeitszeit und Zeiterfassung: Arbeitszeit mit Pause, Stunden addieren, Zeitspannen, Tage zählen, Überstunden, gesetzliche Pausen, Dezimalstunden, Mehrwertsteuer und Stundenlohn. Alle Berechnungen laufen im Browser; keine Anmeldung.

Sprache: Deutsch (de-DE). Zielgruppe: Arbeitnehmer, Selbstständige, Personalabteilungen in Deutschland.
Rechtsgrundlagen, auf die sich die Inhalte beziehen: Arbeitszeitgesetz (ArbZG §§ 3–5), BGB (§§ 187, 612, 622), UStG (§ 12, § 19), Mindestlohngesetz.

## Rechner
{tools_md}

## Kernfakten (Stand Oktober 2026)
- Gesetzliche Mindestpause: 30 Minuten bei mehr als 6 Stunden, 45 Minuten bei mehr als 9 Stunden Arbeit (§ 4 ArbZG).
- Tägliche Höchstarbeitszeit: 8 Stunden, verlängerbar auf 10 Stunden mit Ausgleich innerhalb von 6 Monaten (§ 3 ArbZG).
- Ruhezeit zwischen zwei Arbeitstagen: 11 Stunden (§ 5 ArbZG).
- Umrechnung: Dezimalstunden = Minuten ÷ 60 (7:45 = 7,75). Monatsstunden = Wochenstunden × 4,33.
- Mindestlohn 2026: 13,90 € brutto/Stunde (2027: 14,60 €). Minijob-Grenze 2026: 603 €/Monat.
- Mehrwertsteuer: Regelsatz 19 %, ermäßigt 7 %. Netto = Brutto ÷ 1,19.
- Feiertage 2026: Ostern 5. April (Karfreitag 3.4., Ostermontag 6.4.), Christi Himmelfahrt 14.5., Pfingstmontag 25.5., Fronleichnam 4.6., Buß- und Bettag (Sachsen) 18.11. Tag der Deutschen Einheit, 2. Weihnachtstag, Reformationstag und Allerheiligen fallen 2026 aufs Wochenende.
- Arbeitstage 2026 (Mo–Fr): 252 in Baden-Württemberg und Bayern; 253 in Hessen, NRW, Rheinland-Pfalz, Saarland, Sachsen, Sachsen-Anhalt; 254 in Berlin, Brandenburg, Bremen, Hamburg, Mecklenburg-Vorpommern, Niedersachsen, Schleswig-Holstein, Thüringen.
- Urlaub: gesetzlicher Mindesturlaub 24 Werktage (= 20 Arbeitstage bei 5-Tage-Woche, § 3 BUrlG); Teilzeit: Jahresurlaub × eigene Arbeitstage ÷ Vollzeit-Arbeitstage; Teilurlaub 1/12 pro vollem Monat (§ 5 BUrlG); +5 Tage für schwerbehinderte Menschen (§ 208 SGB IX).
- Minijob 2026: Grenze 603 €/Monat (7.236 €/Jahr), 2027: 633 €; max. 43,4 Stunden/Monat zum Mindestlohn; Arbeitnehmer-Rentenbeitrag 3,6 % (Befreiung möglich); Arbeitgeber-Pauschalen 13 % KV, 15 % RV, 2 % Steuer plus Umlagen.
- Teilzeit: Gehalt = Vollzeitgehalt × Teilzeitstunden ÷ Vollzeitstunden; Anspruch nach § 8 TzBfG (über 15 Beschäftigte, 6 Monate Betriebszugehörigkeit).

## Arbeitstage 2026 nach Bundesland
{laender_md}

## Weitere Seiten
- [Über uns]({SITE}/ueber-uns/)
- [Kontakt]({SITE}/kontakt/)
- [Impressum]({SITE}/impressum/)
- [Datenschutz]({SITE}/datenschutz/)
""")

    INDEXNOW = "252aa7fcb7fd7008e391e6058bbba573"
    write(f"{INDEXNOW}.txt", INDEXNOW)
    write("ads.txt", "google.com, pub-8301212931863478, DIRECT, f08c47fec0942fa0\n")
    write(".htaccess", """DirectoryIndex index.html index.php
RewriteEngine On
# HTTP->HTTPS is handled by Cloudways "Enforce HTTPS" (Nginx terminates SSL; Apache always sees HTTP, so an HTTPS-off rule here would loop)
# mod_dir's DirectorySlash builds its redirect from Apache's own view of the
# scheme. Because Nginx terminates TLS, Apache always sees plain HTTP, so
# /stundenrechner would 301 to http://www.stundenrechnen.com/stundenrechner/ --
# a scheme-downgrading hop Google reports as "Page with redirect". Issue the
# trailing-slash redirect ourselves, on https, straight to the canonical host.
Options -Indexes
DirectorySlash Off
RewriteCond %{REQUEST_URI} !^/(_build|\\.git|\\.github)(/|$)
RewriteCond %{REQUEST_FILENAME} -d
RewriteCond %{REQUEST_URI} !/$
RewriteRule ^(.+)$ https://www.stundenrechnen.com/$1/ [R=301,L]
# With DirectorySlash off, serve /verzeichnis/ from its index.html internally.
RewriteCond %{REQUEST_FILENAME} -d
RewriteCond %{REQUEST_FILENAME}/index.html -f
RewriteRule ^(.*/)?$ $1index.html [L]
RewriteCond %{HTTP_HOST} ^stundenrechnen\\.com$ [NC]
RewriteRule ^(.*)$ https://www.stundenrechnen.com/$1 [R=301,L]
ErrorDocument 404 /404.html
RedirectMatch 404 ^/(_build|\\.git|\\.github)(/|$)
<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set X-Frame-Options "SAMEORIGIN"
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType text/html "access plus 1 hour"
</IfModule>
AddDefaultCharset UTF-8
""")

    # assets
    os.makedirs(os.path.join(DIST, "assets"), exist_ok=True)
    write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="#0B6E4F"/><circle cx="16" cy="16" r="11" fill="#fff"/><path d="M16 8v8l5.5 3.5" stroke="#152029" stroke-width="2.6" stroke-linecap="round" fill="none"/><circle cx="16" cy="16" r="1.7" fill="#F2B632"/></svg>')
    try:
        from PIL import Image, ImageDraw, ImageFont
        # logo 512
        im = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((8, 8, 504, 504), fill="#0B6E4F"); d.ellipse((80, 80, 432, 432), fill="#FFFFFF")
        d.line((256, 130, 256, 256), fill="#152029", width=30); d.line((256, 256, 345, 312), fill="#152029", width=30)
        d.ellipse((230, 230, 282, 282), fill="#F2B632")
        im.save(os.path.join(DIST, "assets/logo.png"))
        # og 1200x630
        og = Image.new("RGB", (1200, 630), "#152029"); d = ImageDraw.Draw(og)
        d.rectangle((0, 0, 1200, 630), fill="#152029")
        d.ellipse((80, 175, 360, 455), fill="#0B6E4F"); d.ellipse((120, 215, 320, 415), fill="#FFFFFF")
        d.line((220, 250, 220, 315), fill="#152029", width=16); d.line((220, 315, 270, 347), fill="#152029", width=16)
        d.ellipse((206, 301, 234, 329), fill="#F2B632")
        try:
            f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
            f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
        except Exception:
            f1 = f2 = ImageFont.load_default()
        d.text((420, 215), "Stundenrechnen", font=f1, fill="#FFFFFF")
        d.text((420, 315), "Arbeitszeit · Stunden · Tage · Überstunden", font=f2, fill="#F2B632")
        d.text((420, 365), "Kostenlose Rechner – direkt im Browser", font=f2, fill="#C9D1CC")
        og.save(os.path.join(DIST, "assets/og.png"), optimize=True)
    except Exception as e:
        print("PIL assets skipped:", e)
    print(f"Built {len(ALL)+1} pages → {DIST}")


if __name__ == "__main__":
    main()
