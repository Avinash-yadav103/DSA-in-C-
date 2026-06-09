"""
DSA Notes — Greedy Algorithms (Complete)
Run:  python Greedy_Algorithms_Notes.py
Output: DSA_Notes_Greedy_Algorithms.pdf  (same folder)
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor, white
import math

# ── Palette ────────────────────────────────────────────────────
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

# ── Chrome ─────────────────────────────────────────────────────
def _chrome(c, doc):
    c.saveState()
    c.setFillColor(NAVY);  c.rect(0, H-26*mm, W, 26*mm, fill=1, stroke=0)
    c.setFillColor(GREEN); c.rect(0, H-28*mm, W, 2*mm,  fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, H-16*mm, "DSA Notes — Greedy Algorithms (Complete)")
    c.setFont("Helvetica", 9)
    c.drawRightString(W-15*mm, H-16*mm, "Topic 12 of 13")
    c.setFillColor(NAVY);  c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(GREEN); c.rect(0, 12*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica", 8)
    c.drawString(15*mm, 4*mm, "DSA Revision Planner  •  C++ Code Edition")
    c.drawRightString(W-15*mm, 4*mm, f"Page {doc.page}")
    c.restoreState()

first_page  = lambda c, doc: _chrome(c, doc)
later_pages = lambda c, doc: _chrome(c, doc)

# ── Flowables ──────────────────────────────────────────────────
class Banner(Flowable):
    def __init__(self, num, title, color=NAVY, accent=GREEN, height=14*mm):
        super().__init__()
        self.num=num; self.title=title; self.color=color
        self.accent=accent; self.bh=height; self.width=W-30*mm
    def wrap(self, *a): return self.width, self.bh+4*mm
    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 2*mm, self.width, self.bh, 3*mm, fill=1, stroke=0)
        c.setFillColor(self.accent)
        c.roundRect(0, 2*mm, 10*mm, self.bh, 3*mm, fill=1, stroke=0)
        c.rect(7*mm, 2*mm, 3*mm, self.bh, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
        c.drawString(13*mm, 2*mm+self.bh/2-2*mm, self.num)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(28*mm, 2*mm+self.bh/2-2.5*mm, self.title)


class InfoBox(Flowable):
    def __init__(self, lines, title="", color=GREEN, bg=GREEN_BG, width=None):
        super().__init__()
        self.lines = lines if isinstance(lines, list) else [lines]
        self.title = title; self.color = color; self.bg = bg
        self._w = width or (W-30*mm); self.pad = 4*mm; self.lh = 5.2*mm
    def wrap(self, *a):
        th = 5.5*mm if self.title else 0
        return self._w, self.pad+th+len(self.lines)*self.lh+self.pad
    def draw(self):
        c = self.canv
        th = 5.5*mm if self.title else 0
        total = self.pad+th+len(self.lines)*self.lh+self.pad
        c.setFillColor(self.bg); c.roundRect(0,0,self._w,total,2*mm,fill=1,stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0,0,3.5*mm,total,1.5*mm,fill=1,stroke=0)
        c.rect(2*mm,0,1.5*mm,total,fill=1,stroke=0)
        y = total-self.pad
        if self.title:
            c.setFillColor(self.color); c.setFont("Helvetica-Bold",9.5)
            c.drawString(7*mm,y-4.5*mm,self.title); y -= 5.5*mm
        c.setFillColor(DARK); c.setFont("Helvetica",8.8)
        for ln in self.lines:
            c.drawString(7*mm,y-4*mm,ln); y -= self.lh


class GreedyViz(Flowable):
    """
    Generic greedy step visualiser — shows items/intervals as bars.
    items: list of (label, start, end, color)
    y_labels: list of row labels (one per row of items laid out)
    mode: 'interval' | 'bar'
    """
    def __init__(self, items, title="", x_max=20, color=GREEN,
                 width=None, height=38*mm, show_x=True):
        super().__init__()
        self.items   = items    # (label, start, end, fill_color)
        self.title   = title
        self.x_max   = x_max
        self.color   = color
        self._w      = width or (W-30*mm)
        self._h      = height
        self.show_x  = show_x
        self.bar_h   = 7*mm
        self.pad_x   = 18*mm   # left margin for row labels

    def wrap(self, *a):
        rows = max((it[3] for it in self.items), default=1) if self.items and len(self.items[0])>3 else 1
        base = rows * self.bar_h + (5*mm if self.title else 0) + (6*mm if self.show_x else 0) + 4*mm
        return self._w, max(base, self._h)

    def draw(self):
        c = self.canv
        bar_w = self._w - self.pad_x - 4*mm
        scale = bar_w / self.x_max

        # Title
        y_off = 0
        if self.title:
            c.setFillColor(DARK); c.setFont("Helvetica-Bold", 9)
            c.drawString(0, self._h - 6*mm + y_off, self.title)

        # Axis
        if self.show_x:
            ax_y = 4*mm
            c.setStrokeColor(BORDER); c.setLineWidth(0.5)
            c.line(self.pad_x, ax_y, self.pad_x+bar_w, ax_y)
            # tick marks
            step = max(1, self.x_max//10)
            c.setFillColor(MUTED); c.setFont("Helvetica",6.5)
            for x in range(0, self.x_max+1, step):
                px = self.pad_x + x*scale
                c.line(px, ax_y, px, ax_y+1.5*mm)
                lbl=str(x); lw=c.stringWidth(lbl,"Helvetica",6.5)
                c.drawString(px-lw/2, ax_y+2*mm, lbl)

        # Items (each has row index as 4th element for interval charts)
        row_heights = {}
        for item in self.items:
            if len(item) >= 5:
                lbl, s, e, fill, row = item
            else:
                lbl, s, e, fill = item; row = 0
            row_heights.setdefault(row, 0)

        total_rows = max((item[4] if len(item)>=5 else 0 for item in self.items), default=0)+1
        row_h = self.bar_h

        for item in self.items:
            if len(item) >= 5:
                lbl, s, e, fill, row = item
            else:
                lbl, s, e, fill = item; row = 0
            px1 = self.pad_x + s*scale
            px2 = self.pad_x + e*scale
            base_y = (6*mm if self.show_x else 2*mm) + (total_rows-1-row)*row_h
            bh = row_h - 1.5*mm
            c.setFillColor(fill); c.setStrokeColor(fill); c.setLineWidth(0.8)
            c.roundRect(px1, base_y, max(px2-px1, 2*mm), bh, 1.5*mm, fill=1, stroke=1)
            # label inside bar
            c.setFillColor(white); c.setFont("Helvetica-Bold",7.5)
            lw = c.stringWidth(lbl,"Helvetica-Bold",7.5)
            bar_width = px2-px1
            if lw < bar_width - 2*mm:
                c.drawString(px1+(bar_width-lw)/2, base_y+bh/2-2*mm, lbl)

        # Row labels on left
        for item in self.items:
            if len(item) < 5: continue
            lbl, s, e, fill, row = item
            base_y = (6*mm if self.show_x else 2*mm) + (total_rows-1-row)*row_h
            # no per-row label needed — just draw row index
            c.setFillColor(MUTED); c.setFont("Helvetica",7)
            c.drawString(1*mm, base_y+row_h/2-2*mm, f"R{row}")


class ExchangeArgViz(Flowable):
    """Show two orderings side by side to illustrate exchange argument."""
    def __init__(self, left_items, right_items, left_label="Current", right_label="After swap",
                 color=GREEN, width=None, height=28*mm):
        super().__init__()
        self.left  = left_items   # list of (text, fill)
        self.right = right_items
        self.ll    = left_label
        self.rl    = right_label
        self.color = color
        self._w    = width or (W-30*mm)
        self._h    = height

    def wrap(self, *a): return self._w, self._h

    def draw(self):
        c = self.canv
        half = (self._w - 8*mm) / 2
        cell_w = half / max(len(self.left), 1)

        for side_idx, (items, lbl) in enumerate([(self.left,self.ll),(self.right,self.rl)]):
            sx = side_idx*(half+8*mm)
            # label
            c.setFillColor(DARK); c.setFont("Helvetica-Bold",9)
            c.drawString(sx, self._h-6*mm, lbl)
            # boxes
            for i,(txt,fill) in enumerate(items):
                x = sx + i*cell_w
                c.setFillColor(fill); c.setStrokeColor(fill); c.setLineWidth(1)
                c.roundRect(x+0.5*mm, 2*mm, cell_w-1*mm, 14*mm, 2*mm, fill=1, stroke=1)
                c.setFillColor(white); c.setFont("Helvetica-Bold",8)
                tw = c.stringWidth(txt,"Helvetica-Bold",8)
                c.drawString(x+cell_w/2-tw/2, 7*mm, txt)

        # arrow between
        ax = half+3*mm; ay = self._h/2-2*mm
        c.setFillColor(GOLD); c.setStrokeColor(GOLD); c.setLineWidth(1.5)
        c.line(ax-2*mm, ay, ax+2*mm, ay)
        p=c.beginPath(); p.moveTo(ax+2*mm,ay)
        p.lineTo(ax,ay+1.5*mm); p.lineTo(ax,ay-1.5*mm); p.close()
        c.drawPath(p,fill=1,stroke=0)


class CppBlock(Flowable):
    KW = {
        'int','long','bool','char','void','string','vector','map','unordered_map',
        'set','unordered_set','pair','deque','stack','queue','priority_queue',
        'auto','const','return','if','else','while','for','do','break','continue',
        'class','struct','public','private','true','false','nullptr','new','delete',
        'include','using','namespace','std','endl','static','inline','template',
        'typename','unsigned','size_t','NULL','function','iota','numeric_limits',
        'sort','max','min','swap','reverse','push_back','pop_back','emplace_back',
        'begin','end','empty','size','insert','erase','count','clear','find',
        'front','back','top','push','pop','fill','greater','less',
        'INT_MAX','INT_MIN','LLONG_MAX','LLONG_MIN','abs','double','float',
        'long long','make_pair','lower_bound','upper_bound','accumulate','nth_element',
        'partial_sort','stable_sort','next_permutation','prev_permutation',
    }
    def __init__(self, lines, width=None):
        super().__init__()
        self.lines = lines; self._w = width or (W-30*mm)
        self.lh = 3.5*mm; self.hh = 6.0*mm; self.pad = 3.0*mm
    def wrap(self, *a):
        return self._w, self.hh+self.pad+len(self.lines)*self.lh+self.pad
    def draw(self):
        c = self.canv
        th = self.hh+self.pad+len(self.lines)*self.lh+self.pad
        c.setFillColor(CODE_BG); c.roundRect(0,0,self._w,th,3*mm,fill=1,stroke=0)
        c.setFillColor(CODE_HDR); c.roundRect(0,th-self.hh,self._w,self.hh,3*mm,fill=1,stroke=0)
        c.rect(0,th-self.hh,self._w,self.hh/2,fill=1,stroke=0)
        c.setFillColor(CPP_TYPE); c.setFont("Helvetica-Bold",7.5)
        c.drawString(4*mm,th-self.hh+2*mm,"C++")
        for i,col in enumerate([HexColor("#FF5F57"),HexColor("#FEBC2E"),HexColor("#28C840")]):
            c.setFillColor(col); c.circle(self._w-(3-i)*5.5*mm,th-self.hh/2,1.4*mm,fill=1,stroke=0)
        y = th-self.hh-self.pad-self.lh
        for idx,raw in enumerate(self.lines):
            c.setFillColor(HexColor("#3D444D")); c.setFont("Courier",7.5)
            c.drawString(3*mm,y+1.2*mm,f"{idx+1:2d}")
            stripped = raw.lstrip(); indent = len(raw)-len(stripped)
            x = 12*mm+indent*2.2*mm
            self._line(c,stripped,x,y+1.2*mm); y -= self.lh
    def _line(self,c,text,x,y):
        import re
        if '//' in text:
            ci=text.index('//')
            x=self._tok(c,text[:ci],x,y)
            c.setFillColor(CPP_CMT); c.setFont("Courier-Oblique",8.5)
            c.drawString(x,y,text[ci:]); return
        if text.startswith('#'):
            c.setFillColor(CPP_KW); c.setFont("Courier-Bold",8.5); c.drawString(x,y,text); return
        if text.strip().startswith(('/*','*')):
            c.setFillColor(CPP_CMT); c.setFont("Courier-Oblique",8.5); c.drawString(x,y,text); return
        self._tok(c,text,x,y)
    def _tok(self,c,text,x,y):
        import re
        for tok in re.findall(r'[A-Za-z_]\w*|"[^"]*"|\'[^\']*\'|\d+\.\d+|\d+|[^\w\s]|\s+',text):
            if not tok: continue
            if tok.strip()=='': x+=c.stringWidth(tok,"Courier",8.5); continue
            if tok in self.KW: c.setFillColor(CPP_KW); c.setFont("Courier-Bold",8.5)
            elif tok.startswith('"') or tok.startswith("'"): c.setFillColor(CPP_STR); c.setFont("Courier",8.5)
            elif tok.isdigit() or tok.replace('.','',1).isdigit(): c.setFillColor(CPP_NUM); c.setFont("Courier",8.5)
            else: c.setFillColor(CODE_FG); c.setFont("Courier",8.5)
            c.drawString(x,y,tok); x+=c.stringWidth(tok,"Courier",8.5)
        return x

# ── Style helpers ────────────────────────────────────────────────
def S(name,**kw):
    base=dict(fontName="Helvetica",fontSize=9.5,textColor=DARK,
              leading=14,spaceBefore=3,spaceAfter=3)
    base.update(kw); return ParagraphStyle(name,**base)

ST={
    "body":    S("body",   alignment=TA_JUSTIFY,leading=15),
    "bullet":  S("bullet", leftIndent=12,firstLineIndent=-8,leading=13,spaceBefore=2,spaceAfter=2),
    "caption": S("caption",fontName="Helvetica-Oblique",fontSize=8.5,textColor=MUTED,spaceBefore=2,spaceAfter=6),
    "toc_h":   S("toc_h", fontName="Helvetica-Bold",fontSize=11,textColor=NAVY,spaceBefore=5,spaceAfter=2,leading=15),
    "toc_i":   S("toc_i", fontSize=9.5,textColor=DARK,spaceBefore=1,spaceAfter=1,leftIndent=8,leading=13),
    "cover_t": S("ct",fontName="Helvetica-Bold",fontSize=34,textColor=white,leading=40,alignment=TA_CENTER),
    "cover_s": S("cs",fontName="Helvetica-Bold",fontSize=19,textColor=HexColor("#A8E6CF"),leading=26,alignment=TA_CENTER),
    "cover_d": S("cd",fontName="Helvetica",fontSize=11,textColor=HexColor("#CBD5E1"),leading=16,alignment=TA_CENTER),
    "h2": S("h2",fontName="Helvetica-Bold",fontSize=14,textColor=BLUE,   leading=20,spaceBefore=10,spaceAfter=4),
    "h3": S("h3",fontName="Helvetica-Bold",fontSize=11.5,textColor=GREEN,leading=16,spaceBefore=8, spaceAfter=3),
    "h4": S("h4",fontName="Helvetica-Bold",fontSize=10,textColor=NAVY,   leading=14,spaceBefore=6, spaceAfter=2),
}

def sp(n=1):  return Spacer(1,n*4*mm)
def body(t):  return Paragraph(t,ST["body"])
def cap(t):   return Paragraph(f"<i>{t}</i>",ST["caption"])
def h2(t,col=BLUE):  return Paragraph(t,ParagraphStyle("_h2",parent=ST["h2"],textColor=col))
def h3(t,col=GREEN): return Paragraph(t,ParagraphStyle("_h3",parent=ST["h3"],textColor=col))
def h4(t,col=NAVY):  return Paragraph(t,ParagraphStyle("_h4",parent=ST["h4"],textColor=col))
def bl(t,col="#1E7A4F"): return Paragraph(f'<font color="{col}">▸</font>  {t}',ST["bullet"])

def mtbl(data,cw,extra=None):
    base=[
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
    if extra: base+=extra
    t=Table(data,colWidths=cw); t.setStyle(TableStyle(base)); return t


# ══════════════════════════════════════════════════════════════
#  STORY
# ══════════════════════════════════════════════════════════════
story=[]

# ── COVER ──────────────────────────────────────────────────────
story.append(sp(4))
cd=[
    [Paragraph("DSA Revision Notes",ST["cover_t"])],
    [Paragraph("Topic 12 — Greedy Algorithms (Complete)",ST["cover_s"])],
    [Paragraph(
        "Greedy choice property · Exchange argument proofs · Activity selection<br/>"
        "Intervals · Huffman · Scheduling · Jump Game · 25+ C++ examples",
        ST["cover_d"]
    )],
]
ct=Table(cd,colWidths=[W-30*mm])
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),NAVY),
    ("TOPPADDING",(0,0),(-1,0),22),("BOTTOMPADDING",(0,0),(-1,0),8),
    ("TOPPADDING",(0,1),(-1,1),8),("BOTTOMPADDING",(0,1),(-1,1),10),
    ("TOPPADDING",(0,2),(-1,2),8),("BOTTOMPADDING",(0,2),(-1,2),22),
    ("ROUNDEDCORNERS",[4*mm]),
]))
story.append(ct); story.append(sp(2))
stats=[[
    Paragraph('<b><font color="#1A3C5E">12</font></b><br/><font size="8" color="#64748B">Sections</font>',
              ParagraphStyle("s1",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">25+</font></b><br/><font size="8" color="#64748B">C++ Examples</font>',
              ParagraphStyle("s2",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">10</font></b><br/><font size="8" color="#64748B">Diagrams</font>',
              ParagraphStyle("s3",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">28+</font></b><br/><font size="8" color="#64748B">LeetCode Problems</font>',
              ParagraphStyle("s4",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
]]
st=Table(stats,colWidths=[(W-30*mm)/4]*4)
st.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),LIGHT),("BOX",(0,0),(-1,-1),0.5,BORDER),
    ("INNERGRID",(0,0),(-1,-1),0.5,BORDER),
    ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
]))
story.append(st); story.append(PageBreak())

# ── TOC ────────────────────────────────────────────────────────
story.append(Banner("TOC","Table of Contents",NAVY,GREEN))
story.append(sp(1))
toc=[
    ("1.", "Greedy Algorithms — Core Theory"),
    ("",   "→ Greedy choice property · Optimal substructure · When greedy fails"),
    ("",   "→ Exchange argument proof technique · Greedy vs DP"),
    ("2.", "Interval Scheduling & Merging"),
    ("",   "→ Activity Selection (earliest finish) · Merge Intervals"),
    ("",   "→ Insert Interval · Non-overlapping Intervals · Meeting Rooms"),
    ("3.", "Interval Covering & Partitioning"),
    ("",   "→ Minimum arrows to burst balloons · Jump Game I & II"),
    ("",   "→ Video Stitching · Minimum number of taps"),
    ("4.", "Sorting-Based Greedy"),
    ("",   "→ Two City Scheduling · Assign Cookies · Queue Reconstruction by Height"),
    ("",   "→ Largest Number · Minimum Cost to Hire K Workers"),
    ("5.", "Scheduling Problems"),
    ("",   "→ Job Scheduling with Deadlines · Task Scheduler"),
    ("",   "→ Minimum Platforms · Course Schedule III"),
    ("6.", "String Greedy"),
    ("",   "→ Remove K Digits · Largest Rectangle via monotonic stack"),
    ("",   "→ Reorganize String · Remove Duplicate Letters"),
    ("7.", "Array & Sequence Greedy"),
    ("",   "→ Gas Station · Candy · Trapping Rain Water (greedy)"),
    ("",   "→ Boats to Save People · Wiggle Subsequence"),
    ("8.", "Greedy on Graphs — MST"),
    ("",   "→ Kruskal's & Prim's correctness via cut property"),
    ("",   "→ Minimum Spanning Tree problems"),
    ("9.", "Huffman Coding"),
    ("",   "→ Optimal prefix-free encoding · Priority queue construction"),
    ("",   "→ Correctness proof via exchange argument"),
    ("10.","Fractional Knapsack"),
    ("",   "→ Value-per-weight greedy · Why 0/1 knapsack needs DP"),
    ("11.","Advanced Greedy Patterns"),
    ("",   "→ IPO (Two Heaps) · Minimum Number of Refueling Stops"),
    ("",   "→ Partition Labels · Hand of Straights"),
    ("12.","Complexity Cheat Sheet & LeetCode Map"),
]
for num,title in toc:
    if num:
        story.append(Paragraph(f'<b><font color="#1A3C5E">{num}</font></b>  <b>{title}</b>',ST["toc_h"]))
    else:
        story.append(Paragraph(f'<font color="#64748B">        {title}</font>',ST["toc_i"]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 1 — CORE THEORY
# ══════════════════════════════════════════════════════════════
story.append(Banner("1","Greedy Algorithms — Core Theory",NAVY,GREEN))
story.append(sp(1))

story.append(h2("1.1  What is a Greedy Algorithm?"))
story.append(body(
    "A <b>greedy algorithm</b> makes the <b>locally optimal choice</b> at each step, "
    "hoping this leads to a globally optimal solution. Unlike DP, it never reconsiders past choices. "
    "Greedy works when the problem has two properties: "
    "(1) <b>Greedy Choice Property</b> — a globally optimal solution can be reached by making locally optimal choices. "
    "(2) <b>Optimal Substructure</b> — the optimal solution to the problem contains optimal solutions to subproblems."
))
story.append(sp(0.5))
story.append(InfoBox([
    "GREEDY SIGNALS in a problem statement:",
    "  • 'Minimum number of...'  or  'Maximum number of...'",
    "  • 'Earliest / latest / shortest / largest first'",
    "  • Intervals: sort by start/end time, then make decisions left to right",
    "  • 'At each step pick the best available option'",
    "",
    "GREEDY FAILS when: a local optimum blocks a better global path.",
    "  Example: coin change with arbitrary denominations [1,3,4], target=6",
    "  Greedy picks 4+1+1=3 coins, but optimal is 3+3=2 coins.",
    "  → Use DP instead.",
],title="⚡ When to Use Greedy",color=GREEN,bg=GREEN_BG))
story.append(sp(0.8))

story.append(h2("1.2  Exchange Argument — Proving Greedy Correctness"))
story.append(body(
    "The <b>exchange argument</b> is the standard technique to prove a greedy algorithm is optimal: "
    "assume an optimal solution OPT that differs from greedy solution G at some step. "
    "Show that swapping OPT's choice at that step with G's choice does not worsen the solution. "
    "Repeat until OPT and G agree on all choices — G is therefore optimal."
))
story.append(sp(0.5))
story.append(ExchangeArgViz(
    left_items =[("a₁",GREEN),("a₂",GREEN),("b",ORANGE),("a₃",GREEN)],
    right_items=[("a₁",GREEN),("a₂",GREEN),("a₃",GREEN),("b",ORANGE)],
    left_label ="OPT: b placed before a₃",
    right_label="After swap: a₃ before b",
    color=GREEN
))
story.append(cap("Exchange argument: swap b and a₃. If result is no worse, greedy choice (a₃ first) is safe."))
story.append(sp(0.8))

story.append(h2("1.3  Greedy vs Dynamic Programming"))
story.append(body(
    "Both require optimal substructure. The key difference: greedy makes one choice and recurses, "
    "DP evaluates all choices and picks the best. Use greedy when a single local rule is provably optimal."
))
gvd=[
    ["Problem",                    "Greedy?","Reason"],
    ["Activity Selection",          "Yes",   "Earliest-finish always leaves max future slots"],
    ["Fractional Knapsack",         "Yes",   "Take best ratio; fractions allowed"],
    ["0/1 Knapsack",                "No",    "Taking one item can block a better combination"],
    ["Shortest Path (pos weights)", "Yes",   "Dijkstra's greedy extraction is provably optimal"],
    ["Coin Change (arbitrary)",     "No",    "Local best denomination may fail globally"],
    ["Coin Change (canonical)",     "Yes",   "US coins: works by mathematical property"],
    ["Huffman Coding",              "Yes",   "Proven optimal by exchange argument"],
    ["LCS / Edit Distance",         "No",    "No greedy choice exists; explore all alignments"],
    ["Jump Game I (reachable?)",    "Yes",   "Track max reach greedily in one pass"],
    ["Jump Game II (min jumps)",    "Yes",   "BFS-level greedy gives optimal jumps"],
    ["Minimum Spanning Tree",       "Yes",   "Cut property guarantees greedy edge selection"],
]
ge=[]
for i in range(1,len(gvd)):
    col=GREEN if gvd[i][1]=="Yes" else RED
    ge+=[("TEXTCOLOR",(1,i),(1,i),col),("FONTNAME",(1,i),(1,i),"Helvetica-Bold")]
story.append(mtbl(gvd,[56*mm,18*mm,84*mm],extra=ge))
story.append(cap("Table 1: Greedy vs DP decision guide"))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 2 — INTERVAL SCHEDULING & MERGING
# ══════════════════════════════════════════════════════════════
story.append(Banner("2","Interval Scheduling & Merging",TEAL,GREEN))
story.append(sp(1))

story.append(h2("2.1  Activity Selection — Earliest Finish Time"))
story.append(body(
    "Select maximum number of non-overlapping activities. "
    "<b>Greedy choice:</b> always pick the activity with the <b>earliest finish time</b> "
    "that starts after the last selected activity ends. "
    "<b>Proof:</b> by exchange argument — replacing any activity with the earliest-finish one "
    "cannot reduce the count (it finishes earlier, leaving at least as much room for future activities)."
))
story.append(sp(0.3))
# interval diagram
story.append(GreedyViz([
    ("A [1,4]",  1,  4,  GREEN,  0),
    ("B [3,5]",  3,  5,  ORANGE, 1),
    ("C [0,6]",  0,  6,  RED,    2),
    ("D [5,7]",  5,  7,  GREEN,  3),
    ("E [3,8]",  3,  8,  ORANGE, 4),
    ("F [5,9]",  5,  9,  ORANGE, 5),
    ("G [6,10]", 6,  10, RED,    6),
    ("H [8,11]", 8,  11, GREEN,  7),
],title="Activity Selection: green=selected (A,D,H), orange/red=rejected", x_max=12,
   color=GREEN,height=75*mm))
story.append(sp(0.3))
story.append(CppBlock([
    "// Activity Selection — Maximum non-overlapping activities",
    "int activitySelection(vector<pair<int,int>>& intervals) {",
    "    // Sort by FINISH time (earliest finish first)",
    "    sort(intervals.begin(), intervals.end(),",
    "         [](auto& a, auto& b){ return a.second < b.second; });",
    "    int count = 1, lastEnd = intervals[0].second;",
    "    for (int i=1; i<(int)intervals.size(); i++) {",
    "        if (intervals[i].first >= lastEnd) {  // starts after last ends",
    "            count++;",
    "            lastEnd = intervals[i].second;",
    "        }",
    "    }",
    "    return count;",
    "}",
    "// Time: O(n log n) sort + O(n) scan   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("2.2  Merge Intervals  (LC 56)  — Medium"))
story.append(body(
    "Merge all overlapping intervals. Sort by start time. "
    "For each interval, if it overlaps with the last merged interval (start <= lastEnd), extend. "
    "Otherwise start a new group."
))
story.append(CppBlock([
    "// LC 56 — Merge Intervals",
    "vector<vector<int>> merge(vector<vector<int>>& intervals) {",
    "    sort(intervals.begin(), intervals.end());  // sort by start",
    "    vector<vector<int>> merged;",
    "    for (auto& iv : intervals) {",
    "        if (merged.empty() || iv[0] > merged.back()[1]) {",
    "            merged.push_back(iv);              // no overlap: new interval",
    "        } else {",
    "            merged.back()[1] = max(merged.back()[1], iv[1]); // overlap: extend",
    "        }",
    "    }",
    "    return merged;",
    "}",
    "// Time: O(n log n)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("2.3  Insert Interval  (LC 57)  — Medium"))
story.append(body(
    "Insert a new interval into a sorted non-overlapping list. Three phases: "
    "(1) add all intervals that end before new interval starts, "
    "(2) merge all overlapping ones with new interval, "
    "(3) add the rest."
))
story.append(CppBlock([
    "// LC 57 — Insert Interval",
    "vector<vector<int>> insert(vector<vector<int>>& intervals,",
    "                            vector<int>& newInterval) {",
    "    vector<vector<int>> result;",
    "    int i=0, n=intervals.size();",
    "    // Phase 1: add all intervals ending before new interval starts",
    "    while (i<n && intervals[i][1] < newInterval[0])",
    "        result.push_back(intervals[i++]);",
    "    // Phase 2: merge overlapping intervals",
    "    while (i<n && intervals[i][0] <= newInterval[1]) {",
    "        newInterval[0] = min(newInterval[0], intervals[i][0]);",
    "        newInterval[1] = max(newInterval[1], intervals[i][1]);",
    "        i++;",
    "    }",
    "    result.push_back(newInterval);",
    "    // Phase 3: add remaining intervals",
    "    while (i<n) result.push_back(intervals[i++]);",
    "    return result;",
    "}",
    "// Time: O(n)   Space: O(n)  — no sorting needed (already sorted)",
]))
story.append(sp(0.8))

story.append(h2("2.4  Non-overlapping Intervals  (LC 435)  — Medium"))
story.append(body(
    "Find minimum number of intervals to remove to make all non-overlapping. "
    "<b>Greedy:</b> sort by end time, keep intervals that don't overlap (Activity Selection). "
    "Answer = total intervals − maximum kept."
))
story.append(CppBlock([
    "// LC 435 — Non-overlapping Intervals",
    "int eraseOverlapIntervals(vector<vector<int>>& intervals) {",
    "    sort(intervals.begin(), intervals.end(),",
    "         [](auto& a, auto& b){ return a[1] < b[1]; }); // sort by end",
    "    int keep=1, lastEnd=intervals[0][1];",
    "    for (int i=1; i<(int)intervals.size(); i++) {",
    "        if (intervals[i][0] >= lastEnd) {  // no overlap",
    "            keep++;",
    "            lastEnd = intervals[i][1];",
    "        }",
    "    }",
    "    return intervals.size() - keep;",
    "}",
    "// Time: O(n log n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("2.5  Meeting Rooms II — Minimum Rooms  (LC 253)  — Medium"))
story.append(body(
    "Find minimum number of rooms for all meetings. "
    "<b>Greedy:</b> sort start times. Use a min-heap of end times to track rooms in use. "
    "If earliest ending room finishes before next meeting starts, reuse it; else open a new room."
))
story.append(CppBlock([
    "// LC 253 — Meeting Rooms II",
    "int minMeetingRooms(vector<vector<int>>& intervals) {",
    "    sort(intervals.begin(), intervals.end()); // sort by start time",
    "    priority_queue<int,vector<int>,greater<int>> pq; // min-heap of end times",
    "    for (auto& iv : intervals) {",
    "        if (!pq.empty() && pq.top() <= iv[0])",
    "            pq.pop();          // reuse room that ends earliest",
    "        pq.push(iv[1]);        // assign this meeting to a room",
    "    }",
    "    return pq.size();          // rooms still in use = total needed",
    "}",
    "// Time: O(n log n)   Space: O(n)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 3 — INTERVAL COVERING & JUMP GAME
# ══════════════════════════════════════════════════════════════
story.append(Banner("3","Interval Covering & Jump Game",GREEN,NAVY))
story.append(sp(1))

story.append(h2("3.1  Minimum Arrows to Burst Balloons  (LC 452)  — Medium"))
story.append(body(
    "Each balloon is a horizontal interval. An arrow shot at x bursts all balloons covering x. "
    "<b>Greedy:</b> sort by end position. Shoot at end of first balloon — this greedily covers "
    "as many subsequent balloons as possible. Move to next unpopped balloon when current arrow misses."
))
story.append(CppBlock([
    "// LC 452 — Minimum Number of Arrows to Burst Balloons",
    "int findMinArrowShots(vector<vector<int>>& points) {",
    "    sort(points.begin(), points.end(),",
    "         [](auto& a, auto& b){ return a[1] < b[1]; }); // sort by end",
    "    int arrows=1, pos=points[0][1];",
    "    for (int i=1; i<(int)points.size(); i++) {",
    "        if (points[i][0] > pos) {  // current arrow misses this balloon",
    "            arrows++;",
    "            pos = points[i][1];    // shoot at end of this balloon",
    "        }",
    "    }",
    "    return arrows;",
    "}",
    "// Time: O(n log n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("3.2  Jump Game I  (LC 55)  — Medium"))
story.append(body(
    "Can you reach the last index? At each position, track the maximum reachable index. "
    "<b>Greedy:</b> if current position ever exceeds maxReach, we're stuck. "
    "Otherwise, update maxReach = max(maxReach, i + nums[i])."
))
story.append(CppBlock([
    "// LC 55 — Jump Game",
    "bool canJump(vector<int>& nums) {",
    "    int maxReach = 0;",
    "    for (int i=0; i<(int)nums.size(); i++) {",
    "        if (i > maxReach) return false;  // stuck — can't reach position i",
    "        maxReach = max(maxReach, i + nums[i]);",
    "    }",
    "    return true;",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("3.3  Jump Game II  (LC 45)  — Medium"))
story.append(body(
    "Find minimum number of jumps to reach the last index. "
    "<b>BFS-level greedy:</b> treat each jump as a BFS level. Track current level's rightmost reach. "
    "When we step past the current farthest, increment jumps and extend the boundary."
))
story.append(CppBlock([
    "// LC 45 — Jump Game II (minimum jumps)",
    "int jump(vector<int>& nums) {",
    "    int jumps=0, curEnd=0, farthest=0;",
    "    for (int i=0; i<(int)nums.size()-1; i++) {",
    "        farthest = max(farthest, i + nums[i]);  // max reach from current level",
    "        if (i == curEnd) {         // reached end of current jump level",
    "            jumps++;",
    "            curEnd = farthest;     // extend to next level",
    "        }",
    "    }",
    "    return jumps;",
    "}",
    "// Time: O(n)   Space: O(1)",
    "// Analogy: BFS where each 'level' is one jump.",
    "// We don't need to know WHICH cell to jump to — just the farthest reachable.",
]))
story.append(sp(0.8))

story.append(h2("3.4  Video Stitching  (LC 1024)  — Medium"))
story.append(body(
    "Given clips [start,end], cover [0,T] with minimum clips. "
    "<b>Greedy:</b> at each step, among all clips that start ≤ current reach, "
    "pick the one with the maximum end time (extends coverage the most)."
))
story.append(CppBlock([
    "// LC 1024 — Video Stitching",
    "int videoStitching(vector<vector<int>>& clips, int time) {",
    "    // maxEnd[i] = farthest end of any clip starting at i",
    "    vector<int> maxEnd(time+1, 0);",
    "    for (auto& c:clips)",
    "        if (c[0]<=time) maxEnd[c[0]]=max(maxEnd[c[0]],c[1]);",
    "    int count=0, curEnd=0, farthest=0;",
    "    for (int i=0; i<time; i++) {",
    "        farthest=max(farthest,maxEnd[i]);",
    "        if (i==curEnd) {",
    "            if (farthest==curEnd) return -1; // no progress possible",
    "            count++;",
    "            curEnd=farthest;",
    "            if (curEnd>=time) break;",
    "        }",
    "    }",
    "    return count;",
    "}",
    "// Time: O(n + T)   Space: O(T)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 4 — SORTING-BASED GREEDY
# ══════════════════════════════════════════════════════════════
story.append(Banner("4","Sorting-Based Greedy",ORANGE,GREEN))
story.append(sp(1))

story.append(h2("4.1  Two City Scheduling  (LC 1029)  — Medium"))
story.append(body(
    "Send n people to city A and n people to city B minimising total cost. "
    "<b>Greedy:</b> compute cost difference (costA - costB) for each person. "
    "Sort by this difference. First n people (biggest preference for A) go to A; rest go to B."
))
story.append(CppBlock([
    "// LC 1029 — Two City Scheduling",
    "int twoCitySchedCost(vector<vector<int>>& costs) {",
    "    // Sort by (costA - costB): send people cheapest-to-divert-to-A first",
    "    sort(costs.begin(), costs.end(),",
    "         [](auto& a, auto& b){",
    "             return (a[0]-a[1]) < (b[0]-b[1]);",
    "         });",
    "    int n=costs.size()/2, total=0;",
    "    for (int i=0;i<n;i++) total+=costs[i][0];    // first n go to A",
    "    for (int i=n;i<2*n;i++) total+=costs[i][1];  // rest go to B",
    "    return total;",
    "}",
    "// Time: O(n log n)   Space: O(1)",
    "// Proof: imagine sending all to A first (cost = sum of costA).",
    "// Switching person i from A to B saves (costA[i] - costB[i]).",
    "// Sort by this savings and switch the n most beneficial.",
]))
story.append(sp(0.8))

story.append(h2("4.2  Queue Reconstruction by Height  (LC 406)  — Medium"))
story.append(body(
    "Each person [h, k] has height h and k people taller in front. "
    "<b>Greedy:</b> sort by height descending (taller first), then by k ascending. "
    "Insert each person at position k — since all people inserted before are taller, "
    "the k-count is automatically satisfied."
))
story.append(CppBlock([
    "// LC 406 — Queue Reconstruction by Height",
    "vector<vector<int>> reconstructQueue(vector<vector<int>>& people) {",
    "    // Sort: taller first, then by k ascending",
    "    sort(people.begin(), people.end(),",
    "         [](auto& a, auto& b){",
    "             return a[0]!=b[0] ? a[0]>b[0] : a[1]<b[1];",
    "         });",
    "    vector<vector<int>> result;",
    "    for (auto& p : people) {",
    "        // Insert at position p[1]",
    "        result.insert(result.begin()+p[1], p);",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n^2) due to insert   Space: O(n)",
    "// O(n log n) possible with BIT/Fenwick tree",
]))
story.append(sp(0.8))

story.append(h2("4.3  Largest Number  (LC 179)  — Medium"))
story.append(body(
    "Arrange numbers to form the largest number. "
    "<b>Greedy comparator:</b> for two numbers a and b, compare string ab vs ba. "
    "If ab > ba, a should come first. Sort using this comparator."
))
story.append(CppBlock([
    "// LC 179 — Largest Number",
    "string largestNumber(vector<int>& nums) {",
    "    vector<string> strs;",
    "    for (int x:nums) strs.push_back(to_string(x));",
    "    sort(strs.begin(), strs.end(),",
    "         [](const string& a, const string& b){",
    "             return a+b > b+a;  // greedy: which concatenation is larger?",
    "         });",
    "    if (strs[0]==\"0\") return \"0\"; // all zeros",
    "    string result=\"\";",
    "    for (auto& s:strs) result+=s;",
    "    return result;",
    "}",
    "// Time: O(n log n * L) where L=max digits   Space: O(n)",
    "// Correctness: comparator a+b > b+a defines a total order (transitivity holds)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 5 — SCHEDULING
# ══════════════════════════════════════════════════════════════
story.append(Banner("5","Scheduling Problems",PURPLE,GREEN))
story.append(sp(1))

story.append(h2("5.1  Task Scheduler  (LC 621)  — Medium"))
story.append(body(
    "Schedule tasks with cooldown n between same tasks. Minimise total time. "
    "<b>Greedy:</b> always schedule the most frequent remaining task. "
    "The mathematical formula: max(n_tasks, (maxFreq-1)*(n+1) + countOfMaxFreq)."
))
story.append(CppBlock([
    "// LC 621 — Task Scheduler",
    "int leastInterval(vector<char>& tasks, int n) {",
    "    vector<int> freq(26,0);",
    "    for (char c:tasks) freq[c-'A']++;",
    "    int maxFreq = *max_element(freq.begin(),freq.end());",
    "    // Count how many tasks share the maximum frequency",
    "    int maxCount = count(freq.begin(),freq.end(),maxFreq);",
    "    // Formula: arrange maxFreq-1 blocks of (n+1) + tail",
    "    int frames = (maxFreq-1)*(n+1) + maxCount;",
    "    // If we have enough tasks to fill all slots, no idle needed",
    "    return max((int)tasks.size(), frames);",
    "}",
    "// Time: O(n)   Space: O(1)",
    "// Example: tasks=[A,A,A,B,B,B], n=2",
    "// maxFreq=3, maxCount=2: frames=(3-1)*(2+1)+2=8",
    "// Layout: A B _ A B _ A B  (8 intervals)",
]))
story.append(sp(0.8))

story.append(h2("5.2  Job Scheduling with Deadlines — Maximise Profit"))
story.append(body(
    "Each job has a deadline and profit. Do each job in one unit. "
    "<b>Greedy:</b> sort by profit descending. For each job, schedule it as late as possible "
    "before its deadline (greedy: delay to leave earlier slots for other jobs)."
))
story.append(CppBlock([
    "// Job Scheduling: each job (profit, deadline), 1 unit each",
    "int jobScheduling(vector<pair<int,int>>& jobs) {",
    "    // Sort by profit descending",
    "    sort(jobs.begin(), jobs.end(),",
    "         [](auto& a, auto& b){ return a.first>b.first; });",
    "    int maxDL = 0;",
    "    for (auto& j:jobs) maxDL=max(maxDL,j.second);",
    "    vector<int> slot(maxDL+1, -1);  // slot[t] = job assigned at time t",
    "    int totalProfit = 0;",
    "    for (auto& [profit,dl]:jobs) {",
    "        // Try to schedule as late as possible before deadline",
    "        for (int t=min(dl,maxDL); t>=1; t--) {",
    "            if (slot[t]==-1) {",
    "                slot[t]=profit;",
    "                totalProfit+=profit;",
    "                break;",
    "            }",
    "        }",
    "    }",
    "    return totalProfit;",
    "}",
    "// Time: O(n^2) naive  —  O(n log n) with Union-Find for slot lookup",
]))
story.append(sp(0.8))

story.append(h2("5.3  Course Schedule III  (LC 630)  — Hard"))
story.append(body(
    "Maximise number of courses taken. Each course has duration and deadline. "
    "<b>Greedy:</b> sort by deadline. Keep a max-heap of durations taken so far. "
    "If adding a course would exceed its deadline, replace the longest taken course "
    "if it is longer than the current one (saves time without reducing count)."
))
story.append(CppBlock([
    "// LC 630 — Course Schedule III",
    "int scheduleCourse(vector<vector<int>>& courses) {",
    "    sort(courses.begin(),courses.end(),",
    "         [](auto& a,auto& b){ return a[1]<b[1]; }); // sort by deadline",
    "    priority_queue<int> pq;  // max-heap of durations taken",
    "    int time=0;",
    "    for (auto& c:courses) {",
    "        int dur=c[0], dl=c[1];",
    "        if (time+dur<=dl) {",
    "            time+=dur; pq.push(dur);  // can take this course",
    "        } else if (!pq.empty() && pq.top()>dur) {",
    "            // Replace longest course with current (shorter → saves time)",
    "            time-=pq.top(); pq.pop();",
    "            time+=dur; pq.push(dur);",
    "        }",
    "    }",
    "    return pq.size();",
    "}",
    "// Time: O(n log n)   Space: O(n)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 6 — STRING GREEDY
# ══════════════════════════════════════════════════════════════
story.append(Banner("6","String Greedy",BLUE,GREEN))
story.append(sp(1))

story.append(h2("6.1  Remove K Digits  (LC 402)  — Medium"))
story.append(body(
    "Remove k digits from a number string to get the smallest possible number. "
    "<b>Greedy:</b> using a monotonic increasing stack, whenever a digit is larger "
    "than the next digit, remove it (costs one of our k removals). "
    "This ensures the most significant digits are as small as possible."
))
story.append(CppBlock([
    "// LC 402 — Remove K Digits",
    "string removeKdigits(string num, int k) {",
    "    string st=\"\";   // use string as monotonic stack",
    "    for (char c:num) {",
    "        // Remove larger digits from top while we still have k removals left",
    "        while (k>0 && !st.empty() && st.back()>c) {",
    "            st.pop_back(); k--;",
    "        }",
    "        st+=c;",
    "    }",
    "    // If k removals remain, remove from end (largest remaining digits)",
    "    st.resize(st.size()-k);",
    "    // Remove leading zeros",
    "    int start=0;",
    "    while (start<(int)st.size()-1 && st[start]=='0') start++;",
    "    return st.substr(start);",
    "}",
    "// Time: O(n)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("6.2  Partition Labels  (LC 763)  — Medium"))
story.append(body(
    "Partition string so each letter appears in at most one part. Maximise number of parts. "
    "<b>Greedy:</b> for each character, track its last occurrence. "
    "Scan left to right, extending the current partition's end to max(end, lastOccurrence[c]). "
    "When we reach the end of the current partition, record it and start a new one."
))
story.append(CppBlock([
    "// LC 763 — Partition Labels",
    "vector<int> partitionLabels(string s) {",
    "    // Step 1: find last occurrence of each character",
    "    vector<int> last(26,0);",
    "    for (int i=0;i<(int)s.size();i++) last[s[i]-'a']=i;",
    "    // Step 2: greedy scan",
    "    vector<int> result;",
    "    int start=0, end=0;",
    "    for (int i=0;i<(int)s.size();i++) {",
    "        end=max(end, last[s[i]-'a']);  // extend partition to include this char's last pos",
    "        if (i==end) {                  // reached end of current partition",
    "            result.push_back(end-start+1);",
    "            start=end+1;",
    "        }",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n)   Space: O(1) — 26-char alphabet",
]))
story.append(sp(0.8))

story.append(h2("6.3  Reorganize String  (LC 767)  — Medium"))
story.append(body(
    "Rearrange so no two adjacent characters are the same. "
    "<b>Greedy:</b> always place the most frequent remaining character that differs from the previous. "
    "Use a max-heap. If max frequency > (n+1)/2, it's impossible."
))
story.append(CppBlock([
    "// LC 767 — Reorganize String",
    "string reorganizeString(string s) {",
    "    vector<int> freq(26,0);",
    "    for (char c:s) freq[c-'a']++;",
    "    // Max-heap of {frequency, character}",
    "    priority_queue<pair<int,char>> pq;",
    "    for (int i=0;i<26;i++) if(freq[i]) pq.push({freq[i],'a'+i});",
    "    string result=\"\";",
    "    while (pq.size()>=2) {",
    "        auto [f1,c1]=pq.top(); pq.pop();",
    "        auto [f2,c2]=pq.top(); pq.pop();",
    "        result+=c1; result+=c2;",
    "        if(f1-1>0) pq.push({f1-1,c1});",
    "        if(f2-1>0) pq.push({f2-1,c2});",
    "    }",
    "    if (!pq.empty()) {",
    "        if(pq.top().first>1) return \"\"; // impossible",
    "        result+=pq.top().second;",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n log k) k=distinct chars   Space: O(k)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 7 — ARRAY GREEDY
# ══════════════════════════════════════════════════════════════
story.append(Banner("7","Array & Sequence Greedy",GOLD,GREEN))
story.append(sp(1))

story.append(h2("7.1  Gas Station  (LC 134)  — Medium"))
story.append(body(
    "Find starting gas station to complete a circular route. "
    "<b>Key insight:</b> if total gas >= total cost, a solution always exists. "
    "<b>Greedy:</b> track running tank. When it goes negative, the start must be after current position."
))
story.append(CppBlock([
    "// LC 134 — Gas Station",
    "int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {",
    "    int total=0, tank=0, start=0;",
    "    for (int i=0;i<(int)gas.size();i++) {",
    "        int diff = gas[i]-cost[i];",
    "        total+=diff;",
    "        tank +=diff;",
    "        if (tank<0) {      // can't start before or at i",
    "            start=i+1;     // try starting from next station",
    "            tank=0;        // reset tank",
    "        }",
    "    }",
    "    return total>=0 ? start : -1;",
    "}",
    "// Time: O(n)   Space: O(1)",
    "// Why is 'start' the answer? If total>=0, there must be a valid start.",
    "// The last segment that made tank negative disqualifies all earlier starts.",
]))
story.append(sp(0.8))

story.append(h2("7.2  Candy  (LC 135)  — Hard"))
story.append(body(
    "Give children candy: (1) each child gets ≥1 candy; (2) child with higher rating than neighbour gets more. "
    "<b>Greedy — two passes:</b> left-to-right satisfies left neighbours; right-to-left satisfies right neighbours. "
    "Take max of both passes for each child."
))
story.append(CppBlock([
    "// LC 135 — Candy",
    "int candy(vector<int>& ratings) {",
    "    int n=ratings.size();",
    "    vector<int> candies(n,1);",
    "    // Pass 1: left to right — if ratings[i] > ratings[i-1], give more than left",
    "    for (int i=1;i<n;i++)",
    "        if (ratings[i]>ratings[i-1]) candies[i]=candies[i-1]+1;",
    "    // Pass 2: right to left — if ratings[i] > ratings[i+1], ensure more than right",
    "    for (int i=n-2;i>=0;i--)",
    "        if (ratings[i]>ratings[i+1])",
    "            candies[i]=max(candies[i], candies[i+1]+1);",
    "    return accumulate(candies.begin(),candies.end(),0);",
    "}",
    "// Time: O(n)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("7.3  Boats to Save People  (LC 881)  — Medium"))
story.append(body(
    "Each boat holds at most 2 people with weight limit. Minimise boats. "
    "<b>Greedy:</b> sort people by weight. Use two pointers — pair heaviest with lightest if possible. "
    "If they fit together, both board; otherwise heaviest boards alone."
))
story.append(CppBlock([
    "// LC 881 — Boats to Save People",
    "int numRescueBoats(vector<int>& people, int limit) {",
    "    sort(people.begin(), people.end());",
    "    int lo=0, hi=people.size()-1, boats=0;",
    "    while (lo<=hi) {",
    "        if (people[lo]+people[hi]<=limit) lo++; // lightest pairs with heaviest",
    "        hi--;      // heaviest always boards (paired or alone)",
    "        boats++;",
    "    }",
    "    return boats;",
    "}",
    "// Time: O(n log n)   Space: O(1)",
]))
story.append(sp(0.8))

story.append(h2("7.4  Wiggle Subsequence  (LC 376)  — Medium"))
story.append(body(
    "Find longest wiggle subsequence (alternating up/down). "
    "<b>Greedy:</b> count direction changes. A peak or valley always contributes."
))
story.append(CppBlock([
    "// LC 376 — Wiggle Subsequence",
    "int wiggleMaxLength(vector<int>& nums) {",
    "    if (nums.size()<2) return nums.size();",
    "    int up=1, down=1;",
    "    for (int i=1;i<(int)nums.size();i++) {",
    "        if (nums[i]>nums[i-1]) up=down+1;    // rising: extend down sequence",
    "        else if (nums[i]<nums[i-1]) down=up+1; // falling: extend up sequence",
    "    }",
    "    return max(up,down);",
    "}",
    "// Time: O(n)   Space: O(1)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 8 — MST (GREEDY GRAPHS)
# ══════════════════════════════════════════════════════════════
story.append(Banner("8","Greedy on Graphs — Minimum Spanning Tree",NAVY,GREEN))
story.append(sp(1))

story.append(h2("8.1  Cut Property — Why MST Greedy is Correct"))
story.append(body(
    "A <b>cut</b> partitions the vertices into two disjoint sets (S, V-S). "
    "The <b>cut property</b>: for any cut, the minimum-weight edge crossing the cut "
    "belongs to SOME minimum spanning tree. "
    "Both Kruskal's and Prim's exploit this: they always add the cheapest edge that "
    "connects the current MST fragment to an unvisited vertex."
))
story.append(sp(0.5))
story.append(InfoBox([
    "Cut Property: if e is the min-weight edge crossing any cut (S, V-S), then e ∈ some MST.",
    "Cycle Property: if e is the max-weight edge in any cycle, then e ∉ any MST.",
    "Kruskal: sort edges by weight → add if it doesn't create a cycle (Union-Find) → O(E log E)",
    "Prim:    start from any vertex → always add cheapest edge to unvisited vertex → O((V+E) log V)",
    "Both are greedy and correct by the cut property.",
    "Key difference: Kruskal = edge-focused (global sort). Prim = vertex-focused (grow tree).",
],title="📐 MST Greedy Correctness",color=NAVY,bg=LIGHT))
story.append(sp(0.5))
story.append(CppBlock([
    "// Kruskal's MST — O(E log E) using Union-Find",
    "int kruskalMST(int n, vector<tuple<int,int,int>>& edges) {",
    "    sort(edges.begin(),edges.end()); // sort by weight",
    "    vector<int> par(n); iota(par.begin(),par.end(),0);",
    "    vector<int> rnk(n,0);",
    "    function<int(int)> find=[&](int x)->int{",
    "        return par[x]==x?x:par[x]=find(par[x]);};",
    "    auto unite=[&](int x,int y)->bool{",
    "        x=find(x);y=find(y);if(x==y)return false;",
    "        if(rnk[x]<rnk[y])swap(x,y);",
    "        par[y]=x;if(rnk[x]==rnk[y])rnk[x]++;return true;};",
    "    int mstCost=0, edges_used=0;",
    "    for (auto&[w,u,v]:edges){",
    "        if(unite(u,v)){mstCost+=w;edges_used++;",
    "            if(edges_used==n-1)break;}",
    "    }",
    "    return edges_used==n-1?mstCost:-1;",
    "}",
    "// Time: O(E log E)   Space: O(V)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 9 — HUFFMAN CODING
# ══════════════════════════════════════════════════════════════
story.append(Banner("9","Huffman Coding — Optimal Prefix-Free Encoding",TEAL,GREEN))
story.append(sp(1))

story.append(h2("9.1  Problem & Greedy Strategy"))
story.append(body(
    "Huffman coding assigns shorter bit codes to more frequent characters. "
    "The result is an optimal prefix-free (no code is prefix of another) binary code. "
    "<b>Greedy strategy:</b> always merge the two least-frequent symbols into a combined node. "
    "This bottom-up tree construction is provably optimal by exchange argument."
))
story.append(sp(0.5))
story.append(InfoBox([
    "Algorithm: use a min-heap of (frequency, node).",
    "1. Insert all characters with their frequencies.",
    "2. While heap has more than 1 node:",
    "   a. Extract two minimum-frequency nodes L and R.",
    "   b. Create parent node with frequency = freq(L) + freq(R).",
    "   c. Insert parent back into heap.",
    "3. The remaining node is the root of the Huffman tree.",
    "4. Assign 0 for left branches, 1 for right. Path from root = code for each character.",
    "Optimality proof: exchange argument shows merging two least-freq nodes first is always safe.",
],title="📐 Huffman Algorithm",color=TEAL,bg=TEAL_BG))
story.append(sp(0.5))
story.append(CppBlock([
    "// Huffman Coding — minimum total encoding cost",
    "struct HNode {",
    "    int freq;",
    "    char ch;",
    "    HNode *left, *right;",
    "    HNode(int f,char c='#'):freq(f),ch(c),left(nullptr),right(nullptr){}",
    "};",
    "struct Cmp { bool operator()(HNode* a,HNode* b){return a->freq>b->freq;} };",
    "",
    "long long huffmanCost(vector<pair<char,int>>& charFreq) {",
    "    priority_queue<HNode*,vector<HNode*>,Cmp> pq;",
    "    for (auto&[c,f]:charFreq) pq.push(new HNode(f,c));",
    "    long long totalCost=0;",
    "    while (pq.size()>1) {",
    "        HNode* L=pq.top(); pq.pop();",
    "        HNode* R=pq.top(); pq.pop();",
    "        int combined=L->freq+R->freq;",
    "        totalCost+=combined;          // each merge costs combined frequency",
    "        HNode* parent=new HNode(combined);",
    "        parent->left=L; parent->right=R;",
    "        pq.push(parent);",
    "    }",
    "    return totalCost;",
    "}",
    "// Time: O(n log n)   Space: O(n)",
    "// totalCost = sum of all internal node frequencies = weighted path length",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 10 — FRACTIONAL KNAPSACK
# ══════════════════════════════════════════════════════════════
story.append(Banner("10","Fractional Knapsack",GOLD,GREEN))
story.append(sp(1))

story.append(h2("10.1  Fractional Knapsack — Value/Weight Greedy"))
story.append(body(
    "Items can be broken into fractions. Fill capacity with the highest value-per-weight items first. "
    "<b>Greedy:</b> sort by value/weight ratio descending. Take as much of each item as possible. "
    "This is optimal because fractional inclusion means we never 'waste' capacity. "
    "<b>Why greedy fails for 0/1 knapsack:</b> without fractions, taking a high-ratio small item "
    "can block a better combination of larger items."
))
story.append(CppBlock([
    "// Fractional Knapsack",
    "double fractionalKnapsack(vector<int>& wt, vector<int>& val, int W) {",
    "    int n=wt.size();",
    "    vector<int> idx(n); iota(idx.begin(),idx.end(),0);",
    "    // Sort by value/weight ratio descending",
    "    sort(idx.begin(),idx.end(),[&](int a,int b){",
    "        return (double)val[a]/wt[a] > (double)val[b]/wt[b];",
    "    });",
    "    double totalVal=0.0;",
    "    int capacity=W;",
    "    for (int i:idx) {",
    "        if (wt[i]<=capacity) {",
    "            totalVal+=val[i];      // take entire item",
    "            capacity-=wt[i];",
    "        } else {",
    "            totalVal+=val[i]*(double)capacity/wt[i]; // take fraction",
    "            break;                // capacity exhausted",
    "        }",
    "    }",
    "    return totalVal;",
    "}",
    "// Time: O(n log n)   Space: O(n)",
    "",
    "// Compare with 0/1 knapsack counterexample:",
    "// Items: {wt=10,val=60},{wt=20,val=100},{wt=30,val=120}, W=50",
    "// Greedy ratios: 6, 5, 4 → take item1(60)+item2(100)+10/30*item3(40)=200",
    "// But 0/1 optimal: item2+item3=220 → greedy gives WRONG answer for 0/1",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 11 — ADVANCED GREEDY
# ══════════════════════════════════════════════════════════════
story.append(Banner("11","Advanced Greedy Patterns",RED,GREEN))
story.append(sp(1))

story.append(h2("11.1  IPO — Maximise Capital  (LC 502)  — Hard"))
story.append(body(
    "Pick at most k projects (one at a time) to maximise capital. "
    "<b>Two-heap greedy:</b> min-heap by capital (locked projects), max-heap by profit (available). "
    "At each step: unlock all affordable projects, then pick the most profitable one."
))
story.append(CppBlock([
    "// LC 502 — IPO (Two Heap Greedy)",
    "int findMaximizedCapital(int k, int w,",
    "                          vector<int>& profits, vector<int>& capital) {",
    "    int n=profits.size();",
    "    // Min-heap by required capital",
    "    priority_queue<pair<int,int>,vector<pair<int,int>>,",
    "                   greater<>> locked;",
    "    // Max-heap by profit (available projects)",
    "    priority_queue<int> available;",
    "    for (int i=0;i<n;i++) locked.push({capital[i],profits[i]});",
    "    for (int i=0;i<k;i++) {",
    "        // Unlock all projects we can afford",
    "        while (!locked.empty() && locked.top().first<=w) {",
    "            available.push(locked.top().second);",
    "            locked.pop();",
    "        }",
    "        if (available.empty()) break; // no affordable project",
    "        w+=available.top(); available.pop(); // take most profitable",
    "    }",
    "    return w;",
    "}",
    "// Time: O(n log n + k log n)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("11.2  Minimum Number of Refueling Stops  (LC 871)  — Hard"))
story.append(body(
    "Drive from 0 to target. Refuel at stations. Find minimum stops. "
    "<b>Greedy:</b> when we run out of fuel, retroactively refuel at the largest-capacity station we passed. "
    "Use a max-heap of passed station fuels."
))
story.append(CppBlock([
    "// LC 871 — Minimum Number of Refueling Stops",
    "int minRefuelStops(int target, int startFuel,",
    "                    vector<vector<int>>& stations) {",
    "    priority_queue<int> pq;  // max-heap of passed station fuels",
    "    int fuel=startFuel, stops=0, prev=0;",
    "    stations.push_back({target,0}); // add target as final station",
    "    for (auto& s:stations) {",
    "        fuel-=(s[0]-prev);           // fuel consumed to reach this station",
    "        prev=s[0];",
    "        while (fuel<0 && !pq.empty()) { // out of fuel — retroactively refuel",
    "            fuel+=pq.top(); pq.pop(); stops++;",
    "        }",
    "        if (fuel<0) return -1;       // can't reach even with all stops",
    "        pq.push(s[1]);               // add this station's fuel to candidates",
    "    }",
    "    return stops;",
    "}",
    "// Time: O(n log n)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("11.3  Hand of Straights  (LC 846)  — Medium"))
story.append(body(
    "Divide hand into groups of consecutive cards of size groupSize. "
    "<b>Greedy:</b> always start a new group with the smallest available card. "
    "Use a sorted map to track counts."
))
story.append(CppBlock([
    "// LC 846 — Hand of Straights",
    "bool isNStraightHand(vector<int>& hand, int groupSize) {",
    "    if (hand.size()%groupSize!=0) return false;",
    "    map<int,int> cnt;",
    "    for (int x:hand) cnt[x]++;",
    "    for (auto&[start,c]:cnt) {",
    "        if (c==0) continue;",
    "        // Try to form 'c' groups starting at 'start'",
    "        for (int i=0;i<groupSize;i++) {",
    "            if (cnt[start+i]<c) return false;",
    "            cnt[start+i]-=c;",
    "        }",
    "    }",
    "    return true;",
    "}",
    "// Time: O(n log n)   Space: O(n)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 12 — CHEAT SHEET
# ══════════════════════════════════════════════════════════════
story.append(Banner("12","Complexity Cheat Sheet & LeetCode Map",NAVY,GREEN))
story.append(sp(1))

story.append(h2("12.1  Greedy Algorithm Complexity Summary"))
cx_data=[
    ["Problem / Pattern",                 "Sort By",             "Data Struct","Time",      "Key Greedy Choice"],
    ["Activity Selection",                 "End time",            "—",          "O(n log n)","Pick earliest-finish non-overlapping"],
    ["Merge Intervals",                    "Start time",          "—",          "O(n log n)","Extend or start new interval"],
    ["Non-overlapping (min remove)",       "End time",            "—",          "O(n log n)","Keep maximum compatible set"],
    ["Meeting Rooms II (min rooms)",       "Start time",          "Min-heap",   "O(n log n)","Reuse earliest-ending room"],
    ["Burst Balloons (min arrows)",        "End position",        "—",          "O(n log n)","Shoot at end of each group"],
    ["Jump Game II (min jumps)",           "—",                   "—",          "O(n)",      "Extend reach level by level"],
    ["Task Scheduler",                     "Frequency",           "Max-heap",   "O(n)",      "Math formula or simulation"],
    ["Job with Deadline (max profit)",     "Profit desc",         "Slots arr",  "O(n^2)",    "Schedule latest before deadline"],
    ["Course Schedule III",                "Deadline",            "Max-heap",   "O(n log n)","Replace longest if shorter fits"],
    ["Gas Station",                        "—",                   "—",          "O(n)",      "Reset start when tank < 0"],
    ["Candy (two-pass)",                   "—",                   "—",          "O(n)",      "L-to-R then R-to-L passes"],
    ["Two City Scheduling",                "costA-costB",         "—",          "O(n log n)","Send n cheapest-to-divert to A"],
    ["Queue Reconstruction",               "Height desc",         "—",          "O(n^2)",    "Insert at position k"],
    ["Largest Number",                     "Custom: a+b>b+a",     "—",          "O(n log n)","Transitive comparator"],
    ["Huffman Coding",                     "Frequency",           "Min-heap",   "O(n log n)","Merge two least frequent"],
    ["Fractional Knapsack",                "Value/weight ratio",  "—",          "O(n log n)","Take highest ratio first"],
    ["IPO (max capital)",                  "Capital",             "Two heaps",  "O(n log n)","Unlock affordable, pick max profit"],
    ["Min Refueling Stops",                "Position",            "Max-heap",   "O(n log n)","Retroactively use largest passed"],
    ["Partition Labels",                   "—",                   "—",          "O(n)",      "Extend cut to last occurrence"],
]
story.append(mtbl(cx_data,[45*mm,28*mm,18*mm,24*mm,43*mm]))
story.append(cap("Table 2: Greedy algorithm patterns with sorting keys and data structures"))
story.append(sp(0.5))

story.append(h2("12.2  Pattern Recognition Guide"))
story.append(CppBlock([
    "/*",
    " * PROBLEM SIGNAL                              → GREEDY PATTERN",
    " * ─────────────────────────────────────────────────────────────────────",
    " * Max non-overlapping intervals               → Sort by END time, scan",
    " * Min intervals to remove                     → Sort by END, count kept",
    " * Merge overlapping intervals                 → Sort by START, extend",
    " * Min rooms / machines needed                 → Sort START, min-heap of END times",
    " * Cover [0,T] with minimum segments           → Jump Game II style (level BFS)",
    " * Min arrows to burst balloons                → Sort by END, shoot at END",
    " * Min jumps to reach end                      → Track farthest reach, count levels",
    " * Max profit from projects with capital req   → Two heaps (locked/available)",
    " * Optimal binary encoding                     → Huffman (min-heap, merge two least)",
    " * Can you complete a circular route?          → Gas Station: track net gain",
    " * Remove digits to minimise number            → Monotonic increasing stack",
    " * Arrange numbers to form max value           → Custom comparator a+b > b+a",
    " * Schedule tasks with cooldown                → Frequency formula or simulation",
    " * Divide items into groups of consecutive     → Sort + map, greedily form groups",
    " * Distribute resources with min cost          → Sort, take greedily with two pointers",
    " * Must prove greedy: use EXCHANGE ARGUMENT    → Swap adjacent choices, show no worse",
    " */",
]))
story.append(sp(0.5))

story.append(h2("12.3  LeetCode Problem Map"))
lc_data=[
    ["#",   "Problem",                               "Pattern",                     "Diff"],
    ["45",  "Jump Game II",                           "BFS-level greedy",            "Medium"],
    ["55",  "Jump Game",                              "Max reach tracking",          "Medium"],
    ["56",  "Merge Intervals",                        "Sort by start, extend",       "Medium"],
    ["57",  "Insert Interval",                        "Three-phase scan",            "Medium"],
    ["134", "Gas Station",                            "Net gain, reset start",       "Medium"],
    ["135", "Candy",                                  "Two-pass greedy",             "Hard"],
    ["179", "Largest Number",                         "Custom comparator sort",      "Medium"],
    ["253", "Meeting Rooms II",                       "Sort + min-heap",             "Medium"],
    ["376", "Wiggle Subsequence",                     "Count direction changes",     "Medium"],
    ["392", "Is Subsequence",                         "Two-pointer greedy",          "Easy"],
    ["402", "Remove K Digits",                        "Monotonic stack greedy",      "Medium"],
    ["406", "Queue Reconstruction by Height",         "Sort + insert at k",          "Medium"],
    ["435", "Non-overlapping Intervals",              "Sort by end, max compatible", "Medium"],
    ["452", "Minimum Arrows to Burst Balloons",       "Sort by end, shoot at end",   "Medium"],
    ["502", "IPO",                                    "Two heaps greedy",            "Hard"],
    ["621", "Task Scheduler",                         "Frequency + formula",         "Medium"],
    ["630", "Course Schedule III",                    "Sort deadline + max-heap",    "Hard"],
    ["646", "Maximum Length of Pair Chain",           "Activity selection",          "Medium"],
    ["714", "Best Time to Buy/Sell Stock with Fee",   "State machine greedy",        "Medium"],
    ["763", "Partition Labels",                       "Last occurrence scan",        "Medium"],
    ["767", "Reorganize String",                      "Max-heap frequency",          "Medium"],
    ["846", "Hand of Straights",                      "Sorted map groups",           "Medium"],
    ["860", "Lemonade Change",                        "Greedy cash tracking",        "Easy"],
    ["871", "Min Refueling Stops",                    "Retroactive max-heap",        "Hard"],
    ["881", "Boats to Save People",                   "Two-pointer greedy",          "Medium"],
    ["1029","Two City Scheduling",                    "Sort by cost diff",           "Medium"],
    ["1024","Video Stitching",                        "Jump Game II style",          "Medium"],
    ["1642","Furthest Building You Can Reach",        "Min-heap + greedy ladders",   "Medium"],
    ["2263","Make Array Beautiful",                   "Greedy scan",                 "Medium"],
]
dc={"Easy":GREEN,"Medium":ORANGE,"Hard":RED}
le=[]
for i,r in enumerate(lc_data[1:],1):
    col=dc.get(r[3],DARK)
    le+=[("TEXTCOLOR",(3,i),(3,i),col),("FONTNAME",(3,i),(3,i),"Helvetica-Bold")]
story.append(mtbl(lc_data,[13*mm,70*mm,48*mm,17*mm],extra=le))
story.append(cap("Table 3: 28 LeetCode problems — Greedy Algorithms"))
story.append(sp(0.8))

story.append(InfoBox([
    "1.  To PROVE greedy: use exchange argument — show swapping greedy choice with any other never worsens the result.",
    "2.  To DISPROVE greedy: find one counterexample where local best blocks global optimum → switch to DP.",
    "3.  Intervals: sort by END for selection/arrows/non-overlap. Sort by START for merging.",
    "4.  Jump Game: track maxReach greedily. Jump Game II: BFS-level — count jumps when i==curEnd.",
    "5.  Two-heap pattern: min-heap of locked resources + max-heap of available → O(log n) per selection.",
    "6.  Gas Station: if total gas >= total cost, solution exists. Reset start whenever tank < 0.",
    "7.  Huffman: always merge two least frequent. Optimality follows from exchange argument.",
    "8.  Fractional Knapsack: sort by value/weight descending. Take greedily. Never works for 0/1.",
    "9.  Custom comparator (Largest Number): a+b > b+a. Must verify transitivity for sort correctness.",
    "10. Meeting Rooms: min rooms = max overlapping at any point = PQ size after greedy assignment.",
],title="🏆 Golden Rules — Greedy Algorithms",color=NAVY,bg=LIGHT))

# ── BUILD ───────────────────────────────────────────────────────
out = "DSA_Notes_Greedy_Algorithms.pdf"
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=34*mm,  bottomMargin=18*mm,
    title="DSA Notes — Greedy Algorithms (Complete)",
    author="DSA Revision Planner",
    subject="Complete Greedy Algorithm Notes with C++",
)
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"\n✅  Done!  →  {out}")
print(f"   Open the PDF in the same folder where you ran this script.")