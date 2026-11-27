import re
import json
import subprocess
import sys
import unicodedata
import urllib.parse

for paquet in ["cloudscraper", "beautifulsoup4", "playwright"]:
    try:
        __import__(paquet if paquet != "beautifulsoup4" else "bs4")
    except ImportError:
        print(f"Instal·lant {paquet} automàticament...", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", paquet])

import cloudscraper
from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_DISPONIBLE = True
except Exception:
    PLAYWRIGHT_DISPONIBLE = False

# ==============================================================================
# 1. LLISTA DE PÀGINES D'ON EXTREURE TOTS ELS PDFs
# Format de cada entrada: (via, assignatura_o_AUTO, url)
# ==============================================================================
SLUGS_SELECAT = [
    "matematiques", "matematiques-aplicades-a-les-ciencies-socials", "biologia", "quimica", "fisica",
    "llengua-catalana-i-literatura", "llengua-castellana-i-literatura", "angles", "frances", "alemany",
    "historia", "historia-de-la-filosofia", "historia-de-lart", "geografia", "economia-de-lempresa",
    "empresa-i-disseny-de-models-de-negoci", "dibuix-tecnic", "dibuix-artistic", "tecnologia-industrial",
    "tecnologia-i-enginyeria", "ciencies-de-la-terra-i-del-medi-ambient", "electrotecnia", "llati", "grec",
    "disseny", "fonaments-de-les-arts", "cultura-audiovisual", "arts-esceniques", "analisi-musical",
    "literatura-castellana", "literatura-catalana"
]

LLISTA_URLS = [
    # 1. PAU Catalunya (Web oficial Canal Universitats Gencat)
    ("pau", "AUTO", "https://universitats.gencat.cat/ca/pau/models-examen-anys-anteriors/"),

    # 2. PAU Majors de 25 anys (Xelu HTML directe)
    ("m25", "AUTO", "https://www.xelu.net/materials/examens-de-les-proves-d-acces-per-a-majors-de-25-anys-a-la-universitat-27"),

    # 3. Cicles Formatius de Grau Superior (Selecat Cicles + Xelu HTML)
    ("gs",  "AUTO", "https://www.selecat.cat/cicles/"),
    *[("gs", "AUTO", f"https://www.selecat.cat/cicles/{slug}/") for slug in SLUGS_SELECAT],
    ("gs",  "AUTO", "https://www.xelu.net/materials/examens-de-les-proves-d-acces-a-cicles-formatius-de-grau-superior-25"),

    # 4. Cicles Formatius de Grau Mitjà (Xelu HTML directe)
    ("gm",  "AUTO", "https://www.xelu.net/materials/examens-de-les-proves-d-acces-a-cicles-formatius-de-grau-mitja-24"),
]

# ==============================================================================
# 2. DICCIONARI D'EQUIVALÈNCIES (CATALÀ + CASTELLÀ -> NOM OFICIAL UNIFICAT)
# ==============================================================================
MATERIES_OFICIALS = [
    ("matematiques aplicades", "Matemàtiques Aplicades a les Ciències Socials", "fa-chart-line"),
    ("matematicas aplicadas",  "Matemàtiques Aplicades a les Ciències Socials", "fa-chart-line"),
    ("ciencias sociales",      "Matemàtiques Aplicades a les Ciències Socials", "fa-chart-line"),
    ("ciencies socials",       "Matemàtiques Aplicades a les Ciències Socials", "fa-chart-line"),
    ("ccss",                   "Matemàtiques Aplicades a les Ciències Socials", "fa-chart-line"),
    ("matematiques",           "Matemàtiques", "fa-square-root-variable"),
    ("matematicas",            "Matemàtiques", "fa-square-root-variable"),
    ("matematica",             "Matemàtiques", "fa-square-root-variable"),
    ("llengua catalana",        "Llengua Catalana i Literatura", "fa-book-open"),
    ("lengua catalana",        "Llengua Catalana i Literatura", "fa-book-open"),
    ("catala",                 "Llengua Catalana i Literatura", "fa-book-open"),
    ("llengua castellana",      "Llengua Castellana i Literatura", "fa-feather-pointed"),
    ("lengua castellana",      "Llengua Castellana i Literatura", "fa-feather-pointed"),
    ("castella",               "Llengua Castellana i Literatura", "fa-feather-pointed"),
    ("angles",                 "Anglès", "fa-language"),
    ("ingles",                 "Anglès", "fa-language"),
    ("frances",                "Francès", "fa-language"),
    ("alemany",                "Alemany", "fa-language"),
    ("aleman",                 "Alemany", "fa-language"),
    ("italia",                 "Italià", "fa-language"),
    ("italiano",               "Italià", "fa-language"),
    ("historia de la filosofia","Història de la Filosofia", "fa-brain"),
    ("filosofia",              "Història de la Filosofia", "fa-brain"),
    ("historia de l art",      "Història de l'Art", "fa-palette"),
    ("historia del arte",      "Història de l'Art", "fa-palette"),
    ("historia de espana",     "Història d'Espanya", "fa-landmark"),
    ("historia d espanya",     "Història d'Espanya", "fa-landmark"),
    ("historia",               "Història", "fa-landmark"),
    ("biologia",               "Biologia", "fa-dna"),
    ("quimica",                "Química", "fa-flask"),
    ("fisica",                 "Física", "fa-atom"),
    ("empresa i disseny",      "Empresa i Disseny de Models de Negoci", "fa-briefcase"),
    ("empresa y diseno",       "Empresa i Disseny de Models de Negoci", "fa-briefcase"),
    ("economia de l empresa",  "Economia de l'Empresa", "fa-briefcase"),
    ("economia de la empresa", "Economia de l'Empresa", "fa-briefcase"),
    ("economia",               "Economia", "fa-coins"),
    ("geografia",              "Geografia", "fa-earth-europe"),
    ("dibuix tecnic",          "Dibuix Tècnic", "fa-compass-drafting"),
    ("dibujo tecnico",         "Dibuix Tècnic", "fa-compass-drafting"),
    ("dibuix artistic",        "Dibuix Artístic", "fa-paintbrush"),
    ("dibujo artistico",       "Dibuix Artístic", "fa-paintbrush"),
    ("tecnologia",             "Tecnologia i Enginyeria", "fa-gears"),
    ("enginyeria",             "Tecnologia i Enginyeria", "fa-gears"),
    ("ingenieria",             "Tecnologia i Enginyeria", "fa-gears"),
    ("ciencies de la terra",   "Ciències de la Terra i del Medi Ambient", "fa-leaf"),
    ("ciencias de la tierra",  "Ciències de la Terra i del Medi Ambient", "fa-leaf"),
    ("ciencies generals",      "Ciències Generals", "fa-microscope"),
    ("ciencias generales",     "Ciències Generals", "fa-microscope"),
    ("electrotecnia",          "Electrotècnia", "fa-bolt"),
    ("llati",                  "Llatí", "fa-scroll"),
    ("latin",                  "Llatí", "fa-scroll"),
    ("grec",                   "Grec", "fa-columns"),
    ("griego",                 "Grec", "fa-columns"),
    ("disseny",                "Disseny", "fa-pen-nib"),
    ("diseno",                 "Disseny", "fa-pen-nib"),
    ("fonaments",              "Fonaments Artístics", "fa-masks-theater"),
    ("fundamentos",            "Fonaments Artístics", "fa-masks-theater"),
    ("cultura audiovisual",    "Cultura Audiovisual", "fa-film"),
    ("arts esceniques",        "Arts Escèniques", "fa-masks-theater"),
    ("artes escenicas",        "Arts Escèniques", "fa-masks-theater"),
    ("analisi musical",        "Anàlisi Musical", "fa-music"),
    ("analisis musical",       "Anàlisi Musical", "fa-music"),
    ("literatura",             "Literatura", "fa-book"),
    ("geologia",               "Geologia i Ciències Ambientals", "fa-mountain"),
    ("psicologia",             "Psicologia", "fa-head-side-virus"),
    ("sociologia",             "Sociologia", "fa-users"),
]

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
_pw_instance = None
_browser_instance = None
_page_instance = None

def iniciar_navegador():
    global _pw_instance, _browser_instance, _page_instance, PLAYWRIGHT_DISPONIBLE
    if not PLAYWRIGHT_DISPONIBLE or _page_instance is not None:
        return
    try:
        _pw_instance = sync_playwright().start()
        _browser_instance = _pw_instance.chromium.launch(headless=True)
        _page_instance = _browser_instance.new_page()
    except Exception:
        print("   [Info] Instal·lant navegador Chromium per a Selecat (només el primer cop)...", flush=True)
        try:
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
            _pw_instance = sync_playwright().start()
            _browser_instance = _pw_instance.chromium.launch(headless=True)
            _page_instance = _browser_instance.new_page()
        except Exception as e:
            print(f"   [Avís] No s'ha pogut iniciar Chromium, fent servir mode estàndard: {e}", flush=True)
            PLAYWRIGHT_DISPONIBLE = False

def tancar_navegador():
    global _pw_instance, _browser_instance, _page_instance
    try:
        if _browser_instance:
            _browser_instance.close()
        if _pw_instance:
            _pw_instance.stop()
    except Exception:
        pass
    _page_instance = None

# ==============================================================================
# 3. FUNCIONS D'EXTRACCIÓ, NETEJA I ESCRIPTURA DE DADES
# ==============================================================================
def domini_sense_www(url):
    return urllib.parse.urlparse(url).netloc.lower().replace("www.", "")

def normalitzar(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()

def detectar_materia(text_context):
    norm = normalitzar(text_context)
    for clau, nom_oficial, icona in MATERIES_OFICIALS:
        if clau in norm:
            return nom_oficial, icona
    return None, None

def detectar_any(text_context):
    coincidencies = re.findall(r"\b(199\d|20[0-2]\d)\b", text_context)
    if coincidencies:
        return int(coincidencies[0])
    curt = re.search(r"(?:pau|juny|set|ord|ext|mod|20)?[-_/]?([012]\d)(?!\d)", text_context.lower())
    if curt:
        val = int(curt.group(1))
        if 0 <= val <= 27:
            return 2000 + val
    return None

def detectar_etiqueta(text_context):
    t = normalitzar(text_context)
    parts = []
    if "juny" in t or "junio" in t:
        parts.append("Juny")
    elif "setembre" in t or "septiembre" in t:
        parts.append("Setembre")
    elif "juliol" in t or "julio" in t:
        parts.append("Juliol")

    if "extraordinar" in t:
        parts.append("Extraordinària")
    elif "ordinar" in t:
        parts.append("Ordinària")
    elif "model" in t:
        parts.append("Model / Mostra")

    serie = re.search(r"serie\s*([1-9a-z])", t)
    if serie:
        parts.append(f"Sèrie {serie.group(1).upper()}")

    return " · ".join(parts) if parts else "Convocatòria"

def es_document_valid(href, text_a):
    h = href.lower()
    t = normalitzar(text_a)
    if h.endswith(".pdf") or ".pdf?" in h:
        return True
    if "drive.google.com" in h or "docs.google.com" in h:
        return True
    if any(k in t for k in ["examen", "enunciat", "solucio", "solucion", "pautes", "criteris", "correccio", "model", "juny", "setembre", "ordinar", "extraordinar"]):
        if not any(x in h for x in ["#", "mailto:", "javascript:", "facebook", "twitter", "instagram"]):
            return True
    return False

def es_solucio(href, text_a):
    comb = normalitzar(f"{href} {text_a}")
    return any(k in comb for k in ["solucio", "solucion", "pautes", "criteris", "correccio", "resolt", "resuelto", "barem"])

def obtenir_html(url):
    dom = domini_sense_www(url)
    if "selecat.cat" in dom:
        iniciar_navegador()
        if _page_instance is not None:
            try:
                resp = _page_instance.goto(url, wait_until="domcontentloaded", timeout=20000)
                if resp and resp.status == 404:
                    return ""
                _page_instance.wait_for_timeout(1500)
                _page_instance.evaluate("""() => {
                    document.querySelectorAll('details, [aria-expanded="false"], .accordion, .elementor-tab-title').forEach(el => {
                        try { el.click(); } catch(e) {}
                    });
                }""")
                _page_instance.wait_for_timeout(600)
                return _page_instance.content()
            except Exception as e:
                print(f"   [Avís Playwright] {url}: {e}", flush=True)

    last_err = ""
    for _ in range(2):
        try:
            resp = scraper.get(url, timeout=35)
            if resp.status_code == 200:
                return resp.text
        except Exception as e_inner:
            last_err = e_inner
    if last_err:
        print(f"   [Avís] Error accedint a {url}: {last_err}", flush=True)
    return ""

def extreure_urls_sitemap(xml_text):
    return re.findall(r"<loc>\s*(https?://[^<\s]+)\s*</loc>", xml_text, flags=re.IGNORECASE)

def processar_font(via, materia_forzada, url_arrel):
    print(f"\n>>> Explorant [{via.upper()}] {url_arrel}", flush=True)
    visitades = set()
    cua = [(url_arrel, 0)]
    domini_base = domini_sense_www(url_arrel)
    resultats = []

    max_profunditat = 2 if "xelu.net" in domini_base else 3

    while cua:
        url_actual, nivell = cua.pop(0)
        if url_actual in visitades:
            continue
        visitades.add(url_actual)

        html = obtenir_html(url_actual)
        if not html:
            continue

        if url_actual.endswith(".xml") or "<urlset" in html[:500] or "<sitemapindex" in html[:500]:
            locs = extreure_urls_sitemap(html)
            print(f"   [Sitemap] Trobades {len(locs)} rutes dins {url_actual}", flush=True)
            for loc in locs:
                if loc not in visitades:
                    if via == "pau" and "/cicles" in loc.lower():
                        continue
                    if via == "gs" and "selecat" in domini_base and "/cicles" not in loc.lower() and not loc.endswith(".xml"):
                        continue
                    cua.append((loc, 1))
            continue

        soup = BeautifulSoup(html, "html.parser")
        titol_pag = urllib.parse.unquote(urllib.parse.urlparse(url_actual).path)
        if soup.title and soup.title.string:
            titol_pag += " " + soup.title.string
        h1_tag = soup.find(["h1", "h2"])
        if h1_tag:
            titol_pag += " " + h1_tag.get_text(" ", strip=True)
        materia_pagina, icona_pagina = detectar_materia(titol_pag)

        candidats = []
        for a in soup.find_all("a", href=True):
            candidats.append((a, a["href"].strip()))
        for el in soup.find_all(attrs={"data-href": True}):
            candidats.append((el, el["data-href"].strip()))
        for el in soup.find_all(attrs={"data-url": True}):
            candidats.append((el, el["data-url"].strip()))
        for el in soup.find_all(attrs={"onclick": True}):
            m_url = re.search(r"""['"](https?://[^'"]+(?:\.pdf|drive\.google\.com|docs\.google\.com)[^'"]*)['"]""", el["onclick"])
            if m_url:
                candidats.append((el, m_url.group(1).strip()))
        for ifr in soup.find_all("iframe", src=True):
            if "drive.google.com" in ifr["src"] or ".pdf" in ifr["src"]:
                candidats.append((ifr, ifr["src"].strip()))

        for el, href_raw in candidats:
            if not href_raw or href_raw.startswith(("#", "mailto:", "javascript:")):
                continue

            url_abs = urllib.parse.urljoin(url_actual, href_raw)
            text_a = el.get_text(" ", strip=True)
            title_attr = el.get("title", "") or el.get("aria-label", "")

            context_pare = ""
            tr = el.find_parent("tr")
            if tr:
                context_pare = tr.get_text(" ", strip=True)
            else:
                heading = el.find_previous(["h2", "h3", "h4", "strong", "b"])
                if heading:
                    context_pare = heading.get_text(" ", strip=True)

            context_complet = f"{titol_pag} {context_pare} {text_a} {title_attr} {urllib.parse.unquote(url_abs)}"

            if es_document_valid(url_abs, f"{text_a} {title_attr}"):
                if materia_forzada != "AUTO":
                    nom_mat, icona = materia_forzada, "fa-book"
                else:
                    nom_mat, icona = detectar_materia(f"{context_pare} {text_a} {title_attr} {urllib.parse.unquote(url_abs)}")
                    if not nom_mat and materia_pagina:
                        nom_mat, icona = materia_pagina, icona_pagina

                if nom_mat:
                    any_doc = detectar_any(context_complet) or 2025
                    etiqueta = detectar_etiqueta(f"{text_a} {title_attr} {context_pare}")
                    tipus = "solucio" if es_solucio(url_abs, f"{text_a} {title_attr}") else "examen"
                    resultats.append({
                        "via": via,
                        "materia": nom_mat,
                        "icona": icona,
                        "any": any_doc,
                        "etiqueta": etiqueta,
                        "tipus": tipus,
                        "url": url_abs
                    })
                continue

            if nivell < max_profunditat:
                parsed = urllib.parse.urlparse(url_abs)
                url_neta = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if domini_sense_www(url_abs) == domini_base and url_neta not in visitades:
                    if via == "gs" and "selecat" in domini_base and "/cicles" not in parsed.path.lower():
                        continue
                    if "xelu.net" in domini_base:
                        if "/materials/" not in parsed.path.lower() and "/materiales/" not in parsed.path.lower():
                            continue
                        if via == "gs" and "grau-superior" not in parsed.path.lower():
                            continue
                        if via == "gm" and "grau-mitja" not in parsed.path.lower():
                            continue
                        if via == "m25" and "majors-de-25" not in parsed.path.lower():
                            continue
                    if "universitats.gencat.cat" in domini_base:
                        if not parsed.path.lower().startswith("/ca/pau/"):
                            continue
                        if "models-examen" not in parsed.path.lower() and "examens" not in parsed.path.lower():
                            continue
                    if any(skip in parsed.path.lower() for skip in ["contact", "privac", "legal", "cookie", "wp-content", "feed", "tag", "author"]):
                        continue
                    cua.append((url_neta, nivell + 1))

    print(f"   + {len(resultats)} documents trobats a [{via.upper()}]", flush=True)
    return resultats

def guardar_js(tots_els_items, fitxer_sortida="dades_generades_2.js"):
    cataleg = {}

    for item in tots_els_items:
        mat = item["materia"]
        any_num = item["any"]
        via = item["via"]
        etiq = item["etiqueta"]
        tipus = item["tipus"]
        url = item["url"]

        if mat not in cataleg:
            cataleg[mat] = {
                "assignaturaNom": mat,
                "icona": item["icona"],
                "anys": {}
            }

        if any_num not in cataleg[mat]["anys"]:
            cataleg[mat]["anys"][any_num] = {
                "any": any_num,
                "pau": [], "m25": [], "gs": [], "gm": []
            }

        llista_via = cataleg[mat]["anys"][any_num][via]

        if any(x.get(tipus) == url for x in llista_via):
            continue

        existent = next((x for x in llista_via if x["etiqueta"] == etiq and x.get(tipus) is None), None)
        if existent:
            existent[tipus] = url
        else:
            nou = {"etiqueta": etiq, "examen": None, "solucio": None}
            nou[tipus] = url
            llista_via.append(nou)

    llista_final = []
    total_pdfs = 0
    for mat in sorted(cataleg.keys()):
        anys_ordenats = [cataleg[mat]["anys"][a] for a in sorted(cataleg[mat]["anys"].keys(), reverse=True)]
        for a in anys_ordenats:
            for v in ["pau", "m25", "gs", "gm"]:
                for doc in a[v]:
                    if doc["examen"]:
                        total_pdfs += 1
                    if doc["solucio"]:
                        total_pdfs += 1
        llista_final.append({
            "assignaturaNom": mat,
            "icona": cataleg[mat]["icona"],
            "anys": anys_ordenats
        })

    contingut_js = "// Fitxer generat automàticament per descarregar_examens.py\n"
    contingut_js += "const dadesMateries = " + json.dumps(llista_final, ensure_ascii=False, indent=2) + ";\n"

    with open(fitxer_sortida, "w", encoding="utf-8") as f:
        f.write(contingut_js)

    print(f"   [Guardat] '{fitxer_sortida}' actualitzat: {len(llista_final)} assignatures i {total_pdfs} PDFs.", flush=True)

if __name__ == "__main__":
    print("=== INICIANT RECULL D'EXÀMENS OFICIALS ===", flush=True)
    tots_documents = []

    try:
        for via, mat_forzada, url in LLISTA_URLS:
            docs = processar_font(via, mat_forzada, url)
            tots_documents.extend(docs)
            guardar_js(tots_documents)
    finally:
        tancar_navegador()

    print("\n=== PROCÉS 100% COMPLETAT! Ja pots obrir index.html ===", flush=True)