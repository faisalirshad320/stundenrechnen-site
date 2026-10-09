# -*- coding: utf-8 -*-
"""German public holidays per Bundesland (server-side pre-render). Mirrors ftDE() JS."""
import datetime as dt

LAENDER = [
    ("BW", "Baden-Württemberg", "baden-wuerttemberg"), ("BY", "Bayern", "bayern"), ("BE", "Berlin", "berlin"),
    ("BB", "Brandenburg", "brandenburg"), ("HB", "Bremen", "bremen"), ("HH", "Hamburg", "hamburg"),
    ("HE", "Hessen", "hessen"), ("MV", "Mecklenburg-Vorpommern", "mecklenburg-vorpommern"),
    ("NI", "Niedersachsen", "niedersachsen"), ("NW", "Nordrhein-Westfalen", "nrw"), ("RP", "Rheinland-Pfalz", "rheinland-pfalz"),
    ("SL", "Saarland", "saarland"), ("SN", "Sachsen", "sachsen"), ("ST", "Sachsen-Anhalt", "sachsen-anhalt"),
    ("SH", "Schleswig-Holstein", "schleswig-holstein"), ("TH", "Thüringen", "thueringen"),
]
LNAME = {c: n for c, n, _ in LAENDER}
WT = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

# holiday name -> states (None = bundesweit)
RULES = {
    "Heilige Drei Könige": ["BW", "BY", "ST"],
    "Internationaler Frauentag": ["BE", "MV"],
    "Ostersonntag": ["BB"], "Pfingstsonntag": ["BB"],
    "Fronleichnam": ["BW", "BY", "HE", "NW", "RP", "SL"],
    "Mariä Himmelfahrt": ["SL", "BY"],
    "Weltkindertag": ["TH"],
    "Reformationstag": ["BB", "HB", "HH", "MV", "NI", "SN", "ST", "SH", "TH"],
    "Allerheiligen": ["BW", "BY", "NW", "RP", "SL"],
    "Buß- und Bettag": ["SN"],
}


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return dt.date(y, (h + l - 7 * m + 114) // 31, ((h + l - 7 * m + 114) % 31) + 1)


def all_holidays(y):
    """list of (date, name, states or None)"""
    E = easter(y)
    td = dt.timedelta
    bb = dt.date(y, 11, 22)
    while bb.weekday() != 2:
        bb -= td(days=1)
    L = [(dt.date(y, 1, 1), "Neujahr"), (dt.date(y, 1, 6), "Heilige Drei Könige"), (dt.date(y, 3, 8), "Internationaler Frauentag"),
         (E - td(days=2), "Karfreitag"), (E, "Ostersonntag"), (E + td(days=1), "Ostermontag"), (dt.date(y, 5, 1), "Tag der Arbeit"),
         (E + td(days=39), "Christi Himmelfahrt"), (E + td(days=49), "Pfingstsonntag"), (E + td(days=50), "Pfingstmontag"),
         (E + td(days=60), "Fronleichnam"), (dt.date(y, 8, 15), "Mariä Himmelfahrt"), (dt.date(y, 9, 20), "Weltkindertag"),
         (dt.date(y, 10, 3), "Tag der Deutschen Einheit"), (dt.date(y, 10, 31), "Reformationstag"), (dt.date(y, 11, 1), "Allerheiligen"),
         (bb, "Buß- und Bettag"), (dt.date(y, 12, 25), "1. Weihnachtstag"), (dt.date(y, 12, 26), "2. Weihnachtstag")]
    return sorted((d, n, RULES.get(n)) for d, n in L)


def feiertage(y, land):
    return {d: n for d, n, s in all_holidays(y) if s is None or land in s}


def arbeitstage_monat(y, m, land):
    H = feiertage(y, land)
    d, n = dt.date(y, m, 1), 0
    while d.month == m:
        if d.weekday() < 5 and d not in H:
            n += 1
        d += dt.timedelta(days=1)
    return n


def arbeitstage_jahr(y, land):
    return sum(arbeitstage_monat(y, m, land) for m in range(1, 13))


def fmt(d):
    return f"{d.day:02d}.{d.month:02d}.{d.year}"


def _span(start, H, vac):
    def free(x):
        return x.weekday() >= 5 or x in H or x in vac
    a = b = start
    while free(a - dt.timedelta(days=1)):
        a -= dt.timedelta(days=1)
    while free(b + dt.timedelta(days=1)):
        b += dt.timedelta(days=1)
    return a, b


def brueckentage(y, land):
    """Return rows (holiday date, name, vac days list, span start, span end, free days) for weekday holidays."""
    H = {**feiertage(y - 1, land), **feiertage(y, land), **feiertage(y + 1, land)}
    rows, seen = [], set()
    for d, n in sorted(feiertage(y, land).items()):
        wd = d.weekday()
        if wd >= 5:
            continue
        opts = []
        if wd in (1, 3):
            opts.append([d - dt.timedelta(days=1) if wd == 1 else d + dt.timedelta(days=1)])
        elif wd == 2:
            opts.append([d + dt.timedelta(days=1), d + dt.timedelta(days=2)])
        elif wd in (0, 4):
            opts.append([])
        mon = d - dt.timedelta(days=wd)
        week = [mon + dt.timedelta(days=i) for i in range(5) if (mon + dt.timedelta(days=i)) not in H]
        opts.append(week)
        for v in opts:
            v = [x for x in v if x not in H and x.weekday() < 5]
            a, b = _span(d, H, set(v))
            if (a, b) in seen:
                continue
            seen.add((a, b))
            rows.append((d, n, v, a, b, (b - a).days + 1))
    return rows


def ft_js():
    return r"""
function easter(y){var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;return new Date(y,mo-1,da,12)}
function isoD(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())}
function ftDE(y,L){var o={},E=easter(y);function a(m,d,n){o[y+'-'+pad(m)+'-'+pad(d)]=n}function e(off,n){var d=new Date(E);d.setDate(d.getDate()+off);o[isoD(d)]=n}function in_(arr){return arr.indexOf(L)>=0}
a(1,1,'Neujahr');e(-2,'Karfreitag');e(1,'Ostermontag');a(5,1,'Tag der Arbeit');e(39,'Christi Himmelfahrt');e(50,'Pfingstmontag');a(10,3,'Tag der Deutschen Einheit');a(12,25,'1. Weihnachtstag');a(12,26,'2. Weihnachtstag');
if(in_(['BW','BY','ST']))a(1,6,'Heilige Drei Könige');if(in_(['BE','MV']))a(3,8,'Internationaler Frauentag');if(L==='BB'){e(0,'Ostersonntag');e(49,'Pfingstsonntag')}
if(in_(['BW','BY','HE','NW','RP','SL']))e(60,'Fronleichnam');if(in_(['SL','BY']))a(8,15,'Mariä Himmelfahrt');if(L==='TH')a(9,20,'Weltkindertag');
if(in_(['BB','HB','HH','MV','NI','SN','ST','SH','TH']))a(10,31,'Reformationstag');if(in_(['BW','BY','NW','RP','SL']))a(11,1,'Allerheiligen');
if(L==='SN'){var d=new Date(y,10,22,12);while(d.getDay()!==3)d.setDate(d.getDate()-1);o[isoD(d)]='Buß- und Bettag'}return o}
function atZaehlen(A,B,L,sa){var c=new Date(A),u=0,f=0,w=0,t=0,n=[],C={};while(c<=B){var y=c.getFullYear();if(!C[y])C[y]=ftDE(y,L);var k=isoD(c),dw=c.getDay(),we=dw===0||(dw===6&&!sa);t++;if(we)w++;else if(C[y][k]){f++;n.push(c.getDate()+'.'+(c.getMonth()+1)+'. '+C[y][k])}else u++;c.setDate(c.getDate()+1)}return{u:u,f:f,w:w,t:t,n:n}}
"""
