#!/usr/bin/env python3
"""
LegalTechOracle — Contract Lifecycle & Legal Compliance MCP v1.0.0
Port 12701 | Part of ToolOracle Whitelabel MCP Platform

Extends LawOracle (research/lookup) with CONTRACT OPERATIONS.
LawOracle = find law → LegalTechOracle = apply law to contracts.

12 Tools:
  ── Contract Generation ──
  1.  contract_draft       — Generate EU-compliant contract from parameters
  2.  nda_generate         — Instant NDA (mutual/unilateral, DE/EN)
  3.  freelancer_contract  — Scheinselbständigkeit-safe freelancer agreement
  4.  dpa_generate         — DSGVO Art.28 Data Processing Agreement

  ── Contract Analysis ──
  5.  clause_risk_scan     — AI-style red-flag clause detection
  6.  contract_summary     — Extract key terms from contract text
  7.  termination_analysis — Kündigungsklausel-Analyse

  ── Compliance Mapping ──
  8.  obligation_matrix    — Map contract to DORA/MiCA/NIS2 obligations
  9.  cross_jurisdiction   — Multi-jurisdiction clause comparison (DE/AT/CH/EU/UK/US)
 10.  regulatory_clause_check — Check if contract meets regulatory requirements
 11.  force_majeure_check  — Höhere Gewalt Klausel-Bewertung
 12.  liability_cap_check  — Haftungsbegrenzung Compliance Check

NO external APIs — legal knowledge engine + template generation.
"""
import os, sys, json, logging, re
from datetime import datetime, timezone, timedelta, date

sys.path.insert(0, "/root/whitelabel")
from shared.utils.mcp_base import WhitelabelMCPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [LegalTechOracle] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("/root/whitelabel/logs/legaltechoracle.log", mode="a")])
logger = logging.getLogger("LegalTechOracle")

PRODUCT_NAME = "LegalTechOracle"
VERSION = "1.0.0"
PORT_MCP = 12701
PORT_HEALTH = 12702

def ts(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

async def handle_contract_draft(args: dict) -> dict:
    """Generate EU-compliant contract from parameters."""
    contract_type = args.get("contract_type", "service")  # service, license, supply, consulting
    party_a = args.get("party_a_name", "")
    party_a_address = args.get("party_a_address", "")
    party_b = args.get("party_b_name", "")
    party_b_address = args.get("party_b_address", "")
    subject = args.get("subject", "")
    value_eur = args.get("value_eur", "")
    duration = args.get("duration", "12 Monate")
    governing_law = args.get("governing_law", "DE")
    language = args.get("language", "DE")

    today = datetime.now().strftime("%d.%m.%Y")

    clauses = {
        "§1 Vertragsgegenstand": f"Gegenstand dieses Vertrags ist: {subject or '[Leistungsbeschreibung einfügen]'}.",
        "§2 Vertragslaufzeit": f"Der Vertrag beginnt am {today} und läuft für {duration}. Er verlängert sich automatisch um jeweils 12 Monate, sofern er nicht mit einer Frist von 3 Monaten zum Laufzeitende gekündigt wird.",
        "§3 Vergütung": f"Die Vergütung beträgt {value_eur or '[Betrag]'} EUR zzgl. gesetzlicher USt. Zahlungsziel: 30 Tage netto.",
        "§4 Leistungspflichten": "Der Auftragnehmer erbringt die vereinbarten Leistungen mit der Sorgfalt eines ordentlichen Kaufmanns (§347 HGB).",
        "§5 Haftung": "Die Haftung richtet sich nach den gesetzlichen Bestimmungen. Die Haftung für leichte Fahrlässigkeit wird ausgeschlossen, soweit nicht Schäden aus der Verletzung des Lebens, des Körpers oder der Gesundheit betroffen sind. Die Haftung ist begrenzt auf den vorhersehbaren, vertragstypischen Schaden.",
        "§6 Vertraulichkeit": "Die Parteien verpflichten sich, alle im Rahmen dieses Vertrags erlangten vertraulichen Informationen geheim zu halten. Diese Pflicht besteht über die Beendigung des Vertrags hinaus für einen Zeitraum von 3 Jahren.",
        "§7 Datenschutz": "Soweit personenbezogene Daten verarbeitet werden, gelten die Bestimmungen der DSGVO. Bei Auftragsverarbeitung (Art. 28 DSGVO) ist ein gesonderter Auftragsverarbeitungsvertrag abzuschließen.",
        "§8 Höhere Gewalt": "Keine Partei haftet für die Nichterfüllung ihrer Pflichten, soweit diese durch höhere Gewalt verursacht wird (Naturkatastrophen, Pandemien, Krieg, behördliche Anordnungen). Die betroffene Partei hat die andere Partei unverzüglich zu informieren.",
        "§9 Kündigung": "Das Recht zur außerordentlichen Kündigung aus wichtigem Grund (§314 BGB) bleibt unberührt. Die Kündigung bedarf der Schriftform (§126 BGB).",
        "§10 Schlussbestimmungen": f"Es gilt das Recht der Bundesrepublik {'Deutschland' if governing_law == 'DE' else governing_law}. Gerichtsstand ist {'[Ort]'}. Änderungen dieses Vertrags bedürfen der Schriftform. Sollte eine Bestimmung unwirksam sein, bleibt der Vertrag im Übrigen wirksam (Salvatorische Klausel).",
    }

    contract_text = f"""VERTRAG

zwischen

{party_a or '[Vertragspartei A]'}
{party_a_address or '[Adresse A]'}
— nachfolgend „Auftraggeber" —

und

{party_b or '[Vertragspartei B]'}
{party_b_address or '[Adresse B]'}
— nachfolgend „Auftragnehmer" —

Datum: {today}

"""
    for title, content in clauses.items():
        contract_text += f"{title}\n{content}\n\n"

    contract_text += f"""
_______________________          _______________________
{party_a or 'Auftraggeber'}                  {party_b or 'Auftragnehmer'}
Ort, Datum                       Ort, Datum"""

    return {
        "contract_type": contract_type,
        "governing_law": governing_law,
        "clauses_count": len(clauses),
        "contract_text": contract_text,
        "mandatory_checks": [
            "AGB-Kontrolle: §305-310 BGB beachten (keine überraschenden Klauseln)",
            "Schriftformerfordernis: §126 BGB für Kündigungen/Änderungen",
            "DSGVO: Art.28 AVV erforderlich bei Datenverarbeitung",
            "Handelsrecht: §347 HGB Sorgfaltspflicht bei Kaufleuten",
        ],
        "disclaimer": "Vertragsentwurf — keine Rechtsberatung. Anwaltliche Prüfung empfohlen.",
        "retrieved_at": ts(),
    }

async def handle_nda_generate(args: dict) -> dict:
    """Instant NDA generation."""
    nda_type = args.get("type", "mutual")  # mutual | unilateral
    discloser = args.get("discloser", "")
    recipient = args.get("recipient", "")
    purpose = args.get("purpose", "Bewertung einer möglichen Geschäftsbeziehung")
    duration_years = int(args.get("duration_years", 3))
    language = args.get("language", "DE")
    governing_law = args.get("governing_law", "DE")
    penalty_eur = args.get("penalty_eur", "")

    today = datetime.now().strftime("%d.%m.%Y")

    if nda_type == "mutual":
        parties_desc = "Beide Parteien können vertrauliche Informationen austauschen."
    else:
        parties_desc = f"{discloser or 'Der Offenleger'} gibt vertrauliche Informationen an {recipient or 'den Empfänger'} weiter."

    nda_text = f"""GEHEIMHALTUNGSVEREINBARUNG (NDA)
{'Gegenseitige' if nda_type == 'mutual' else 'Einseitige'} Vertraulichkeitsvereinbarung

Datum: {today}

Parteien:
Partei A: {discloser or '[Name/Firma A]'}
Partei B: {recipient or '[Name/Firma B]'}

§1 Zweck
{parties_desc}
Zweck: {purpose}

§2 Vertrauliche Informationen
Als vertraulich gelten alle Informationen, die als solche gekennzeichnet sind oder deren Vertraulichkeit sich aus den Umständen ergibt, einschließlich: Geschäftsgeheimnisse, technisches Know-how, Kundendaten, Finanzdaten, Strategien, Software, Prototypen.

§3 Pflichten
Die empfangende Partei verpflichtet sich:
a) Vertrauliche Informationen nur für den vereinbarten Zweck zu verwenden
b) Vertrauliche Informationen nicht an Dritte weiterzugeben
c) Vertrauliche Informationen mit mindestens derselben Sorgfalt zu schützen wie eigene
d) Den Zugang auf Mitarbeiter zu beschränken, die diese für den Zweck benötigen

§4 Ausnahmen
Keine Vertraulichkeit besteht für Informationen, die:
a) Zum Zeitpunkt der Offenlegung bereits öffentlich bekannt waren
b) Ohne Verschulden der empfangenden Partei öffentlich werden
c) Der empfangenden Partei bereits rechtmäßig bekannt waren
d) Von einem Dritten ohne Vertraulichkeitspflicht erhalten wurden
e) Von der empfangenden Partei unabhängig entwickelt wurden

§5 Laufzeit
Diese Vereinbarung gilt für {duration_years} Jahre ab Unterzeichnung. Die Geheimhaltungspflicht überlebt die Beendigung um weitere {duration_years} Jahre.

§6 Rückgabe
Nach Beendigung sind alle vertraulichen Informationen zurückzugeben oder nachweislich zu vernichten.

{"§7 Vertragsstrafe" + chr(10) + f"Bei Verstoß wird eine Vertragsstrafe in Höhe von {penalty_eur} EUR vereinbart (§339 BGB)." if penalty_eur else ""}

§{'8' if penalty_eur else '7'} GeschGehG
Diese Vereinbarung ergänzt den Schutz nach dem Geschäftsgeheimnisgesetz (GeschGehG). Verstöße können nach §§23 GeschGehG strafbar sein.

§{'9' if penalty_eur else '8'} Schlussbestimmungen
Gerichtsstand: [Ort]. Anwendbares Recht: Recht der Bundesrepublik {'Deutschland' if governing_law == 'DE' else governing_law}.
Änderungen bedürfen der Schriftform.
"""

    return {
        "nda_type": nda_type, "duration_years": duration_years,
        "nda_text": nda_text,
        "legal_references": ["GeschGehG (Geschäftsgeheimnisgesetz)", "§§311 Abs.2, 241 Abs.2 BGB (vorvertragliche Pflichten)",
                             "EU Trade Secrets Directive 2016/943"],
        "tips": [
            "Vertragsstrafe: In DE wirksam, aber nicht unangemessen hoch (§343 BGB)",
            "Einseitige NDAs: Empfänger hat weniger Schutz — mutual bevorzugen",
            "GeschGehG: Seit 2019 ersetzt §17 UWG — angemessene Schutzmaßnahmen erforderlich",
        ],
        "disclaimer": "Muster-NDA — anwaltliche Prüfung empfohlen.",
        "retrieved_at": ts(),
    }

async def handle_freelancer_contract(args: dict) -> dict:
    """Scheinselbständigkeit-safe freelancer agreement."""
    freelancer_name = args.get("freelancer_name", "")
    client_name = args.get("client_name", "")
    project = args.get("project_description", "")
    hourly_rate = args.get("hourly_rate", "")
    project_fee = args.get("project_fee", "")

    scheinselbstaendigkeit_checks = [
        {"criterion": "Weisungsfreiheit", "required": True, "clause": "Der Auftragnehmer ist in der Gestaltung seiner Tätigkeit frei und unterliegt keinen Weisungen hinsichtlich Ort, Zeit und Art der Ausführung."},
        {"criterion": "Eigene Betriebsmittel", "required": True, "clause": "Der Auftragnehmer setzt eigene Betriebsmittel (Hard-/Software, Büro) ein."},
        {"criterion": "Eigene Kunden", "required": True, "clause": "Der Auftragnehmer ist berechtigt, für andere Auftraggeber tätig zu sein."},
        {"criterion": "Keine Eingliederung", "required": True, "clause": "Der Auftragnehmer ist nicht in die betriebliche Organisation des Auftraggebers eingegliedert."},
        {"criterion": "Unternehmerisches Risiko", "required": True, "clause": "Der Auftragnehmer trägt das unternehmerische Risiko und haftet für die vertragsgemäße Erbringung."},
        {"criterion": "Keine festen Arbeitszeiten", "required": True, "clause": "Der Auftragnehmer bestimmt seine Arbeitszeiten selbst."},
        {"criterion": "Vertretungsbefugnis", "required": True, "clause": "Der Auftragnehmer ist berechtigt, die Leistung durch qualifizierte Dritte erbringen zu lassen."},
        {"criterion": "Eigene Rechnungsstellung", "required": True, "clause": "Der Auftragnehmer stellt Rechnungen mit gesondertem USt-Ausweis."},
    ]

    return {
        "freelancer": freelancer_name, "client": client_name,
        "scheinselbstaendigkeit_protection": scheinselbstaendigkeit_checks,
        "mandatory_clauses": [c["clause"] for c in scheinselbstaendigkeit_checks],
        "red_flags_to_avoid": [
            "Feste Arbeitszeiten vorschreiben → Indiz für Scheinselbständigkeit",
            "Nur einen Auftraggeber → §7 Abs.1 SGB IV",
            "Firmen-E-Mail/Visitenkarten → Eingliederung in Organisation",
            "Urlaubsanspruch/Entgeltfortzahlung → Arbeitnehmermerkmal",
            "Stundenlohn statt Projektpauschale → Indiz (aber allein nicht ausreichend)",
        ],
        "konsequenzen_scheinselbstaendigkeit": {
            "sv_nachzahlung": "Bis 4 Jahre rückwirkend SV-Beiträge (AG + AN-Anteil!)",
            "steuern": "Lohnsteuernachzahlung + Säumniszuschläge",
            "strafrechtlich": "§266a StGB: Vorenthalten von Arbeitsentgelt (bis 5 Jahre Freiheitsstrafe)",
            "statusfeststellung": "DRV-Statusfeststellungsverfahren (§7a SGB IV) empfohlen",
        },
        "legal_basis": "§7 SGB IV, §611a BGB, BSG-Rechtsprechung zur Scheinselbständigkeit",
        "disclaimer": "Prüfung im Einzelfall durch Fachanwalt für Arbeitsrecht empfohlen.",
        "retrieved_at": ts(),
    }

async def handle_dpa_generate(args: dict) -> dict:
    """DSGVO Art.28 Data Processing Agreement."""
    controller = args.get("controller_name", "")
    processor = args.get("processor_name", "")
    data_types = args.get("data_types", "Kundendaten, E-Mail-Adressen, Nutzungsdaten")
    data_subjects = args.get("data_subjects", "Kunden, Mitarbeiter, Website-Besucher")
    processing_purpose = args.get("purpose", "")
    sub_processors = args.get("sub_processors", [])
    third_country = args.get("third_country_transfer", False)

    mandatory_art28 = [
        {"clause": "Gegenstand und Dauer der Verarbeitung", "article": "Art.28(3)"},
        {"clause": "Art und Zweck der Verarbeitung", "article": "Art.28(3)"},
        {"clause": "Art der personenbezogenen Daten", "article": "Art.28(3)", "content": data_types},
        {"clause": "Kategorien betroffener Personen", "article": "Art.28(3)", "content": data_subjects},
        {"clause": "Weisungsgebundenheit des Auftragsverarbeiters", "article": "Art.28(3)(a)"},
        {"clause": "Vertraulichkeitsverpflichtung", "article": "Art.28(3)(b)"},
        {"clause": "Technische und organisatorische Maßnahmen (TOMs)", "article": "Art.28(3)(c) + Art.32"},
        {"clause": "Unterauftragsverarbeiter (Genehmigungspflicht)", "article": "Art.28(2)(3)(d)"},
        {"clause": "Unterstützung bei Betroffenenrechten", "article": "Art.28(3)(e)"},
        {"clause": "Unterstützung bei DPIA und Meldepflichten", "article": "Art.28(3)(f)"},
        {"clause": "Löschung/Rückgabe nach Beendigung", "article": "Art.28(3)(g)"},
        {"clause": "Prüf- und Kontrollrechte des Verantwortlichen", "article": "Art.28(3)(h)"},
    ]

    toms = [
        "Pseudonymisierung und Verschlüsselung (Art.32(1)(a))",
        "Vertraulichkeit, Integrität, Verfügbarkeit (Art.32(1)(b))",
        "Wiederherstellbarkeit (Art.32(1)(c))",
        "Regelmäßige Überprüfung (Art.32(1)(d))",
        "Zutrittskontrolle, Zugangskontrolle, Zugriffskontrolle",
        "Weitergabekontrolle, Eingabekontrolle",
        "Auftragskontrolle, Verfügbarkeitskontrolle",
        "Trennungsgebot",
    ]

    return {
        "controller": controller, "processor": processor,
        "mandatory_clauses_art28": mandatory_art28,
        "required_toms": toms,
        "sub_processors": sub_processors if sub_processors else "Keine (oder: Liste der genehmigten Unterauftragsverarbeiter beifügen)",
        "third_country_transfer": {
            "applicable": third_country,
            "requirements": [
                "Angemessenheitsbeschluss (Art.45 DSGVO) — aktuell: CH, JP, KR, UK, CA, IL, NZ, US (DPF)",
                "Standardvertragsklauseln (SCCs) nach Durchführungsbeschluss 2021/914",
                "Transfer Impact Assessment (TIA) erforderlich",
                "Binding Corporate Rules (BCRs) als Alternative",
            ] if third_country else ["Kein Drittlandtransfer — keine zusätzlichen Maßnahmen erforderlich"],
        },
        "bussgelder": "Verstoß gegen Art.28: bis zu €10M oder 2% des Jahresumsatzes (Art.83(4)(a) DSGVO)",
        "legal_basis": "DSGVO Art.28, Art.32; BDSG §62",
        "disclaimer": "AVV-Entwurf — Datenschutzbeauftragter sollte prüfen.",
        "retrieved_at": ts(),
    }

async def handle_clause_risk(args: dict) -> dict:
    """Red-flag clause detection in contract text."""
    text = args.get("contract_text", "")
    if len(text) < 50:
        return {"error": "Provide 'contract_text' with at least 50 characters"}

    text_lower = text.lower()
    red_flags = []
    yellow_flags = []
    green_flags = []

    # Red flags
    patterns_red = [
        (r'unbeschränkt(?:e)?\s+haftung|unlimited\s+liability', "Unbeschränkte Haftung", "Haftungsbegrenzung fehlt — existenzbedrohend"),
        (r'einseitig(?:es)?\s+änderungsrecht|right\s+to\s+modify\s+unilateral', "Einseitiges Änderungsrecht", "§308 Nr.4 BGB — AGB-widrig"),
        (r'automatische?\s+verlängerung.*ohne.*kündigung', "Automatische Verlängerung ohne Kündigung", "Kann zur ungewollten Langzeitbindung führen"),
        (r'verzicht\s+auf\s+(?:alle\s+)?ansprüche|waiver\s+of\s+all\s+claims', "Globalverzicht", "Möglicherweise unwirksam nach §307 BGB"),
        (r'(?:vertragsstrafe|penalty).*(?:unangemessen|excessive|unlimited)', "Unangemessene Vertragsstrafe", "§343 BGB — richterliche Herabsetzung möglich"),
        (r'gerichtsstand\s+(?:im\s+ausland|abroad|foreign)', "Ausländischer Gerichtsstand", "Erschwert Rechtsdurchsetzung erheblich"),
    ]

    patterns_yellow = [
        (r'salvatorische\s+klausel', "Salvatorische Klausel", "Vorhanden — gut, aber kein Allheilmittel"),
        (r'schriftform(?:erfordernis)?|schriftlich', "Schriftformklausel", "Gut — verhindert mündliche Änderungen"),
        (r'höhere\s+gewalt|force\s+majeure', "Force-Majeure-Klausel", "Vorhanden — prüfen ob Pandemie explizit erwähnt"),
        (r'konkurrenzverbot|wettbewerbsverbot|non-?compete', "Wettbewerbsverbot", "Prüfen: Max. 2 Jahre, Karenzentschädigung (§74 HGB)?"),
    ]

    patterns_green = [
        (r'dsgvo|gdpr|datenschutz|data\s+protection', "Datenschutz-Klausel", "DSGVO-Bezug vorhanden"),
        (r'vertraulichkeit|geheimhaltung|confidential', "Vertraulichkeitsklausel", "NDA-Elemente enthalten"),
        (r'haftungsbegrenzung|liability\s+cap|begrenz', "Haftungsbegrenzung", "Haftung ist begrenzt — gut"),
    ]

    for pattern, name, note in patterns_red:
        if re.search(pattern, text_lower):
            red_flags.append({"flag": name, "severity": "RED", "note": note})

    for pattern, name, note in patterns_yellow:
        if re.search(pattern, text_lower):
            yellow_flags.append({"flag": name, "severity": "YELLOW", "note": note})

    for pattern, name, note in patterns_green:
        if re.search(pattern, text_lower):
            green_flags.append({"flag": name, "severity": "GREEN", "note": note})

    risk_score = len(red_flags) * 30 + len(yellow_flags) * 10
    risk_score = min(100, risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": "CRITICAL" if risk_score >= 60 else "HIGH" if risk_score >= 40 else "MEDIUM" if risk_score >= 20 else "LOW",
        "red_flags": red_flags, "yellow_flags": yellow_flags, "green_flags": green_flags,
        "stats": {"red": len(red_flags), "yellow": len(yellow_flags), "green": len(green_flags)},
        "text_length": len(text),
        "agb_check": "§§305-310 BGB AGB-Kontrolle beachten — insbesondere bei Formularverträgen",
        "disclaimer": "Automatische Musterprüfung — ersetzt keine anwaltliche Vertragsprüfung.",
        "retrieved_at": ts(),
    }

async def handle_contract_summary(args: dict) -> dict:
    """Extract key terms from contract text."""
    text = args.get("contract_text", "")
    if len(text) < 50:
        return {"error": "Provide 'contract_text'"}

    extracted = {}
    patterns = {
        "laufzeit": [r'(?:laufzeit|dauer|term)[:\s]+([^\n.]{5,80})', r'(?:beginnt am|wirksam ab)[:\s]+(\d{1,2}[./]\d{1,2}[./]\d{2,4})'],
        "kuendigungsfrist": [r'(?:kündigungsfrist|notice\s+period)[:\s]+([^\n.]{5,60})'],
        "verguetung": [r'(?:vergütung|entgelt|honorar|preis|fee)[:\s]+([^\n.]{5,80})', r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s*(?:EUR|€|USD|\$))'],
        "haftung": [r'(?:haftung|liability)[:\s]+([^\n.]{10,120})'],
        "gerichtsstand": [r'(?:gerichtsstand|jurisdiction|zuständig)[:\s]+([^\n.]{5,60})'],
        "anwendbares_recht": [r'(?:anwendbares?\s+recht|applicable\s+law|recht\s+(?:der|von))[:\s]+([^\n.]{5,60})'],
        "vertraulichkeit": [r'(?:vertraulichkeit|geheimhaltung|confidential)[:\s]+([^\n.]{10,120})'],
    }

    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                extracted[field] = m.group(1).strip()
                break

    return {
        "extracted_terms": extracted,
        "fields_found": len(extracted),
        "text_length": len(text),
        "note": "Regex-basierte Extraktion — prüfen Sie die Ergebnisse gegen das Original",
        "retrieved_at": ts(),
    }

async def handle_termination(args: dict) -> dict:
    """Kündigungsklausel-Analyse."""
    contract_type = args.get("contract_type", "dienstvertrag")
    duration_type = args.get("duration_type", "unbefristet")
    notice_period = args.get("notice_period_months", 0)
    auto_renewal = args.get("auto_renewal", False)

    analysis = {"contract_type": contract_type, "duration_type": duration_type}

    if duration_type == "befristet":
        analysis["ordentliche_kuendigung"] = "Grundsätzlich ausgeschlossen bei befristeten Verträgen (§620 Abs.1 BGB), sofern nicht vertraglich vereinbart"
    else:
        analysis["ordentliche_kuendigung"] = "Möglich mit vereinbarter oder gesetzlicher Frist"

    analysis["ausserordentliche_kuendigung"] = "Immer möglich aus wichtigem Grund (§314 BGB) — kann vertraglich nicht ausgeschlossen werden"
    analysis["notice_period_assessment"] = "Angemessen" if notice_period <= 6 else "Sehr lang — prüfen ob AGB-widrig (§307 BGB)"

    if auto_renewal:
        analysis["auto_renewal_warning"] = "§309 Nr.9 BGB: Verlängerung max. 1 Jahr, Kündigungsfrist max. 3 Monate (bei AGB)"

    analysis["formerfordernis"] = "Schriftform empfohlen (§126 BGB). Arbeitsverträge: Schriftform zwingend für Kündigung (§623 BGB)"
    analysis["legal_basis"] = "§§314, 620-628 BGB, §§543, 580a BGB (Miete), §§621-623 BGB (Dienst), §89 HGB (Handelsvertreter)"
    analysis["retrieved_at"] = ts()
    return analysis

async def handle_obligation_matrix(args: dict) -> dict:
    """Map contract clauses to regulatory obligations."""
    regulations = args.get("regulations", ["DORA", "MiCA", "NIS2"])
    if isinstance(regulations, str):
        regulations = [r.strip() for r in regulations.split(",")]

    matrix = {}
    if "DORA" in regulations:
        matrix["DORA"] = [
            {"article": "Art.28", "topic": "Third-party ICT risk", "contract_requirement": "Exit strategy, audit rights, sub-contracting restrictions, performance targets"},
            {"article": "Art.30", "topic": "Key contractual provisions", "contract_requirement": "SLAs, data location, incident notification, BCP provisions, termination rights"},
            {"article": "Art.31", "topic": "CTPP designation", "contract_requirement": "Oversight framework compliance if provider is designated critical"},
        ]
    if "MiCA" in regulations:
        matrix["MiCA"] = [
            {"article": "Art.60", "topic": "Outsourcing by token issuers", "contract_requirement": "Risk management, audit rights, regulatory notification"},
            {"article": "Art.66", "topic": "Custody agreements", "contract_requirement": "Segregation of assets, liability, insurance"},
        ]
    if "NIS2" in regulations:
        matrix["NIS2"] = [
            {"article": "Art.21(2)(d)", "topic": "Supply chain security", "contract_requirement": "Security requirements for suppliers, vulnerability handling agreements"},
        ]
    if "GDPR" in regulations or "DSGVO" in regulations:
        matrix["GDPR"] = [
            {"article": "Art.28", "topic": "Data processing agreements", "contract_requirement": "AVV mit allen Pflichtangaben, TOMs, Unterauftragnehmer"},
        ]

    return {
        "regulations_checked": regulations,
        "obligation_matrix": matrix,
        "total_requirements": sum(len(v) for v in matrix.values()),
        "recommendation": "Jede Vertragsklausel gegen die relevanten Artikel prüfen — Compliance-Lücken dokumentieren",
        "retrieved_at": ts(),
    }

async def handle_cross_jurisdiction(args: dict) -> dict:
    """Multi-jurisdiction clause comparison."""
    clause_type = args.get("clause_type", "limitation_of_liability")
    jurisdictions = args.get("jurisdictions", ["DE", "AT", "CH", "UK", "US"])

    comparisons = {
        "limitation_of_liability": {
            "DE": {"rule": "§276 Abs.3 BGB: Haftung für Vorsatz kann nicht ausgeschlossen werden. §309 Nr.7 BGB: Haftung für Leben/Körper/Gesundheit nie ausschließbar in AGB."},
            "AT": {"rule": "§879 ABGB: Sittenwidrige Haftungsausschlüsse sind nichtig. Grobes Verschulden nicht ausschließbar."},
            "CH": {"rule": "Art.100 OR: Haftung für absichtliche Schädigung nicht ausschließbar. Große Vertragsfreiheit."},
            "UK": {"rule": "UCTA 1977: Unreasonable exclusions void. Negligence causing death/injury: always void."},
            "US": {"rule": "State-by-state. UCC §2-719: Unconscionable limitations void. Personal injury caps vary."},
        },
        "non_compete": {
            "DE": {"rule": "§74-75 HGB: Max. 2 Jahre, Karenzentschädigung mind. 50% der letzten Vergütung."},
            "AT": {"rule": "§36 AngG: Max. 1 Jahr, unwirksam bei Arbeitgeberkündigung ohne Grund."},
            "CH": {"rule": "Art.340-340c OR: Max. 3 Jahre, örtlich und sachlich beschränkt."},
            "UK": {"rule": "Common law restraint of trade: Must be reasonable in scope, duration, geography."},
            "US": {"rule": "State-specific. CA: Generally void (§16600 BPC). NY/TX: Enforceable if reasonable. FTC proposed ban (2024)."},
        },
        "force_majeure": {
            "DE": {"rule": "Kein gesetzliches Force-Majeure-Recht. §275 BGB (Unmöglichkeit) + §313 BGB (Störung der Geschäftsgrundlage). Vertragliche Regelung essenziell."},
            "AT": {"rule": "Ähnlich DE. §1447 ABGB bei Unmöglichkeit. Vertragsanpassung bei Wegfall der Geschäftsgrundlage."},
            "CH": {"rule": "Art.119 OR: Unmöglichkeit befreit. Art.97 OR: Nicht-Verschulden als Entschuldigung."},
            "UK": {"rule": "Doctrine of frustration (narrow). Contractual FM clauses strongly recommended."},
            "US": {"rule": "UCC §2-615 (impracticability). Common law frustration of purpose. FM clauses essential."},
        },
    }

    comparison = comparisons.get(clause_type, {})
    filtered = {k: v for k, v in comparison.items() if k in jurisdictions}

    return {
        "clause_type": clause_type,
        "jurisdictions": jurisdictions,
        "comparison": filtered,
        "available_clause_types": list(comparisons.keys()),
        "recommendation": "Bei grenzüberschreitenden Verträgen: Strengstes Regime als Maßstab nehmen",
        "retrieved_at": ts(),
    }

async def handle_regulatory_clause(args: dict) -> dict:
    """Check if contract meets regulatory requirements."""
    has_audit_rights = args.get("audit_rights", False)
    has_exit_strategy = args.get("exit_strategy", False)
    has_sla = args.get("service_level_agreement", False)
    has_data_location = args.get("data_location_clause", False)
    has_incident_notification = args.get("incident_notification", False)
    has_sub_outsourcing = args.get("sub_outsourcing_restrictions", False)
    has_bcp = args.get("business_continuity_provisions", False)
    has_termination = args.get("termination_rights", False)
    regulation = args.get("regulation", "DORA")

    checks = [
        {"clause": "Audit & access rights", "required_by": "DORA Art.28(3), Art.30(2)(d)", "met": has_audit_rights, "priority": "CRITICAL"},
        {"clause": "Exit strategy / transition plan", "required_by": "DORA Art.28(8)", "met": has_exit_strategy, "priority": "CRITICAL"},
        {"clause": "Service Level Agreement (SLAs)", "required_by": "DORA Art.30(2)(a)", "met": has_sla, "priority": "HIGH"},
        {"clause": "Data location / processing location", "required_by": "DORA Art.30(2)(b), GDPR Art.28", "met": has_data_location, "priority": "HIGH"},
        {"clause": "Incident notification (ICT + data breach)", "required_by": "DORA Art.30(2)(e), GDPR Art.33", "met": has_incident_notification, "priority": "CRITICAL"},
        {"clause": "Sub-outsourcing restrictions", "required_by": "DORA Art.30(2)(a), GDPR Art.28(2)", "met": has_sub_outsourcing, "priority": "HIGH"},
        {"clause": "Business continuity provisions", "required_by": "DORA Art.30(2)(c)", "met": has_bcp, "priority": "HIGH"},
        {"clause": "Termination rights", "required_by": "DORA Art.28(7)", "met": has_termination, "priority": "HIGH"},
    ]

    met = [c for c in checks if c["met"]]
    missing = [c for c in checks if not c["met"]]
    score = len(met) / len(checks) * 100

    return {
        "regulation": regulation, "compliance_score": round(score),
        "status": "COMPLIANT" if not missing else "NON-COMPLIANT",
        "met": met, "missing": missing,
        "critical_missing": [c for c in missing if c["priority"] == "CRITICAL"],
        "legal_basis": "DORA Art.28-30 (ICT third-party risk), GDPR Art.28 (DPA), EBA Guidelines on Outsourcing",
        "retrieved_at": ts(),
    }

async def handle_force_majeure(args: dict) -> dict:
    """Force Majeure clause assessment."""
    clause_text = args.get("clause_text", "")
    has_pandemic = args.get("covers_pandemic", False)
    has_cyber = args.get("covers_cyber_attack", False)
    has_sanctions = args.get("covers_sanctions", False)
    has_supply_chain = args.get("covers_supply_chain_disruption", False)
    notification_days = int(args.get("notification_days", 0))
    termination_days = int(args.get("termination_after_days", 0))

    modern_events = [
        {"event": "Pandemie/Epidemie", "covered": has_pandemic, "recommendation": "ESSENTIAL post-COVID — explizit aufnehmen"},
        {"event": "Cyberangriff", "covered": has_cyber, "recommendation": "NIS2/DORA relevant — klare Definition nötig"},
        {"event": "Sanktionen/Embargo", "covered": has_sanctions, "recommendation": "EU/US Sanktionen können Vertragserfüllung unmöglich machen"},
        {"event": "Lieferkettenunterbrechung", "covered": has_supply_chain, "recommendation": "LkSG-relevant — Verhältnismäßigkeit wahren"},
    ]

    score = sum(1 for e in modern_events if e["covered"]) / len(modern_events) * 100

    return {
        "events_assessment": modern_events,
        "coverage_score": round(score),
        "notification_requirement": f"{notification_days} Tage" if notification_days > 0 else "Nicht definiert — RISIKO",
        "termination_trigger": f"Nach {termination_days} Tagen FM" if termination_days > 0 else "Nicht definiert — RISIKO",
        "best_practice": [
            "Explizite Event-Liste + Auffangklausel ('einschließlich aber nicht beschränkt auf...')",
            "Benachrichtigungspflicht: Max. 5-10 Werktage",
            "Beendigungsrecht: Nach 30-90 Tagen andauernder FM",
            "Mitwirkungspflicht: Beide Parteien müssen Auswirkungen minimieren",
            "Kein automatischer Haftungsausschluss — nur Leistungsbefreiung",
        ],
        "legal_basis": "§275 BGB (Unmöglichkeit), §313 BGB (Störung der Geschäftsgrundlage), ICC Force Majeure Clause 2020",
        "retrieved_at": ts(),
    }

async def handle_liability_cap(args: dict) -> dict:
    """Haftungsbegrenzung compliance check."""
    cap_type = args.get("cap_type", "")  # per_incident, annual, contract_value
    cap_amount = args.get("cap_amount_eur", 0)
    contract_value = float(args.get("contract_value_eur", 0))
    excludes_gross_negligence = args.get("excludes_gross_negligence", False)
    excludes_willful = args.get("excludes_willful_misconduct", True)
    excludes_personal_injury = args.get("excludes_personal_injury", True)
    is_agb = args.get("is_standard_terms", False)

    issues = []
    if not excludes_willful:
        issues.append({"issue": "Haftung für Vorsatz ausgeschlossen", "severity": "CRITICAL",
                       "note": "§276 Abs.3 BGB: IMMER unwirksam — kann nicht ausgeschlossen werden"})
    if not excludes_personal_injury and is_agb:
        issues.append({"issue": "Haftung für Personenschäden ausgeschlossen in AGB", "severity": "CRITICAL",
                       "note": "§309 Nr.7a BGB: In AGB IMMER unwirksam"})
    if cap_amount > 0 and contract_value > 0:
        ratio = cap_amount / contract_value
        if ratio < 1:
            issues.append({"issue": f"Cap nur {ratio:.0%} des Vertragswertes", "severity": "MEDIUM",
                           "note": "Sehr niedrig — prüfen ob angemessen für den Vertragswert"})

    return {
        "cap_type": cap_type, "cap_amount": cap_amount,
        "issues": issues,
        "compliant": len([i for i in issues if i["severity"] == "CRITICAL"]) == 0,
        "mandatory_exceptions_de": [
            "Vorsätzliche Schädigung (§276 Abs.3 BGB) — IMMER",
            "Verletzung von Leben, Körper, Gesundheit (§309 Nr.7a BGB in AGB)",
            "Arglistiges Verschweigen von Mängeln",
            "Haftung nach Produkthaftungsgesetz (ProdHaftG)",
            "Garantiezusagen",
        ],
        "best_practice": "Cap = 1-2x jährlicher Vertragswert oder versicherbare Summe. Separate Caps für IP-Verletzung und Datenschutz.",
        "legal_basis": "§§276, 307-309 BGB, ProdHaftG",
        "retrieved_at": ts(),
    }


def main():
    server = WhitelabelMCPServer(product_name=PRODUCT_NAME, product_slug="legaltechoracle",
                                 version=VERSION, port_mcp=PORT_MCP, port_health=PORT_HEALTH)

    server.register_tool("contract_draft", "Generate EU-compliant contract from parameters. Service, license, supply, consulting templates with mandatory DE/EU clauses (AGB, DSGVO, Haftung).",
        {"contract_type":{"type":"string","description":"service|license|supply|consulting"},"party_a_name":{"type":"string"},"party_a_address":{"type":"string"},"party_b_name":{"type":"string"},"party_b_address":{"type":"string"},"subject":{"type":"string"},"value_eur":{"type":"string"},"duration":{"type":"string"},"governing_law":{"type":"string","description":"DE|AT|CH (default: DE)"}}, handle_contract_draft, credits=3)

    server.register_tool("nda_generate", "Generate NDA (Geheimhaltungsvereinbarung) — mutual or unilateral. GeschGehG-compliant with optional Vertragsstrafe clause.",
        {"type":{"type":"string","description":"mutual|unilateral"},"discloser":{"type":"string"},"recipient":{"type":"string"},"purpose":{"type":"string"},"duration_years":{"type":"integer"},"penalty_eur":{"type":"string","description":"Vertragsstrafe amount (optional)"}}, handle_nda_generate, credits=2)

    server.register_tool("freelancer_contract", "Scheinselbständigkeit-safe freelancer agreement generator. All 8 DRV-checked criteria with mandatory clauses. §7 SGB IV compliant.",
        {"freelancer_name":{"type":"string"},"client_name":{"type":"string"},"project_description":{"type":"string"},"hourly_rate":{"type":"string"},"project_fee":{"type":"string"}}, handle_freelancer_contract, credits=3)

    server.register_tool("dpa_generate", "DSGVO Art.28 Auftragsverarbeitungsvertrag (AVV/DPA) generator. All 12 mandatory clauses, TOMs checklist, Drittlandtransfer requirements.",
        {"controller_name":{"type":"string"},"processor_name":{"type":"string"},"data_types":{"type":"string"},"data_subjects":{"type":"string"},"purpose":{"type":"string"},"third_country_transfer":{"type":"boolean"}}, handle_dpa_generate, credits=3)

    server.register_tool("clause_risk_scan", "Red-flag clause detection in German/English contracts. Scans for unlimited liability, unfair modification rights, AGB violations (§§305-310 BGB).",
        {"contract_text":{"type":"string","description":"Full contract text to analyze"}}, handle_clause_risk, credits=2)

    server.register_tool("contract_summary", "Extract key terms from contract text: Laufzeit, Kündigungsfrist, Vergütung, Haftung, Gerichtsstand, anwendbares Recht.",
        {"contract_text":{"type":"string","description":"Full contract text"}}, handle_contract_summary, credits=2)

    server.register_tool("termination_analysis", "Kündigungsklausel-Analyse. Ordentliche/außerordentliche Kündigung, Formerfordernis, AGB-Kontrolle bei Auto-Renewal.",
        {"contract_type":{"type":"string","description":"dienstvertrag|werkvertrag|mietvertrag|lizenz"},"duration_type":{"type":"string","description":"befristet|unbefristet"},"notice_period_months":{"type":"number"},"auto_renewal":{"type":"boolean"}}, handle_termination, credits=1)

    server.register_tool("obligation_matrix", "Map contract clauses to DORA/MiCA/NIS2/GDPR regulatory obligations. Returns article-by-article requirements per regulation.",
        {"regulations":{"type":"string","description":"Comma-separated: DORA, MiCA, NIS2, GDPR"}}, handle_obligation_matrix, credits=2)

    server.register_tool("cross_jurisdiction", "Compare contract clause rules across DE/AT/CH/UK/US. Covers liability limitation, non-compete, force majeure.",
        {"clause_type":{"type":"string","description":"limitation_of_liability|non_compete|force_majeure"},"jurisdictions":{"type":"array","description":"Country codes e.g. [DE, AT, CH, UK, US]"}}, handle_cross_jurisdiction, credits=2)

    server.register_tool("regulatory_clause_check", "Check if contract meets DORA Art.28-30 regulatory requirements. Audit rights, exit strategy, SLAs, data location, incident notification.",
        {"audit_rights":{"type":"boolean"},"exit_strategy":{"type":"boolean"},"service_level_agreement":{"type":"boolean"},"data_location_clause":{"type":"boolean"},"incident_notification":{"type":"boolean"},"sub_outsourcing_restrictions":{"type":"boolean"},"business_continuity_provisions":{"type":"boolean"},"termination_rights":{"type":"boolean"},"regulation":{"type":"string","description":"DORA|NIS2|GDPR"}}, handle_regulatory_clause, credits=2)

    server.register_tool("force_majeure_check", "Force Majeure clause assessment. Checks coverage of modern events (pandemic, cyber, sanctions, supply chain). Best practice recommendations.",
        {"clause_text":{"type":"string"},"covers_pandemic":{"type":"boolean"},"covers_cyber_attack":{"type":"boolean"},"covers_sanctions":{"type":"boolean"},"covers_supply_chain_disruption":{"type":"boolean"},"notification_days":{"type":"integer"},"termination_after_days":{"type":"integer"}}, handle_force_majeure, credits=1)

    server.register_tool("liability_cap_check", "Haftungsbegrenzung compliance check (DE law). Validates against §276/§307-309 BGB. Checks mandatory exceptions, AGB rules.",
        {"cap_type":{"type":"string","description":"per_incident|annual|contract_value"},"cap_amount_eur":{"type":"number"},"contract_value_eur":{"type":"number"},"excludes_gross_negligence":{"type":"boolean"},"excludes_willful_misconduct":{"type":"boolean"},"excludes_personal_injury":{"type":"boolean"},"is_standard_terms":{"type":"boolean","description":"AGB (standard terms) — stricter rules apply"}}, handle_liability_cap, credits=1)

    logger.info(f"🚀 {PRODUCT_NAME} v{VERSION} starting on port {PORT_MCP}")
    server.run()

if __name__ == "__main__":
    main()
