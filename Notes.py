from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor, white, black

# ─── Palette ─────────────────────────────────────────────────
NAVY      = HexColor("#1A3C5E")
BLUE      = HexColor("#2E75B6")
TEAL      = HexColor("#1F7A8C")
GREEN     = HexColor("#1E7A4F")
ORANGE    = HexColor("#D45F00")
PURPLE    = HexColor("#5B3087")
RED       = HexColor("#C0392B")
GOLD      = HexColor("#B8860B")
LIGHT     = HexColor("#EBF3FB")
TEAL_BG   = HexColor("#E0F2F5")
GREEN_BG  = HexColor("#E6F4EE")
PURPLE_BG = HexColor("#F0EAF8")
ORANGE_BG = HexColor("#FEF0E6")
CODE_BG   = HexColor("#0D1117")
CODE_HEADER = HexColor("#161B22")
ALT_ROW   = HexColor("#F2F7FC")
BORDER    = HexColor("#CBD5E1")
DARK      = HexColor("#1E293B")
MUTED     = HexColor("#64748B")
CPP_KW    = HexColor("#FF7B72")   # red  – keywords
CPP_TYPE  = HexColor("#79C0FF")   # blue – types
CPP_CMT   = HexColor("#8B949E")   # grey – comments
CPP_STR   = HexColor("#A5D6FF")   # light blue – strings
CPP_NUM   = HexColor("#F8C83A")   # yellow – numbers
CPP_FN    = HexColor("#D2A8FF")   # purple – function names
CODE_FG   = HexColor("#E6EDF3")   # default text

W, H = A4

# ─── Header / Footer ─────────────────────────────────────────
def first_page(c, doc):
    _draw_chrome(c, doc)

def later_pages(c, doc):
    _draw_chrome(c, doc)

def _draw_chrome(c, doc):
    c.saveState()
    # Header
    c.setFillColor(NAVY)
    c.rect(0, H - 26*mm, W, 26*mm, fill=1, stroke=0)
    # Accent stripe
    c.setFillColor(TEAL)
    c.rect(0, H - 28*mm, W, 2*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, H - 16*mm, "DSA Notes — Two Pointers & Sliding Window")
    c.setFont("Helvetica", 9)
    c.drawRightString(W - 15*mm, H - 16*mm, "Topic 2 of 13")
    # Footer
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 12*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica", 8)
    c.drawString(15*mm, 4*mm, "DSA Revision Planner  •  C++ Code Edition")
    c.drawRightString(W - 15*mm, 4*mm, f"Page {doc.page}")
    c.restoreState()

# ─── Custom Flowables ─────────────────────────────────────────
class SectionBanner(Flowable):
    def __init__(self, num, title, color=NAVY, accent=TEAL):
        super().__init__()
        self.num = num
        self.title = title
        self.color = color
        self.accent = accent
        self.width = W - 30*mm
        self.bh = 14*mm

    def wrap(self, *args):
        return self.width, self.bh + 4*mm

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 2*mm, self.width, self.bh, 3*mm, fill=1, stroke=0)
        c.setFillColor(self.accent)
        c.roundRect(0, 2*mm, 10*mm, self.bh, 3*mm, fill=1, stroke=0)
        c.rect(7*mm, 2*mm, 3*mm, self.bh, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(13*mm, 2*mm + self.bh/2 - 1.5*mm, self.num)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(28*mm, 2*mm + self.bh/2 - 2*mm, self.title)


class SubBanner(Flowable):
    def __init__(self, text, color=BLUE, bg=LIGHT):
        super().__init__()
        self.text = text
        self.color = color
        self.bg = bg
        self.width = W - 30*mm
        self.bh = 9*mm

    def wrap(self, *args):
        return self.width, self.bh + 3*mm

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 1.5*mm, self.width, self.bh, 2*mm, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 1.5*mm, 4*mm, self.bh, 1.5*mm, fill=1, stroke=0)
        c.rect(2*mm, 1.5*mm, 2*mm, self.bh, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(8*mm, 1.5*mm + self.bh/2 - 2*mm, self.text)


class CppCodeBlock(Flowable):
    """C++ syntax-aware code block with dark theme."""
    KEYWORDS = {
        'int','long','long long','bool','char','void','string','vector','map',
        'unordered_map','set','unordered_set','pair','auto','const','return',
        'if','else','while','for','do','break','continue','class','struct',
        'public','private','true','false','nullptr','new','delete','include',
        'using','namespace','std','endl','size_t','template','typename',
        'static','inline','unsigned','short','double','float','deque','queue',
        'stack','priority_queue','multiset','multimap','sort','max','min',
        'swap','reverse','lower_bound','upper_bound','find','push_back',
        'pop_back','push','pop','top','front','back','begin','end','empty',
        'size','insert','erase','count','clear','emplace_back'
    }

    def __init__(self, lines, width=None):
        super().__init__()
        self.lines = lines
        self._w = width or (W - 30*mm)
        self.lh = 4.6*mm
        self.hh = 7*mm
        self.pad = 4*mm

    def wrap(self, *args):
        return self._w, self.hh + self.pad + len(self.lines)*self.lh + self.pad

    def draw(self):
        c = self.canv
        th = self.hh + self.pad + len(self.lines)*self.lh + self.pad

        # Background
        c.setFillColor(CODE_BG)
        c.roundRect(0, 0, self._w, th, 3*mm, fill=1, stroke=0)

        # Header bar
        c.setFillColor(CODE_HEADER)
        c.roundRect(0, th - self.hh, self._w, self.hh, 3*mm, fill=1, stroke=0)
        c.rect(0, th - self.hh, self._w, self.hh/2, fill=1, stroke=0)

        # Lang tag
        c.setFillColor(CPP_TYPE)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, th - self.hh + 2.2*mm, "C++")

        # Traffic dots
        for i, col in enumerate([HexColor("#FF5F57"), HexColor("#FEBC2E"), HexColor("#28C840")]):
            c.setFillColor(col)
            c.circle(self._w - (3-i)*5.5*mm, th - self.hh/2, 1.4*mm, fill=1, stroke=0)

        # Code lines
        y = th - self.hh - self.pad - self.lh
        for idx, raw in enumerate(self.lines):
            # Line number
            c.setFillColor(HexColor("#3D444D"))
            c.setFont("Courier", 7.5)
            c.drawString(3*mm, y + 1.2*mm, f"{idx+1:2d}")

            stripped = raw.lstrip()
            indent_n = len(raw) - len(stripped)
            x = 12*mm + indent_n * 2.2*mm

            # Simple tokenizer
            self._draw_line(c, stripped, x, y + 1.2*mm)
            y -= self.lh

    def _draw_line(self, c, text, x, y):
        import re
        # Comment detection
        if '//' in text:
            cmt_pos = text.index('//')
            code_part = text[:cmt_pos]
            cmt_part  = text[cmt_pos:]
            x = self._draw_tokens(c, code_part, x, y)
            c.setFillColor(CPP_CMT)
            c.setFont("Courier-Oblique", 8.5)
            c.drawString(x, y, cmt_part)
            return

        # Preprocessor
        if text.startswith('#'):
            c.setFillColor(CPP_KW)
            c.setFont("Courier-Bold", 8.5)
            c.drawString(x, y, text)
            return

        self._draw_tokens(c, text, x, y)

    def _draw_tokens(self, c, text, x, y):
        import re
        tokens = re.findall(r'[A-Za-z_]\w*|"[^"]*"|\'[^\']*\'|\d+\.\d+|\d+|[^\w\s]|\s+', text)
        for tok in tokens:
            if not tok:
                continue
            if tok.strip() == '':
                c.setFont("Courier", 8.5)
                x += c.stringWidth(tok, "Courier", 8.5)
                continue

            # Choose color
            if tok in self.KEYWORDS:
                c.setFillColor(CPP_KW)
                c.setFont("Courier-Bold", 8.5)
            elif tok.startswith('"') or tok.startswith("'"):
                c.setFillColor(CPP_STR)
                c.setFont("Courier", 8.5)
            elif tok.isdigit() or (tok.replace('.','',1).isdigit()):
                c.setFillColor(CPP_NUM)
                c.setFont("Courier", 8.5)
            elif len(tok) > 1 and tok[0].islower() and '(' in ''.join([]):
                c.setFillColor(CPP_FN)
                c.setFont("Courier", 8.5)
            else:
                c.setFillColor(CODE_FG)
                c.setFont("Courier", 8.5)

            w = c.stringWidth(tok, "Courier", 8.5)
            c.drawString(x, y, tok)
            x += w
        return x


class InfoBox(Flowable):
    def __init__(self, lines, title="", color=BLUE, bg=LIGHT, width=None):
        super().__init__()
        self.lines = lines if isinstance(lines, list) else [lines]
        self.title = title
        self.color = color
        self.bg = bg
        self._w = width or (W - 30*mm)
        self.pad = 4*mm
        self.lh = 5.2*mm

    def wrap(self, *args):
        th = 5.5*mm if self.title else 0
        return self._w, self.pad + th + len(self.lines)*self.lh + self.pad

    def draw(self):
        c = self.canv
        th = 5.5*mm if self.title else 0
        total = self.pad + th + len(self.lines)*self.lh + self.pad
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self._w, total, 2*mm, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 0, 3.5*mm, total, 1.5*mm, fill=1, stroke=0)
        c.rect(2*mm, 0, 1.5*mm, total, fill=1, stroke=0)
        y = total - self.pad
        if self.title:
            c.setFillColor(self.color)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(7*mm, y - 4.5*mm, self.title)
            y -= 5.5*mm
        c.setFillColor(DARK)
        c.setFont("Helvetica", 8.8)
        for line in self.lines:
            c.drawString(7*mm, y - 4*mm, line)
            y -= self.lh


class VisualBox(Flowable):
    """Draw an array/pointer visualization."""
    def __init__(self, cells, pointers=None, label="", color=TEAL, width=None):
        super().__init__()
        self.cells = cells       # list of strings
        self.pointers = pointers or {}  # index -> label
        self.label = label
        self.color = color
        self._w = width or (W - 30*mm)
        self.cell_h = 10*mm
        self.ptr_h  = 8*mm

    def wrap(self, *args):
        return self._w, self.cell_h + self.ptr_h + (6*mm if self.label else 0)

    def draw(self):
        c = self.canv
        n = len(self.cells)
        cell_w = min(14*mm, (self._w - 20*mm) / n)
        start_x = (self._w - n * cell_w) / 2
        base_y = self.ptr_h

        # Cells
        for i, val in enumerate(self.cells):
            x = start_x + i * cell_w
            highlighted = i in self.pointers
            c.setFillColor(self.color if highlighted else HexColor("#1E293B"))
            c.setStrokeColor(self.color)
            c.setLineWidth(1.2)
            c.rect(x, base_y, cell_w, self.cell_h, fill=1, stroke=1)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold" if highlighted else "Helvetica", 9)
            tw = c.stringWidth(str(val), "Helvetica-Bold", 9)
            c.drawString(x + cell_w/2 - tw/2, base_y + 3*mm, str(val))

        # Index labels
        for i in range(n):
            x = start_x + i * cell_w
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 7)
            iw = c.stringWidth(str(i), "Helvetica", 7)
            c.drawString(x + cell_w/2 - iw/2, base_y - 4*mm, str(i))

        # Pointer arrows
        for idx, ptr_label in self.pointers.items():
            x = start_x + idx * cell_w + cell_w/2
            c.setFillColor(self.color)
            c.setStrokeColor(self.color)
            c.setLineWidth(1.5)
            c.line(x, base_y + self.cell_h + 1*mm, x, base_y + self.cell_h + 5*mm)
            c.setFont("Helvetica-Bold", 8)
            lw = c.stringWidth(ptr_label, "Helvetica-Bold", 8)
            c.drawString(x - lw/2, base_y + self.cell_h + 5.5*mm, ptr_label)

        if self.label:
            c.setFillColor(MUTED)
            c.setFont("Helvetica-Oblique", 8)
            lw = c.stringWidth(self.label, "Helvetica-Oblique", 8)
            c.drawString(self._w/2 - lw/2, 0, self.label)


# ─── Styles ─────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.5, textColor=DARK,
                leading=14, spaceBefore=3, spaceAfter=3)
    base.update(kw)
    return ParagraphStyle(name, **base)

ST = {
    "h1": S("h1", fontName="Helvetica-Bold", fontSize=20, textColor=NAVY, leading=26, spaceBefore=14, spaceAfter=6),
    "h2": S("h2", fontName="Helvetica-Bold", fontSize=14, textColor=BLUE, leading=20, spaceBefore=10, spaceAfter=4),
    "h3": S("h3", fontName="Helvetica-Bold", fontSize=11.5, textColor=TEAL, leading=16, spaceBefore=8, spaceAfter=3),
    "h4": S("h4", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=14, spaceBefore=6, spaceAfter=2),
    "body": S("body", alignment=TA_JUSTIFY, leading=15),
    "bullet": S("bullet", leftIndent=12, firstLineIndent=-8, leading=13, spaceBefore=2, spaceAfter=2),
    "caption": S("caption", fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED, spaceBefore=2, spaceAfter=6),
    "toc_h": S("toc_h", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY, spaceBefore=5, spaceAfter=2, leading=15),
    "toc_i": S("toc_i", fontSize=9.5, textColor=DARK, spaceBefore=1, spaceAfter=1, leftIndent=8, leading=13),
    "note":  S("note",  fontName="Helvetica-Oblique", fontSize=9, textColor=MUTED),
    "cover_title": S("ct", fontName="Helvetica-Bold", fontSize=34, textColor=white, leading=40, alignment=TA_CENTER),
    "cover_sub":   S("cs", fontName="Helvetica-Bold", fontSize=20, textColor=HexColor("#A8D4F5"), leading=26, alignment=TA_CENTER),
    "cover_desc":  S("cd", fontName="Helvetica",      fontSize=11, textColor=HexColor("#CBD5E1"), leading=16, alignment=TA_CENTER),
}

def sp(n=1):   return Spacer(1, n * 4*mm)
def hr(color=BORDER): return HRFlowable(width="100%", thickness=0.5, color=color, spaceAfter=2*mm, spaceBefore=2*mm)
def h2(t, col=BLUE):  return Paragraph(t, ParagraphStyle("_h2", parent=ST["h2"], textColor=col))
def h3(t, col=TEAL):  return Paragraph(t, ParagraphStyle("_h3", parent=ST["h3"], textColor=col))
def h4(t, col=NAVY):  return Paragraph(t, ParagraphStyle("_h4", parent=ST["h4"], textColor=col))
def body(t):          return Paragraph(t, ST["body"])
def cap(t):           return Paragraph(f"<i>{t}</i>", ST["caption"])

def bl(text, col="#2E75B6"):
    return Paragraph(f'<font color="{col}">▸</font>  {text}', ST["bullet"])

def nb(text, n, col="#2E75B6"):
    return Paragraph(f'<font color="{col}"><b>{n}.</b></font>  {text}', ST["bullet"])

def tbl(data, col_widths, style_extra=None):
    base = [
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",      (0,1), (0,-1), "Helvetica-Bold"),
        ("BACKGROUND",    (0,1), (0,-1), LIGHT),
        ("TEXTCOLOR",     (0,1), (0,-1), NAVY),
        ("ROWBACKGROUNDS",(1,1), (-1,-1), [white, ALT_ROW]),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, BORDER),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    if style_extra:
        base += style_extra
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(base))
    return t

# ════════════════════════════════════════════════════════════
#  BUILD STORY
# ════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────
story.append(sp(4))
cover_data = [
    [Paragraph("DSA Revision Notes", ST["cover_title"])],
    [Paragraph("Topic 2 — Two Pointers &amp; Sliding Window", ST["cover_sub"])],
    [Paragraph(
        "Complete theory  ·  All patterns  ·  Complexity analysis<br/>"
        "C++ code for every technique  ·  Visual diagrams  ·  LeetCode prep",
        ST["cover_desc"]
    )],
]
cover_t = Table(cover_data, colWidths=[W - 30*mm])
cover_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,0), 22),
    ("BOTTOMPADDING", (0,0), (-1,0), 10),
    ("TOPPADDING",    (0,1), (-1,1), 8),
    ("BOTTOMPADDING", (0,1), (-1,1), 10),
    ("TOPPADDING",    (0,2), (-1,2), 8),
    ("BOTTOMPADDING", (0,2), (-1,2), 22),
    ("ROUNDEDCORNERS",[4*mm]),
]))
story.append(cover_t)
story.append(sp(2))

stats = [[
    Paragraph('<b><font color="#1A3C5E">10</font></b><br/><font size="8" color="#64748B">Sections</font>',
              ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, alignment=TA_CENTER, leading=22)),
    Paragraph('<b><font color="#1A3C5E">20+</font></b><br/><font size="8" color="#64748B">C++ Examples</font>',
              ParagraphStyle("st2", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, alignment=TA_CENTER, leading=22)),
    Paragraph('<b><font color="#1A3C5E">15+</font></b><br/><font size="8" color="#64748B">Patterns</font>',
              ParagraphStyle("st3", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, alignment=TA_CENTER, leading=22)),
    Paragraph('<b><font color="#1A3C5E">8</font></b><br/><font size="8" color="#64748B">Visuals</font>',
              ParagraphStyle("st4", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, alignment=TA_CENTER, leading=22)),
]]
st = Table(stats, colWidths=[(W-30*mm)/4]*4)
st.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("INNERGRID",     (0,0), (-1,-1), 0.5, BORDER),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(st)
story.append(PageBreak())

# ── TABLE OF CONTENTS ───────────────────────────────────────
story.append(SectionBanner("TOC", "Table of Contents", NAVY, TEAL))
story.append(sp(1))

toc_items = [
    ("1.", "Introduction — What are Two Pointers & Sliding Window?"),
    ("", "→ Core idea, When to use, Problem signals"),
    ("2.", "Two Pointers — Opposite Ends Pattern"),
    ("", "→ Template, Sorted array pairs, Container With Most Water"),
    ("", "→ Trapping Rain Water, 3Sum, 4Sum"),
    ("3.", "Two Pointers — Same Direction (Fast/Slow)"),
    ("", "→ Remove duplicates, Move zeroes, Partition"),
    ("", "→ Is Subsequence, Merge sorted arrays"),
    ("4.", "Two Pointers — Dutch National Flag"),
    ("", "→ Sort Colors, 3-way partition template"),
    ("5.", "Two Pointers — Palindrome Patterns"),
    ("", "→ Valid Palindrome, Valid Palindrome II"),
    ("6.", "Sliding Window — Fixed Size"),
    ("", "→ Template, Max sum of size K, First negative in window"),
    ("7.", "Sliding Window — Variable Size (Expand/Shrink)"),
    ("", "→ Template, Longest substring without repeat"),
    ("", "→ Min Window Substring, Permutation in String"),
    ("8.", "Sliding Window — At-Most-K Trick"),
    ("", "→ Exactly K = AtMost(K) - AtMost(K-1)"),
    ("", "→ Subarrays with K different integers"),
    ("9.", "Advanced Patterns"),
    ("", "→ Sliding Window Maximum (Monotonic Deque)"),
    ("", "→ Longest Repeating Character Replacement"),
    ("10.", "Complexity & Pattern Cheat Sheet"),
]
for num, title in toc_items:
    if num:
        story.append(Paragraph(f'<b><font color="#1A3C5E">{num}</font></b>  <b>{title}</b>', ST["toc_h"]))
    else:
        story.append(Paragraph(f'<font color="#64748B">        {title}</font>', ST["toc_i"]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 1 — INTRODUCTION
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("1", "Introduction", NAVY, TEAL))
story.append(sp(1))

story.append(h2("1.1  What are Two Pointers?"))
story.append(body(
    "The <b>Two Pointer</b> technique uses two index variables that traverse a data structure — "
    "usually an array or string — simultaneously. Instead of nested loops (O(n²)), "
    "each pointer moves at most n steps total, giving <b>O(n)</b> time with <b>O(1)</b> extra space. "
    "It is one of the most powerful tricks for reducing brute-force solutions."
))
story.append(sp(0.5))
story.append(InfoBox([
    "Opposite ends: l=0, r=n-1, converge inward. Use on SORTED arrays for pair/triplet problems.",
    "Same direction: slow and fast both move left-to-right. Use for partitioning or subsequences.",
    "Fast/Slow (Floyd): one moves 1 step, other 2 steps. Use for cycle detection in linked lists.",
], title="⚡ Three Two-Pointer Variants", color=NAVY, bg=LIGHT))
story.append(sp(0.5))

story.append(h2("1.2  What is Sliding Window?"))
story.append(body(
    "A <b>Sliding Window</b> is a contiguous subarray/substring that 'slides' across the data. "
    "Instead of recomputing the window from scratch each step (O(n²)), we add the new right element "
    "and remove the old left element — O(1) per slide. Two types exist:"
))
story.append(bl("<b>Fixed window:</b> window size k is constant. Slide by one position each step."))
story.append(bl("<b>Variable window:</b> expand right freely; shrink left when window becomes invalid."))
story.append(sp(0.5))

story.append(h2("1.3  When to Use — Problem Signals"))
signals = [
    ["Signal in Problem",                    "Likely Technique"],
    ['"Find pair that sums to target"',       "Two Pointers (opposite ends) on sorted array"],
    ['"Longest subarray/substring with..."', "Sliding Window (variable)"],
    ['"Subarray of size k with max sum"',     "Sliding Window (fixed)"],
    ['"Remove duplicates in-place"',          "Two Pointers (same direction)"],
    ['"Is S a subsequence of T?"',            "Two Pointers (same direction)"],
    ['"Minimum window containing all chars"', "Sliding Window + frequency map"],
    ['"Exactly K distinct / equal K"',        "AtMost(K) - AtMost(K-1) trick"],
    ['"Sort array with 3 values"',            "Dutch National Flag (three pointers)"],
    ['"Container / trap water"',              "Two Pointers (opposite ends)"],
    ['"Cycle in linked list"',                "Fast/Slow pointers (Floyd)"],
]
story.append(tbl(signals, [75*mm, 93*mm]))
story.append(cap("Table 1: Problem signal → technique mapping"))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 2 — OPPOSITE ENDS
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("2", "Two Pointers — Opposite Ends Pattern", BLUE, TEAL))
story.append(sp(1))

story.append(h2("2.1  Core Template"))
story.append(body(
    "Place one pointer at the start and one at the end. Move them toward each other based on a condition. "
    "Works on <b>sorted arrays</b> because sorted order gives us a monotone property: "
    "if arr[l]+arr[r] &lt; target, increasing l increases the sum; if too large, decreasing r decreases it."
))
story.append(sp(0.5))

story.append(VisualBox(
    ["1", "3", "5", "7", "9", "11", "14"],
    {0: "l", 6: "r"},
    label="Opposite ends: l starts at 0, r starts at n-1",
    color=BLUE
))
story.append(sp(0.5))

story.append(CppCodeBlock([
    "// ── OPPOSITE ENDS TEMPLATE ──────────────────────────────",
    "// Precondition: array is SORTED",
    "int l = 0, r = n - 1;",
    "while (l < r) {",
    "    if (condition_met(arr[l], arr[r])) {",
    "        // record answer",
    "        l++; r--;              // or just one of them",
    "    } else if (need_larger) {",
    "        l++;                   // increase sum",
    "    } else {",
    "        r--;                   // decrease sum",
    "    }",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("2.2  Two Sum II — Sorted Array  (LC 167)"))
story.append(body(
    "Given a <b>1-indexed</b> sorted array, find two numbers that add up to target. "
    "Because the array is sorted, opposite-ends two pointers gives O(n) with O(1) space."
))
story.append(CppCodeBlock([
    "#include <vector>",
    "using namespace std;",
    "",
    "vector<int> twoSum(vector<int>& numbers, int target) {",
    "    int l = 0, r = numbers.size() - 1;",
    "    while (l < r) {",
    "        int sum = numbers[l] + numbers[r];",
    "        if (sum == target)  return {l + 1, r + 1};  // 1-indexed",
    "        else if (sum < target) l++;   // need bigger sum",
    "        else                   r--;   // need smaller sum",
    "    }",
    "    return {};   // guaranteed to find per problem",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("2.3  Container With Most Water  (LC 11)"))
story.append(body(
    "Given heights of walls, find two walls that trap the most water. "
    "Area = min(height[l], height[r]) × (r − l). "
    "<b>Greedy insight:</b> always move the pointer with the <i>shorter</i> wall — "
    "keeping the taller wall gives a chance for a larger area with a closer wall."
))
story.append(CppCodeBlock([
    "int maxArea(vector<int>& height) {",
    "    int l = 0, r = height.size() - 1;",
    "    int best = 0;",
    "    while (l < r) {",
    "        int area = min(height[l], height[r]) * (r - l);",
    "        best = max(best, area);",
    "        // Move the shorter wall inward",
    "        if (height[l] < height[r]) l++;",
    "        else                        r--;",
    "    }",
    "    return best;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.5))
story.append(InfoBox([
    "Why does moving the shorter wall work?",
    "Current area is limited by min(h[l], h[r]). Moving the TALLER wall can only make it worse",
    "or equal (width shrinks, height capped by shorter wall). Moving SHORTER gives a chance.",
], title="💡 Proof of Greedy Choice", color=BLUE, bg=LIGHT))
story.append(sp(0.8))

story.append(h2("2.4  Trapping Rain Water  (LC 42)"))
story.append(body(
    "Water at index i = min(maxLeft[i], maxRight[i]) − height[i]. "
    "Brute force: O(n²). Prefix arrays: O(n) time O(n) space. "
    "<b>Two pointers: O(n) time O(1) space.</b> "
    "Key insight: if maxLeft &lt; maxRight, the water at l is determined by maxLeft alone — "
    "process l and move it inward."
))
story.append(CppCodeBlock([
    "int trap(vector<int>& height) {",
    "    int l = 0, r = height.size() - 1;",
    "    int maxL = 0, maxR = 0, water = 0;",
    "    while (l < r) {",
    "        if (height[l] <= height[r]) {",
    "            // Left side is the bottleneck",
    "            if (height[l] >= maxL) maxL = height[l];",
    "            else                   water += maxL - height[l];",
    "            l++;",
    "        } else {",
    "            // Right side is the bottleneck",
    "            if (height[r] >= maxR) maxR = height[r];",
    "            else                   water += maxR - height[r];",
    "            r--;",
    "        }",
    "    }",
    "    return water;",
    "}",
    "// Time: O(n)   Space: O(1)  — optimal solution",
]))
story.append(sp(0.8))

story.append(h2("2.5  3Sum  (LC 15)"))
story.append(body(
    "Find all unique triplets that sum to zero. Strategy: <b>sort</b> the array, "
    "then for each element i, run two pointers on the remaining subarray [i+1, n-1]. "
    "Skip duplicates explicitly to avoid repeated triplets."
))
story.append(CppCodeBlock([
    "vector<vector<int>> threeSum(vector<int>& nums) {",
    "    sort(nums.begin(), nums.end());",
    "    vector<vector<int>> res;",
    "    int n = nums.size();",
    "    for (int i = 0; i < n - 2; i++) {",
    "        if (i > 0 && nums[i] == nums[i-1]) continue; // skip dup",
    "        int l = i + 1, r = n - 1;",
    "        while (l < r) {",
    "            int sum = nums[i] + nums[l] + nums[r];",
    "            if (sum == 0) {",
    "                res.push_back({nums[i], nums[l], nums[r]});",
    "                while (l < r && nums[l] == nums[l+1]) l++; // skip dup",
    "                while (l < r && nums[r] == nums[r-1]) r--; // skip dup",
    "                l++; r--;",
    "            } else if (sum < 0) l++;",
    "            else                r--;",
    "        }",
    "    }",
    "    return res;",
    "}",
    "// Time: O(n^2)   Space: O(1) extra (output not counted)",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 3 — SAME DIRECTION
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("3", "Two Pointers — Same Direction (Fast / Slow)", TEAL, BLUE))
story.append(sp(1))

story.append(h2("3.1  Core Template"))
story.append(body(
    "Both pointers start at the left. <b>Fast</b> pointer scans every element; "
    "<b>Slow</b> pointer marks the boundary of the valid/processed region. "
    "When fast finds a qualifying element, write it to slow's position and advance slow. "
    "This pattern modifies the array <b>in-place</b> with O(1) space."
))
story.append(VisualBox(
    ["0", "1", "0", "3", "12", "0"],
    {1: "slow", 3: "fast"},
    label="Move Zeroes: slow tracks last non-zero, fast scans ahead",
    color=TEAL
))
story.append(sp(0.5))
story.append(CppCodeBlock([
    "// ── SAME DIRECTION TEMPLATE ─────────────────────────────",
    "int slow = 0;",
    "for (int fast = 0; fast < n; fast++) {",
    "    if (qualifies(arr[fast])) {",
    "        arr[slow] = arr[fast];  // write qualifying element",
    "        slow++;",
    "    }",
    "}",
    "// Result: arr[0..slow-1] contains all qualifying elements",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("3.2  Remove Duplicates from Sorted Array  (LC 26)"))
story.append(body(
    "Slow pointer tracks the position to write the next unique element. "
    "Fast scans; when arr[fast] != arr[slow-1], it's a new unique — write it."
))
story.append(CppCodeBlock([
    "int removeDuplicates(vector<int>& nums) {",
    "    if (nums.empty()) return 0;",
    "    int slow = 1;                    // first element always unique",
    "    for (int fast = 1; fast < nums.size(); fast++) {",
    "        if (nums[fast] != nums[slow - 1]) {  // new unique found",
    "            nums[slow] = nums[fast];",
    "            slow++;",
    "        }",
    "    }",
    "    return slow;   // new length",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("3.3  Move Zeroes  (LC 283)"))
story.append(body(
    "Move all zeroes to the end while preserving relative order of non-zero elements. "
    "Slow pointer is the insertion position for non-zeroes."
))
story.append(CppCodeBlock([
    "void moveZeroes(vector<int>& nums) {",
    "    int slow = 0;",
    "    // Phase 1: copy all non-zeroes to front",
    "    for (int fast = 0; fast < nums.size(); fast++) {",
    "        if (nums[fast] != 0) {",
    "            nums[slow++] = nums[fast];",
    "        }",
    "    }",
    "    // Phase 2: fill rest with 0",
    "    while (slow < nums.size()) nums[slow++] = 0;",
    "}",
    "",
    "// Alternative: swap version (preserves relative order of 0s too)",
    "void moveZeroesSwap(vector<int>& nums) {",
    "    int slow = 0;",
    "    for (int fast = 0; fast < nums.size(); fast++) {",
    "        if (nums[fast] != 0)",
    "            swap(nums[slow++], nums[fast]);",
    "    }",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("3.4  Is Subsequence  (LC 392)"))
story.append(body(
    "Check if string s is a subsequence of t. Use two pointers: i on s, j on t. "
    "Advance j always; advance i only when t[j] == s[i]. If i reaches end of s → true."
))
story.append(CppCodeBlock([
    "bool isSubsequence(string s, string t) {",
    "    int i = 0, j = 0;",
    "    while (i < s.size() && j < t.size()) {",
    "        if (s[i] == t[j]) i++;  // matched one char of s",
    "        j++;                    // always advance t",
    "    }",
    "    return i == s.size();  // matched all of s?",
    "}",
    "// Time: O(|s| + |t|)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("3.5  Merge Sorted Array  (LC 88)"))
story.append(body(
    "Merge nums2 into nums1 in-place. <b>Key trick: start from the end</b> to avoid overwriting. "
    "Three pointers: p1 at end of nums1's data, p2 at end of nums2, p at end of merged."
))
story.append(CppCodeBlock([
    "void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {",
    "    int p1 = m - 1;         // pointer in nums1 data",
    "    int p2 = n - 1;         // pointer in nums2",
    "    int p  = m + n - 1;     // write position (end)",
    "    while (p1 >= 0 && p2 >= 0) {",
    "        if (nums1[p1] > nums2[p2])",
    "            nums1[p--] = nums1[p1--];",
    "        else",
    "            nums1[p--] = nums2[p2--];",
    "    }",
    "    // Copy remaining nums2 (nums1 leftover already in place)",
    "    while (p2 >= 0)",
    "        nums1[p--] = nums2[p2--];",
    "}",
    "// Time: O(m+n)   Space: O(1)",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 4 — DUTCH NATIONAL FLAG
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("4", "Two Pointers — Dutch National Flag", PURPLE, BLUE))
story.append(sp(1))

story.append(h2("4.1  Three-Way Partition Template"))
story.append(body(
    "Partition an array with <b>three distinct values</b> (e.g. 0, 1, 2) into three sections "
    "in a single pass. Uses three pointers: <b>lo</b> (boundary of 0s), "
    "<b>mid</b> (current element), <b>hi</b> (boundary of 2s). "
    "All elements in [lo, mid) are 0, [mid, hi] are 1, (hi, n-1] are 2."
))
story.append(sp(0.5))
story.append(VisualBox(
    ["0","0","1","1","1","2","2"],
    {1: "lo", 4: "mid", 5: "hi"},
    label="Invariant after sort: 0s | 1s | 2s",
    color=PURPLE
))
story.append(sp(0.5))
story.append(CppCodeBlock([
    "// ── DUTCH NATIONAL FLAG TEMPLATE ────────────────────────",
    "int lo = 0, mid = 0, hi = n - 1;",
    "while (mid <= hi) {",
    "    if (arr[mid] == LOW_VAL) {",
    "        swap(arr[lo], arr[mid]);",
    "        lo++;  mid++;          // both advance: arr[lo] was 1 (already seen)",
    "    } else if (arr[mid] == MID_VAL) {",
    "        mid++;                 // 1 is in correct region, just advance",
    "    } else {                   // arr[mid] == HIGH_VAL",
    "        swap(arr[mid], arr[hi]);",
    "        hi--;                  // do NOT advance mid (swapped val unknown)",
    "    }",
    "}",
]))
story.append(sp(0.8))

story.append(h2("4.2  Sort Colors  (LC 75)"))
story.append(CppCodeBlock([
    "void sortColors(vector<int>& nums) {",
    "    int lo = 0, mid = 0, hi = nums.size() - 1;",
    "    while (mid <= hi) {",
    "        if (nums[mid] == 0) {",
    "            swap(nums[lo++], nums[mid++]);",
    "        } else if (nums[mid] == 1) {",
    "            mid++;",
    "        } else {               // nums[mid] == 2",
    "            swap(nums[mid], nums[hi--]);",
    "            // DON'T mid++ — swapped element needs checking",
    "        }",
    "    }",
    "}",
    "// Time: O(n)   Space: O(1)  — single pass only",
]))
story.append(sp(0.5))
story.append(InfoBox([
    "Why NOT increment mid after swapping with hi?",
    "When we swap arr[mid] with arr[hi], the new arr[mid] came from hi — it has not been examined yet.",
    "If we incremented mid, we would skip checking this newly placed element.",
    "But when we swap with lo, arr[lo] must have been 1 (since mid >= lo always), so it is safe to advance both.",
], title="🔑 Critical Insight", color=PURPLE, bg=PURPLE_BG))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 5 — PALINDROME PATTERNS
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("5", "Two Pointers — Palindrome Patterns", RED, ORANGE))
story.append(sp(1))

story.append(h2("5.1  Valid Palindrome  (LC 125)"))
story.append(body(
    "A phrase is a palindrome if, after converting to lowercase and removing non-alphanumeric characters, "
    "it reads the same forward and backward. Classic opposite-ends two-pointer."
))
story.append(CppCodeBlock([
    "#include <cctype>",
    "",
    "bool isPalindrome(string s) {",
    "    int l = 0, r = s.size() - 1;",
    "    while (l < r) {",
    "        // Skip non-alphanumeric from both ends",
    "        while (l < r && !isalnum(s[l])) l++;",
    "        while (l < r && !isalnum(s[r])) r--;",
    "        if (tolower(s[l]) != tolower(s[r])) return false;",
    "        l++;  r--;",
    "    }",
    "    return true;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("5.2  Valid Palindrome II  (LC 680)"))
story.append(body(
    "Can you make a string palindrome by removing <b>at most one</b> character? "
    "When pointers mismatch, try skipping either s[l] or s[r] and check if the rest is a palindrome."
))
story.append(CppCodeBlock([
    "bool checkPalin(string& s, int l, int r) {",
    "    while (l < r) {",
    "        if (s[l] != s[r]) return false;",
    "        l++; r--;",
    "    }",
    "    return true;",
    "}",
    "",
    "bool validPalindrome(string s) {",
    "    int l = 0, r = s.size() - 1;",
    "    while (l < r) {",
    "        if (s[l] != s[r])",
    "            // Try deleting either character",
    "            return checkPalin(s, l+1, r) || checkPalin(s, l, r-1);",
    "        l++;  r--;",
    "    }",
    "    return true;   // already palindrome",
    "}",
    "// Time: O(n)   Space: O(1)",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 6 — FIXED SLIDING WINDOW
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("6", "Sliding Window — Fixed Size", TEAL, BLUE))
story.append(sp(1))

story.append(h2("6.1  Core Template"))
story.append(body(
    "Maintain a window of exactly size <b>k</b>. "
    "Build the first window, then slide: <b>add arr[r] and remove arr[r-k]</b> each step. "
    "This avoids re-summing the whole window — O(1) per slide."
))
story.append(VisualBox(
    ["2","1","5","1","3","2"],
    {0: "l", 2: "r"},
    label="Fixed window k=3: [2,1,5] → slide → [1,5,1] → ...",
    color=TEAL
))
story.append(sp(0.5))
story.append(CppCodeBlock([
    "// ── FIXED WINDOW TEMPLATE ───────────────────────────────",
    "int windowVal = 0;",
    "// Build first window",
    "for (int i = 0; i < k; i++) windowVal += arr[i];",
    "int best = windowVal;",
    "// Slide window",
    "for (int r = k; r < n; r++) {",
    "    windowVal += arr[r];           // add new right element",
    "    windowVal -= arr[r - k];       // remove old left element",
    "    best = max(best, windowVal);   // update answer",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("6.2  Maximum Average Subarray I  (LC 643)"))
story.append(CppCodeBlock([
    "double findMaxAverage(vector<int>& nums, int k) {",
    "    double windowSum = 0;",
    "    for (int i = 0; i < k; i++) windowSum += nums[i];",
    "    double maxSum = windowSum;",
    "    for (int r = k; r < nums.size(); r++) {",
    "        windowSum += nums[r] - nums[r - k];",
    "        maxSum = max(maxSum, windowSum);",
    "    }",
    "    return maxSum / k;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("6.3  First Negative Number in Every Window of Size K"))
story.append(CppCodeBlock([
    "vector<int> firstNegative(vector<int>& arr, int k) {",
    "    deque<int> dq;     // stores indices of negative numbers",
    "    vector<int> result;",
    "    int n = arr.size();",
    "    for (int r = 0; r < n; r++) {",
    "        // Add new negative to deque",
    "        if (arr[r] < 0) dq.push_back(r);",
    "        // Remove elements outside window",
    "        if (!dq.empty() && dq.front() <= r - k) dq.pop_front();",
    "        // Record answer once window is full",
    "        if (r >= k - 1) {",
    "            result.push_back(dq.empty() ? 0 : arr[dq.front()]);",
    "        }",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n)   Space: O(k)",
]))
story.append(sp(0.8))

story.append(h2("6.4  Count Occurrences of Anagrams  (LC 438)"))
story.append(body(
    "Fixed window of size p.length(). Use a frequency map. "
    "When window's freq map equals p's freq map → anagram found."
))
story.append(CppCodeBlock([
    "vector<int> findAnagrams(string s, string p) {",
    "    if (s.size() < p.size()) return {};",
    "    vector<int> pCount(26, 0), wCount(26, 0), result;",
    "    int k = p.size();",
    "    // Build freq maps for p and first window",
    "    for (int i = 0; i < k; i++) {",
    "        pCount[p[i] - 'a']++;",
    "        wCount[s[i] - 'a']++;",
    "    }",
    "    if (pCount == wCount) result.push_back(0);",
    "    // Slide window",
    "    for (int r = k; r < s.size(); r++) {",
    "        wCount[s[r] - 'a']++;           // add right",
    "        wCount[s[r - k] - 'a']--;       // remove left",
    "        if (pCount == wCount) result.push_back(r - k + 1);",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n)   Space: O(1) — fixed 26-char arrays",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 7 — VARIABLE SLIDING WINDOW
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("7", "Sliding Window — Variable Size", BLUE, PURPLE))
story.append(sp(1))

story.append(h2("7.1  Core Template — Expand Right, Shrink Left"))
story.append(body(
    "Expand the right boundary freely. When the window becomes <b>invalid</b>, "
    "shrink from the left until it's valid again. At every step, the window [l, r] is valid "
    "so we can update the answer. This gives O(n) because each pointer moves at most n times."
))
story.append(CppCodeBlock([
    "// ── VARIABLE WINDOW TEMPLATE ────────────────────────────",
    "int l = 0, best = 0;",
    "// some data structure to track window state",
    "for (int r = 0; r < n; r++) {",
    "    // 1. Expand: add arr[r] to window",
    "    add_to_window(arr[r]);",
    "",
    "    // 2. Shrink: while window is INVALID, move l right",
    "    while (window_is_invalid()) {",
    "        remove_from_window(arr[l]);",
    "        l++;",
    "    }",
    "    // 3. Window [l..r] is now valid — update answer",
    "    best = max(best, r - l + 1);",
    "}",
    "return best;",
    "// Time: O(n)  — each element enters and leaves window once",
    "// Space: O(window size) for tracking structure",
]))
story.append(sp(0.8))

story.append(h2("7.2  Longest Substring Without Repeating Characters  (LC 3)"))
story.append(body(
    "Window is invalid when a character appears more than once. "
    "Use a hash set or last-seen map to track characters in the current window."
))
story.append(CppCodeBlock([
    "int lengthOfLongestSubstring(string s) {",
    "    unordered_map<char, int> lastSeen;  // char -> last seen index",
    "    int l = 0, best = 0;",
    "    for (int r = 0; r < s.size(); r++) {",
    "        // If char was seen and is inside current window",
    "        if (lastSeen.count(s[r]) && lastSeen[s[r]] >= l) {",
    "            l = lastSeen[s[r]] + 1;  // jump l past the duplicate",
    "        }",
    "        lastSeen[s[r]] = r;",
    "        best = max(best, r - l + 1);",
    "    }",
    "    return best;",
    "}",
    "// Time: O(n)   Space: O(min(n, charset_size))",
]))
story.append(sp(0.5))
story.append(InfoBox([
    "Alternative using set: add s[r], while s[r] in set -> remove s[l], l++",
    "The map version is faster: jump l directly to lastSeen[s[r]]+1 without one-by-one shrinking",
    "Edge case: only jump l if lastSeen[s[r]] >= l (char was seen but before current window is OK)",
], title="💡 Two Implementations", color=BLUE, bg=LIGHT))
story.append(sp(0.8))

story.append(h2("7.3  Minimum Window Substring  (LC 76)  — Hard"))
story.append(body(
    "Find the smallest substring of s that contains all characters of t (with frequency). "
    "<b>Strategy:</b> use two frequency maps and a counter 'have' vs 'need'. "
    "Expand right until window is valid (have == need), then shrink left to minimise."
))
story.append(CppCodeBlock([
    "string minWindow(string s, string t) {",
    "    if (t.empty()) return \"\";",
    "    unordered_map<char,int> need, have_map;",
    "    for (char c : t) need[c]++;",
    "    int have = 0, required = need.size();  // distinct chars needed",
    "    int l = 0, minLen = INT_MAX, minL = 0;",
    "    for (int r = 0; r < s.size(); r++) {",
    "        char c = s[r];",
    "        have_map[c]++;",
    "        // Check if this char's freq now satisfies 'need'",
    "        if (need.count(c) && have_map[c] == need[c]) have++;",
    "        // Shrink from left while window is valid",
    "        while (have == required) {",
    "            if (r - l + 1 < minLen) {",
    "                minLen = r - l + 1;",
    "                minL = l;",
    "            }",
    "            char lc = s[l];",
    "            have_map[lc]--;",
    "            if (need.count(lc) && have_map[lc] < need[lc]) have--;",
    "            l++;",
    "        }",
    "    }",
    "    return minLen == INT_MAX ? \"\" : s.substr(minL, minLen);",
    "}",
    "// Time: O(|s| + |t|)   Space: O(|t|)",
]))
story.append(sp(0.8))

story.append(h2("7.4  Permutation in String  (LC 567)"))
story.append(body(
    "Check if any permutation of s1 exists as a substring of s2. "
    "Equivalent to: does any fixed window of size |s1| in s2 have the same freq map as s1?"
))
story.append(CppCodeBlock([
    "bool checkInclusion(string s1, string s2) {",
    "    if (s1.size() > s2.size()) return false;",
    "    vector<int> need(26, 0), window(26, 0);",
    "    int k = s1.size();",
    "    for (char c : s1) need[c - 'a']++;",
    "    // Build first window",
    "    for (int i = 0; i < k; i++) window[s2[i] - 'a']++;",
    "    if (need == window) return true;",
    "    // Slide",
    "    for (int r = k; r < s2.size(); r++) {",
    "        window[s2[r] - 'a']++;",
    "        window[s2[r - k] - 'a']--;",
    "        if (need == window) return true;",
    "    }",
    "    return false;",
    "}",
    "// Time: O(|s1| + |s2|)   Space: O(1) — fixed 26-element arrays",
]))
story.append(sp(0.8))

story.append(h2("7.5  Longest Subarray of 1s After Deleting One Element  (LC 1493)"))
story.append(body(
    "At most one zero allowed in the window (the 'deleted' element). "
    "Window invalid when it contains more than one zero — shrink left."
))
story.append(CppCodeBlock([
    "int longestSubarray(vector<int>& nums) {",
    "    int l = 0, zeros = 0, best = 0;",
    "    for (int r = 0; r < nums.size(); r++) {",
    "        if (nums[r] == 0) zeros++;",
    "        while (zeros > 1) {          // window invalid",
    "            if (nums[l] == 0) zeros--;",
    "            l++;",
    "        }",
    "        // -1 because one element must be deleted",
    "        best = max(best, r - l);    // window size - 1",
    "    }",
    "    return best;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 8 — AT MOST K TRICK
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("8", "Sliding Window — At-Most-K Trick", GOLD, ORANGE))
story.append(sp(1))

story.append(h2("8.1  The Core Identity"))
story.append(body(
    "Many problems ask for subarrays with <b>exactly K</b> of something. "
    "Direct sliding window doesn't work for 'exactly' because we can't grow and shrink symmetrically. "
    "<b>The trick:</b>"
))
story.append(InfoBox([
    "count(exactly K) = count(at most K) - count(at most K-1)",
    "",
    "atMost(K) is easy: standard variable window. When distinct > K, shrink left.",
    "Run atMost twice with K and K-1, subtract the results.",
], title="🔑 ExactlyK = AtMost(K) - AtMost(K-1)", color=GOLD, bg=HexColor("#FEF9E7")))
story.append(sp(0.8))

story.append(h2("8.2  Subarrays with K Different Integers  (LC 992)"))
story.append(CppCodeBlock([
    "int atMost(vector<int>& nums, int k) {",
    "    unordered_map<int,int> freq;",
    "    int l = 0, count = 0;",
    "    for (int r = 0; r < nums.size(); r++) {",
    "        freq[nums[r]]++;",
    "        while (freq.size() > k) {   // too many distinct",
    "            freq[nums[l]]--;",
    "            if (freq[nums[l]] == 0) freq.erase(nums[l]);",
    "            l++;",
    "        }",
    "        count += r - l + 1;  // all subarrays ending at r with <=k distinct",
    "    }",
    "    return count;",
    "}",
    "",
    "int subarraysWithKDistinct(vector<int>& nums, int k) {",
    "    return atMost(nums, k) - atMost(nums, k - 1);",
    "}",
    "// Time: O(n)   Space: O(k)",
]))
story.append(sp(0.8))

story.append(h2("8.3  Binary Subarrays With Sum  (LC 930)"))
story.append(body("Exact sum S in binary array = atMost(S) - atMost(S-1)."))
story.append(CppCodeBlock([
    "int atMostSum(vector<int>& nums, int goal) {",
    "    if (goal < 0) return 0;",
    "    int l = 0, windowSum = 0, count = 0;",
    "    for (int r = 0; r < nums.size(); r++) {",
    "        windowSum += nums[r];",
    "        while (windowSum > goal) windowSum -= nums[l++];",
    "        count += r - l + 1;",
    "    }",
    "    return count;",
    "}",
    "",
    "int numSubarraysWithSum(vector<int>& nums, int goal) {",
    "    return atMostSum(nums, goal) - atMostSum(nums, goal - 1);",
    "}",
    "// Time: O(n)   Space: O(1)",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 9 — ADVANCED PATTERNS
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("9", "Advanced Patterns", PURPLE, RED))
story.append(sp(1))

story.append(h2("9.1  Sliding Window Maximum  (LC 239)  — Monotonic Deque"))
story.append(body(
    "Find the maximum of every window of size k. Brute force O(nk). "
    "<b>Monotonic deque</b> approach: maintain a deque of indices in <b>decreasing</b> order of values. "
    "Front is always the current window maximum. O(n) time, O(k) space."
))
story.append(CppCodeBlock([
    "#include <deque>",
    "",
    "vector<int> maxSlidingWindow(vector<int>& nums, int k) {",
    "    deque<int> dq;     // stores INDICES, values are decreasing",
    "    vector<int> result;",
    "    int n = nums.size();",
    "    for (int r = 0; r < n; r++) {",
    "        // Remove elements outside window from front",
    "        while (!dq.empty() && dq.front() <= r - k)",
    "            dq.pop_front();",
    "        // Maintain decreasing order: remove smaller elements from back",
    "        while (!dq.empty() && nums[dq.back()] <= nums[r])",
    "            dq.pop_back();",
    "        dq.push_back(r);",
    "        // Window is full — record max (front of deque)",
    "        if (r >= k - 1)",
    "            result.push_back(nums[dq.front()]);",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n)   Space: O(k)",
]))
story.append(sp(0.5))
story.append(InfoBox([
    "Deque invariant: indices in deque are always in increasing order (left to right in window).",
    "Values at those indices are in DECREASING order (front = max).",
    "New element: pop all back elements with smaller value — they can NEVER be the max while r is in window.",
    "Front expiry: if dq.front() <= r - k, it has left the window — pop it.",
], title="📐 Monotonic Deque Invariant", color=PURPLE, bg=PURPLE_BG))
story.append(sp(0.8))

story.append(h2("9.2  Longest Repeating Character Replacement  (LC 424)"))
story.append(body(
    "You can replace at most k characters. Find the longest substring where you can make all chars the same. "
    "<b>Key insight:</b> window is valid when (window_size - max_frequency) &lt;= k. "
    "We only need to track the max frequency, and it only needs to increase (not decrease) for optimal answer."
))
story.append(CppCodeBlock([
    "int characterReplacement(string s, int k) {",
    "    vector<int> freq(26, 0);",
    "    int l = 0, maxFreq = 0, best = 0;",
    "    for (int r = 0; r < s.size(); r++) {",
    "        freq[s[r] - 'A']++;",
    "        maxFreq = max(maxFreq, freq[s[r] - 'A']);",
    "        // If window invalid: (size - maxFreq) > k",
    "        // NOTE: we only shrink by 1, never fully recompute maxFreq",
    "        if ((r - l + 1) - maxFreq > k) {",
    "            freq[s[l] - 'A']--;",
    "            l++;",
    "        }",
    "        best = max(best, r - l + 1);",
    "    }",
    "    return best;",
    "}",
    "// Time: O(n)   Space: O(1) — 26-letter alphabet",
]))
story.append(sp(0.5))
story.append(InfoBox([
    "Why not recompute maxFreq when shrinking? The answer only improves when maxFreq increases.",
    "Even if the actual max freq drops after shrinking, we do not need a smaller window than best.",
    "This is a key non-obvious optimization — the window size never decreases, it only slides.",
], title="💡 Why maxFreq Only Increases", color=PURPLE, bg=PURPLE_BG))
story.append(sp(0.8))

story.append(h2("9.3  Max Consecutive Ones III  (LC 1004)"))
story.append(body(
    "Flip at most k zeros to ones. Find the longest subarray of 1s. "
    "Window invalid when zeros in window exceed k."
))
story.append(CppCodeBlock([
    "int longestOnes(vector<int>& nums, int k) {",
    "    int l = 0, zeros = 0, best = 0;",
    "    for (int r = 0; r < nums.size(); r++) {",
    "        if (nums[r] == 0) zeros++;",
    "        if (zeros > k) {               // window invalid",
    "            if (nums[l] == 0) zeros--;",
    "            l++;",
    "        }",
    "        best = max(best, r - l + 1);",
    "    }",
    "    return best;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("9.4  Minimum Size Subarray Sum  (LC 209)"))
story.append(body(
    "Find shortest subarray with sum &gt;= target. Variable window: expand until sum &gt;= target, "
    "then shrink left to find the minimum length."
))
story.append(CppCodeBlock([
    "int minSubArrayLen(int target, vector<int>& nums) {",
    "    int l = 0, windowSum = 0, minLen = INT_MAX;",
    "    for (int r = 0; r < nums.size(); r++) {",
    "        windowSum += nums[r];",
    "        while (windowSum >= target) {       // window is valid",
    "            minLen = min(minLen, r - l + 1);",
    "            windowSum -= nums[l];",
    "            l++;",
    "        }",
    "    }",
    "    return minLen == INT_MAX ? 0 : minLen;",
    "}",
    "// Time: O(n)   Space: O(1)",
    "",
    "// O(n log n) alternative: prefix sum + binary search",
    "// For each r, binary search for smallest l where prefix[r]-prefix[l] >= target",
]))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════
#  SECTION 10 — CHEAT SHEET
# ════════════════════════════════════════════════════════════
story.append(SectionBanner("10", "Complexity & Pattern Cheat Sheet", NAVY, TEAL))
story.append(sp(1))

story.append(h2("10.1  Two Pointers — All Patterns"))
tp_data = [
    ["Pattern",               "Setup",                        "Key Condition",                  "Time",  "Space", "Problems"],
    ["Opposite Ends",         "l=0, r=n-1",                   "Sorted; sum comparison",         "O(n)",  "O(1)",  "LC 1,11,15,42,167"],
    ["Same Direction",        "slow=0, fast=0",               "fast qualifies → write to slow", "O(n)",  "O(1)",  "LC 26,27,88,283,392"],
    ["Dutch National Flag",   "lo=0, mid=0, hi=n-1",          "3 groups; invariant zone",       "O(n)",  "O(1)",  "LC 75"],
    ["Palindrome Check",      "l=0, r=n-1",                   "Chars must match inward",        "O(n)",  "O(1)",  "LC 125,680"],
    ["Fast/Slow (Cycle)",     "slow=head, fast=head",         "fast moves 2x; meet = cycle",   "O(n)",  "O(1)",  "LC 141,142,287"],
    ["3Sum / kSum",           "Fix one; two-ptr on rest",     "Skip duplicates after sort",     "O(n^2)","O(1)",  "LC 15,18,259"],
]
story.append(tbl(tp_data, [32*mm, 32*mm, 40*mm, 16*mm, 16*mm, 32*mm]))
story.append(cap("Table 2: Two Pointer Patterns"))
story.append(sp(0.5))

story.append(h2("10.2  Sliding Window — All Patterns"))
sw_data = [
    ["Pattern",             "Window Control",                       "Data Structure",    "Time",  "Problems"],
    ["Fixed size",          "Add arr[r], remove arr[r-k]",         "Sum / freq array",  "O(n)",  "LC 438,567,643"],
    ["Variable (maximize)", "Expand r; shrink l while invalid",    "Map / set / count", "O(n)",  "LC 3,76,424"],
    ["Variable (minimize)", "Expand r; shrink l while valid",      "Map / count",       "O(n)",  "LC 76,209"],
    ["Exactly K trick",     "atMost(K) - atMost(K-1)",            "Map",               "O(n)",  "LC 930,992"],
    ["Monotonic Deque",     "Maintain decreasing deque of indices","deque<int>",        "O(n)",  "LC 239,862"],
    ["Two-pass",            "Left pass + right pass combine",      "Two arrays",        "O(n)",  "LC 42,135"],
]
story.append(tbl(sw_data, [34*mm, 55*mm, 33*mm, 16*mm, 30*mm]))
story.append(cap("Table 3: Sliding Window Patterns"))
story.append(sp(0.5))

story.append(h2("10.3  Decision Tree — Which Pattern to Choose?"))
story.append(CppCodeBlock([
    "/*",
    " * Problem asks for...                 Use...",
    " * ─────────────────────────────────────────────────────────────────",
    " * Pair/triplet sum in SORTED array  → Two Pointers (opposite ends)",
    " * Pair sum in UNSORTED array        → HashMap (not two pointers)",
    " * Remove/partition elements in-place→ Two Pointers (same direction)",
    " * 3 groups sort (0,1,2 or similar)  → Dutch National Flag",
    " * Palindrome check                  → Two Pointers (opposite ends)",
    " * Subsequence matching              → Two Pointers (same direction)",
    " *",
    " * Fixed window size k               → Sliding Window (fixed)",
    " * Longest subarray satisfying X     → Sliding Window (variable, max)",
    " * Shortest subarray satisfying X    → Sliding Window (variable, min)",
    " * Exactly K distinct/sum            → atMost(K) - atMost(K-1)",
    " * Max in every window of size k     → Monotonic Deque",
    " * Window of chars = permutation     → Fixed window + freq array",
    " */",
]))
story.append(sp(0.8))

story.append(h2("10.4  Complete LeetCode Problem Map"))
lc_data = [
    ["#",    "Problem",                                  "Pattern",               "Difficulty"],
    ["3",    "Longest Substring Without Repeating Chars","Sliding Window Variable","Medium"],
    ["11",   "Container With Most Water",                "Opposite Ends",         "Medium"],
    ["15",   "3Sum",                                     "Sort + Two Pointers",   "Medium"],
    ["18",   "4Sum",                                     "Sort + Two Pointers",   "Medium"],
    ["26",   "Remove Duplicates from Sorted Array",      "Same Direction",        "Easy"],
    ["27",   "Remove Element",                           "Same Direction",        "Easy"],
    ["42",   "Trapping Rain Water",                      "Opposite Ends",         "Hard"],
    ["75",   "Sort Colors",                              "Dutch National Flag",   "Medium"],
    ["76",   "Minimum Window Substring",                 "Sliding Window + Map",  "Hard"],
    ["88",   "Merge Sorted Array",                       "Three Pointers",        "Easy"],
    ["125",  "Valid Palindrome",                         "Opposite Ends",         "Easy"],
    ["167",  "Two Sum II",                               "Opposite Ends",         "Medium"],
    ["209",  "Minimum Size Subarray Sum",                "Sliding Window Min",    "Medium"],
    ["239",  "Sliding Window Maximum",                   "Monotonic Deque",       "Hard"],
    ["283",  "Move Zeroes",                              "Same Direction",        "Easy"],
    ["392",  "Is Subsequence",                           "Same Direction",        "Easy"],
    ["424",  "Longest Repeating Char Replacement",       "Sliding Window Variable","Medium"],
    ["438",  "Find All Anagrams in a String",            "Fixed Window + Freq",   "Medium"],
    ["567",  "Permutation in String",                    "Fixed Window + Freq",   "Medium"],
    ["680",  "Valid Palindrome II",                      "Opposite Ends",         "Easy"],
    ["930",  "Binary Subarrays With Sum",                "AtMost trick",          "Medium"],
    ["992",  "Subarrays with K Different Integers",      "AtMost trick",          "Hard"],
    ["1004", "Max Consecutive Ones III",                 "Sliding Window Variable","Medium"],
    ["1493", "Longest Subarray of 1s After Deleting One","Sliding Window Variable","Medium"],
]
diff_colors = {"Easy": GREEN, "Medium": ORANGE, "Hard": RED}
lc_style_extra = []
for i, row in enumerate(lc_data[1:], 1):
    col = diff_colors.get(row[3], DARK)
    lc_style_extra.append(("TEXTCOLOR", (3, i), (3, i), col))
    lc_style_extra.append(("FONTNAME",  (3, i), (3, i), "Helvetica-Bold"))
story.append(tbl(lc_data, [12*mm, 65*mm, 48*mm, 23*mm], style_extra=lc_style_extra))
story.append(cap("Table 4: Complete LeetCode problem map for Two Pointers & Sliding Window"))

story.append(sp(1))
story.append(InfoBox([
    "1. Two Pointers on SORTED array → think opposite ends. On unsorted → think same direction or hashmap.",
    "2. Sliding window window state = what makes it VALID. Define invalid clearly before coding.",
    "3. For minimum subarray: shrink while VALID (greedy: take smallest valid window at each r).",
    "4. For maximum subarray: shrink while INVALID (expand as much as possible before shrinking).",
    "5. AtMost(K) trick: whenever 'exactly K' doesn't fit a direct window, subtract two atMost calls.",
    "6. Monotonic deque: always ask 'can this old element ever be the answer for a future window?'",
    "7. When window is fixed size k: sliding formula is add arr[r], remove arr[r-k] every step.",
    "8. Two pointers is O(n); nested loop is O(n^2). Always ask: can I make one pointer never go back?",
], title="🏆 Golden Rules — Two Pointers & Sliding Window", color=NAVY, bg=LIGHT))

# ── BUILD PDF ────────────────────────────────────────────────
out = "DSA_Notes_TwoPointers_SlidingWindow.pdf"
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=34*mm, bottomMargin=18*mm,
    title="DSA Notes — Two Pointers & Sliding Window",
    author="DSA Revision Planner",
    subject="Complete Two Pointers and Sliding Window Notes with C++ Code",
)
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"Done! → {out}")