from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor, white, black

# ─── Palette ──────────────────────────────────────────────────
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
RED_BG    = HexColor("#FDEDEC")
GOLD_BG   = HexColor("#FEF9E7")
CODE_BG   = HexColor("#0D1117")
CODE_HDR  = HexColor("#161B22")
ALT_ROW   = HexColor("#F2F7FC")
BORDER    = HexColor("#CBD5E1")
DARK      = HexColor("#1E293B")
MUTED     = HexColor("#64748B")
CPP_KW    = HexColor("#FF7B72")
CPP_TYPE  = HexColor("#79C0FF")
CPP_CMT   = HexColor("#8B949E")
CPP_STR   = HexColor("#A5D6FF")
CPP_NUM   = HexColor("#F8C83A")
CODE_FG   = HexColor("#E6EDF3")

W, H = A4

# ─── Chrome ───────────────────────────────────────────────────
def _chrome(c, doc):
    c.saveState()
    c.setFillColor(NAVY);  c.rect(0, H-26*mm, W, 26*mm, fill=1, stroke=0)
    c.setFillColor(TEAL);  c.rect(0, H-28*mm, W, 2*mm,  fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, H-16*mm, "DSA Notes — Linked List (All Types & Operations)")
    c.setFont("Helvetica", 9)
    c.drawRightString(W-15*mm, H-16*mm, "Topic 5 of 13")
    c.setFillColor(NAVY);  c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(TEAL);  c.rect(0, 12*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica", 8)
    c.drawString(15*mm, 4*mm, "DSA Revision Planner  •  C++ Code Edition")
    c.drawRightString(W-15*mm, 4*mm, f"Page {doc.page}")
    c.restoreState()

first_page  = lambda c, doc: _chrome(c, doc)
later_pages = lambda c, doc: _chrome(c, doc)

# ─── Flowables ────────────────────────────────────────────────
class Banner(Flowable):
    def __init__(self, num, title, color=NAVY, accent=TEAL, height=14*mm):
        super().__init__()
        self.num=num; self.title=title; self.color=color
        self.accent=accent; self.bh=height; self.width=W-30*mm
    def wrap(self,*a): return self.width, self.bh+4*mm
    def draw(self):
        c=self.canv
        c.setFillColor(self.color)
        c.roundRect(0,2*mm,self.width,self.bh,3*mm,fill=1,stroke=0)
        c.setFillColor(self.accent)
        c.roundRect(0,2*mm,10*mm,self.bh,3*mm,fill=1,stroke=0)
        c.rect(7*mm,2*mm,3*mm,self.bh,fill=1,stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold",11)
        c.drawString(13*mm, 2*mm+self.bh/2-2*mm, self.num)
        c.setFont("Helvetica-Bold",14)
        c.drawString(28*mm, 2*mm+self.bh/2-2.5*mm, self.title)

class InfoBox(Flowable):
    def __init__(self, lines, title="", color=BLUE, bg=LIGHT, width=None):
        super().__init__()
        self.lines=lines if isinstance(lines,list) else [lines]
        self.title=title; self.color=color; self.bg=bg
        self._w=width or (W-30*mm); self.pad=4*mm; self.lh=5.2*mm
    def wrap(self,*a):
        th=5.5*mm if self.title else 0
        return self._w, self.pad+th+len(self.lines)*self.lh+self.pad
    def draw(self):
        c=self.canv
        th=5.5*mm if self.title else 0
        total=self.pad+th+len(self.lines)*self.lh+self.pad
        c.setFillColor(self.bg); c.roundRect(0,0,self._w,total,2*mm,fill=1,stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0,0,3.5*mm,total,1.5*mm,fill=1,stroke=0)
        c.rect(2*mm,0,1.5*mm,total,fill=1,stroke=0)
        y=total-self.pad
        if self.title:
            c.setFillColor(self.color); c.setFont("Helvetica-Bold",9.5)
            c.drawString(7*mm,y-4.5*mm,self.title); y-=5.5*mm
        c.setFillColor(DARK); c.setFont("Helvetica",8.8)
        for ln in self.lines:
            c.drawString(7*mm,y-4*mm,ln); y-=self.lh

# ── Node diagram: draws linked list nodes with arrows ──────────
class NodeDiagram(Flowable):
    """Draw a singly or doubly linked list with boxes and arrows."""
    def __init__(self, nodes, highlights=None, label="",
                 color=TEAL, doubly=False, circular=False, width=None):
        super().__init__()
        self.nodes     = nodes          # list of strings (node values)
        self.highlights= highlights or {}  # index -> color override
        self.label     = label
        self.color     = color
        self.doubly    = doubly
        self.circular  = circular
        self._w        = width or (W - 30*mm)
        self.node_w    = 18*mm
        self.node_h    = 10*mm
        self.arrow_w   = 8*mm
        self.null_w    = 10*mm
        self.ptr_h     = 7*mm          # space for pointer labels above

    def _total_draw_w(self):
        n = len(self.nodes)
        return n * self.node_w + (n - 1) * self.arrow_w + self.null_w

    def wrap(self, *a):
        h = self.node_h + self.ptr_h + (5*mm if self.label else 0) + 4*mm
        return self._w, h

    def _draw_arrow(self, c, x1, y, x2, color, up=False):
        """Draw a right-pointing arrow from x1 to x2 at height y."""
        ay = y + self.node_h / 2 if not up else y + self.node_h + 2*mm
        c.setStrokeColor(color); c.setFillColor(color)
        c.setLineWidth(1.3)
        c.line(x1, ay, x2 - 2*mm, ay)
        # arrowhead
        c.setLineWidth(0)
        p = c.beginPath()
        p.moveTo(x2, ay)
        p.lineTo(x2 - 2.5*mm, ay + 1.2*mm)
        p.lineTo(x2 - 2.5*mm, ay - 1.2*mm)
        p.close(); c.drawPath(p, fill=1, stroke=0)

    def _draw_back_arrow(self, c, x1, y, x2, color):
        """Draw a left-pointing arrow (for doubly linked list prev pointer)."""
        ay = y + self.node_h / 2 - 2.5*mm
        c.setStrokeColor(color); c.setFillColor(color)
        c.setLineWidth(1.0)
        c.line(x2 + 2*mm, ay, x1, ay)
        p = c.beginPath()
        p.moveTo(x2, ay)
        p.lineTo(x2 + 2.5*mm, ay + 1.2*mm)
        p.lineTo(x2 + 2.5*mm, ay - 1.2*mm)
        p.close(); c.drawPath(p, fill=1, stroke=0)

    def draw(self):
        c   = self.canv
        n   = len(self.nodes)
        tdw = self._total_draw_w()
        sx  = max(0, (self._w - tdw) / 2)
        base_y = 4*mm

        # ── Draw each node ──
        for i, val in enumerate(self.nodes):
            x   = sx + i * (self.node_w + self.arrow_w)
            col = self.highlights.get(i, self.color)

            # node box
            c.setFillColor(col)
            c.setStrokeColor(col)
            c.setLineWidth(1.4)
            c.roundRect(x, base_y, self.node_w, self.node_h, 2*mm, fill=1, stroke=1)

            # value text
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 9)
            tw = c.stringWidth(str(val), "Helvetica-Bold", 9)
            c.drawString(x + self.node_w/2 - tw/2, base_y + 3.2*mm, str(val))

            # index below node
            c.setFillColor(MUTED); c.setFont("Helvetica", 7)
            iw = c.stringWidth(str(i), "Helvetica", 7)
            c.drawString(x + self.node_w/2 - iw/2, base_y - 3.5*mm, str(i))

            # ── Forward arrow (next pointer) ──
            if i < n - 1:
                ax1 = x + self.node_w
                ax2 = x + self.node_w + self.arrow_w
                self._draw_arrow(c, ax1, base_y, ax2, MUTED)

            # ── Back arrow for doubly linked list ──
            if self.doubly and i < n - 1:
                ax1 = x + self.node_w
                ax2 = x + self.node_w + self.arrow_w
                self._draw_back_arrow(c, ax1, base_y, ax2, HexColor("#94A3B8"))

        # ── NULL terminator ──
        null_x = sx + n * self.node_w + (n - 1) * self.arrow_w + 2*mm
        c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8)
        c.drawString(null_x, base_y + 3*mm, "NULL")

        # ── Circular back-arrow ──
        if self.circular and n > 0:
            last_x = sx + (n - 1) * (self.node_w + self.arrow_w) + self.node_w
            # draw arc below
            c.setStrokeColor(GOLD); c.setLineWidth(1.3)
            arc_y = base_y - 5*mm
            c.line(last_x, base_y + self.node_h/2, last_x + 4*mm, base_y + self.node_h/2)
            c.line(last_x + 4*mm, base_y + self.node_h/2, last_x + 4*mm, arc_y)
            c.line(last_x + 4*mm, arc_y, sx, arc_y)
            c.line(sx, arc_y, sx, base_y + self.node_h/2)
            p = c.beginPath()
            p.moveTo(sx, base_y + self.node_h/2)
            p.lineTo(sx + 2.5*mm, base_y + self.node_h/2 + 1.2*mm)
            p.lineTo(sx + 2.5*mm, base_y + self.node_h/2 - 1.2*mm)
            p.close(); c.setFillColor(GOLD); c.drawPath(p, fill=1, stroke=0)

        # ── Pointer labels (head, slow, fast, etc.) above nodes ──
        for i, lbl in self.highlights.items():
            if isinstance(lbl, str):  # label mode
                pass  # handled separately
        # Draw pointer labels
        for i, info in self.highlights.items():
            if isinstance(info, tuple):  # (color, label)
                col, lbl = info
                x = sx + i * (self.node_w + self.arrow_w)
                c.setFillColor(col); c.setFont("Helvetica-Bold", 8)
                lw = c.stringWidth(lbl, "Helvetica-Bold", 8)
                py = base_y + self.node_h + 1.5*mm
                c.drawString(x + self.node_w/2 - lw/2, py, lbl)
                c.setLineWidth(1); c.setStrokeColor(col)
                c.line(x + self.node_w/2, py - 0.5*mm,
                       x + self.node_w/2, base_y + self.node_h)

        # ── Label ──
        if self.label:
            c.setFillColor(MUTED); c.setFont("Helvetica-Oblique", 8)
            lw = c.stringWidth(self.label, "Helvetica-Oblique", 8)
            top_y = base_y + self.node_h + self.ptr_h
            c.drawString(self._w/2 - lw/2, top_y, self.label)


class CppBlock(Flowable):
    KW = {
        'int','long','bool','char','void','string','vector','map','unordered_map',
        'set','unordered_set','pair','deque','stack','queue','priority_queue',
        'auto','const','return','if','else','while','for','do','break','continue',
        'class','struct','public','private','protected','true','false','nullptr',
        'new','delete','include','using','namespace','std','endl','static',
        'inline','template','typename','unsigned','size_t','this','NULL',
        'ListNode','Node','DLinkedNode','forward_list',
        'sort','max','min','swap','reverse','push_back','pop_back',
        'begin','end','empty','size','insert','erase','count','clear',
        'INT_MAX','INT_MIN','next','prev','val','head','tail',
    }
    def __init__(self, lines, width=None):
        super().__init__()
        self.lines = lines; self._w = width or (W-30*mm)
        self.lh = 4.7*mm; self.hh = 7*mm; self.pad = 4*mm
    def wrap(self, *a):
        return self._w, self.hh + self.pad + len(self.lines)*self.lh + self.pad
    def draw(self):
        c = self.canv
        th = self.hh + self.pad + len(self.lines)*self.lh + self.pad
        c.setFillColor(CODE_BG); c.roundRect(0,0,self._w,th,3*mm,fill=1,stroke=0)
        c.setFillColor(CODE_HDR); c.roundRect(0,th-self.hh,self._w,self.hh,3*mm,fill=1,stroke=0)
        c.rect(0,th-self.hh,self._w,self.hh/2,fill=1,stroke=0)
        c.setFillColor(CPP_TYPE); c.setFont("Helvetica-Bold",7.5)
        c.drawString(4*mm,th-self.hh+2.2*mm,"C++")
        for i,col in enumerate([HexColor("#FF5F57"),HexColor("#FEBC2E"),HexColor("#28C840")]):
            c.setFillColor(col); c.circle(self._w-(3-i)*5.5*mm,th-self.hh/2,1.4*mm,fill=1,stroke=0)
        y = th - self.hh - self.pad - self.lh
        for idx, raw in enumerate(self.lines):
            c.setFillColor(HexColor("#3D444D")); c.setFont("Courier",7.5)
            c.drawString(3*mm, y+1.2*mm, f"{idx+1:2d}")
            stripped = raw.lstrip(); indent = len(raw)-len(stripped)
            x = 12*mm + indent*2.2*mm
            self._draw_line(c, stripped, x, y+1.2*mm)
            y -= self.lh
    def _draw_line(self, c, text, x, y):
        import re
        if '//' in text:
            ci = text.index('//')
            x = self._draw_tokens(c, text[:ci], x, y)
            c.setFillColor(CPP_CMT); c.setFont("Courier-Oblique",8.5)
            c.drawString(x,y,text[ci:]); return
        if text.startswith('#'):
            c.setFillColor(CPP_KW); c.setFont("Courier-Bold",8.5)
            c.drawString(x,y,text); return
        if text.strip().startswith('/*') or text.strip().startswith('*'):
            c.setFillColor(CPP_CMT); c.setFont("Courier-Oblique",8.5)
            c.drawString(x,y,text); return
        self._draw_tokens(c, text, x, y)
    def _draw_tokens(self, c, text, x, y):
        import re
        tokens = re.findall(r'[A-Za-z_]\w*|"[^"]*"|\'[^\']*\'|\d+\.\d+|\d+|[^\w\s]|\s+', text)
        for tok in tokens:
            if not tok: continue
            if tok.strip() == '':
                x += c.stringWidth(tok,"Courier",8.5); continue
            if tok in self.KW:
                c.setFillColor(CPP_KW); c.setFont("Courier-Bold",8.5)
            elif tok.startswith('"') or tok.startswith("'"):
                c.setFillColor(CPP_STR); c.setFont("Courier",8.5)
            elif tok.isdigit() or tok.replace('.','',1).isdigit():
                c.setFillColor(CPP_NUM); c.setFont("Courier",8.5)
            else:
                c.setFillColor(CODE_FG); c.setFont("Courier",8.5)
            c.drawString(x,y,tok); x += c.stringWidth(tok,"Courier",8.5)
        return x

# ─── Style helpers ─────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName="Helvetica",fontSize=9.5,textColor=DARK,
                leading=14,spaceBefore=3,spaceAfter=3)
    base.update(kw); return ParagraphStyle(name,**base)

ST = {
    "body":    S("body",   alignment=TA_JUSTIFY, leading=15),
    "bullet":  S("bullet", leftIndent=12, firstLineIndent=-8, leading=13, spaceBefore=2, spaceAfter=2),
    "caption": S("caption",fontName="Helvetica-Oblique",fontSize=8.5,textColor=MUTED,spaceBefore=2,spaceAfter=6),
    "toc_h":   S("toc_h", fontName="Helvetica-Bold",fontSize=11,textColor=NAVY,spaceBefore=5,spaceAfter=2,leading=15),
    "toc_i":   S("toc_i", fontSize=9.5,textColor=DARK,spaceBefore=1,spaceAfter=1,leftIndent=8,leading=13),
    "cover_t": S("ct", fontName="Helvetica-Bold",fontSize=34,textColor=white,leading=40,alignment=TA_CENTER),
    "cover_s": S("cs", fontName="Helvetica-Bold",fontSize=19,textColor=HexColor("#A0DDE6"),leading=26,alignment=TA_CENTER),
    "cover_d": S("cd", fontName="Helvetica",fontSize=11,textColor=HexColor("#CBD5E1"),leading=16,alignment=TA_CENTER),
    "h2": S("h2",fontName="Helvetica-Bold",fontSize=14,textColor=BLUE,leading=20,spaceBefore=10,spaceAfter=4),
    "h3": S("h3",fontName="Helvetica-Bold",fontSize=11.5,textColor=TEAL,leading=16,spaceBefore=8,spaceAfter=3),
    "h4": S("h4",fontName="Helvetica-Bold",fontSize=10,textColor=NAVY,leading=14,spaceBefore=6,spaceAfter=2),
}

def sp(n=1):  return Spacer(1, n*4*mm)
def hr(c=BORDER): return HRFlowable(width="100%",thickness=0.5,color=c,spaceAfter=2*mm,spaceBefore=2*mm)
def body(t):  return Paragraph(t, ST["body"])
def cap(t):   return Paragraph(f"<i>{t}</i>", ST["caption"])
def h2(t, col=BLUE):   return Paragraph(t, ParagraphStyle("_h2",parent=ST["h2"],textColor=col))
def h3(t, col=TEAL):   return Paragraph(t, ParagraphStyle("_h3",parent=ST["h3"],textColor=col))
def h4(t, col=NAVY):   return Paragraph(t, ParagraphStyle("_h4",parent=ST["h4"],textColor=col))
def bl(t, col="#1F7A8C"): return Paragraph(f'<font color="{col}">▸</font>  {t}', ST["bullet"])
def nb(n, t, col="#1F7A8C"): return Paragraph(f'<font color="{col}"><b>{n}.</b></font>  {t}', ST["bullet"])

def mtbl(data, cw, extra=None):
    base = [
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),
        ("BACKGROUND",(0,1),(0,-1),LIGHT),("TEXTCOLOR",(0,1),(0,-1),NAVY),
        ("ROWBACKGROUNDS",(1,1),(-1,-1),[white,ALT_ROW]),
        ("FONTSIZE",(0,0),(-1,-1),8.5),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),
        ("BOX",(0,0),(-1,-1),0.5,BORDER),("INNERGRID",(0,0),(-1,-1),0.3,BORDER),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]
    if extra: base += extra
    t = Table(data, colWidths=cw); t.setStyle(TableStyle(base)); return t

# ══════════════════════════════════════════════════════════════
#  STORY
# ══════════════════════════════════════════════════════════════
story = []

# ── COVER ──────────────────────────────────────────────────────
story.append(sp(4))
cd = [
    [Paragraph("DSA Revision Notes", ST["cover_t"])],
    [Paragraph("Topic 5 — Linked List (All Types &amp; Operations)", ST["cover_s"])],
    [Paragraph(
        "Singly · Doubly · Circular · XOR List  •  All Operations with Diagrams<br/>"
        "Floyd's Cycle · Reversal · Merge · LRU Cache · 20+ C++ examples",
        ST["cover_d"]
    )],
]
ct = Table(cd, colWidths=[W-30*mm])
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),NAVY),
    ("TOPPADDING",(0,0),(-1,0),22),("BOTTOMPADDING",(0,0),(-1,0),8),
    ("TOPPADDING",(0,1),(-1,1),8),("BOTTOMPADDING",(0,1),(-1,1),10),
    ("TOPPADDING",(0,2),(-1,2),8),("BOTTOMPADDING",(0,2),(-1,2),22),
    ("ROUNDEDCORNERS",[4*mm]),
]))
story.append(ct); story.append(sp(2))

stats = [[
    Paragraph('<b><font color="#1A3C5E">11</font></b><br/><font size="8" color="#64748B">Sections</font>',
              ParagraphStyle("s1",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">25+</font></b><br/><font size="8" color="#64748B">C++ Examples</font>',
              ParagraphStyle("s2",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">12</font></b><br/><font size="8" color="#64748B">Node Diagrams</font>',
              ParagraphStyle("s3",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">22+</font></b><br/><font size="8" color="#64748B">LeetCode Problems</font>',
              ParagraphStyle("s4",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
]]
st = Table(stats, colWidths=[(W-30*mm)/4]*4)
st.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),LIGHT),("BOX",(0,0),(-1,-1),0.5,BORDER),
    ("INNERGRID",(0,0),(-1,-1),0.5,BORDER),
    ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
]))
story.append(st); story.append(PageBreak())

# ── TOC ────────────────────────────────────────────────────────
story.append(Banner("TOC","Table of Contents",NAVY,TEAL))
story.append(sp(1))
toc = [
    ("1.", "Introduction — What is a Linked List?"),
    ("",   "→ Definition · Memory layout · vs Array comparison"),
    ("2.", "Singly Linked List — Full Implementation"),
    ("",   "→ Node struct · All operations with C++ code"),
    ("",   "→ Insert at head/tail/position · Delete · Search · Reverse"),
    ("3.", "Doubly Linked List — Full Implementation"),
    ("",   "→ DNode struct with prev/next · All operations"),
    ("",   "→ Insert/Delete at both ends · Bidirectional traversal"),
    ("4.", "Circular Linked List"),
    ("",   "→ Singly circular · Doubly circular · Josephus problem"),
    ("5.", "XOR Linked List (Memory-Efficient Doubly LL)"),
    ("",   "→ XOR trick · insert/delete with XOR addresses"),
    ("6.", "Two Pointer Techniques on Linked Lists"),
    ("",   "→ Find middle · Nth from end · Detect cycle (Floyd's)"),
    ("",   "→ Find cycle entry · Intersection of two lists"),
    ("7.", "Reversal Patterns"),
    ("",   "→ Reverse full list · Reverse between L and R"),
    ("",   "→ Reverse in K-groups · Reverse alternate K nodes"),
    ("8.", "Merge & Sort Patterns"),
    ("",   "→ Merge two sorted lists · Merge K sorted lists"),
    ("",   "→ Sort a linked list (Merge Sort)"),
    ("9.", "Linked List + HashMap Patterns"),
    ("",   "→ Copy list with random pointer · Detect & remove loop"),
    ("",   "→ LRU Cache (DLL + HashMap)"),
    ("10.","Palindrome, Reorder & Other Patterns"),
    ("",   "→ Palindrome check · Reorder list · Odd-Even grouping"),
    ("11.","Complexity Cheat Sheet & LeetCode Map"),
]
for num, title in toc:
    if num:
        story.append(Paragraph(f'<b><font color="#1A3C5E">{num}</font></b>  <b>{title}</b>', ST["toc_h"]))
    else:
        story.append(Paragraph(f'<font color="#64748B">        {title}</font>', ST["toc_i"]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 1 — INTRODUCTION
# ══════════════════════════════════════════════════════════════
story.append(Banner("1","Introduction — What is a Linked List?",NAVY,TEAL))
story.append(sp(1))

story.append(h2("1.1  Definition"))
story.append(body(
    "A <b>Linked List</b> is a linear data structure where elements (<b>nodes</b>) are stored at "
    "<b>non-contiguous memory locations</b>. Each node contains a <b>data field</b> and one or more "
    "<b>pointer fields</b> that link it to the next (and/or previous) node. "
    "Unlike arrays, linked lists have no random access — to reach node at position i, you must "
    "traverse from the head, taking O(i) time."
))
story.append(sp(0.5))

# Basic SLL diagram
story.append(NodeDiagram(
    ["10","20","30","40","50"],
    highlights={0:(TEAL,"head"), 4:(RED,"tail")},
    label="Singly Linked List — each node stores value + pointer to next",
    color=TEAL
))
story.append(sp(0.5))

story.append(h2("1.2  Memory Layout — Array vs Linked List"))
story.append(body(
    "Arrays store elements in <b>contiguous memory</b> — element i is at base + i×size. "
    "Linked list nodes can be anywhere in memory; pointers stitch them together. "
    "This gives linked lists O(1) insert/delete at known positions but O(n) access by index."
))
story.append(sp(0.5))

cmp_data = [
    ["Property",            "Array",               "Linked List"],
    ["Memory layout",       "Contiguous",          "Non-contiguous (scattered)"],
    ["Access by index",     "O(1) direct",         "O(n) traversal"],
    ["Insert at front",     "O(n) shift all",      "O(1) update head pointer"],
    ["Insert at end",       "O(1)* amortized",     "O(n) traverse / O(1) with tail ptr"],
    ["Insert at position i","O(n) shift",          "O(n) traverse + O(1) relink"],
    ["Delete at front",     "O(n) shift all",      "O(1) move head"],
    ["Delete at position i","O(n) shift",          "O(n) traverse + O(1) unlink"],
    ["Search",              "O(n) / O(log n) sorted","O(n) always"],
    ["Memory overhead",     "None (pure data)",    "Extra pointer(s) per node"],
    ["Cache performance",   "Excellent (locality)","Poor (pointer chasing)"],
    ["Size flexibility",    "Fixed (static) / resize","Dynamic — grows node by node"],
    ["Reverse",             "O(n)",                "O(n)"],
]
extra_cmp = []
for i in range(1, len(cmp_data)):
    extra_cmp.append(("TEXTCOLOR",(1,i),(1,i),NAVY))
    extra_cmp.append(("TEXTCOLOR",(2,i),(2,i),TEAL))
story.append(mtbl(cmp_data, [45*mm,55*mm,68*mm], extra=extra_cmp))
story.append(cap("Table 1: Array vs Linked List — complete comparison"))
story.append(sp(0.5))

story.append(h2("1.3  Types of Linked Lists"))
types = [
    ("Singly Linked List",   "Each node has one pointer: next. Traversal only forward."),
    ("Doubly Linked List",   "Each node has two pointers: prev and next. Bidirectional traversal."),
    ("Circular Linked List", "Last node's next points back to head (no NULL terminator)."),
    ("Doubly Circular LL",   "Doubly linked + tail.next = head + head.prev = tail."),
    ("XOR Linked List",      "Memory-efficient doubly LL: one pointer stores XOR of prev and next addresses."),
    ("Skip List",            "Multiple layers of linked lists for O(log n) average search."),
]
for name, desc in types:
    story.append(bl(f"<b>{name}:</b> {desc}"))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 2 — SINGLY LINKED LIST
# ══════════════════════════════════════════════════════════════
story.append(Banner("2","Singly Linked List — Full Implementation",TEAL,NAVY))
story.append(sp(1))

story.append(h2("2.1  Node Structure"))
story.append(CppBlock([
    "// Standard LeetCode ListNode definition",
    "struct ListNode {",
    "    int val;",
    "    ListNode* next;",
    "    ListNode()          : val(0),  next(nullptr) {}",
    "    ListNode(int x)     : val(x),  next(nullptr) {}",
    "    ListNode(int x, ListNode* next) : val(x), next(next) {}",
    "};",
    "",
    "// Full SLL class",
    "class SinglyLinkedList {",
    "    ListNode* head;",
    "    int _size;",
    "public:",
    "    SinglyLinkedList() : head(nullptr), _size(0) {}",
    "    ~SinglyLinkedList() {",
    "        while (head) { ListNode* tmp = head; head = head->next; delete tmp; }",
    "    }",
    "    int size()  const { return _size; }",
    "    bool empty()const { return head == nullptr; }",
    "};",
]))
story.append(sp(0.8))

story.append(h2("2.2  Insert Operations"))
story.append(h3("Insert at Head — O(1)"))
story.append(NodeDiagram(
    ["NEW","10","20","30"],
    highlights={0:(GREEN,"new"), 1:(TEAL,"old head")},
    label="Insert at head: new->next = head; head = new  →  O(1)",
    color=TEAL
))
story.append(sp(0.3))
story.append(CppBlock([
    "void insertAtHead(int val) {",
    "    ListNode* node = new ListNode(val);",
    "    node->next = head;   // point new node to old head",
    "    head = node;         // update head to new node",
    "    _size++;",
    "}",
    "// Time: O(1)   Space: O(1)",
]))
story.append(sp(0.5))

story.append(h3("Insert at Tail — O(n) without tail ptr, O(1) with tail ptr"))
story.append(CppBlock([
    "void insertAtTail(int val) {",
    "    ListNode* node = new ListNode(val);",
    "    if (!head) { head = node; _size++; return; }",
    "    ListNode* curr = head;",
    "    while (curr->next) curr = curr->next;  // traverse to last node",
    "    curr->next = node;    // link last node to new node",
    "    _size++;",
    "}",
    "// Time: O(n) — must find tail.  Optimize: keep a 'tail' pointer → O(1)",
]))
story.append(sp(0.5))

story.append(h3("Insert at Position k — O(k)"))
story.append(CppBlock([
    "void insertAt(int pos, int val) {",
    "    if (pos < 0 || pos > _size) return;  // invalid",
    "    if (pos == 0) { insertAtHead(val); return; }",
    "    ListNode* node = new ListNode(val);",
    "    ListNode* curr = head;",
    "    for (int i = 0; i < pos - 1; i++)    // stop at node BEFORE pos",
    "        curr = curr->next;",
    "    node->next = curr->next;              // link new node forward",
    "    curr->next = node;                    // link predecessor to new",
    "    _size++;",
    "}",
    "// Time: O(pos)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("2.3  Delete Operations"))
story.append(h3("Delete at Head — O(1)"))
story.append(CppBlock([
    "int deleteAtHead() {",
    "    if (!head) throw underflow_error(\"List empty\");",
    "    ListNode* tmp = head;",
    "    int val = tmp->val;",
    "    head = head->next;   // advance head",
    "    delete tmp;          // free old head",
    "    _size--;",
    "    return val;",
    "}",
    "// Time: O(1)   Space: O(1)",
]))
story.append(sp(0.5))

story.append(h3("Delete at Position k — O(k)"))
story.append(CppBlock([
    "int deleteAt(int pos) {",
    "    if (pos < 0 || pos >= _size) throw out_of_range(\"Invalid pos\");",
    "    if (pos == 0) return deleteAtHead();",
    "    ListNode* curr = head;",
    "    for (int i = 0; i < pos - 1; i++)     // stop at node BEFORE pos",
    "        curr = curr->next;",
    "    ListNode* toDelete = curr->next;",
    "    int val = toDelete->val;",
    "    curr->next = toDelete->next;            // bypass the deleted node",
    "    delete toDelete;",
    "    _size--;",
    "    return val;",
    "}",
    "// Time: O(pos)   Space: O(1)",
]))
story.append(sp(0.5))

story.append(h3("Delete Node with Given Value — O(n)"))
story.append(CppBlock([
    "// LC 203 — Remove Linked List Elements",
    "ListNode* removeElements(ListNode* head, int val) {",
    "    ListNode dummy(0, head);           // dummy node before head",
    "    ListNode* curr = &dummy;",
    "    while (curr->next) {",
    "        if (curr->next->val == val) {",
    "            ListNode* tmp = curr->next;",
    "            curr->next = tmp->next;    // bypass",
    "            delete tmp;",
    "        } else {",
    "            curr = curr->next;",
    "        }",
    "    }",
    "    return dummy.next;",
    "}",
    "// Dummy node simplifies edge case: deleting head",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("2.4  Traversal & Search"))
story.append(CppBlock([
    "// Forward traversal — O(n)",
    "void printList(ListNode* head) {",
    "    ListNode* curr = head;",
    "    while (curr) {",
    "        cout << curr->val;",
    "        if (curr->next) cout << \" -> \";",
    "        curr = curr->next;",
    "    }",
    "    cout << \" -> NULL\" << endl;",
    "}",
    "",
    "// Search — O(n)",
    "ListNode* search(ListNode* head, int target) {",
    "    ListNode* curr = head;",
    "    while (curr) {",
    "        if (curr->val == target) return curr;",
    "        curr = curr->next;",
    "    }",
    "    return nullptr;   // not found",
    "}",
    "",
    "// Length — O(n)",
    "int length(ListNode* head) {",
    "    int cnt = 0;",
    "    for (ListNode* c = head; c; c = c->next) cnt++;",
    "    return cnt;",
    "}",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 3 — DOUBLY LINKED LIST
# ══════════════════════════════════════════════════════════════
story.append(Banner("3","Doubly Linked List — Full Implementation",BLUE,TEAL))
story.append(sp(1))

story.append(h2("3.1  Node Structure & Memory Layout"))
story.append(NodeDiagram(
    ["10","20","30","40"],
    highlights={0:(NAVY,"head"), 3:(RED,"tail")},
    label="Doubly Linked List — each node has prev and next pointers",
    color=BLUE, doubly=True
))
story.append(sp(0.5))
story.append(CppBlock([
    "struct DNode {",
    "    int val;",
    "    DNode* prev;",
    "    DNode* next;",
    "    DNode(int v) : val(v), prev(nullptr), next(nullptr) {}",
    "};",
    "",
    "class DoublyLinkedList {",
    "    DNode* head;",
    "    DNode* tail;",
    "    int _size;",
    "public:",
    "    DoublyLinkedList() : head(nullptr), tail(nullptr), _size(0) {}",
    "};",
]))
story.append(sp(0.8))

story.append(h2("3.2  Insert Operations"))
story.append(CppBlock([
    "// Insert at HEAD — O(1)",
    "void insertFront(int val) {",
    "    DNode* node = new DNode(val);",
    "    if (!head) { head = tail = node; }",
    "    else {",
    "        node->next = head;   // new->next = old head",
    "        head->prev = node;   // old head->prev = new",
    "        head = node;         // update head",
    "    }",
    "    _size++;",
    "}",
    "",
    "// Insert at TAIL — O(1) with tail pointer",
    "void insertBack(int val) {",
    "    DNode* node = new DNode(val);",
    "    if (!tail) { head = tail = node; }",
    "    else {",
    "        tail->next = node;   // old tail->next = new",
    "        node->prev = tail;   // new->prev = old tail",
    "        tail = node;         // update tail",
    "    }",
    "    _size++;",
    "}",
    "",
    "// Insert AFTER a given node — O(1) if node is known",
    "void insertAfter(DNode* node, int val) {",
    "    if (!node) return;",
    "    DNode* newNode = new DNode(val);",
    "    newNode->next = node->next;",
    "    newNode->prev = node;",
    "    if (node->next) node->next->prev = newNode;",
    "    else            tail = newNode;   // new node is new tail",
    "    node->next = newNode;",
    "    _size++;",
    "}",
]))
story.append(sp(0.8))

story.append(h2("3.3  Delete Operations"))
story.append(CppBlock([
    "// Delete a given NODE — O(1) if pointer is known",
    "void deleteNode(DNode* node) {",
    "    if (!node) return;",
    "    if (node->prev) node->prev->next = node->next;  // bypass backward",
    "    else            head = node->next;               // deleting head",
    "    if (node->next) node->next->prev = node->prev;  // bypass forward",
    "    else            tail = node->prev;               // deleting tail",
    "    delete node;",
    "    _size--;",
    "}",
    "// KEY ADVANTAGE over SLL: O(1) delete when node pointer is known",
    "// SLL needs O(n) to find the predecessor",
    "",
    "// Delete from FRONT — O(1)",
    "int deleteFront() {",
    "    if (!head) throw underflow_error(\"Empty list\");",
    "    DNode* tmp = head;",
    "    int val = tmp->val;",
    "    head = head->next;",
    "    if (head) head->prev = nullptr;",
    "    else      tail = nullptr;   // list became empty",
    "    delete tmp; _size--;",
    "    return val;",
    "}",
    "",
    "// Delete from BACK — O(1)",
    "int deleteBack() {",
    "    if (!tail) throw underflow_error(\"Empty list\");",
    "    DNode* tmp = tail;",
    "    int val = tmp->val;",
    "    tail = tail->prev;",
    "    if (tail) tail->next = nullptr;",
    "    else      head = nullptr;",
    "    delete tmp; _size--;",
    "    return val;",
    "}",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 4 — CIRCULAR LINKED LIST
# ══════════════════════════════════════════════════════════════
story.append(Banner("4","Circular Linked List",GOLD,TEAL))
story.append(sp(1))

story.append(h2("4.1  Singly Circular Linked List"))
story.append(NodeDiagram(
    ["10","20","30","40"],
    highlights={0:(GOLD,"head")},
    label="Circular SLL — last node's next points back to head (no NULL)",
    color=GOLD, circular=True
))
story.append(sp(0.5))
story.append(CppBlock([
    "struct CNode { int val; CNode* next; CNode(int v): val(v), next(nullptr){} };",
    "",
    "class CircularSLL {",
    "    CNode* tail;   // Keep TAIL pointer (tail->next = head)",
    "    int _size;",
    "public:",
    "    CircularSLL() : tail(nullptr), _size(0) {}",
    "",
    "    void insertFront(int val) {",
    "        CNode* node = new CNode(val);",
    "        if (!tail) { node->next = node; tail = node; }  // only node",
    "        else {",
    "            node->next = tail->next;   // new->next = head",
    "            tail->next = node;         // tail->next = new (becomes head)",
    "        }",
    "        _size++;",
    "    }",
    "    void insertBack(int val) {",
    "        insertFront(val);              // insert, then advance tail",
    "        tail = tail->next;",
    "    }",
    "    void traverse() {",
    "        if (!tail) return;",
    "        CNode* curr = tail->next;      // start from head",
    "        do {",
    "            cout << curr->val << \" \";",
    "            curr = curr->next;",
    "        } while (curr != tail->next);  // stop when back at head",
    "        cout << endl;",
    "    }",
    "};",
    "// Key: use do-while loop (not while) since we start at head",
]))
story.append(sp(0.8))

story.append(h2("4.2  Josephus Problem — Classic Circular LL Application"))
story.append(body(
    "n people in a circle; every k-th person is eliminated. Find the last survivor's position. "
    "Model with circular linked list: traverse k steps, remove node, repeat until 1 remains."
))
story.append(CppBlock([
    "// Josephus: n people, every k-th eliminated. Returns 0-indexed survivor position.",
    "int josephus(int n, int k) {",
    "    // Mathematical O(n) solution (no list needed)",
    "    int pos = 0;                    // survivor position with 1 person",
    "    for (int i = 2; i <= n; i++)",
    "        pos = (pos + k) % i;        // recurrence relation",
    "    return pos;                     // 0-indexed position",
    "}",
    "",
    "// Simulation with circular linked list — O(nk)",
    "int josephusSim(int n, int k) {",
    "    list<int> circle;",
    "    for (int i = 1; i <= n; i++) circle.push_back(i);",
    "    auto it = circle.begin();",
    "    while (circle.size() > 1) {",
    "        for (int i = 1; i < k; i++) {",
    "            it++;",
    "            if (it == circle.end()) it = circle.begin();",
    "        }",
    "        it = circle.erase(it);",
    "        if (it == circle.end()) it = circle.begin();",
    "    }",
    "    return circle.front();",
    "}",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 5 — XOR LINKED LIST
# ══════════════════════════════════════════════════════════════
story.append(Banner("5","XOR Linked List — Memory-Efficient Doubly LL",PURPLE,TEAL))
story.append(sp(1))

story.append(h2("5.1  Core Concept"))
story.append(body(
    "A normal doubly linked list stores two pointers per node (16 bytes on 64-bit). "
    "An <b>XOR Linked List</b> stores only one pointer per node: the <b>XOR of prev and next addresses</b>. "
    "This halves pointer memory. To navigate: XOR the known neighbor address with the stored value to get the other."
))
story.append(sp(0.5))
story.append(InfoBox([
    "node->both = XOR(prev_addr, next_addr)",
    "To get next: next = XOR(node->both, prev_addr)",
    "To get prev: prev = XOR(node->both, next_addr)",
    "XOR properties: A^A=0, A^0=A, A^B^A=B  →  (prev^next)^prev = next",
],title="🔑 XOR Trick",color=PURPLE,bg=PURPLE_BG))
story.append(sp(0.5))
story.append(CppBlock([
    "#include <cstdint>",
    "",
    "struct XorNode {",
    "    int val;",
    "    XorNode* both;   // stores XOR(prev, next)",
    "    XorNode(int v) : val(v), both(nullptr) {}",
    "};",
    "",
    "// Helper: XOR two pointers safely",
    "XorNode* XOR(XorNode* a, XorNode* b) {",
    "    return (XorNode*)((uintptr_t)a ^ (uintptr_t)b);",
    "}",
    "",
    "// Insert at head",
    "XorNode* insertFront(XorNode* head, int val) {",
    "    XorNode* node = new XorNode(val);",
    "    node->both = XOR(nullptr, head);   // prev=NULL, next=head",
    "    if (head) head->both = XOR(node, XOR(nullptr, head->both));",
    "    return node;   // new head",
    "}",
    "",
    "// Traverse forward",
    "void traverse(XorNode* head) {",
    "    XorNode* prev = nullptr;",
    "    XorNode* curr = head;",
    "    while (curr) {",
    "        cout << curr->val << \" \";",
    "        XorNode* next = XOR(prev, curr->both);",
    "        prev = curr;",
    "        curr = next;",
    "    }",
    "}",
    "// Space: O(1) pointer overhead vs DLL's O(2) per node",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 6 — TWO POINTER TECHNIQUES
# ══════════════════════════════════════════════════════════════
story.append(Banner("6","Two Pointer Techniques on Linked Lists",RED,TEAL))
story.append(sp(1))

story.append(h2("6.1  Find Middle Node  (LC 876)  — Easy"))
story.append(body(
    "Use fast and slow pointers. Slow moves 1 step, fast moves 2. "
    "When fast reaches end, slow is at middle. "
    "For even-length lists, returns the <b>second</b> middle."
))
story.append(NodeDiagram(
    ["1","2","3","4","5"],
    highlights={2:(GREEN,(GREEN,"slow=mid")), 4:(RED,(RED,"fast=end"))},
    label="slow at middle (index 2) when fast reaches end (index 4)",
    color=TEAL
))
story.append(sp(0.3))
story.append(CppBlock([
    "// LC 876 — Middle of the Linked List",
    "ListNode* middleNode(ListNode* head) {",
    "    ListNode* slow = head;",
    "    ListNode* fast = head;",
    "    while (fast && fast->next) {",
    "        slow = slow->next;         // move 1 step",
    "        fast = fast->next->next;   // move 2 steps",
    "    }",
    "    return slow;   // slow is at middle",
    "}",
    "// Time: O(n)   Space: O(1)",
    "// For [1,2,3,4,5]  → returns node 3 (index 2)",
    "// For [1,2,3,4]    → returns node 3 (second middle)",
]))
story.append(sp(0.8))

story.append(h2("6.2  Remove Nth Node From End  (LC 19)  — Medium"))
story.append(body(
    "Move fast pointer n+1 steps ahead, then advance both until fast hits NULL. "
    "Slow is now at the node <b>before</b> the target — unlink target."
))
story.append(CppBlock([
    "ListNode* removeNthFromEnd(ListNode* head, int n) {",
    "    ListNode dummy(0, head);",
    "    ListNode* fast = &dummy;",
    "    ListNode* slow = &dummy;",
    "    // Advance fast n+1 steps (slow will stop BEFORE the target)",
    "    for (int i = 0; i <= n; i++) fast = fast->next;",
    "    // Move both until fast reaches NULL",
    "    while (fast) {",
    "        slow = slow->next;",
    "        fast = fast->next;",
    "    }",
    "    // slow->next is the node to delete",
    "    ListNode* toDelete = slow->next;",
    "    slow->next = toDelete->next;",
    "    delete toDelete;",
    "    return dummy.next;",
    "}",
    "// Time: O(n)   Space: O(1)  — single pass",
]))
story.append(sp(0.8))

story.append(h2("6.3  Detect Cycle — Floyd's Algorithm  (LC 141/142)"))
story.append(body(
    "Floyd's Tortoise and Hare: slow moves 1 step, fast moves 2. "
    "If a cycle exists, they will eventually meet inside the cycle. "
    "<b>Phase 2:</b> reset one pointer to head, move both 1 step — they meet at cycle entry."
))
story.append(NodeDiagram(
    ["3","1","2","4","5"],
    highlights={
        0:(TEAL,(TEAL,"head")),
        2:(GREEN,(GREEN,"slow")),
        4:(RED,(RED,"fast")),
    },
    label="Floyd's: slow and fast will meet inside the cycle",
    color=TEAL
))
story.append(sp(0.3))
story.append(CppBlock([
    "// LC 141 — Linked List Cycle (detect)",
    "bool hasCycle(ListNode* head) {",
    "    ListNode* slow = head;",
    "    ListNode* fast = head;",
    "    while (fast && fast->next) {",
    "        slow = slow->next;",
    "        fast = fast->next->next;",
    "        if (slow == fast) return true;   // cycle detected",
    "    }",
    "    return false;   // fast reached NULL — no cycle",
    "}",
    "// Time: O(n)   Space: O(1)",
    "",
    "// LC 142 — Find ENTRY POINT of cycle",
    "ListNode* detectCycle(ListNode* head) {",
    "    ListNode* slow = head, *fast = head;",
    "    // Phase 1: detect meeting point",
    "    while (fast && fast->next) {",
    "        slow = slow->next;",
    "        fast = fast->next->next;",
    "        if (slow == fast) break;",
    "    }",
    "    if (!fast || !fast->next) return nullptr;  // no cycle",
    "    // Phase 2: find entry — reset slow to head, move both 1 step",
    "    slow = head;",
    "    while (slow != fast) {",
    "        slow = slow->next;",
    "        fast = fast->next;",
    "    }",
    "    return slow;   // cycle entry point",
    "}",
    "// Proof: if cycle starts at distance F from head, and cycle length C",
    "// meeting point is at distance C - (F % C) from entry",
    "// resetting slow to head and stepping both by 1 aligns them at entry",
]))
story.append(sp(0.8))

story.append(h2("6.4  Intersection of Two Linked Lists  (LC 160)  — Easy"))
story.append(body(
    "Find the node where two lists merge. Trick: traverse both lists. "
    "When a pointer reaches its end, redirect it to the <b>other</b> list's head. "
    "After at most m+n steps they meet at the intersection (or both at NULL if none)."
))
story.append(CppBlock([
    "ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {",
    "    ListNode* a = headA;",
    "    ListNode* b = headB;",
    "    // Each pointer traverses: own list + other list",
    "    // Total distance same for both: lenA + lenB",
    "    while (a != b) {",
    "        a = a ? a->next : headB;   // redirect to B when A ends",
    "        b = b ? b->next : headA;   // redirect to A when B ends",
    "    }",
    "    return a;   // intersection node, or nullptr if none",
    "}",
    "// Time: O(m+n)   Space: O(1)",
    "// If no intersection: both become nullptr simultaneously → loop ends",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 7 — REVERSAL PATTERNS
# ══════════════════════════════════════════════════════════════
story.append(Banner("7","Reversal Patterns",ORANGE,TEAL))
story.append(sp(1))

story.append(h2("7.1  Reverse Full List  (LC 206)  — Easy"))
story.append(body(
    "Three-pointer iterative reversal: prev, curr, next. "
    "At each step, redirect curr->next to prev, then advance all three. "
    "The most fundamental linked list operation."
))
story.append(NodeDiagram(
    ["1","2","3","4","5"],
    highlights={0:(TEAL,(TEAL,"head"))},
    label="Before reversal: 1→2→3→4→5→NULL",
    color=TEAL
))
story.append(sp(0.2))
story.append(NodeDiagram(
    ["5","4","3","2","1"],
    highlights={0:(RED,(RED,"new head"))},
    label="After reversal:  5→4→3→2→1→NULL",
    color=RED
))
story.append(sp(0.3))
story.append(CppBlock([
    "// LC 206 — Reverse Linked List",
    "ListNode* reverseList(ListNode* head) {",
    "    ListNode* prev = nullptr;",
    "    ListNode* curr = head;",
    "    while (curr) {",
    "        ListNode* nextTmp = curr->next;  // save next",
    "        curr->next = prev;               // reverse link",
    "        prev = curr;                     // advance prev",
    "        curr = nextTmp;                  // advance curr",
    "    }",
    "    return prev;   // prev is new head",
    "}",
    "// Time: O(n)   Space: O(1)",
    "",
    "// Recursive version",
    "ListNode* reverseListRec(ListNode* head) {",
    "    if (!head || !head->next) return head;  // base case",
    "    ListNode* newHead = reverseListRec(head->next);",
    "    head->next->next = head;   // reverse the link",
    "    head->next = nullptr;      // disconnect original link",
    "    return newHead;",
    "}",
    "// Recursive: Time O(n)   Space O(n) stack frames",
]))
story.append(sp(0.8))

story.append(h2("7.2  Reverse Between L and R  (LC 92)  — Medium"))
story.append(body(
    "Reverse only the sublist from position left to right (1-indexed). "
    "Use a dummy node; find the node just before left, then reverse the segment."
))
story.append(CppBlock([
    "ListNode* reverseBetween(ListNode* head, int left, int right) {",
    "    ListNode dummy(0, head);",
    "    ListNode* pre = &dummy;",
    "    // Step 1: advance pre to node just BEFORE left",
    "    for (int i = 1; i < left; i++) pre = pre->next;",
    "    ListNode* curr = pre->next;   // first node to reverse",
    "    // Step 2: reverse (right - left) times",
    "    for (int i = 0; i < right - left; i++) {",
    "        ListNode* nxt = curr->next;",
    "        curr->next = nxt->next;        // remove nxt from its position",
    "        nxt->next  = pre->next;        // insert nxt at front of sublist",
    "        pre->next  = nxt;",
    "    }",
    "    return dummy.next;",
    "}",
    "// Time: O(n)   Space: O(1)  — single pass, in-place",
]))
story.append(sp(0.8))

story.append(h2("7.3  Reverse Nodes in K-Groups  (LC 25)  — Hard"))
story.append(body(
    "Reverse the list in groups of k. If remaining nodes &lt; k, leave them as-is. "
    "Strategy: check if k nodes exist ahead, reverse the group, recurse on the rest."
))
story.append(CppBlock([
    "ListNode* reverseKGroup(ListNode* head, int k) {",
    "    // Check if k nodes remain",
    "    ListNode* curr = head;",
    "    for (int i = 0; i < k; i++) {",
    "        if (!curr) return head;   // fewer than k nodes — don't reverse",
    "        curr = curr->next;",
    "    }",
    "    // Reverse k nodes starting from head",
    "    ListNode* prev = nullptr;",
    "    ListNode* node = head;",
    "    for (int i = 0; i < k; i++) {",
    "        ListNode* nxt = node->next;",
    "        node->next = prev;",
    "        prev = node;",
    "        node = nxt;",
    "    }",
    "    // head is now the tail of reversed segment",
    "    // Recurse on remaining list and connect",
    "    head->next = reverseKGroup(node, k);",
    "    return prev;   // prev is new head of this segment",
    "}",
    "// Time: O(n)   Space: O(n/k) recursive calls",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 8 — MERGE & SORT
# ══════════════════════════════════════════════════════════════
story.append(Banner("8","Merge & Sort Patterns",GREEN,TEAL))
story.append(sp(1))

story.append(h2("8.1  Merge Two Sorted Lists  (LC 21)  — Easy"))
story.append(body(
    "Classic two-pointer merge. Use a dummy head node to simplify logic. "
    "Compare heads of both lists, attach the smaller, advance that pointer. "
    "Attach remaining nodes at the end."
))
story.append(CppBlock([
    "ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {",
    "    ListNode dummy(0);",
    "    ListNode* curr = &dummy;",
    "    while (l1 && l2) {",
    "        if (l1->val <= l2->val) {",
    "            curr->next = l1;",
    "            l1 = l1->next;",
    "        } else {",
    "            curr->next = l2;",
    "            l2 = l2->next;",
    "        }",
    "        curr = curr->next;",
    "    }",
    "    curr->next = l1 ? l1 : l2;   // attach remaining",
    "    return dummy.next;",
    "}",
    "// Time: O(m+n)   Space: O(1)  — iterative, no extra memory",
    "",
    "// Recursive version",
    "ListNode* mergeTwoListsRec(ListNode* l1, ListNode* l2) {",
    "    if (!l1) return l2;",
    "    if (!l2) return l1;",
    "    if (l1->val <= l2->val) { l1->next = mergeTwoListsRec(l1->next, l2); return l1; }",
    "    else                    { l2->next = mergeTwoListsRec(l1, l2->next); return l2; }",
    "}",
    "// Recursive: Space O(m+n) stack",
]))
story.append(sp(0.8))

story.append(h2("8.2  Merge K Sorted Lists  (LC 23)  — Hard"))
story.append(body(
    "Three approaches: (1) Brute force: collect all, sort, rebuild — O(Nk log Nk). "
    "(2) Sequential merge: merge lists one by one — O(Nk²). "
    "(3) <b>Min-heap (priority queue):</b> always extract the smallest head — O(Nk log k). "
    "Heap approach is optimal."
))
story.append(CppBlock([
    "#include <queue>",
    "",
    "ListNode* mergeKLists(vector<ListNode*>& lists) {",
    "    // Min-heap: compare by node value",
    "    auto cmp = [](ListNode* a, ListNode* b){ return a->val > b->val; };",
    "    priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);",
    "",
    "    // Push head of each list into heap",
    "    for (ListNode* l : lists)",
    "        if (l) pq.push(l);",
    "",
    "    ListNode dummy(0);",
    "    ListNode* curr = &dummy;",
    "    while (!pq.empty()) {",
    "        ListNode* node = pq.top(); pq.pop();",
    "        curr->next = node;",
    "        curr = curr->next;",
    "        if (node->next) pq.push(node->next);  // push next of extracted",
    "    }",
    "    return dummy.next;",
    "}",
    "// Time: O(Nk * log k)  where Nk = total nodes, k = number of lists",
    "// Space: O(k) for the heap",
]))
story.append(sp(0.8))

story.append(h2("8.3  Sort a Linked List  (LC 148)  — Medium"))
story.append(body(
    "Best sort for linked lists is <b>Merge Sort</b>: O(n log n) time, O(log n) space (stack). "
    "No random access issues. Split at middle, sort each half, merge. "
    "Quick sort on LL is tricky (no easy random pivot). Heap sort requires O(n) extra space."
))
story.append(CppBlock([
    "ListNode* sortList(ListNode* head) {",
    "    if (!head || !head->next) return head;  // 0 or 1 node",
    "",
    "    // Step 1: find middle (split point)",
    "    ListNode* slow = head, *fast = head->next;",
    "    while (fast && fast->next) {",
    "        slow = slow->next;",
    "        fast = fast->next->next;",
    "    }",
    "    ListNode* mid = slow->next;",
    "    slow->next = nullptr;      // cut the list in half",
    "",
    "    // Step 2: recursively sort both halves",
    "    ListNode* left  = sortList(head);",
    "    ListNode* right = sortList(mid);",
    "",
    "    // Step 3: merge sorted halves",
    "    return mergeTwoLists(left, right);",
    "}",
    "// Time: O(n log n)   Space: O(log n) recursive stack",
    "// Note: fast starts at head->next to get LEFT middle for even-length lists",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 9 — HASHMAP PATTERNS
# ══════════════════════════════════════════════════════════════
story.append(Banner("9","Linked List + HashMap Patterns",PURPLE,TEAL))
story.append(sp(1))

story.append(h2("9.1  Copy List with Random Pointer  (LC 138)  — Medium"))
story.append(body(
    "Each node has a 'random' pointer pointing to any node (or null). "
    "Deep copy the entire list. Approach: HashMap maps original nodes to their copies. "
    "First pass: create all copies. Second pass: wire next and random pointers."
))
story.append(CppBlock([
    "class Node { public: int val; Node* next; Node* random;",
    "    Node(int v) : val(v), next(nullptr), random(nullptr) {} };",
    "",
    "Node* copyRandomList(Node* head) {",
    "    if (!head) return nullptr;",
    "    unordered_map<Node*, Node*> oldToNew;",
    "",
    "    // Pass 1: create all new nodes",
    "    Node* curr = head;",
    "    while (curr) {",
    "        oldToNew[curr] = new Node(curr->val);",
    "        curr = curr->next;",
    "    }",
    "    // Pass 2: wire next and random pointers",
    "    curr = head;",
    "    while (curr) {",
    "        oldToNew[curr]->next   = oldToNew[curr->next];",
    "        oldToNew[curr]->random = oldToNew[curr->random];",
    "        curr = curr->next;",
    "    }",
    "    return oldToNew[head];",
    "}",
    "// Time: O(n)   Space: O(n) for the hashmap",
    "",
    "// O(1) space trick: interleave original and copy nodes",
    "// 1->1'->2->2'->3->3'->NULL, then separate the two lists",
]))
story.append(sp(0.8))

story.append(h2("9.2  LRU Cache  (LC 146)  — Medium"))
story.append(body(
    "Least Recently Used Cache: get/put both O(1). "
    "<b>Data structure:</b> Doubly Linked List + HashMap. "
    "DLL maintains access order (most recent at front, LRU at back). "
    "HashMap gives O(1) lookup to any node. "
    "On access/update: move node to front. On eviction: remove from back."
))
story.append(CppBlock([
    "class LRUCache {",
    "    struct DLinkedNode {",
    "        int key, val;",
    "        DLinkedNode* prev;",
    "        DLinkedNode* next;",
    "        DLinkedNode(int k=0, int v=0): key(k), val(v), prev(nullptr), next(nullptr){}",
    "    };",
    "    int capacity;",
    "    unordered_map<int, DLinkedNode*> cache;   // key → node",
    "    DLinkedNode* head;   // dummy head (most recent side)",
    "    DLinkedNode* tail;   // dummy tail (LRU side)",
    "",
    "    void addToFront(DLinkedNode* node) {",
    "        node->next = head->next;",
    "        node->prev = head;",
    "        head->next->prev = node;",
    "        head->next = node;",
    "    }",
    "    void removeNode(DLinkedNode* node) {",
    "        node->prev->next = node->next;",
    "        node->next->prev = node->prev;",
    "    }",
    "    DLinkedNode* removeLRU() {   // remove from tail side",
    "        DLinkedNode* lru = tail->prev;",
    "        removeNode(lru); return lru;",
    "    }",
    "public:",
    "    LRUCache(int cap) : capacity(cap) {",
    "        head = new DLinkedNode(); tail = new DLinkedNode();",
    "        head->next = tail; tail->prev = head;",
    "    }",
    "    int get(int key) {",
    "        if (!cache.count(key)) return -1;",
    "        DLinkedNode* node = cache[key];",
    "        removeNode(node); addToFront(node);  // move to front",
    "        return node->val;",
    "    }",
    "    void put(int key, int value) {",
    "        if (cache.count(key)) {",
    "            cache[key]->val = value;",
    "            removeNode(cache[key]); addToFront(cache[key]);",
    "        } else {",
    "            if ((int)cache.size() == capacity) {",
    "                DLinkedNode* lru = removeLRU();",
    "                cache.erase(lru->key); delete lru;",
    "            }",
    "            DLinkedNode* node = new DLinkedNode(key, value);",
    "            cache[key] = node; addToFront(node);",
    "        }",
    "    }",
    "};",
    "// get: O(1)   put: O(1)   Space: O(capacity)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 10 — PALINDROME, REORDER & OTHER
# ══════════════════════════════════════════════════════════════
story.append(Banner("10","Palindrome, Reorder & Other Patterns",GOLD,TEAL))
story.append(sp(1))

story.append(h2("10.1  Palindrome Linked List  (LC 234)  — Easy"))
story.append(body(
    "Check if a list is a palindrome in O(n) time and O(1) space. "
    "Strategy: find middle, reverse second half, compare with first half, restore."
))
story.append(CppBlock([
    "bool isPalindrome(ListNode* head) {",
    "    // Step 1: find middle",
    "    ListNode* slow = head, *fast = head;",
    "    while (fast && fast->next) {",
    "        slow = slow->next;",
    "        fast = fast->next->next;",
    "    }",
    "    // Step 2: reverse second half",
    "    ListNode* prev = nullptr, *curr = slow;",
    "    while (curr) {",
    "        ListNode* nxt = curr->next;",
    "        curr->next = prev;",
    "        prev = curr; curr = nxt;",
    "    }",
    "    // Step 3: compare first and reversed second half",
    "    ListNode* left = head, *right = prev;",
    "    bool result = true;",
    "    while (right) {   // second half may be shorter (odd length)",
    "        if (left->val != right->val) { result = false; break; }",
    "        left = left->next; right = right->next;",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n)   Space: O(1)  — best possible",
]))
story.append(sp(0.8))

story.append(h2("10.2  Reorder List  (LC 143)  — Medium"))
story.append(body(
    "Reorder: L0→L1→…→Ln to L0→Ln→L1→Ln-1→… in-place. "
    "Three steps: (1) find middle, (2) reverse second half, (3) interleave."
))
story.append(CppBlock([
    "void reorderList(ListNode* head) {",
    "    if (!head || !head->next) return;",
    "",
    "    // Step 1: find middle",
    "    ListNode* slow = head, *fast = head;",
    "    while (fast->next && fast->next->next) {",
    "        slow = slow->next; fast = fast->next->next;",
    "    }",
    "    // Step 2: reverse second half",
    "    ListNode* prev = nullptr, *curr = slow->next;",
    "    slow->next = nullptr;          // disconnect first half",
    "    while (curr) {",
    "        ListNode* nxt = curr->next; curr->next = prev;",
    "        prev = curr; curr = nxt;",
    "    }",
    "    // Step 3: interleave first half and reversed second half",
    "    ListNode* first = head, *second = prev;",
    "    while (second) {",
    "        ListNode* tmp1 = first->next, *tmp2 = second->next;",
    "        first->next  = second;",
    "        second->next = tmp1;",
    "        first = tmp1; second = tmp2;",
    "    }",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("10.3  Odd Even Linked List  (LC 328)  — Medium"))
story.append(body(
    "Group all odd-indexed nodes together followed by even-indexed nodes. "
    "Use two pointers: odd and even. Link odd->odd->odd and even->even->even, then connect."
))
story.append(CppBlock([
    "ListNode* oddEvenList(ListNode* head) {",
    "    if (!head) return head;",
    "    ListNode* odd  = head;",
    "    ListNode* even = head->next;",
    "    ListNode* evenHead = even;   // save even head to connect later",
    "    while (even && even->next) {",
    "        odd->next  = even->next;  // odd skips even",
    "        odd        = odd->next;",
    "        even->next = odd->next;   // even skips odd",
    "        even       = even->next;",
    "    }",
    "    odd->next = evenHead;         // connect odd tail to even head",
    "    return head;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("10.4  Add Two Numbers  (LC 2)  — Medium"))
story.append(body(
    "Numbers stored in reverse order as linked lists. Add digit by digit with carry."
))
story.append(CppBlock([
    "ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {",
    "    ListNode dummy(0);",
    "    ListNode* curr = &dummy;",
    "    int carry = 0;",
    "    while (l1 || l2 || carry) {",
    "        int sum = carry;",
    "        if (l1) { sum += l1->val; l1 = l1->next; }",
    "        if (l2) { sum += l2->val; l2 = l2->next; }",
    "        carry = sum / 10;",
    "        curr->next = new ListNode(sum % 10);",
    "        curr = curr->next;",
    "    }",
    "    return dummy.next;",
    "}",
    "// Time: O(max(m,n))   Space: O(max(m,n)) for result list",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 11 — CHEAT SHEET
# ══════════════════════════════════════════════════════════════
story.append(Banner("11","Complexity Cheat Sheet & LeetCode Map",NAVY,TEAL))
story.append(sp(1))

story.append(h2("11.1  Complete Complexity Table"))
cx_data = [
    ["Operation",              "SLL",    "DLL",    "Circular","Notes"],
    ["Access by index",        "O(n)",   "O(n)",   "O(n)",    "Must traverse from head"],
    ["Insert at head",         "O(1)",   "O(1)",   "O(1)",    "Just update head pointer"],
    ["Insert at tail",         "O(n)*",  "O(1)",   "O(1)",    "*O(1) with tail pointer"],
    ["Insert at position i",   "O(n)",   "O(n)",   "O(n)",    "Traverse to i-1, then O(1)"],
    ["Insert given node ptr",  "O(1)**", "O(1)",   "O(1)",    "**SLL needs predecessor"],
    ["Delete at head",         "O(1)",   "O(1)",   "O(1)",    "Move head forward"],
    ["Delete at tail",         "O(n)",   "O(1)",   "O(1)",    "DLL: tail->prev is new tail"],
    ["Delete given node ptr",  "O(n)",   "O(1)",   "O(n)",    "SLL needs predecessor O(n)"],
    ["Search",                 "O(n)",   "O(n)",   "O(n)",    "Linear scan always"],
    ["Reverse",                "O(n)",   "O(n)",   "O(n)",    "Update all pointers"],
    ["Find middle",            "O(n)",   "O(n)",   "O(n)",    "Fast/slow pointer trick"],
    ["Detect cycle",           "O(n)",   "O(n)",   "—",       "Floyd's O(n) O(1) space"],
    ["Space per node",         "O(1)+1ptr","O(1)+2ptr","O(1)+1ptr","Pointer overhead"],
]
cx_extra=[]
for i in range(1, len(cx_data)):
    for j in range(1,4):
        v = cx_data[i][j]
        col = GREEN if v=="O(1)" else (HexColor("#1E7A4F") if "O(1)*" in v or "*" in v else (ORANGE if v=="O(n)" else DARK))
        cx_extra += [("TEXTCOLOR",(j,i),(j,i),col),("FONTNAME",(j,i),(j,i),"Helvetica-Bold")]
story.append(mtbl(cx_data,[40*mm,20*mm,20*mm,22*mm,66*mm],extra=cx_extra))
story.append(cap("Table 2: Complete linked list operation complexity"))
story.append(sp(0.5))

story.append(h2("11.2  Key Tricks & Patterns Quick Reference"))
story.append(CppBlock([
    "/*",
    " * TRICK                         USAGE                             COMPLEXITY",
    " * ─────────────────────────────────────────────────────────────────────────",
    " * Dummy head node               Simplify insert/delete at head   O(1) setup",
    " * Fast/slow pointers            Find middle, detect cycle         O(n) O(1)",
    " * Floyd's Phase 2 reset         Find cycle entry point            O(n) O(1)",
    " * Reverse + compare             Palindrome check                  O(n) O(1)",
    " * Reverse half + interleave     Reorder list                      O(n) O(1)",
    " * Three-pointer reversal        Reverse full/partial list         O(n) O(1)",
    " * DLL + HashMap                 LRU Cache O(1) get/put            O(1) ops",
    " * HashMap old→new               Deep copy with random pointers    O(n)",
    " * Merge sort on LL              Sort linked list                  O(n log n)",
    " * Min-heap                      Merge K sorted lists              O(Nk log k)",
    " * Two redirects                 Intersection of two lists         O(m+n) O(1)",
    " * XOR both                      XOR linked list prev+next         O(1) space",
    " * Advance gap of n+1            Remove nth from end               O(n) O(1)",
    " * Tail pointer                  O(1) insert at tail               O(1)",
    " * Skip even/odd in-place        Odd-even list grouping            O(n) O(1)",
    " */",
]))
story.append(sp(0.5))

story.append(h2("11.3  Complete LeetCode Problem Map"))
lc_data = [
    ["#",   "Problem",                               "Pattern",                    "Diff"],
    ["2",   "Add Two Numbers",                        "Digit-by-digit + carry",     "Medium"],
    ["19",  "Remove Nth Node From End",               "Fast/slow gap of n+1",       "Medium"],
    ["21",  "Merge Two Sorted Lists",                 "Two-pointer merge",          "Easy"],
    ["23",  "Merge K Sorted Lists",                   "Min-heap / D&C merge",       "Hard"],
    ["24",  "Swap Nodes in Pairs",                    "Iterative pointer juggle",   "Medium"],
    ["25",  "Reverse Nodes in K-Group",               "Reverse + recurse",          "Hard"],
    ["61",  "Rotate List",                            "Find new tail, reconnect",   "Medium"],
    ["82",  "Remove Duplicates II",                   "Dummy + skip duplicates",    "Medium"],
    ["83",  "Remove Duplicates",                      "In-place dedup scan",        "Easy"],
    ["92",  "Reverse Linked List II",                 "Reverse sublist",            "Medium"],
    ["138", "Copy List with Random Pointer",          "HashMap old→new nodes",      "Medium"],
    ["141", "Linked List Cycle",                      "Floyd's detect",             "Easy"],
    ["142", "Linked List Cycle II",                   "Floyd's Phase 1+2",          "Medium"],
    ["143", "Reorder List",                           "Middle+Reverse+Interleave",  "Medium"],
    ["146", "LRU Cache",                              "DLL + HashMap",              "Medium"],
    ["148", "Sort List",                              "Merge Sort on LL",           "Medium"],
    ["160", "Intersection of Two Linked Lists",       "Two-redirect trick",         "Easy"],
    ["203", "Remove Linked List Elements",            "Dummy + scan",               "Easy"],
    ["206", "Reverse Linked List",                    "Three-pointer iterative",    "Easy"],
    ["234", "Palindrome Linked List",                 "Middle+Reverse+Compare",     "Easy"],
    ["237", "Delete Node in a Linked List",           "Copy-next trick",            "Medium"],
    ["328", "Odd Even Linked List",                   "Separate odd/even chains",   "Medium"],
    ["430", "Flatten Multilevel Doubly LL",           "DFS/stack flattening",       "Medium"],
    ["432", "All O(1) Data Structure",                "DLL + two HashMaps",         "Hard"],
    ["876", "Middle of the Linked List",              "Fast/slow pointers",         "Easy"],
]
dc = {"Easy":GREEN,"Medium":ORANGE,"Hard":RED}
le = []
for i,r in enumerate(lc_data[1:],1):
    col=dc.get(r[3],DARK)
    le+=[("TEXTCOLOR",(3,i),(3,i),col),("FONTNAME",(3,i),(3,i),"Helvetica-Bold")]
story.append(mtbl(lc_data,[13*mm,68*mm,52*mm,15*mm],extra=le))
story.append(cap("Table 3: Complete LeetCode map — 25 problems across all linked list patterns"))
story.append(sp(0.8))

story.append(InfoBox([
    "1.  Always use a DUMMY head node — it eliminates special cases for deleting/inserting at head.",
    "2.  Fast/slow pointer: fast moves 2x slow. When fast=NULL, slow=middle. Master this pattern.",
    "3.  Floyd's Cycle: Phase 1 detects. Phase 2 (reset slow to head, step both by 1) finds entry.",
    "4.  Reverse: prev=NULL, curr=head, save next, flip link, advance. Three lines — memorize them.",
    "5.  Never lose a pointer: always save 'next' before overwriting curr->next.",
    "6.  DLL: O(1) delete of a known node. SLL: need predecessor → O(n). Use DLL when delete is frequent.",
    "7.  LRU = DLL + HashMap. DLL gives order, map gives O(1) access. Together: O(1) get and put.",
    "8.  Merge Sort is the best sort for linked lists: O(n log n) time, O(log n) space, no random access.",
    "9.  Two-redirect intersection: when a reaches end, send to headB; when b reaches end, send to headA.",
    "10. For deep copy with random pointers: HashMap maps old→new; two passes: create then wire.",
],title="🏆 Golden Rules — Linked List",color=NAVY,bg=LIGHT))

# ── BUILD ──────────────────────────────────────────────────────
out = "DSA_Notes_LinkedList.pdf"
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=34*mm, bottomMargin=18*mm,
    title="DSA Notes — Linked List (All Types & Operations)",
    author="DSA Revision Planner",
    subject="Complete Linked List Notes with C++",
)
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"Done! → {out}")