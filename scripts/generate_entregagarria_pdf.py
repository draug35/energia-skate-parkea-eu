from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "assets/energia-skate-parkea-fitxa-entregagarria.pdf"
SIM_URL = "https://draug35.github.io/energia-skate-parkea-eu/"


def style_sheet():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#16201f"),
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["Normal"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#61706d"),
            fontSize=10,
            leading=13,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "HeadingCustom",
            parent=base["Heading1"],
            textColor=colors.HexColor("#17615e"),
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "Heading2Custom",
            parent=base["Heading2"],
            textColor=colors.HexColor("#16201f"),
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=6,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["Normal"],
            textColor=colors.HexColor("#16201f"),
            fontSize=9.5,
            leading=13,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "SmallCustom",
            parent=base["Normal"],
            textColor=colors.HexColor("#61706d"),
            fontSize=8.5,
            leading=11,
        ),
        "box": ParagraphStyle(
            "BoxCustom",
            parent=base["Normal"],
            textColor=colors.HexColor("#16201f"),
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
        ),
    }


def p(text, styles, name="body"):
    return Paragraph(text, styles[name])


def info_table(styles):
    data = [
        [p("<b>Ikaslea:</b>", styles), "", p("<b>Taldea:</b>", styles), "", p("<b>Data:</b>", styles), ""],
    ]
    table = Table(data, colWidths=[2.0 * cm, 5.2 * cm, 1.8 * cm, 3.0 * cm, 1.4 * cm, 2.8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEBELOW", (1, 0), (1, 0), 0.8, colors.HexColor("#9eadab")),
                ("LINEBELOW", (3, 0), (3, 0), 0.8, colors.HexColor("#9eadab")),
                ("LINEBELOW", (5, 0), (5, 0), 0.8, colors.HexColor("#9eadab")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def answer_box(lines=4):
    data = [[""] for _ in range(lines)]
    table = Table(data, colWidths=[16.8 * cm], rowHeights=[0.58 * cm] * lines)
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#cddbd7")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e3eae7")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbfcfb")),
            ]
        )
    )
    return table


def data_table(headers, rows):
    data = [[Paragraph(f"<b>{h}</b>", style_sheet()["small"]) for h in headers]] + rows
    table = Table(data, colWidths=[16.8 * cm / len(headers)] * len(headers), repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#cddbd7")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e7f3f1")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#134d4a")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfcfb")]),
            ]
        )
    )
    return table


def checkbox_table(items, styles):
    data = [[p(f"[ ] {item}", styles, "body")] for item in items]
    table = Table(data, colWidths=[16.8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#d9e1dd")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#e3eae7")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbfcfb")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d9e1dd"))
    canvas.line(1.6 * cm, 1.25 * cm, 19.4 * cm, 1.25 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#61706d"))
    canvas.drawString(1.6 * cm, 0.85 * cm, "Energia skate-parkean - fitxa entregagarria")
    canvas.drawRightString(19.4 * cm, 0.85 * cm, f"{doc.page}")
    canvas.restoreState()


def build_pdf():
    styles = style_sheet()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.55 * cm,
        title="Energia skate-parkean - fitxa entregagarria",
        author="Codex",
    )

    story = []
    story.append(p("Energia skate-parkean", styles, "title"))
    story.append(p("Fitxa entregagarria: simulagailuarekin ikertzeko galderak", styles, "subtitle"))
    story.append(info_table(styles))
    story.append(Spacer(1, 8))
    story.append(p("<b>Helburua:</b> energia potentziala, zinetikoa, termikoa eta energia totalaren portaera aztertzea, simulagailuan datuak hartuta eta ondorioak arrazoituta.", styles))
    story.append(p(f"<b>Simulagailua:</b> {SIM_URL}", styles, "small"))
    story.append(p("<b>Lan-araua:</b> proba bakoitzean aldagai bakarra aldatu. Datuak hartzeko, erabili simulagailuko <i>Datuak hartu</i> botoia edo neurgailuak.", styles))

    story.append(p("1. jarduera - Energia mekanikoa marruskadurarik gabe", styles, "h1"))
    story.append(p("Prestaketa: hautatu U-pista, masa 55 kg, g = 9.8 m/s^2 eta marruskadura 0. Abiarazi eta hartu datuak hiru unetan: hasieran, beheko puntuan eta beste aldera igotzean.", styles))
    story.append(
        data_table(
            ["Uneak", "h (m)", "v (m/s)", "Ez (J)", "Ep (J)", "Et (J)", "Guztira (J)"],
            [["Hasiera", "", "", "", "", "", ""], ["Behean", "", "", "", "", "", ""], ["Igotzean", "", "", "", "", "", ""]],
        )
    )
    story.append(Spacer(1, 7))
    story.append(p("Test galdera: marruskadurarik gabe, energia totalaren balioa...", styles, "h2"))
    story.append(checkbox_table(["ia konstante mantentzen da.", "beheko puntuan desagertzen da.", "masaren arabera beti zero bihurtzen da."], styles))
    story.append(p("Azalpena datuekin:", styles, "h2"))
    story.append(answer_box(4))

    story.append(p("2. jarduera - Masa aldatuta zer gertatzen da?", styles, "h1"))
    story.append(p("Prestaketa: pista bera mantendu. Egin bi proba marruskadurarik gabe: 55 kg eta 90 kg. Konparatu beheko puntuko abiadura eta energia.", styles))
    story.append(
        data_table(
            ["Masa", "h hasieran", "v max.", "Ez max.", "Ep hasieran", "Zer aldatu da?"],
            [["55 kg", "", "", "", "", ""], ["90 kg", "", "", "", "", ""]],
        )
    )
    story.append(Spacer(1, 7))
    story.append(p("Test galdera: masa handitzean, altuera bera bada, abiadura maximoa...", styles, "h2"))
    story.append(checkbox_table(["ez da zertan handitzen eredu ideal honetan.", "beti bikoizten da.", "marruskadura 0 denean ezin da neurtu."], styles))
    story.append(p("Zergatik? Erabili energia per masa edo datuen konparazioa:", styles, "h2"))
    story.append(answer_box(4))

    story.append(PageBreak())
    story.append(p("3. jarduera - Marruskadura eta energia termikoa", styles, "h1"))
    story.append(p("Prestaketa: U-pista, masa 55 kg, g = 9.8 m/s^2. Egin lehen proba marruskadura 0-rekin eta bigarrena marruskadura 0.055 inguruan. Begiratu Et barra eta grafikoa.", styles))
    story.append(
        data_table(
            ["Proba", "Marr.", "v amaieran", "Ez", "Ep", "Et", "Energia mekanikoa"],
            [["A", "0", "", "", "", "", ""], ["B", "0.055", "", "", "", "", ""]],
        )
    )
    story.append(Spacer(1, 7))
    story.append(p("Test galdera: marruskadurarekin energia mekanikoaren zati bat...", styles, "h2"))
    story.append(checkbox_table(["energia termiko bihurtzen da.", "desagertu egiten da inolako arrastorik gabe.", "energia potentzial bihurtzen da beti."], styles))
    story.append(p("Azaldu zer frogatzen duen energia termikoaren balioak:", styles, "h2"))
    story.append(answer_box(5))

    story.append(p("4. jarduera - Loop-aren erronka", styles, "h1"))
    story.append(p("Prestaketa: hautatu Loop-a. Marruskadurarik gabe hasi. Behatu ea patinatzaileak loop-a osatzen duen. Ondoren, gehitu marruskadura pixka bat eta konparatu.", styles))
    story.append(
        data_table(
            ["Proba", "Marr.", "h hasieran", "v goian", "Osatu du?", "Arrazoia"],
            [["1", "0", "", "", "Bai / Ez", ""], ["2", "0.055", "", "", "Bai / Ez", ""]],
        )
    )
    story.append(Spacer(1, 7))
    story.append(p("Test galdera: loop-a osatzeko baldintza nagusia da...", styles, "h2"))
    story.append(checkbox_table(["hasieran energia nahikoa izatea.", "masa oso handia izatea.", "marruskadura ahalik eta handiena izatea."], styles))
    story.append(p("Ondorioa: zer harreman dago altuera, abiadura eta energia totalaren artean?", styles, "h2"))
    story.append(answer_box(5))

    story.append(p("Amaierako sintesia", styles, "h1"))
    story.append(p("Idatzi 5-6 lerrotan zer ikasi duzun. Derrigor erabili hitz hauek: energia potentziala, energia zinetikoa, energia termikoa, marruskadura eta kontserbazioa.", styles))
    story.append(answer_box(7))
    story.append(p("Entregatu aurretik egiaztatu:", styles, "h2"))
    story.append(checkbox_table(["Datu-taulak osatu ditut.", "Test galderetan aukera bat markatu dut.", "Erantzun laburrak datuekin justifikatu ditut.", "Amaierako sintesia idatzi dut."], styles))

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)


if __name__ == "__main__":
    build_pdf()
