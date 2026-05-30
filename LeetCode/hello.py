from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

# ── Color palette ──────────────────────────────────────────────────────────
RED      = colors.HexColor("#E53935")
DARK     = colors.HexColor("#1A1A2E")
ACCENT   = colors.HexColor("#FF6F00")
SOFT_BG  = colors.HexColor("#FFF8F0")
GRAY     = colors.HexColor("#5C5C7B")
LGRAY    = colors.HexColor("#F5F5F5")
WHITE    = colors.white
GREEN    = colors.HexColor("#2E7D32")
BLUE     = colors.HexColor("#1565C0")
PURPLE   = colors.HexColor("#6A1B9A")

W, H = A4

# ── Doc setup ─────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "output/YouTube_Channel_Launch_Guide.pdf",
    pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=22*mm, bottomMargin=22*mm,
)

# ── Styles ────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S("CoverTitle", fontSize=32, textColor=WHITE,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=40)
cover_sub   = S("CoverSub", fontSize=14, textColor=colors.HexColor("#FFD54F"),
                fontName="Helvetica", alignment=TA_CENTER, leading=20)
cover_name  = S("CoverName", fontSize=11, textColor=colors.HexColor("#B0BEC5"),
                fontName="Helvetica", alignment=TA_CENTER)

ch_title    = S("ChTitle", fontSize=22, textColor=WHITE,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=28)
ch_sub      = S("ChSub", fontSize=10, textColor=colors.HexColor("#FFD54F"),
                fontName="Helvetica-Oblique", alignment=TA_CENTER)

sec_head    = S("SecHead", fontSize=16, textColor=DARK,
                fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=14)
sub_head    = S("SubHead", fontSize=13, textColor=RED,
                fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=10)
sub2_head   = S("Sub2Head", fontSize=11, textColor=ACCENT,
                fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=7)

body        = S("Body", fontSize=10, textColor=DARK,
                fontName="Helvetica", leading=16, spaceAfter=4,
                alignment=TA_JUSTIFY)
body_b      = S("BodyB", fontSize=10, textColor=DARK,
                fontName="Helvetica-Bold", leading=16, spaceAfter=3)
bullet      = S("Bullet", fontSize=10, textColor=DARK,
                fontName="Helvetica", leading=15, spaceAfter=2,
                leftIndent=14, firstLineIndent=-10)
bullet2     = S("Bullet2", fontSize=9.5, textColor=GRAY,
                fontName="Helvetica", leading=14, spaceAfter=2,
                leftIndent=26, firstLineIndent=-10)

script_head = S("ScriptHead", fontSize=11, textColor=WHITE,
                fontName="Helvetica-Bold", leading=15)
script_body = S("ScriptBody", fontSize=10, textColor=DARK,
                fontName="Helvetica", leading=15, spaceAfter=3)
script_dir  = S("ScriptDir", fontSize=9.5, textColor=ACCENT,
                fontName="Helvetica-Oblique", leading=13, spaceAfter=2)

note        = S("Note", fontSize=9, textColor=GREEN,
                fontName="Helvetica-Oblique", leading=13,
                leftIndent=10, spaceAfter=4)
tip_style   = S("TipStyle", fontSize=9.5, textColor=DARK,
                fontName="Helvetica", leading=14, leftIndent=8)

tag_style   = S("Tag", fontSize=9, textColor=WHITE,
                fontName="Helvetica-Bold", alignment=TA_CENTER)

footer_style= S("Footer", fontSize=8, textColor=GRAY,
                fontName="Helvetica", alignment=TA_CENTER)

# ── Helpers ───────────────────────────────────────────────────────────────
def hr(color=RED, thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=6, spaceBefore=4)

def SP(n=6):
    return Spacer(1, n)

def colored_box(paragraphs, bg=LGRAY, padding=8, radius=4):
    """Wrap content in a colored rounded table cell."""
    data = [[paragraphs]]
    t = Table(data, colWidths=[doc.width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("ROUNDEDCORNERS", [radius]),
        ("TOPPADDING",    (0,0), (-1,-1), padding),
        ("BOTTOMPADDING", (0,0), (-1,-1), padding),
        ("LEFTPADDING",   (0,0), (-1,-1), padding+2),
        ("RIGHTPADDING",  (0,0), (-1,-1), padding+2),
    ]))
    return t

def chapter_banner(title, subtitle="", color=DARK):
    data = [[Paragraph(title, ch_title)]]
    if subtitle:
        data.append([Paragraph(subtitle, ch_sub)])
    t = Table(data, colWidths=[doc.width])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS",[5]),
    ]))
    return t

def two_col(left_items, right_items, header_left="", header_right=""):
    half = doc.width / 2 - 3*mm
    rows = []
    if header_left:
        rows.append([
            Paragraph(f"<b>{header_left}</b>", sub2_head),
            Paragraph(f"<b>{header_right}</b>", sub2_head),
        ])
    max_len = max(len(left_items), len(right_items))
    for i in range(max_len):
        l = Paragraph(left_items[i],  bullet) if i < len(left_items)  else Paragraph("", body)
        r = Paragraph(right_items[i], bullet) if i < len(right_items) else Paragraph("", body)
        rows.append([l, r])
    t = Table(rows, colWidths=[half, half])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))
    return t

def script_block(lines):
    """lines = list of (label, text, style_key)
       style_key: 'head'|'dir'|'body'
    """
    rows = []
    for label, text, sk in lines:
        if sk == "head":
            st = script_head; bg = DARK
        elif sk == "dir":
            st = script_dir;  bg = colors.HexColor("#FFF3E0")
        else:
            st = script_body; bg = WHITE
        rows.append([
            Paragraph(f"<b>{label}</b>", ParagraphStyle("_l", fontSize=9,
                       textColor=ACCENT if sk!="head" else WHITE,
                       fontName="Helvetica-Bold")),
            Paragraph(text, st),
        ])
    t = Table(rows, colWidths=[22*mm, doc.width - 22*mm])
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[LGRAY, WHITE]),
        ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#DDDDDD")),
        ("LINEBELOW",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
    ]))
    return t

def timeline_table(rows_data):
    """rows_data = [(day_label, task, detail)]"""
    header = [
        Paragraph("<b>DAY / PHASE</b>", ParagraphStyle("_h", fontSize=9,
                   textColor=WHITE, fontName="Helvetica-Bold")),
        Paragraph("<b>TASK</b>", ParagraphStyle("_h", fontSize=9,
                   textColor=WHITE, fontName="Helvetica-Bold")),
        Paragraph("<b>DETAILS</b>", ParagraphStyle("_h", fontSize=9,
                   textColor=WHITE, fontName="Helvetica-Bold")),
    ]
    rows = [header]
    for d, task, detail in rows_data:
        rows.append([
            Paragraph(d, ParagraphStyle("_d", fontSize=9, textColor=DARK,
                       fontName="Helvetica-Bold")),
            Paragraph(task, ParagraphStyle("_t", fontSize=9, textColor=DARK,
                       fontName="Helvetica-Bold")),
            Paragraph(detail, ParagraphStyle("_dt", fontSize=9, textColor=GRAY,
                       fontName="Helvetica")),
        ])
    t = Table(rows, colWidths=[28*mm, 45*mm, doc.width-73*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), DARK),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
        ("VALIGN",        (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
        ("RIGHTPADDING",  (0,0),(-1,-1), 7),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("BOX",           (0,0),(-1,-1), 0.8, colors.HexColor("#CCCCCC")),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#DDDDDD")),
    ]))
    return t

def checklist_table(items, cols=2):
    half = doc.width / cols - 3*mm
    rows = []
    chunk = [items[i:i+cols] for i in range(0, len(items), cols)]
    for c in chunk:
        row = []
        for item in c:
            row.append(Paragraph(f"&#9744; {item}", bullet))
        while len(row) < cols:
            row.append(Paragraph("", body))
        rows.append(row)
    t = Table(rows, colWidths=[half]*cols)
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, LGRAY]),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ═══════════════════════════════════════════════════════════════════════════
story = []

# ── COVER PAGE ─────────────────────────────────────────────────────────────
cover_bg = Table(
    [[Paragraph("🎬 YouTube Channel", cover_title)],
     [Paragraph("COMPLETE LAUNCH GUIDE", cover_title)],
     [SP(8)],
     [Paragraph("Scripts · Storylines · 90-Day Roadmap · Video Plans", cover_sub)],
     [SP(6)],
     [Paragraph("Tech + AI + Coding Channel for Students & Freshers", cover_sub)],
     [SP(16)],
     [Paragraph("Your personal step-by-step playbook to go from 0 to uploading", cover_name)],
     [Paragraph("Created for: Avinash  |  2026 Edition", cover_name)],
    ],
    colWidths=[doc.width]
)
cover_bg.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), DARK),
    ("TOPPADDING",    (0,0),(-1,-1), 18),
    ("BOTTOMPADDING", (0,0),(-1,-1), 18),
    ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ("RIGHTPADDING",  (0,0),(-1,-1), 20),
    ("ROUNDEDCORNERS",[8]),
]))
story += [cover_bg, SP(20)]

accent_strip = Table([[Paragraph(
    "&#9733; This PDF covers: Channel Setup &nbsp;|&nbsp; 90-Day Plan &nbsp;|&nbsp; "
    "5 Full Video Scripts &nbsp;|&nbsp; 20 Shorts Ideas &nbsp;|&nbsp; Weekly Schedule &nbsp;|&nbsp; Monetization",
    ParagraphStyle("strip", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                   alignment=TA_CENTER)
)]],colWidths=[doc.width])
accent_strip.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), ACCENT),
    ("TOPPADDING",    (0,0),(-1,-1), 10),
    ("BOTTOMPADDING", (0,0),(-1,-1), 10),
    ("ROUNDEDCORNERS",[4]),
]))
story += [accent_strip, PageBreak()]

# ── TABLE OF CONTENTS ───────────────────────────────────────────────────────
story.append(chapter_banner("📋  TABLE OF CONTENTS", color=PURPLE))
story.append(SP(10))

toc = [
    ("01", "Channel Foundation & Positioning", "Brand, Name, Setup Checklist"),
    ("02", "90-Day Complete Roadmap", "Phase 1 → Phase 4 with daily tasks"),
    ("03", "Day 1–14 Exact Plan", "Copy-paste daily action list"),
    ("04", "Weekly Posting Schedule", "Mon–Sun calendar system"),
    ("05", "Video 1 — Full Script", "AI Tools for Students (Long, 10 min)"),
    ("06", "Video 2 — Full Script", "Coding Roadmap for Beginners (Long, 12 min)"),
    ("07", "Video 3 — Short Script", "Resume in 60 Seconds using AI"),
    ("08", "Video 4 — Short Script", "3 VS Code Extensions (Short 40s)"),
    ("09", "Video 5 — Short Script", "Git & GitHub in 40 Seconds"),
    ("10", "20 Shorts Ideas Bank", "Ready-to-record topic list"),
    ("11", "Thumbnail & Title Formulas", "CTR-boosting frameworks"),
    ("12", "Gear & Tool Stack", "Free tools to start today"),
    ("13", "Monetization Roadmap", "How to earn in 90 days"),
    ("14", "Analytics Checklist", "What to track weekly"),
]
toc_rows = [[
    Paragraph(f"<b>{n}</b>", ParagraphStyle("tc_n", fontSize=11, textColor=RED,
               fontName="Helvetica-Bold")),
    Paragraph(f"<b>{title}</b>", ParagraphStyle("tc_t", fontSize=10, textColor=DARK,
               fontName="Helvetica-Bold")),
    Paragraph(sub, ParagraphStyle("tc_s", fontSize=9, textColor=GRAY,
               fontName="Helvetica")),
] for n, title, sub in toc]

toc_table = Table(toc_rows, colWidths=[14*mm, 72*mm, doc.width-86*mm])
toc_table.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, LGRAY]),
    ("VALIGN",         (0,0),(-1,-1), "MIDDLE"),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("TOPPADDING",     (0,0),(-1,-1), 6),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 6),
    ("BOX",            (0,0),(-1,-1), 0.5, colors.HexColor("#DDDDDD")),
    ("LINEBELOW",      (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [toc_table, PageBreak()]

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 01 — CHANNEL FOUNDATION
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("01 — CHANNEL FOUNDATION & POSITIONING",
    "Build your brand before your first upload", RED))
story.append(SP(10))

story.append(Paragraph("Your Channel Position", sec_head))
story.append(hr())
story.append(colored_box([
    Paragraph("🎯 <b>Recommended Positioning Statement:</b>", body_b),
    SP(4),
    Paragraph(
        '"I simplify Tech + AI tools for Students, Beginners, and Job Seekers."',
        ParagraphStyle("quote", fontSize=13, textColor=RED,
                       fontName="Helvetica-BoldOblique", alignment=TA_CENTER, leading=18)
    ),
    SP(4),
    Paragraph("This single line tells viewers <i>who you are</i>, <i>what you teach</i>, "
              "and <i>who it's for</i>. Put it everywhere — banner, About, bio, pinned comment.", body),
], bg=SOFT_BG, padding=12))
story.append(SP(8))

story.append(Paragraph("Channel Name Options", sub_head))
name_data = [
    [Paragraph("<b>Name</b>", body_b), Paragraph("<b>Why it works</b>", body_b),
     Paragraph("<b>Best for</b>", body_b)],
    [Paragraph("TechWithAvinash", body), Paragraph("Personal + topic combo", body),
     Paragraph("Branding long term", body)],
    [Paragraph("Avinash Learns Tech", body), Paragraph("Growth journey vibe, relatable", body),
     Paragraph("Fast early subscribers", body)],
    [Paragraph("Tech Simplified", body), Paragraph("Clean, searchable keyword", body),
     Paragraph("Discovery via search", body)],
    [Paragraph("AIwalaAvinash", body), Paragraph("Memorable, niche-specific", body),
     Paragraph("AI-focused content", body)],
]
name_table = Table(name_data, colWidths=[45*mm, 60*mm, doc.width-105*mm])
name_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), DARK),
    ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("TOPPADDING",    (0,0),(-1,-1), 6),
    ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [name_table, SP(10)]

story.append(Paragraph("Channel Setup Checklist", sub_head))
story.append(Paragraph("Complete these before uploading Video 1:", body))
setup_checks = [
    "Channel name chosen & URL set",
    "Profile picture uploaded (clear face photo)",
    "Banner created in Canva (2560×1440px)",
    "About section written (use positioning statement)",
    "4 Playlists created (AI Tools / Coding / Career / Students)",
    "Links added: Instagram, LinkedIn, Email",
    "Channel trailer planned (30-sec hook video)",
    "OBS or screen recorder tested",
    "CapCut / VN installed for editing",
    "Canva thumbnail template made",
    "Google Doc created for Tool Lists (shareable link)",
    "First 5 Shorts topics written down",
]
story += [SP(4), checklist_table(setup_checks), SP(8)]

story.append(Paragraph("Brand Rules (Stay Consistent)", sub_head))
brand_rows = [
    [Paragraph("<b>Element</b>", body_b), Paragraph("<b>Your Rule</b>", body_b)],
    [Paragraph("Language", body), Paragraph("Hinglish (Hindi + English mix) — most relatable for Indian students", body)],
    [Paragraph("Tone", body), Paragraph("Friendly older brother / mentor — not boring teacher", body)],
    [Paragraph("Thumbnail style", body), Paragraph("Bold text + your face + 1 icon — always same font (Montserrat Bold)", body)],
    [Paragraph("Video promise", body), Paragraph("Practical + Short + Easy — say this in your bio", body)],
    [Paragraph("CTA phrase", body), Paragraph('Comment a keyword (e.g., "TOOLS", "RESUME") — builds engagement signals', body)],
    [Paragraph("Intro length", body), Paragraph("Max 15 seconds — hook first, name second", body)],
]
brand_t = Table(brand_rows, colWidths=[38*mm, doc.width-38*mm])
brand_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), DARK),
    ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("TOPPADDING",    (0,0),(-1,-1), 6),
    ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [brand_t, PageBreak()]

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 02 — 90-DAY ROADMAP
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("02 — 90-DAY COMPLETE ROADMAP",
    "Phase-by-phase plan: from setup to monetization", colors.HexColor("#1565C0")))
story.append(SP(10))

phases = [
    ("PHASE 1: Days 1–7", "SETUP & STRATEGY", RED,
     "Make the channel ready + create your content system.",
     ["Set up channel (name, banner, about, playlists)",
      "Create your Canva thumbnail template",
      "Record and edit your first Short (any topic)",
      "Write scripts for Week 1 (5 Shorts + 1 Long)",
      "Set up OBS for screen recording",
      "Create a Google Doc for resources/notes",
      "Study 3 top channels in your niche for 30 min"]),
    ("PHASE 2: Days 8–30", "CONSISTENCY (SHORTS-FIRST)", ACCENT,
     "Train the algorithm + build habit. Target: 25 Shorts + 4 Long videos.",
     ["Upload 5 Shorts every week (Mon–Fri)",
      "Upload 1 Long video every weekend",
      "Post 1 community poll/question weekly",
      "Focus: 'Quick Win' Shorts (tool tips, hacks, myths)",
      "End every Short with a keyword CTA",
      "Reply to every comment in first 24 hrs",
      "Review analytics every Sunday (what worked?)"]),
    ("PHASE 3: Days 31–60", "AUTHORITY + SERIES CONTENT", GREEN,
     "Start series-based content so people binge-watch your channel.",
     ["Launch Series 1: 'AI Tools for Students' (Shorts + Long)",
      "Launch Series 2: 'Coding from Zero' (Long + 2 Shorts each)",
      "Add timestamps to every long video",
      "Create downloadable Google Doc notes for long videos",
      "Pin a comment summary on every video",
      "Reach out to 1 similar creator for collab/shoutout",
      "Upload a 'channel trailer' (30-sec who-am-I video)"]),
    ("PHASE 4: Days 61–90", "GROWTH + MONETIZATION FOUNDATION", PURPLE,
     "Improve retention, grow subscribers, and start earning.",
     ["Create a free 'Roadmap PDF' lead magnet (collect emails)",
      "Add affiliate links (Notion, Canva, Hostinger etc.)",
      "Offer optional freelance: Resume Review / Portfolio Review",
      "Apply for YouTube Partner Program if 500+ subs & 3000 hrs",
      "Post a YouTube Community 'milestone' update",
      "Start a weekly analytics review habit",
      "Plan Month 4 content based on top-performing videos"]),
]

for phase_title, phase_sub, color, goal, tasks in phases:
    banner = Table([[Paragraph(phase_title, ParagraphStyle("_ph", fontSize=14,
                    textColor=WHITE, fontName="Helvetica-Bold")),
                     Paragraph(phase_sub, ParagraphStyle("_ps", fontSize=10,
                    textColor=colors.HexColor("#FFD54F"), fontName="Helvetica-Bold"))]],
                   colWidths=[65*mm, doc.width-65*mm])
    banner.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), color),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("ROUNDEDCORNERS",[4]),
    ]))
    story += [banner, SP(4)]
    story.append(Paragraph(f"<b>Goal:</b> {goal}", note))
    for t in tasks:
        story.append(Paragraph(f"&#9654; {t}", bullet))
    story.append(SP(8))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 03 — DAY 1–14 PLAN
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("03 — DAY 1–14 EXACT ACTION PLAN",
    "Copy this. Follow this. Upload this.", GREEN))
story.append(SP(10))

d1_14 = [
    ("Day 1", "Channel Setup", "Name, banner, about, playlists, profile pic"),
    ("Day 2", "Gear & Tools", "Install OBS, CapCut, Canva. Test mic quality."),
    ("Day 3", "Script Writing", "Write scripts for Week 1 Shorts (5 topics)"),
    ("Day 4", "Record Shorts 1–3", "AI tool for notes / Resume prompt / 3 keyboard shortcuts"),
    ("Day 5", "Record Shorts 4–5", "Git vs GitHub / 3 learning websites"),
    ("Day 6", "Long Video Script", "Write full script: AI Tools for Students"),
    ("Day 7", "Record Long Video 1", "Record, edit, create thumbnail. Schedule for Day 8"),
    ("Day 8 (Mon)", "Upload Short 1", "AI tool for notes — include keyword CTA"),
    ("Day 9 (Tue)", "Upload Short 2", "Resume bullet prompt — pin comment with prompt"),
    ("Day 10 (Wed)", "Upload Short 3", "3 keyboard shortcuts — community poll: which was new?"),
    ("Day 11 (Thu)", "Upload Short 4", "Git vs GitHub — link to future long video in comment"),
    ("Day 12 (Fri)", "Upload Short 5", "3 learning websites — pin freebie link"),
    ("Day 13 (Sat)", "Upload Long Video 1", "AI Tools for Students — timestamps + notes doc"),
    ("Day 14 (Sun)", "Review + Plan", "Check analytics, reply all comments, write Week 3 scripts"),
]
story += [timeline_table(d1_14), SP(8)]

story.append(colored_box([
    Paragraph("&#128161; <b>Week 2 Preview (Days 15–21):</b>", body_b),
    SP(3),
    Paragraph("&#9654; Short 6: VS Code Extensions", bullet),
    Paragraph("&#9654; Short 7: Host website free (teaser)", bullet),
    Paragraph("&#9654; Short 8: LinkedIn headline formula for freshers", bullet),
    Paragraph("&#9654; Short 9: Best beginner project idea", bullet),
    Paragraph("&#9654; Short 10: 'API explained in 30 sec'", bullet),
    Paragraph("&#9654; Long Video 2: Coding Roadmap (Choose Your Path)", bullet),
], bg=colors.HexColor("#E8F5E9"), padding=10))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 04 — WEEKLY SCHEDULE
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("04 — WEEKLY POSTING SCHEDULE",
    "Repeatable system — Mon to Sun", ACCENT))
story.append(SP(10))

sched_rows = [
    [Paragraph("<b>Day</b>", body_b), Paragraph("<b>Content Type</b>", body_b),
     Paragraph("<b>Topic Theme</b>", body_b), Paragraph("<b>Format</b>", body_b)],
    [Paragraph("Monday", body), Paragraph("Short", body),
     Paragraph("AI Tool of the week", body), Paragraph("20–35s", body)],
    [Paragraph("Tuesday", body), Paragraph("Short", body),
     Paragraph("Coding tip / shortcut", body), Paragraph("25–40s", body)],
    [Paragraph("Wednesday", body), Paragraph("Short", body),
     Paragraph("Career / Resume tip", body), Paragraph("20–35s", body)],
    [Paragraph("Thursday", body), Paragraph("Short", body),
     Paragraph("Productivity app / hack", body), Paragraph("25–40s", body)],
    [Paragraph("Friday", body), Paragraph("Short", body),
     Paragraph("Tech news explained (1 news, simple impact)", body), Paragraph("30–45s", body)],
    [Paragraph("Saturday", body), Paragraph("Long Video", body),
     Paragraph("Tutorial / Deep Dive / Series episode", body), Paragraph("8–15 min", body)],
    [Paragraph("Sunday", body), Paragraph("Review + Prep", body),
     Paragraph("Analytics check + script writing for next week", body), Paragraph("2 hrs work", body)],
]
sched_t = Table(sched_rows, colWidths=[22*mm, 28*mm, 80*mm, doc.width-130*mm])
sched_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), DARK),
    ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("TOPPADDING",    (0,0),(-1,-1), 7),
    ("BOTTOMPADDING", (0,0),(-1,-1), 7),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [sched_t, SP(10)]

story.append(Paragraph("Shorts Format Templates", sub_head))
story.append(hr(ACCENT))

templates = [
    ("A) 1 Problem → 1 Tool → 1 Result", [
        "Hook (0–2s): 'Stop doing this manually…'",
        "Tool name (2–5s): 'Use [Tool Name]'",
        "Demo (5–25s): Show 2–3 steps on screen",
        "Result (25–30s): Before/After or end screen",
        "CTA (last 2s): 'Comment TOOL for the link'",
    ], "Most effective format for AI tool videos"),
    ("B) 3 Quick Tips", [
        "Hook (0–3s): '3 [topic] you must know'",
        "Tip 1 + visual (3–15s)",
        "Tip 2 + visual (15–27s)",
        "Tip 3 + visual (27–40s)",
        "CTA: 'Save this for later'",
    ], "High watch-time — people stay to hear all 3"),
    ("C) Myth vs Fact", [
        "Hook: 'Most people think X — they are WRONG'",
        "State myth clearly on screen",
        "Bust with fact + short demo",
        "CTA: 'Share if this changed your mind'",
    ], "Fast engagement, shares, comments"),
    ("D) Mini Tutorial: 1 Feature", [
        "Hook: 'Here is how to do X in 30 seconds'",
        "Step 1 → Step 2 → Step 3 (screen recording)",
        "Show final result",
        "CTA: 'Try this and comment your result'",
    ], "Great for beginners — very actionable"),
]

for title, steps, note_text in templates:
    story.append(Paragraph(title, sub2_head))
    story.append(Paragraph(f"<i>Best for: {note_text}</i>", note))
    for s in steps:
        story.append(Paragraph(f"&#9654; {s}", bullet))
    story.append(SP(5))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 05 — VIDEO 1 FULL SCRIPT
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("05 — VIDEO 1: FULL SCRIPT",
    "AI Tools for Students (2026) — Long Video, 8–12 min", RED))
story.append(SP(10))

# Metadata box
meta1 = [
    [Paragraph("<b>Title</b>", body_b),
     Paragraph("AI Tools for Students (2026): Notes, PPT, Resume — Complete Free Toolkit", body)],
    [Paragraph("<b>Duration</b>", body_b), Paragraph("8–12 minutes", body)],
    [Paragraph("<b>Goal</b>", body_b), Paragraph("High search traffic + high shares from students", body)],
    [Paragraph("<b>CTA keyword</b>", body_b), Paragraph("'TOOLS' — promise link in pinned comment", body)],
    [Paragraph("<b>Thumbnail text</b>", body_b), Paragraph("FREE AI TOOLS · Notes + PPT + Resume", body)],
    [Paragraph("<b>Tags</b>", body_b),
     Paragraph("AI tools students, free AI tools 2026, AI for students India, notes AI, resume AI", body)],
]
meta_t1 = Table(meta1, colWidths=[30*mm, doc.width-30*mm])
meta_t1.setStyle(TableStyle([
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [meta_t1, SP(10)]

story.append(Paragraph("Complete Script", sub_head))
story.append(hr(RED))

script1 = [
    ("INTRO", "HOOK (0:00–0:20)", "head"),
    ("SCREEN", "[Show a student with piles of notes / stressed face image]", "dir"),
    ("SPEAK", "Yaar, agar tum abhi bhi manually notes bana rahe ho, assignments type kar rahe ho, "
              "aur resume khud se likh rahe ho… toh tum seriously 10 ghante waste kar rahe ho har hafte. "
              "Aaj main tumhe 5 AI tools dikhaunga — completely free — jo ye sab 10 minutes mein kar denge. "
              "Aur ye tools 2026 mein actually kaam karte hain. Ready? Let's go.", "body"),

    ("SECTION 1", "TOOL 1 — AI Notes Summarizer (0:20–2:00)", "head"),
    ("SCREEN", "[Open browser → go to tool website → paste sample PDF or text]", "dir"),
    ("SPEAK", "Pehla tool hai PDF ya lecture notes summarizer. "
              "Tum apni PDF upload karo, aur ye tool tumhara ek-page ka summary de deta hai — "
              "key points, headings, aur important terms ke saath. "
              "Main abhi ek real example dikhata hun.", "body"),
    ("DEMO", "[Paste a 5-page PDF → show 30-second summary output → highlight key points]", "dir"),
    ("SPEAK", "Dekha? Jo kaam tumhe 1 ghanta laggta — notes banana — ye 30 seconds mein ho gaya. "
              "Tool ka naam main comment mein pin karunga. Aage chalte hain.", "body"),

    ("SECTION 2", "TOOL 2 — AI PPT Generator (2:00–4:00)", "head"),
    ("SCREEN", "[Open Gamma.app or similar — type a topic name]", "dir"),
    ("SPEAK", "Doosra tool hai AI PPT generator. Aaj main Gamma use kar raha hun. "
              "Tum sirf topic type karo — jaise 'Machine Learning for Beginners' — aur ye "
              "automatically 8–10 slides bana deta hai, with content, headings, aur design.", "body"),
    ("DEMO", "[Type topic → click generate → show slides appearing]", "dir"),
    ("SPEAK", "Bas itna hi. 2 minutes mein presentation ready. Isko export karo as PDF ya PPT. "
              "College ke assignments ke liye perfect hai. Aur ye free hai.", "body"),

    ("SECTION 3", "TOOL 3 — AI Resume Bullet Helper (4:00–6:00)", "head"),
    ("SCREEN", "[Open ChatGPT or Claude → show prompt being typed]", "dir"),
    ("SPEAK", "Teesra tool — jo freshers ke liye sabse important hai — hai AI resume writer. "
              "Tum apni internship ya project ka description type karo, aur ye usse "
              "professional ATS-friendly bullet points mein convert kar deta hai.", "body"),
    ("DEMO", "[Type: 'I made a student attendance system in Python using Flask and MySQL' → "
             "show output bullet points]", "dir"),
    ("SPEAK", "Dekho kitna polished lag raha hai! Ye exactly waise bullets hain jo "
              "companies dekhna chahti hain. Comment karo 'RESUME' aur main tumhe "
              "exact prompt bhejunga.", "body"),

    ("SECTION 4", "TOOL 4 — AI Grammar & Writing (6:00–7:30)", "head"),
    ("SCREEN", "[Open Grammarly or QuillBot → paste a rough paragraph]", "dir"),
    ("SPEAK", "Chautha tool — especially important agar tum emails ya reports English mein likhte ho — "
              "hai AI grammar and rewriting tool. Rough paragraph paste karo, "
              "aur ye instantly professional bana deta hai.", "body"),

    ("SECTION 5", "TOOL 5 — AI Study Planner (7:30–9:00)", "head"),
    ("SCREEN", "[Show prompt: 'Create a 30-day study plan for DBMS exam' → show output]", "dir"),
    ("SPEAK", "Paanchwa aur last tool — AI study planner. Sirf apna subject aur exam date batao, "
              "aur ChatGPT ek complete day-wise plan bana deta hai. "
              "Ye mera personal favorite hai exam season mein.", "body"),

    ("OUTRO", "OUTRO + CTA (9:00–end)", "head"),
    ("SCREEN", "[Show all 5 tool names on screen as list]", "dir"),
    ("SPEAK", "Toh yahi the 5 AI tools jo tumhe 2026 mein zaroor use karne chahiye. "
              "Inka poora list main pinned comment mein dalunga — bilkul free. "
              "Agar ye video helpful lagi toh Like karo — seriously, ek like se bahut fark padta hai. "
              "Subscribe karo kyunki main aisi hi practical videos laata rehta hun. "
              "Aur comment karo — 'TOOLS' — main list bhejunga. "
              "Next video mein main dikhaunga coding ka roadmap — web dev, Python, ya data — "
              "kya choose karna chahiye? Tab tak — stay curious!", "body"),
]
story.append(script_block(script1))
story.append(SP(8))

story.append(colored_box([
    Paragraph("&#128204; <b>Pin in Comment:</b>", body_b),
    Paragraph("Tool 1: [NotesAI name + link]", bullet),
    Paragraph("Tool 2: Gamma.app (gamma.app)", bullet),
    Paragraph("Tool 3: ChatGPT prompt: 'Turn this into 3 ATS resume bullets: [your text]'", bullet),
    Paragraph("Tool 4: Grammarly.com (free tier)", bullet),
    Paragraph("Tool 5: ChatGPT prompt: 'Create 30-day plan for [subject] exam on [date]'", bullet),
], bg=colors.HexColor("#E3F2FD"), padding=10))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 06 — VIDEO 2 FULL SCRIPT
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("06 — VIDEO 2: FULL SCRIPT",
    "Coding Roadmap for Beginners (0 to Job) — Long Video, 10–15 min", BLUE))
story.append(SP(10))

meta2 = [
    [Paragraph("<b>Title</b>", body_b),
     Paragraph("Coding Roadmap for Beginners (0 to Job): Web Dev vs Python vs Data — What to Choose?", body)],
    [Paragraph("<b>Duration</b>", body_b), Paragraph("10–15 minutes", body)],
    [Paragraph("<b>Goal</b>", body_b), Paragraph("Builds authority + long-term subscriber loyalty", body)],
    [Paragraph("<b>CTA</b>", body_b), Paragraph("'Comment your background — I'll suggest your path'", body)],
    [Paragraph("<b>Thumbnail</b>", body_b), Paragraph("0 to Job Roadmap · Choose the Right Path", body)],
]
meta_t2 = Table(meta2, colWidths=[30*mm, doc.width-30*mm])
meta_t2.setStyle(TableStyle([
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [meta_t2, SP(10)]

story.append(Paragraph("Complete Script", sub_head))
story.append(hr(BLUE))

script2 = [
    ("INTRO", "HOOK (0:00–0:30)", "head"),
    ("SCREEN", "[Show confused student choosing between laptop screens showing code]", "dir"),
    ("SPEAK", "Tumne decide kar liya ki coding seekhni hai. Bahut acchi baat hai. "
              "Lekin phir tum Google karte ho — aur confuse ho jaate ho. "
              "'Web development seekhun ya Python? Python seekhun ya Data Science?' "
              "Aaj main ye confusion hamesha ke liye khatam kar deta hun. "
              "Main tumhe 3 clear paths dikhaunga — aur bataunga ki tumhare liye kaunsa best hai.", "body"),

    ("SECTION 1", "PATH 1 — WEB DEVELOPMENT (0:30–4:00)", "head"),
    ("SCREEN", "[Show logos: HTML, CSS, JavaScript, React, Node.js in order]", "dir"),
    ("SPEAK", "Pehla path hai Web Development. Agar tumhara sapna hai — "
              "websites aur apps banana, freelancing karna, ya startup mein join karna — "
              "toh yahi path hai tumhare liye.", "body"),
    ("SCREEN", "[Show 30-day roadmap: Week 1-2: HTML+CSS, Week 3-4: JS basics]", "dir"),
    ("SPEAK", "30-day starter plan: Pehle 2 hafte — HTML aur CSS seekho, ek website banao. "
              "3rd week — JavaScript basics. 4th week — ek interactive project. "
              "Resources: freeCodeCamp, The Odin Project — dono free hain.", "body"),
    ("SCREEN", "[Show who it's for — checklist style]", "dir"),
    ("SPEAK", "Web Dev choose karo agar: tum visuals pasand karte ho, "
              "jaldi results chahiye, aur freelancing mein interested ho. "
              "Average fresher salary: 3–5 LPA. With 1 year experience: 6–10 LPA.", "body"),

    ("SECTION 2", "PATH 2 — PYTHON + AUTOMATION (4:00–7:30)", "head"),
    ("SCREEN", "[Show Python logo + automation gif + data graph]", "dir"),
    ("SPEAK", "Doosra path hai Python. Ye sabse flexible language hai aaj ke time mein. "
              "Python se tum websites bana sakte ho, automation scripts likh sakte ho, "
              "aur agar aage jaana ho toh Data Science aur AI bhi kar sakte ho.", "body"),
    ("SPEAK", "30-day starter: Week 1 — Python basics (variables, loops, functions). "
              "Week 2 — File handling aur simple scripts. "
              "Week 3 — Web scraping ya automation project. "
              "Week 4 — 1 complete mini-project on GitHub.", "body"),
    ("SPEAK", "Python choose karo agar: tum logic aur problem-solving enjoy karte ho, "
              "ya government/corporate job mein jaana chahte ho. "
              "Average fresher: 3.5–6 LPA. Python + ML: 6–12 LPA.", "body"),

    ("SECTION 3", "PATH 3 — DATA SCIENCE / ML BASICS (7:30–10:00)", "head"),
    ("SCREEN", "[Show graphs, Jupyter notebook, model accuracy chart]", "dir"),
    ("SPEAK", "Teesra path — Data Science aur Machine Learning. "
              "Ye sabse high-paying hai — lekin sabse zyada time bhi laggta hai. "
              "Pehle Python seekho. Phir statistics thoda. Phir pandas, numpy, matplotlib. "
              "Tab jaake ML algorithms.", "body"),
    ("SPEAK", "Ye path mat chuno agar tum pehle coding hi nahi jaante. "
              "Pehle Python seekho — 3 mahine — tab ye path consider karo. "
              "Data Analyst fresher: 4–8 LPA. ML Engineer: 8–18 LPA.", "body"),

    ("SECTION 4", "COMMON MISTAKES (10:00–11:30)", "head"),
    ("SCREEN", "[Red X marks on screen for each mistake]", "dir"),
    ("SPEAK", "Ab kuch common mistakes jo beginners karte hain. "
              "Mistake 1: Tutorial hell — sirf videos dekhte rehna, khud code nahi karna. "
              "Fix: Har 2 tutorials ke baad ek project banao. "
              "Mistake 2: 3 cheezein ek saath seekhna. Fix: Ek path, ek mahina. "
              "Mistake 3: GitHub use na karna. Fix: Day 1 se hi GitHub pe code upload karo.", "body"),

    ("OUTRO", "OUTRO + CTA (11:30–end)", "head"),
    ("SCREEN", "[Show all 3 paths as comparison table]", "dir"),
    ("SPEAK", "Toh decision simple hai: "
              "Websites + freelancing chahiye? Web Dev. "
              "Logic + flexibility + AI future chahiye? Python. "
              "Maximum salary + patience hai? Data Science — but Python pehle. "
              "Comment karo apna background — 10th/12th/college/working — "
              "main personally suggest karunga kaunsa path tumhare liye best hai. "
              "Like karo agar ye helpful laga. Subscribe karo — aur next video mein "
              "main dikhaunga first project kaise banate hain. Milte hain!", "body"),
]
story.append(script_block(script2))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 07 — SHORT SCRIPT 1
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("07 — SHORT SCRIPT: RESUME IN 60 SECONDS",
    "30–45 second Short — High share potential", RED))
story.append(SP(8))

story.append(Paragraph(
    "<b>Title:</b> 'Make a Resume in 60 Seconds using AI (Free)' &nbsp;&nbsp; "
    "<b>Duration:</b> 30–45s &nbsp;&nbsp; <b>CTA:</b> Comment 'RESUME'", body))
story.append(SP(6))

short1 = [
    ("HOOK", "0–3s: [Show blank resume + stressed face emoji]", "head"),
    ("SPEAK", "Freshers! Stop writing resume from scratch in 2026.", "body"),
    ("PROMPT", "3–8s: [Type on screen — big text:]", "dir"),
    ("TEXT", "'Turn this into 3 professional ATS-friendly resume bullets:\nI built a student attendance system using Python + Flask + MySQL'", "body"),
    ("DEMO", "8–25s: [Paste prompt into ChatGPT → show output appearing in 3 seconds]", "dir"),
    ("RESULT", "25–35s: [Highlight the 3 bullets → copy-paste into resume template]", "dir"),
    ("SPEAK", "Done. 3 bullets. ATS-ready. Under a minute.", "body"),
    ("CTA", "35–40s: [Text on screen] Comment 'RESUME' — I'll send you the exact prompt + template.", "body"),
]
story.append(script_block(short1))
story.append(SP(8))

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 08 — SHORT SCRIPT 2
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("08 — SHORT SCRIPT: 3 VS CODE EXTENSIONS",
    "35–50 second Short — High save rate", ACCENT))
story.append(SP(8))

story.append(Paragraph(
    "<b>Title:</b> '3 VS Code Extensions Every Beginner Must Use' &nbsp;&nbsp; "
    "<b>Duration:</b> 35–50s &nbsp;&nbsp; <b>CTA:</b> Comment 'SETUP'", body))
story.append(SP(6))

short2 = [
    ("HOOK", "0–3s: [VS Code open on screen]", "head"),
    ("SPEAK", "If you code without these 3 extensions, you are wasting time.", "body"),
    ("EXT 1", "3–17s: Install 'Prettier'", "dir"),
    ("SPEAK", "Number 1 — Prettier. Auto-formats your messy code instantly. "
              "One save — clean code. No more manual indentation.", "body"),
    ("EXT 2", "17–30s: Install 'Live Server'", "dir"),
    ("SPEAK", "Number 2 — Live Server. Your HTML page auto-refreshes every time you save. "
              "No more pressing F5 like a maniac.", "body"),
    ("EXT 3", "30–43s: Install 'Error Lens'", "dir"),
    ("SPEAK", "Number 3 — Error Lens. Shows errors inline — right next to the line. "
              "You'll fix bugs 3x faster. Seriously.", "body"),
    ("CTA", "43–50s:", "head"),
    ("SPEAK", "Comment 'SETUP' and I'll share my complete VS Code config file — for free.", "body"),
]
story.append(script_block(short2))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 09 — SHORT SCRIPT 3
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("09 — SHORT SCRIPT: GIT & GITHUB IN 40 SECONDS",
    "Educational Short — Chain to next video", PURPLE))
story.append(SP(8))

story.append(Paragraph(
    "<b>Title:</b> 'Git & GitHub in 40 Seconds (Super Simple)' &nbsp;&nbsp; "
    "<b>Duration:</b> 35–45s &nbsp;&nbsp; <b>CTA:</b> Follow for Part 2", body))
story.append(SP(6))

short3 = [
    ("HOOK", "0–3s: [Text on screen: GitHub is NOT just a coding website]", "head"),
    ("SPEAK", "Most beginners think GitHub is just a website to store code. Nope.", "body"),
    ("GIT", "3–15s: [Animate: folders → timeline with versions]", "dir"),
    ("SPEAK", "Git is like an undo button for your entire project. "
              "Every change you save is tracked. You can go back to any version — any time.", "body"),
    ("GITHUB", "15–28s: [Animate: laptop → cloud → two laptops syncing]", "dir"),
    ("SPEAK", "GitHub is the cloud + the collaboration platform. "
              "Your project lives there. Your team can contribute. Employers can see your work.", "body"),
    ("REAL", "28–37s: [Show 1 real repo — show commit history]", "dir"),
    ("SPEAK", "Real example: Every save here is one commit. Timeline of your progress. Employers LOVE this.", "body"),
    ("CTA", "37–43s:", "head"),
    ("SPEAK", "Follow me — next Short: how to upload your first project to GitHub. Step by step.", "body"),
]
story.append(script_block(short3))
story.append(SP(10))

story.append(colored_box([
    Paragraph("&#128279; <b>Chain Strategy:</b> After this Short → record these in order:", body_b),
    Paragraph("Part 2: 'Upload your first project to GitHub (beginner)'", bullet),
    Paragraph("Part 3: 'Host your project on GitHub Pages — free website!'", bullet),
    Paragraph("Part 4: 'GitHub profile for freshers — make it recruiter-ready'", bullet),
    SP(3),
    Paragraph("Chained content = viewers subscribe to see the next part. Very powerful for growth.", note),
], bg=colors.HexColor("#EDE7F6"), padding=10))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 10 — 20 SHORTS IDEAS
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("10 — 20 SHORTS IDEAS BANK",
    "Ready-to-record topics — first 2–3 weeks", GREEN))
story.append(SP(10))

ideas = [
    ("01", "Top 3 free AI tools for students", "List + demo", "Use format B (3 tips)"),
    ("02", "Remove background from image for free", "Tool demo", "1 Problem → 1 Tool → 1 Result"),
    ("03", "Make resume bullets using AI (1 prompt)", "ChatGPT demo", "CTA: Comment 'RESUME'"),
    ("04", "Best Chrome extensions for productivity", "3 extensions show", "High save rate"),
    ("05", "Convert speech to text on phone (fast)", "App demo", "Very relatable for students"),
    ("06", "3 Google Docs shortcut keys", "Screen recording", "Lots of saves/shares"),
    ("07", "VS Code: auto format code in 1 setting", "Show Prettier setup", "Developer niche"),
    ("08", "Deploy site on GitHub Pages (overview)", "Teaser → long video", "CTA to full tutorial"),
    ("09", "What is API in 30 seconds", "Animation/text", "Educational — comment magnet"),
    ("10", "What is Cloud Computing in 30 seconds", "Animation/text", "High search volume"),
    ("11", "ChatGPT prompt to learn anything faster", "Prompt + demo", "Viral potential"),
    ("12", "Best website for learning roadmaps", "Show roadmap.sh", "Very useful, lots of saves"),
    ("13", "LinkedIn headline formula for freshers", "Before/After", "Career niche"),
    ("14", "Common resume mistake (and the fix)", "Myth vs fact style", "High comment engagement"),
    ("15", "Top 3 project ideas for beginners", "List format", "Questions flood in comments"),
    ("16", "How to create a QR code for free", "Quick demo", "Easy to make, high views"),
    ("17", "Best free certificate platforms (honest)", "Show 3 sites", "'Honest' = trust building"),
    ("18", "How to make study timetable in Notion", "Screen recording", "Notion niche + students"),
    ("19", "Tech term of the day: Git", "Text animation + explain", "Series potential"),
    ("20", "Tech term of the day: Repository", "Text animation + explain", "Follow-up to #19"),
]

idea_header = [
    Paragraph("<b>#</b>", body_b),
    Paragraph("<b>Topic</b>", body_b),
    Paragraph("<b>Format/Demo</b>", body_b),
    Paragraph("<b>Why it works</b>", body_b),
]
idea_rows = [idea_header]
for num, topic, fmt, why in ideas:
    idea_rows.append([
        Paragraph(num, ParagraphStyle("_n", fontSize=10, textColor=RED,
                   fontName="Helvetica-Bold")),
        Paragraph(topic, body),
        Paragraph(fmt, ParagraphStyle("_f", fontSize=9, textColor=BLUE,
                   fontName="Helvetica")),
        Paragraph(why, ParagraphStyle("_w", fontSize=9, textColor=GRAY,
                   fontName="Helvetica-Oblique")),
    ])

idea_t = Table(idea_rows, colWidths=[10*mm, 60*mm, 42*mm, doc.width-112*mm])
idea_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), DARK),
    ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [idea_t, PageBreak()]

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 11 — THUMBNAIL & TITLE FORMULAS
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("11 — THUMBNAIL & TITLE FORMULAS",
    "CTR-boosting frameworks that actually work", ACCENT))
story.append(SP(10))

story.append(Paragraph("Title Formulas (High CTR)", sub_head))
story.append(hr(ACCENT))

title_formulas = [
    ("[Number] + [Topic] + [Benefit] + (Year)",
     "'5 AI Tools for Students (2026)' — Numbers + year = high CTR"),
    ("How to [Action] in [Time] (Free/For Beginners)",
     "'How to Build a Website in 30 Minutes (Free + Beginner)'"),
    ("[Mistake/Problem] + Fix it with [Solution]",
     "'Resume Mistake Every Fresher Makes (Fix with AI)'"),
    ("From [Zero State] to [Goal]: Complete [Topic] Guide",
     "'From Zero to First Job: Complete Python Roadmap 2026'"),
    ("Stop [Bad Habit] — Do This Instead",
     "'Stop Googling Errors — Use This VS Code Extension Instead'"),
]

for formula, example in title_formulas:
    story.append(colored_box([
        Paragraph(f"<b>Formula:</b> {formula}", body_b),
        Paragraph(f"<b>Example:</b> {example}", note),
    ], bg=SOFT_BG, padding=8))
    story.append(SP(4))

story.append(SP(6))
story.append(Paragraph("Thumbnail Rules", sub_head))
story.append(hr(ACCENT))

thumb_rules = [
    "Use Montserrat Bold or Impact for main text — always",
    "Max 4–6 words on thumbnail — people see it for 2 seconds",
    "Your face + surprise/happy expression = higher CTR",
    "Use 1 icon or visual element (robot, laptop, arrow)",
    "Dark background + bright text OR bright background + dark text",
    "Keep a consistent template — same font, same layout always",
    "Use contrast — red/yellow on dark background works best",
    "Test with a 'squint test' — can you read it when blurry?",
]
story += [SP(4), checklist_table(thumb_rules, cols=2), PageBreak()]

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 12 — GEAR & TOOLS
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("12 — GEAR & FREE TOOL STACK",
    "Everything you need to start — most are free", DARK))
story.append(SP(10))

tools_data = [
    [Paragraph("<b>Category</b>", body_b), Paragraph("<b>Tool</b>", body_b),
     Paragraph("<b>Cost</b>", body_b), Paragraph("<b>Use for</b>", body_b)],
    [Paragraph("Recording", body), Paragraph("Your Phone (720p+)", body),
     Paragraph("Free", body), Paragraph("Shorts recording", body)],
    [Paragraph("Screen Record", body), Paragraph("OBS Studio (PC)", body),
     Paragraph("Free", body), Paragraph("Long video tutorials", body)],
    [Paragraph("Screen Record", body), Paragraph("Built-in screen record (phone)", body),
     Paragraph("Free", body), Paragraph("Mobile Shorts", body)],
    [Paragraph("Mic", body), Paragraph("Earphones with mic", body),
     Paragraph("You already have", body), Paragraph("Start with this", body)],
    [Paragraph("Editing", body), Paragraph("CapCut (mobile)", body),
     Paragraph("Free", body), Paragraph("Shorts editing", body)],
    [Paragraph("Editing", body), Paragraph("VN Video Editor", body),
     Paragraph("Free", body), Paragraph("Shorts + long", body)],
    [Paragraph("Thumbnail", body), Paragraph("Canva (free tier)", body),
     Paragraph("Free", body), Paragraph("All thumbnails", body)],
    [Paragraph("Script", body), Paragraph("Google Docs", body),
     Paragraph("Free", body), Paragraph("Write scripts", body)],
    [Paragraph("Resources", body), Paragraph("Google Drive", body),
     Paragraph("Free", body), Paragraph("Share notes/PDFs", body)],
    [Paragraph("Analytics", body), Paragraph("YouTube Studio", body),
     Paragraph("Free", body), Paragraph("Track performance", body)],
    [Paragraph("AI help", body), Paragraph("ChatGPT (free tier)", body),
     Paragraph("Free", body), Paragraph("Scripts, titles, ideas", body)],
]
tools_t = Table(tools_data, colWidths=[28*mm, 45*mm, 22*mm, doc.width-95*mm])
tools_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), DARK),
    ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
    ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ("TOPPADDING",    (0,0),(-1,-1), 6),
    ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
]))
story += [tools_t, SP(8)]

story.append(colored_box([
    Paragraph("&#128161; <b>Upgrade when ready (optional):</b>", body_b),
    Paragraph("Mic upgrade: Boya BY-M1 lavalier mic (~Rs. 800–1200) — huge audio quality jump", bullet),
    Paragraph("Editing upgrade: DaVinci Resolve (free, PC) for long videos", bullet),
    Paragraph("Canva Pro (~Rs. 500/month) — more templates, remove background", bullet),
    Paragraph("ChatGPT Plus (~Rs. 1700/month) — faster + GPT-4 for better scripts", bullet),
], bg=colors.HexColor("#E8F5E9"), padding=10))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 13 — MONETIZATION
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("13 — MONETIZATION ROADMAP",
    "How to start earning in 90 days (ethical + realistic)", GREEN))
story.append(SP(10))

mono_streams = [
    ("YouTube AdSense", "1,000 subs + 4,000 hrs OR 1,000 subs + 10M Short views",
     "Apply as soon as you hit threshold",
     "Est. Rs. 50–200 per 1000 views (India traffic)"),
    ("Affiliate Marketing", "No minimum subs needed — start Day 1",
     "Canva, Hostinger, Notion, Grammarly all have affiliate programs",
     "Rs. 200–2000 per referral depending on product"),
    ("Digital Products", "50+ engaged subscribers",
     "Sell PDF roadmaps, template packs, Notion templates",
     "Rs. 99–499 per sale — 100% profit"),
    ("Freelance Services", "Portfolio of 5+ videos = proof of skill",
     "Offer: Resume review, LinkedIn optimization, tech guidance",
     "Rs. 300–1000 per session (start low, raise with experience)"),
    ("Sponsorships", "5,000–10,000 subscribers",
     "Approach: AI tools, hosting companies, e-learning platforms",
     "Rs. 5,000–50,000 per video (micro-influencer range)"),
]

for stream, when, how, earn in mono_streams:
    rows = [
        [Paragraph(f"<b>{stream}</b>", ParagraphStyle("_ms", fontSize=12, textColor=WHITE,
                    fontName="Helvetica-Bold")), ""],
        [Paragraph("<b>When to start:</b>", body_b), Paragraph(when, body)],
        [Paragraph("<b>How:</b>", body_b), Paragraph(how, body)],
        [Paragraph("<b>Earnings est:</b>", body_b),
         Paragraph(earn, ParagraphStyle("_earn", fontSize=10, textColor=GREEN,
                    fontName="Helvetica-Bold"))],
    ]
    t = Table(rows, colWidths=[32*mm, doc.width-32*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), DARK),
        ("SPAN",          (0,0),(-1,0)),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LGRAY, WHITE]),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ("INNERGRID",     (0,1),(-1,-1), 0.3, colors.HexColor("#EEEEEE")),
    ]))
    story += [t, SP(6)]

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 14 — ANALYTICS CHECKLIST
# ════════════════════════════════════════════════════════════════════════════
story.append(chapter_banner("14 — WEEKLY ANALYTICS CHECKLIST",
    "Know your numbers. Improve every week.", RED))
story.append(SP(10))

story.append(Paragraph("Check These Every Sunday — 30 Minutes", sub_head))
story.append(hr(RED))

analytics_checks = [
    "Shorts: Average view duration (goal: >50%)",
    "Shorts: Swipe-away rate in first 2 seconds",
    "Long videos: Audience retention graph (where do they drop off?)",
    "Long videos: Click-through rate on thumbnail (goal: 4–8%)",
    "Overall: Subscriber growth this week",
    "Which video got the most impressions?",
    "Which video got the most watch time?",
    "How many comments did you get? Did you reply to all?",
    "Did your CTA keyword work? (count comment keywords)",
    "Top traffic source: YouTube Search vs Shorts feed vs Browse",
    "Most liked video this week — replicate the format",
    "Worst performing video — what was different?",
]
story += [SP(4), checklist_table(analytics_checks, cols=1)]

story.append(SP(8))
story.append(Paragraph("Questions to Ask Yourself Every Week", sub_head))
story.append(hr(RED))
weekly_qs = [
    "Which video would I watch again? — Make more like that.",
    "What did viewers comment most? — That's your next video topic.",
    "Did I stick to my posting schedule? If not — why not? Fix it.",
    "What can I improve: thumbnail, hook, or CTA?",
    "Did I engage with any other creators this week?",
]
for q in weekly_qs:
    story.append(Paragraph(f"&#10067; {q}", bullet))

story.append(SP(12))

# ── FINAL MOTIVATIONAL PAGE ────────────────────────────────────────────────
final = Table([[
    Paragraph("You have everything you need.", ParagraphStyle("_f1", fontSize=18,
               textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=24)),
    ],[
    Paragraph("The only thing left is to press Record.", ParagraphStyle("_f2", fontSize=14,
               textColor=colors.HexColor("#FFD54F"), fontName="Helvetica-BoldOblique",
               alignment=TA_CENTER, leading=20)),
    ],[
    Spacer(1, 10),
    ],[
    Paragraph("Your first video doesn't need to be perfect. It needs to exist.", ParagraphStyle("_f3",
               fontSize=11, textColor=colors.HexColor("#B0BEC5"), fontName="Helvetica",
               alignment=TA_CENTER, leading=16)),
    ],[
    Spacer(1, 6),
    ],[
    Paragraph("Start with Short #1. Do it today.", ParagraphStyle("_f4", fontSize=13,
               textColor=ACCENT, fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ],
], colWidths=[doc.width])
final.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), DARK),
    ("TOPPADDING",    (0,0),(-1,-1), 16),
    ("BOTTOMPADDING", (0,0),(-1,-1), 16),
    ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ("RIGHTPADDING",  (0,0),(-1,-1), 20),
    ("ROUNDEDCORNERS",[8]),
]))
story += [SP(16), final, SP(8)]

story.append(Paragraph(
    "PDF created for Avinash  ·  YouTube Channel Launch Guide 2026  ·  All content is original and personalised.",
    footer_style))

# ── BUILD ─────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF created successfully!")
