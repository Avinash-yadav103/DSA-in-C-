"""
DSA Notes — Backtracking & Trie
Run:  python Backtracking_Trie_Notes.py
Output: DSA_Notes_Backtracking_Trie.pdf  (same folder)
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
    c.setFillColor(RED);   c.rect(0, H-28*mm, W, 2*mm,  fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, H-16*mm, "DSA Notes — Backtracking & Trie")
    c.setFont("Helvetica", 9)
    c.drawRightString(W-15*mm, H-16*mm, "Topic 11 of 13")
    c.setFillColor(NAVY);  c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(RED);   c.rect(0, 12*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica", 8)
    c.drawString(15*mm, 4*mm, "DSA Revision Planner  •  C++ Code Edition")
    c.drawRightString(W-15*mm, 4*mm, f"Page {doc.page}")
    c.restoreState()

first_page  = lambda c, doc: _chrome(c, doc)
later_pages = lambda c, doc: _chrome(c, doc)

# ── Flowables ──────────────────────────────────────────────────
class Banner(Flowable):
    def __init__(self, num, title, color=NAVY, accent=RED, height=14*mm):
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
    def __init__(self, lines, title="", color=RED, bg=RED_BG, width=None):
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
        c.setFillColor(self.bg); c.roundRect(0, 0, self._w, total, 2*mm, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 0, 3.5*mm, total, 1.5*mm, fill=1, stroke=0)
        c.rect(2*mm, 0, 1.5*mm, total, fill=1, stroke=0)
        y = total-self.pad
        if self.title:
            c.setFillColor(self.color); c.setFont("Helvetica-Bold", 9.5)
            c.drawString(7*mm, y-4.5*mm, self.title); y -= 5.5*mm
        c.setFillColor(DARK); c.setFont("Helvetica", 8.8)
        for ln in self.lines:
            c.drawString(7*mm, y-4*mm, ln); y -= self.lh


class TrieDiagram(Flowable):
    """
    Draw a Trie tree.
    nodes: list of (id, label, x_frac, y_frac, is_end)
    edges: list of (parent_id, child_id, edge_label)
    """
    def __init__(self, nodes, edges, highlights=None, label="",
                 color=TEAL, width=None, height=60*mm):
        super().__init__()
        self.nodes      = nodes
        self.edges      = edges
        self.highlights = highlights or {}
        self.label      = label
        self.color      = color
        self._w         = width or (W-30*mm)
        self._h         = height
        self.r          = 6*mm

    def wrap(self, *a):
        return self._w, self._h + (5*mm if self.label else 0)

    def _pos(self, xf, yf):
        pad = self.r + 2*mm
        return (xf*(self._w-2*pad)+pad,
                yf*(self._h-2*pad-(5*mm if self.label else 0))+pad)

    def draw(self):
        c = self.canv
        r = self.r
        # edges first
        for (pid, cid, elbl) in self.edges:
            pn = next((n for n in self.nodes if n[0]==pid), None)
            cn = next((n for n in self.nodes if n[0]==cid), None)
            if not pn or not cn: continue
            x1,y1 = self._pos(pn[2], pn[3])
            x2,y2 = self._pos(cn[2], cn[3])
            dx,dy  = x2-x1, y2-y1
            dist   = math.sqrt(dx*dx+dy*dy) or 1
            ux,uy  = dx/dist, dy/dist
            c.setStrokeColor(HexColor("#475569")); c.setLineWidth(1.2)
            c.line(x1+ux*r, y1+uy*r, x2-ux*r, y2-uy*r)
            # edge label
            mx,my = (x1+x2)/2, (y1+y2)/2
            c.setFillColor(RED); c.setFont("Helvetica-Bold", 8.5)
            ew = c.stringWidth(elbl,"Helvetica-Bold",8.5)
            c.setFillColor(HexColor("#FFF1F2"))
            c.roundRect(mx-ew/2-1.5*mm, my-2.5*mm, ew+3*mm, 5.5*mm, 1*mm, fill=1, stroke=0)
            c.setFillColor(RED)
            c.drawString(mx-ew/2, my-1.5*mm, elbl)
        # nodes
        for node in self.nodes:
            nid, lbl, nx, ny, is_end = node
            x,y = self._pos(nx, ny)
            fill = self.highlights.get(nid, self.color if not is_end else GREEN)
            c.setFillColor(fill)
            c.setStrokeColor(fill); c.setLineWidth(1.5)
            c.circle(x, y, r, fill=1, stroke=1)
            if is_end:  # double circle for end nodes
                c.setFillColor(fill); c.setStrokeColor(white); c.setLineWidth(1.5)
                c.circle(x, y, r-1.5*mm, fill=0, stroke=1)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
            s = str(lbl); sw = c.stringWidth(s,"Helvetica-Bold",9)
            c.drawString(x-sw/2, y-3*mm, s)
        if self.label:
            c.setFillColor(MUTED); c.setFont("Helvetica-Oblique", 8)
            lw = c.stringWidth(self.label,"Helvetica-Oblique",8)
            c.drawString(self._w/2-lw/2, 0.5*mm, self.label)


class BacktrackTreeViz(Flowable):
    """
    Visualise a partial backtracking decision tree.
    nodes: list of (id, label, depth, pos_in_level, pruned=False)
    edges: list of (parent_id, child_id, label)
    """
    def __init__(self, nodes, edges, pruned_ids=None, answer_ids=None,
                 label="", color=RED, width=None, height=55*mm):
        super().__init__()
        self.nodes       = nodes
        self.edges       = edges
        self.pruned_ids  = pruned_ids or set()
        self.answer_ids  = answer_ids or set()
        self.label       = label
        self.color       = color
        self._w          = width or (W-30*mm)
        self._h          = height
        self.r           = 5*mm

    def wrap(self, *a):
        return self._w, self._h + (5*mm if self.label else 0)

    def draw(self):
        c = self.canv
        r = self.r
        # compute positions
        max_depth = max(n[2] for n in self.nodes) if self.nodes else 0
        max_pos   = {}
        for n in self.nodes:
            d = n[2]
            max_pos[d] = max(max_pos.get(d,0), n[3])
        pos = {}
        for n in self.nodes:
            nid, lbl, depth, pidx, *_ = n
            slots = max_pos.get(depth,0)+1
            x = (pidx+0.5)/slots * self._w
            y = self._h - (depth/(max_depth+0.5))*(self._h-2*r) - r - (5*mm if self.label else 0)
            pos[nid] = (x,y)
        # edges
        for (pid, cid, elbl) in self.edges:
            if pid not in pos or cid not in pos: continue
            x1,y1 = pos[pid]; x2,y2 = pos[cid]
            dx,dy  = x2-x1, y2-y1
            dist   = math.sqrt(dx*dx+dy*dy) or 1
            ux,uy  = dx/dist, dy/dist
            is_pruned = cid in self.pruned_ids
            c.setStrokeColor(ORANGE if is_pruned else HexColor("#475569"))
            c.setLineWidth(1.0)
            c.line(x1+ux*r, y1+uy*r, x2-ux*r, y2-uy*r)
            if elbl:
                mx,my = (x1+x2)/2,(y1+y2)/2
                c.setFillColor(MUTED); c.setFont("Helvetica",7)
                ew = c.stringWidth(elbl,"Helvetica",7)
                c.drawString(mx-ew/2, my-1.5*mm, elbl)
        # nodes
        for n in self.nodes:
            nid, lbl, depth, pidx, *_ = n
            if nid not in pos: continue
            x,y = pos[nid]
            is_pruned = nid in self.pruned_ids
            is_answer = nid in self.answer_ids
            fill = GREEN if is_answer else (ORANGE if is_pruned else self.color)
            c.setFillColor(fill); c.setStrokeColor(fill); c.setLineWidth(1.2)
            c.circle(x,y,r,fill=1,stroke=1)
            c.setFillColor(white); c.setFont("Helvetica-Bold",7.5)
            s = str(lbl); sw = c.stringWidth(s,"Helvetica-Bold",7.5)
            c.drawString(x-sw/2, y-2.5*mm, s)
        if self.label:
            c.setFillColor(MUTED); c.setFont("Helvetica-Oblique",8)
            lw = c.stringWidth(self.label,"Helvetica-Oblique",8)
            c.drawString(self._w/2-lw/2, 0.5*mm, self.label)


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
        'front','back','top','push','pop','fill','fill_n','greater','less',
        'INT_MAX','INT_MIN','abs','double','float','long long','make_pair',
        'lower_bound','upper_bound','accumulate','bitset','array',
    }
    def __init__(self, lines, width=None):
        super().__init__()
        self.lines = lines; self._w = width or (W-30*mm)
        self.lh = 4.1*mm; self.hh = 6.5*mm; self.pad = 3.5*mm
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
    "cover_s": S("cs",fontName="Helvetica-Bold",fontSize=19,textColor=HexColor("#FFC0C0"),leading=26,alignment=TA_CENTER),
    "cover_d": S("cd",fontName="Helvetica",fontSize=11,textColor=HexColor("#CBD5E1"),leading=16,alignment=TA_CENTER),
    "h2": S("h2",fontName="Helvetica-Bold",fontSize=14,textColor=BLUE,  leading=20,spaceBefore=10,spaceAfter=4),
    "h3": S("h3",fontName="Helvetica-Bold",fontSize=11.5,textColor=RED, leading=16,spaceBefore=8, spaceAfter=3),
    "h4": S("h4",fontName="Helvetica-Bold",fontSize=10,textColor=NAVY,  leading=14,spaceBefore=6, spaceAfter=2),
}

def sp(n=1):  return Spacer(1,n*4*mm)
def body(t):  return Paragraph(t,ST["body"])
def cap(t):   return Paragraph(f"<i>{t}</i>",ST["caption"])
def h2(t,col=BLUE): return Paragraph(t,ParagraphStyle("_h2",parent=ST["h2"],textColor=col))
def h3(t,col=RED):  return Paragraph(t,ParagraphStyle("_h3",parent=ST["h3"],textColor=col))
def h4(t,col=NAVY): return Paragraph(t,ParagraphStyle("_h4",parent=ST["h4"],textColor=col))
def bl(t,col="#C0392B"): return Paragraph(f'<font color="{col}">▸</font>  {t}',ST["bullet"])

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
    [Paragraph("Topic 11 — Backtracking &amp; Trie",ST["cover_s"])],
    [Paragraph(
        "Backtracking template · Pruning · Subsets · Permutations · Combinations<br/>"
        "N-Queens · Sudoku · Word Search II · Trie from scratch · 25+ C++ examples",
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
    Paragraph('<b><font color="#1A3C5E">8</font></b><br/><font size="8" color="#64748B">Tree Diagrams</font>',
              ParagraphStyle("s3",fontName="Helvetica-Bold",fontSize=18,textColor=NAVY,alignment=TA_CENTER,leading=22)),
    Paragraph('<b><font color="#1A3C5E">22+</font></b><br/><font size="8" color="#64748B">LeetCode Problems</font>',
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
story.append(Banner("TOC","Table of Contents",NAVY,RED))
story.append(sp(1))
toc=[
    ("1.", "Backtracking — Core Theory"),
    ("",   "→ Choose–Explore–Unchoose template · Decision tree"),
    ("",   "→ Pruning strategies · Time complexity analysis"),
    ("2.", "Subsets (Power Set)"),
    ("",   "→ Iterative approach · Backtracking approach"),
    ("",   "→ Subsets II (with duplicates) · Subsets of size k"),
    ("3.", "Permutations"),
    ("",   "→ Permutations I (distinct) · Permutations II (duplicates)"),
    ("",   "→ Next Permutation · Permutation Sequence"),
    ("4.", "Combinations"),
    ("",   "→ Combinations (nCk) · Combination Sum I, II, III"),
    ("",   "→ Letter combinations of phone number"),
    ("5.", "Palindrome Partitioning"),
    ("",   "→ All palindrome partitions · Min cuts (DP + BT)"),
    ("6.", "N-Queens & N-Queens II"),
    ("",   "→ Constraint modelling · Diagonal checks · Optimisations"),
    ("7.", "Sudoku Solver  (LC 37)"),
    ("",   "→ Constraint propagation · Row/col/box bitmask"),
    ("8.", "Word Search on Grid"),
    ("",   "→ Word Search I (DFS) · Word Search II (Trie + DFS)"),
    ("9.", "Trie — Core Theory & Implementation"),
    ("",   "→ Trie node structure · Insert · Search · StartsWith"),
    ("",   "→ Time/space analysis · Compressed Trie"),
    ("10.","Trie — Classic Problems"),
    ("",   "→ Implement Trie · Replace Words · Map Sum Pairs"),
    ("",   "→ Search Suggestions System · Design Add-Search Words"),
    ("11.","Trie — Advanced Applications"),
    ("",   "→ Maximum XOR of Two Numbers · XOR Trie"),
    ("",   "→ Word Search II (Trie + Backtracking combined)"),
    ("12.","Complexity Cheat Sheet & LeetCode Map"),
]
for num,title in toc:
    if num:
        story.append(Paragraph(f'<b><font color="#1A3C5E">{num}</font></b>  <b>{title}</b>',ST["toc_h"]))
    else:
        story.append(Paragraph(f'<font color="#64748B">        {title}</font>',ST["toc_i"]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 1 — BACKTRACKING CORE THEORY
# ══════════════════════════════════════════════════════════════
story.append(Banner("1","Backtracking — Core Theory",NAVY,RED))
story.append(sp(1))

story.append(h2("1.1  What is Backtracking?"))
story.append(body(
    "Backtracking is a systematic way to enumerate all possible solutions by building candidates "
    "incrementally and <b>abandoning (backtracking)</b> a candidate as soon as it is determined "
    "that it cannot lead to a valid solution. "
    "It is essentially DFS on an implicit decision tree, with pruning to skip infeasible branches early. "
    "Used for: constraint satisfaction (N-Queens, Sudoku), combinatorial generation (subsets, permutations), "
    "and path-finding problems (Word Search)."
))
story.append(sp(0.5))
story.append(InfoBox([
    "CHOOSE:   Make a choice from available options at the current decision point.",
    "EXPLORE:  Recurse deeper with that choice (move to next decision point).",
    "UNCHOOSE: Undo the choice (restore state) and try the next option.",
    "",
    "Pruning: before EXPLORE, check if the current partial solution CAN lead to a valid answer.",
    "If not → skip this branch entirely. Good pruning is the difference between fast and TLE.",
], title="🔑 Choose–Explore–Unchoose Template", color=RED, bg=RED_BG))
story.append(sp(0.5))

story.append(h2("1.2  Universal Backtracking Template"))
story.append(CppBlock([
    "// ── Universal Backtracking Template ────────────────────",
    "void backtrack(int pos, vector<int>& current,",
    "               vector<vector<int>>& result,",
    "               /* problem-specific params */ ) {",
    "    // Base case: valid complete solution",
    "    if (isComplete(pos, current)) {",
    "        result.push_back(current);",
    "        return;",
    "    }",
    "    // Iterate all choices at this decision point",
    "    for (auto choice : getChoices(pos)) {",
    "        if (!isValid(choice, current)) continue;  // PRUNE",
    "        // ── CHOOSE ──",
    "        current.push_back(choice);",
    "        markUsed(choice);",
    "        // ── EXPLORE ──",
    "        backtrack(pos + 1, current, result);",
    "        // ── UNCHOOSE ──",
    "        current.pop_back();",
    "        unmarkUsed(choice);",
    "    }",
    "}",
    "// Time: O(b^d) worst case — b=branching factor, d=depth",
    "// Good pruning makes practical time much better",
]))
story.append(sp(0.5))

story.append(h2("1.3  Decision Tree Visualisation"))
story.append(BacktrackTreeViz(
    nodes=[
        (0, "[]",   0, 2, False),
        (1, "[1]",  1, 0, False), (2, "[2]",  1, 1, False), (3, "[3]",  1, 2, False), (4, "[4]",  1, 3, False),
        (5, "[1,2]",2, 0, False), (6, "[1,3]",2, 1, False), (7, "[1,4]",2, 2, False),
        (8, "[2,3]",2, 3, False), (9, "[2,4]",2, 4, False),
        (10,"[3,4]",2, 5, False),
    ],
    edges=[
        (0,1,"1"),(0,2,"2"),(0,3,"3"),(0,4,"4"),
        (1,5,"2"),(1,6,"3"),(1,7,"4"),
        (2,8,"3"),(2,9,"4"),
        (3,10,"4"),
    ],
    answer_ids={5,6,7,8,9,10},
    pruned_ids={4},
    label="Combinations C(4,2): green=answer, orange=pruned (no more choices after 4)",
    color=RED, height=52*mm
))
story.append(cap("Decision tree for combinations of size 2 from [1,2,3,4]. Each level = one element added."))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 2 — SUBSETS
# ══════════════════════════════════════════════════════════════
story.append(Banner("2","Subsets (Power Set)",RED,NAVY))
story.append(sp(1))

story.append(h2("2.1  Subsets I — All Subsets of Distinct Elements  (LC 78)"))
story.append(body(
    "Generate all 2^n subsets of a set of distinct integers. "
    "Backtracking: at each index, either include or exclude the element. "
    "Alternative: iterate index <b>start</b> to avoid duplicates — each element appears at most once per subset."
))
story.append(CppBlock([
    "// LC 78 — Subsets",
    "vector<vector<int>> subsets(vector<int>& nums) {",
    "    vector<vector<int>> result;",
    "    vector<int> current;",
    "    function<void(int)> bt = [&](int start) {",
    "        result.push_back(current);         // every state is a valid subset",
    "        for (int i = start; i < (int)nums.size(); i++) {",
    "            current.push_back(nums[i]);    // CHOOSE",
    "            bt(i + 1);                     // EXPLORE (i+1: no reuse)",
    "            current.pop_back();            // UNCHOOSE",
    "        }",
    "    };",
    "    bt(0);",
    "    return result;",
    "}",
    "// Time: O(n * 2^n)   Space: O(n) recursion depth",
    "",
    "// Iterative bit-mask approach",
    "vector<vector<int>> subsetsBit(vector<int>& nums) {",
    "    int n = nums.size();",
    "    vector<vector<int>> result;",
    "    for (int mask = 0; mask < (1<<n); mask++) {",
    "        vector<int> sub;",
    "        for (int i = 0; i < n; i++)",
    "            if (mask & (1<<i)) sub.push_back(nums[i]);",
    "        result.push_back(sub);",
    "    }",
    "    return result;  // Time: O(n * 2^n)   Space: O(1) extra",
    "}",
]))
story.append(sp(0.8))

story.append(h2("2.2  Subsets II — With Duplicates  (LC 90)"))
story.append(body(
    "When the input has duplicates, sort first, then skip duplicates at the same recursion level. "
    "Key: skip if <code>i > start && nums[i] == nums[i-1]</code> — this means the same value "
    "was already chosen at this level, so we'd generate a duplicate subset."
))
story.append(CppBlock([
    "// LC 90 — Subsets II (with duplicates)",
    "vector<vector<int>> subsetsWithDup(vector<int>& nums) {",
    "    sort(nums.begin(), nums.end());          // MUST sort first",
    "    vector<vector<int>> result;",
    "    vector<int> current;",
    "    function<void(int)> bt = [&](int start) {",
    "        result.push_back(current);",
    "        for (int i = start; i < (int)nums.size(); i++) {",
    "            // Skip duplicate values at the SAME level",
    "            if (i > start && nums[i] == nums[i-1]) continue;",
    "            current.push_back(nums[i]);",
    "            bt(i + 1);",
    "            current.pop_back();",
    "        }",
    "    };",
    "    bt(0);",
    "    return result;",
    "}",
    "// The condition i > start (NOT i > 0) is crucial:",
    "// It only skips duplicates at the SAME recursive level",
    "// i > 0 would incorrectly skip valid elements in deeper levels",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 3 — PERMUTATIONS
# ══════════════════════════════════════════════════════════════
story.append(Banner("3","Permutations",RED,NAVY))
story.append(sp(1))

story.append(h2("3.1  Permutations I — Distinct Elements  (LC 46)"))
story.append(body(
    "Generate all n! permutations of distinct integers. "
    "Use a <b>used[]</b> boolean array to track which elements are in the current permutation. "
    "At each position, try all unused elements."
))
story.append(CppBlock([
    "// LC 46 — Permutations",
    "vector<vector<int>> permute(vector<int>& nums) {",
    "    int n = nums.size();",
    "    vector<vector<int>> result;",
    "    vector<int> current;",
    "    vector<bool> used(n, false);",
    "    function<void()> bt = [&]() {",
    "        if ((int)current.size() == n) {",
    "            result.push_back(current); return;",
    "        }",
    "        for (int i = 0; i < n; i++) {",
    "            if (used[i]) continue;",
    "            used[i] = true;            // CHOOSE",
    "            current.push_back(nums[i]);",
    "            bt();                      // EXPLORE",
    "            current.pop_back();        // UNCHOOSE",
    "            used[i] = false;",
    "        }",
    "    };",
    "    bt();",
    "    return result;",
    "}",
    "// Time: O(n * n!)   Space: O(n)",
    "",
    "// Alternative: swap-based (no used[] array)",
    "void btSwap(vector<int>& nums, int start, vector<vector<int>>& res) {",
    "    if (start == (int)nums.size()) { res.push_back(nums); return; }",
    "    for (int i = start; i < (int)nums.size(); i++) {",
    "        swap(nums[start], nums[i]);",
    "        btSwap(nums, start+1, res);",
    "        swap(nums[start], nums[i]); // UNCHOOSE: restore",
    "    }",
    "}",
]))
story.append(sp(0.8))

story.append(h2("3.2  Permutations II — With Duplicates  (LC 47)"))
story.append(body(
    "Sort first. Skip a duplicate element if its previous identical element has NOT been used "
    "(meaning it was already chosen at this level and we'd generate the same permutation). "
    "Condition: <code>!used[i-1] && nums[i] == nums[i-1]</code>."
))
story.append(CppBlock([
    "// LC 47 — Permutations II (with duplicates)",
    "vector<vector<int>> permuteUnique(vector<int>& nums) {",
    "    sort(nums.begin(), nums.end());",
    "    int n = nums.size();",
    "    vector<vector<int>> result;",
    "    vector<int> current;",
    "    vector<bool> used(n, false);",
    "    function<void()> bt = [&]() {",
    "        if ((int)current.size() == n) { result.push_back(current); return; }",
    "        for (int i = 0; i < n; i++) {",
    "            if (used[i]) continue;",
    "            // Skip: same value as previous AND previous was NOT used",
    "            // (means we already explored this choice at this level)",
    "            if (i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue;",
    "            used[i] = true; current.push_back(nums[i]);",
    "            bt();",
    "            current.pop_back(); used[i] = false;",
    "        }",
    "    };",
    "    bt();",
    "    return result;",
    "}",
    "// The !used[i-1] condition ensures we only use the first occurrence",
    "// of each duplicate value at each recursive level",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 4 — COMBINATIONS
# ══════════════════════════════════════════════════════════════
story.append(Banner("4","Combinations",ORANGE,RED))
story.append(sp(1))

story.append(h2("4.1  Combination Sum I — Unlimited Reuse  (LC 39)"))
story.append(body(
    "Find all combinations of candidates that sum to target. Each number can be used unlimited times. "
    "Pass the same index <code>i</code> (not i+1) to allow reuse. Prune if remaining target &lt; 0."
))
story.append(CppBlock([
    "// LC 39 — Combination Sum (unlimited reuse, distinct candidates)",
    "vector<vector<int>> combinationSum(vector<int>& cands, int target) {",
    "    sort(cands.begin(), cands.end());        // sort for pruning",
    "    vector<vector<int>> result;",
    "    vector<int> current;",
    "    function<void(int,int)> bt = [&](int start, int rem) {",
    "        if (rem == 0) { result.push_back(current); return; }",
    "        for (int i = start; i < (int)cands.size(); i++) {",
    "            if (cands[i] > rem) break;       // PRUNE: sorted, all larger won't work",
    "            current.push_back(cands[i]);",
    "            bt(i, rem - cands[i]);           // i (not i+1): allow reuse",
    "            current.pop_back();",
    "        }",
    "    };",
    "    bt(0, target);",
    "    return result;",
    "}",
    "// Time: O(n^(T/M)) where T=target, M=min candidate  Space: O(T/M)",
]))
story.append(sp(0.8))

story.append(h2("4.2  Combination Sum II — Each Number Used Once  (LC 40)"))
story.append(body(
    "Each number used at most once. Has duplicates. Sort + skip same value at same level. "
    "Pass i+1 (not i) to prevent reuse."
))
story.append(CppBlock([
    "// LC 40 — Combination Sum II (each used once, duplicates in input)",
    "vector<vector<int>> combinationSum2(vector<int>& cands, int target) {",
    "    sort(cands.begin(), cands.end());",
    "    vector<vector<int>> result;",
    "    vector<int> current;",
    "    function<void(int,int)> bt = [&](int start, int rem) {",
    "        if (rem == 0) { result.push_back(current); return; }",
    "        for (int i = start; i < (int)cands.size(); i++) {",
    "            if (cands[i] > rem) break;",
    "            // Skip duplicates at same level",
    "            if (i > start && cands[i] == cands[i-1]) continue;",
    "            current.push_back(cands[i]);",
    "            bt(i + 1, rem - cands[i]);       // i+1: no reuse",
    "            current.pop_back();",
    "        }",
    "    };",
    "    bt(0, target);",
    "    return result;",
    "}",
]))
story.append(sp(0.8))

story.append(h2("4.3  Letter Combinations of Phone Number  (LC 17)"))
story.append(CppBlock([
    "// LC 17 — Letter Combinations of a Phone Number",
    "vector<string> letterCombinations(string digits) {",
    "    if (digits.empty()) return {};",
    "    vector<string> phone = {\"\",\"\",\"abc\",\"def\",\"ghi\",\"jkl\",",
    "                             \"mno\",\"pqrs\",\"tuv\",\"wxyz\"};",
    "    vector<string> result;",
    "    string current = \"\";",
    "    function<void(int)> bt = [&](int pos) {",
    "        if (pos == (int)digits.size()) { result.push_back(current); return; }",
    "        for (char ch : phone[digits[pos]-'0']) {",
    "            current += ch;                   // CHOOSE",
    "            bt(pos + 1);                     // EXPLORE",
    "            current.pop_back();              // UNCHOOSE",
    "        }",
    "    };",
    "    bt(0);",
    "    return result;",
    "}",
    "// Time: O(4^n * n)  n=digits length (max 4 letters per digit)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 5 — PALINDROME PARTITIONING
# ══════════════════════════════════════════════════════════════
story.append(Banner("5","Palindrome Partitioning",PURPLE,RED))
story.append(sp(1))

story.append(h2("5.1  All Palindrome Partitions  (LC 131)  — Medium"))
story.append(body(
    "Partition string s into substrings where every substring is a palindrome. "
    "Precompute isPalin[i][j] to check palindromes in O(1) during backtracking. "
    "At each position, try all valid palindrome endings."
))
story.append(CppBlock([
    "// LC 131 — Palindrome Partitioning",
    "vector<vector<string>> partition(string s) {",
    "    int n = s.size();",
    "    // Precompute palindrome table — O(n^2)",
    "    vector<vector<bool>> isPalin(n, vector<bool>(n,false));",
    "    for (int i=n-1; i>=0; i--)",
    "        for (int j=i; j<n; j++)",
    "            isPalin[i][j]=(s[i]==s[j])&&(j-i<=2||isPalin[i+1][j-1]);",
    "    vector<vector<string>> result;",
    "    vector<string> current;",
    "    function<void(int)> bt = [&](int start) {",
    "        if (start == n) { result.push_back(current); return; }",
    "        for (int end = start; end < n; end++) {",
    "            if (isPalin[start][end]) {         // PRUNE: only palindromes",
    "                current.push_back(s.substr(start, end-start+1));",
    "                bt(end + 1);",
    "                current.pop_back();",
    "            }",
    "        }",
    "    };",
    "    bt(0);",
    "    return result;",
    "}",
    "// Time: O(n * 2^n)   Space: O(n^2) for palindrome table",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 6 — N-QUEENS
# ══════════════════════════════════════════════════════════════
story.append(Banner("6","N-Queens & N-Queens II  (LC 51, 52)",RED,NAVY))
story.append(sp(1))

story.append(h2("6.1  N-Queens — Place n queens on n×n board with no attacks"))
story.append(body(
    "Place one queen per row. Track which columns, main diagonals (row-col), "
    "and anti-diagonals (row+col) are occupied. "
    "<b>Key insight:</b> for the main diagonal, row-col is constant; for anti-diagonal, row+col is constant. "
    "Use bitmasks or sets for O(1) conflict checking."
))
story.append(CppBlock([
    "// LC 51 — N-Queens: return all valid board configurations",
    "vector<vector<string>> solveNQueens(int n) {",
    "    vector<vector<string>> result;",
    "    vector<int> queens(n, -1);      // queens[row] = col",
    "    set<int> cols, diag1, diag2;   // diag1=row-col, diag2=row+col",
    "    function<void(int)> bt = [&](int row) {",
    "        if (row == n) {",
    "            // Build board from queens[]",
    "            vector<string> board(n, string(n,'.'));",
    "            for (int r=0;r<n;r++) board[r][queens[r]]='Q';",
    "            result.push_back(board);",
    "            return;",
    "        }",
    "        for (int col = 0; col < n; col++) {",
    "            if (cols.count(col)||diag1.count(row-col)||diag2.count(row+col))",
    "                continue;                    // PRUNE: under attack",
    "            queens[row] = col;",
    "            cols.insert(col); diag1.insert(row-col); diag2.insert(row+col);",
    "            bt(row + 1);",
    "            cols.erase(col); diag1.erase(row-col); diag2.erase(row+col);",
    "        }",
    "    };",
    "    bt(0);",
    "    return result;",
    "}",
    "// Time: O(n!)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("6.2  N-Queens — Bitmask Optimisation  (LC 52)"))
story.append(body(
    "Use integer bitmasks instead of sets for O(1) bitwise column/diagonal checks. "
    "Available positions = ~(cols | diag1 | diag2) & fullMask."
))
story.append(CppBlock([
    "// LC 52 — N-Queens II: count solutions only (bitmask approach)",
    "int totalNQueens(int n) {",
    "    int count = 0;",
    "    int full = (1<<n)-1;        // all n bits set = all columns available",
    "    function<void(int,int,int)> bt = [&](int cols, int d1, int d2) {",
    "        if (cols == full) { count++; return; }",
    "        // Available positions: columns not attacked",
    "        int avail = ~(cols|d1|d2) & full;",
    "        while (avail) {",
    "            int pos = avail & (-avail);   // lowest set bit = rightmost available col",
    "            avail &= avail-1;             // clear that bit",
    "            bt(cols|pos, (d1|pos)<<1, (d2|pos)>>1);",
    "            //  new cols  new main diag  new anti diag",
    "        }",
    "    };",
    "    bt(0, 0, 0);",
    "    return count;",
    "}",
    "// Time: O(n!)   Space: O(n) — much faster in practice than set-based",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 7 — SUDOKU SOLVER
# ══════════════════════════════════════════════════════════════
story.append(Banner("7","Sudoku Solver  (LC 37)  — Hard",RED,NAVY))
story.append(sp(1))

story.append(h2("7.1  Constraint Modelling"))
story.append(body(
    "Maintain bitmasks for each row (9 bits), each column (9 bits), and each 3x3 box (9 bits). "
    "Bit i is set if digit i+1 is already placed. "
    "Available digits for cell (r,c) = ~(rowMask[r] | colMask[c] | boxMask[r/3*3+c/3]) & 0x1FF."
))
story.append(CppBlock([
    "// LC 37 — Sudoku Solver",
    "void solveSudoku(vector<vector<char>>& board) {",
    "    int rowM[9]={}, colM[9]={}, boxM[9]={};",
    "    vector<pair<int,int>> empty;",
    "    // Initialise masks from existing digits",
    "    for (int r=0;r<9;r++) for (int c=0;c<9;c++) {",
    "        if (board[r][c]=='.') { empty.push_back({r,c}); continue; }",
    "        int bit = 1<<(board[r][c]-'1');",
    "        rowM[r]|=bit; colM[c]|=bit; boxM[r/3*3+c/3]|=bit;",
    "    }",
    "    function<bool(int)> bt = [&](int idx) -> bool {",
    "        if (idx==(int)empty.size()) return true;",
    "        auto [r,c] = empty[idx];",
    "        int avail = ~(rowM[r]|colM[c]|boxM[r/3*3+c/3]) & 0x1FF;",
    "        while (avail) {",
    "            int bit = avail & (-avail);    // lowest available digit bit",
    "            avail &= avail-1;",
    "            int d = __builtin_ctz(bit);    // digit index (0-based)",
    "            board[r][c] = '1'+d;",
    "            rowM[r]|=bit; colM[c]|=bit; boxM[r/3*3+c/3]|=bit;",
    "            if (bt(idx+1)) return true;    // solved!",
    "            rowM[r]^=bit; colM[c]^=bit; boxM[r/3*3+c/3]^=bit;",
    "            board[r][c]='.';",
    "        }",
    "        return false;",
    "    };",
    "    bt(0);",
    "}",
    "// Time: O(9^empty_cells) worst case   Space: O(1) extra",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 8 — WORD SEARCH
# ══════════════════════════════════════════════════════════════
story.append(Banner("8","Word Search on Grid",ORANGE,RED))
story.append(sp(1))

story.append(h2("8.1  Word Search I  (LC 79)  — Medium"))
story.append(body(
    "Search for a word in a 2D grid — can move in 4 directions, no reuse. "
    "DFS from each cell. Mark cell visited during recursion, restore after."
))
story.append(CppBlock([
    "// LC 79 — Word Search",
    "bool exist(vector<vector<char>>& board, string word) {",
    "    int m=board.size(), n=board[0].size();",
    "    int dr[]={-1,1,0,0}, dc[]={0,0,-1,1};",
    "    function<bool(int,int,int)> dfs = [&](int r, int c, int k) -> bool {",
    "        if (k == (int)word.size()) return true;   // all chars matched",
    "        if (r<0||r>=m||c<0||c>=n||board[r][c]!=word[k]) return false;",
    "        char orig = board[r][c];",
    "        board[r][c] = '#';                         // mark visited",
    "        for (int d=0;d<4;d++)",
    "            if (dfs(r+dr[d], c+dc[d], k+1)) { board[r][c]=orig; return true; }",
    "        board[r][c] = orig;                        // restore",
    "        return false;",
    "    };",
    "    for (int r=0;r<m;r++) for (int c=0;c<n;c++)",
    "        if (dfs(r,c,0)) return true;",
    "    return false;",
    "}",
    "// Time: O(m*n * 4^L) L=word length   Space: O(L) recursion",
]))
story.append(sp(0.8))

story.append(h2("8.2  Word Search II — Multiple Words via Trie  (LC 212)  — Hard"))
story.append(body(
    "Find all words from a dictionary that exist in the board. "
    "Naive approach: run Word Search I for each word → O(words * m*n * 4^L). "
    "Trie approach: build Trie of all words, then DFS using Trie to guide search. "
    "Remove found words from Trie to avoid duplicates and prune exhausted branches."
))
story.append(CppBlock([
    "struct TrieNode {",
    "    TrieNode* ch[26]={};",
    "    string word = \"\";   // non-empty means a word ends here",
    "};",
    "vector<string> findWords(vector<vector<char>>& board,",
    "                          vector<string>& words) {",
    "    TrieNode* root = new TrieNode();",
    "    // Build trie from word list",
    "    for (auto& w : words) {",
    "        TrieNode* cur=root;",
    "        for (char c:w) { if(!cur->ch[c-'a']) cur->ch[c-'a']=new TrieNode();",
    "                         cur=cur->ch[c-'a']; }",
    "        cur->word=w;",
    "    }",
    "    int m=board.size(), n=board[0].size();",
    "    vector<string> result;",
    "    int dr[]={-1,1,0,0}, dc[]={0,0,-1,1};",
    "    function<void(int,int,TrieNode*)> dfs=[&](int r,int c,TrieNode* node){",
    "        if(r<0||r>=m||c<0||c>=n||board[r][c]=='#') return;",
    "        char ch=board[r][c];",
    "        TrieNode* next=node->ch[ch-'a'];",
    "        if(!next) return;                    // PRUNE: no word with this prefix",
    "        if(next->word!=\"\") {               // found a word",
    "            result.push_back(next->word);",
    "            next->word=\"\";                 // remove to avoid duplicates",
    "        }",
    "        board[r][c]='#';                     // mark visited",
    "        for(int d=0;d<4;d++) dfs(r+dr[d],c+dc[d],next);",
    "        board[r][c]=ch;                      // restore",
    "    };",
    "    for(int r=0;r<m;r++) for(int c=0;c<n;c++) dfs(r,c,root);",
    "    return result;",
    "}",
    "// Time: O(m*n*4^L + W*L)  W=#words, L=avg length   Space: O(W*L)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 9 — TRIE CORE
# ══════════════════════════════════════════════════════════════
story.append(Banner("9","Trie — Core Theory & Implementation",TEAL,RED))
story.append(sp(1))

story.append(h2("9.1  What is a Trie?"))
story.append(body(
    "A <b>Trie</b> (prefix tree or digital tree) is a tree where each node represents "
    "a character, and paths from root to marked nodes spell out words. "
    "All strings sharing a common prefix share the same path in the Trie. "
    "This enables O(L) insert, search, and prefix queries — where L is the string length — "
    "independent of the number of stored strings."
))
story.append(sp(0.5))

# Trie diagram for {app, apple, apply, apt}
story.append(TrieDiagram(
    nodes=[
        (0, "root",0.5, 0.88, False),
        (1, "a",   0.5, 0.65, False),
        (2, "p",   0.5, 0.42, False),
        (3, "p",   0.2, 0.20, False),
        (4, "t",   0.8, 0.20, False),
        (5, "l",   0.1, 0.04, False),
        (6, "e",   0.25,0.04, True),
        (7, "y",   0.4, 0.04, True),
        (8, "p",   0.8, 0.04, True),
    ],
    edges=[
        (0,1,"a"),(1,2,"p"),(2,3,"p"),(2,4,"t"),
        (3,5,"l"),(3,6,"le"),(3,7,"ly"),(4,8,"t"),
    ],
    highlights={0:NAVY},
    label="Trie for {apple, apply, apt}: double-circle = end of word, shared prefix 'ap'",
    color=TEAL, height=62*mm
))
story.append(sp(0.5))

story.append(h2("9.2  Full Trie Implementation  (LC 208)"))
story.append(CppBlock([
    "// LC 208 — Implement Trie (Prefix Tree)",
    "class Trie {",
    "    struct TrieNode {",
    "        TrieNode* children[26];",
    "        bool isEnd;",
    "        TrieNode() : isEnd(false) {",
    "            fill(children, children+26, nullptr);",
    "        }",
    "    };",
    "    TrieNode* root;",
    "public:",
    "    Trie() { root = new TrieNode(); }",
    "",
    "    void insert(const string& word) {",
    "        TrieNode* cur = root;",
    "        for (char c : word) {",
    "            int idx = c - 'a';",
    "            if (!cur->children[idx])",
    "                cur->children[idx] = new TrieNode();",
    "            cur = cur->children[idx];",
    "        }",
    "        cur->isEnd = true;",
    "    }   // Time: O(L)   Space: O(L * 26) per word",
    "",
    "    bool search(const string& word) {",
    "        TrieNode* cur = root;",
    "        for (char c : word) {",
    "            int idx = c - 'a';",
    "            if (!cur->children[idx]) return false;",
    "            cur = cur->children[idx];",
    "        }",
    "        return cur->isEnd;",
    "    }   // Time: O(L)",
    "",
    "    bool startsWith(const string& prefix) {",
    "        TrieNode* cur = root;",
    "        for (char c : prefix) {",
    "            if (!cur->children[c-'a']) return false;",
    "            cur = cur->children[c-'a'];",
    "        }",
    "        return true;",
    "    }   // Time: O(L)",
    "",
    "    // Delete a word from the trie",
    "    bool remove(const string& word) {",
    "        function<bool(TrieNode*, int)> del = [&](TrieNode* n, int i) -> bool {",
    "            if (i == (int)word.size()) {",
    "                if (!n->isEnd) return false;",
    "                n->isEnd = false;",
    "                // Can delete node if it has no children",
    "                for (auto c : n->children) if (c) return false;",
    "                return true;",
    "            }",
    "            int idx = word[i]-'a';",
    "            if (!n->children[idx]) return false;",
    "            if (del(n->children[idx], i+1)) {",
    "                delete n->children[idx];",
    "                n->children[idx] = nullptr;",
    "                // Can delete this node too if no other children",
    "                if (!n->isEnd) {",
    "                    for (auto c : n->children) if (c) return false;",
    "                    return true;",
    "                }",
    "            }",
    "            return false;",
    "        };",
    "        return del(root, 0);",
    "    }",
    "};",
    "// Space: O(ALPHABET_SIZE * L * W)  W=number of words",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 10 — TRIE CLASSIC PROBLEMS
# ══════════════════════════════════════════════════════════════
story.append(Banner("10","Trie — Classic Problems",TEAL,RED))
story.append(sp(1))

story.append(h2("10.1  Design Add and Search Words  (LC 211)  — Medium"))
story.append(body(
    "Support wildcard '.' which matches any character. "
    "Normal characters traverse the Trie deterministically. "
    "For '.', try all 26 children recursively."
))
story.append(CppBlock([
    "class WordDictionary {",
    "    struct Node { Node* ch[26]={}; bool end=false; };",
    "    Node* root;",
    "public:",
    "    WordDictionary() { root = new Node(); }",
    "    void addWord(string word) {",
    "        Node* cur=root;",
    "        for (char c:word) {",
    "            if(!cur->ch[c-'a']) cur->ch[c-'a']=new Node();",
    "            cur=cur->ch[c-'a'];",
    "        }",
    "        cur->end=true;",
    "    }",
    "    bool search(string word) {",
    "        function<bool(Node*,int)> dfs=[&](Node* n, int i)->bool{",
    "            if(i==(int)word.size()) return n->end;",
    "            char c=word[i];",
    "            if(c!='.') {",
    "                return n->ch[c-'a'] && dfs(n->ch[c-'a'],i+1);",
    "            }",
    "            // Wildcard: try all children",
    "            for(int j=0;j<26;j++)",
    "                if(n->ch[j] && dfs(n->ch[j],i+1)) return true;",
    "            return false;",
    "        };",
    "        return dfs(root,0);",
    "    }",
    "};",
    "// search: O(26^wildcards * L) worst case",
]))
story.append(sp(0.8))

story.append(h2("10.2  Replace Words  (LC 648)  — Medium"))
story.append(body(
    "Given a list of roots and a sentence, replace each word in the sentence with its shortest root. "
    "Build Trie from roots. For each word, traverse Trie to find shortest prefix."
))
story.append(CppBlock([
    "string replaceWords(vector<string>& dictionary, string sentence) {",
    "    // Build Trie from roots",
    "    struct Node { Node* ch[26]={}; bool isRoot=false; };",
    "    Node* root = new Node();",
    "    for (auto& r : dictionary) {",
    "        Node* cur=root;",
    "        for (char c:r) { if(!cur->ch[c-'a']) cur->ch[c-'a']=new Node();",
    "                         cur=cur->ch[c-'a']; }",
    "        cur->isRoot=true;",
    "    }",
    "    // Replace each word",
    "    istringstream iss(sentence);",
    "    string result, word;",
    "    while (iss >> word) {",
    "        if (!result.empty()) result += ' ';",
    "        Node* cur=root; string prefix=\"\";",
    "        bool replaced=false;",
    "        for (char c:word) {",
    "            if(!cur->ch[c-'a']) break;",
    "            cur=cur->ch[c-'a']; prefix+=c;",
    "            if(cur->isRoot) { result+=prefix; replaced=true; break; }",
    "        }",
    "        if(!replaced) result+=word;",
    "    }",
    "    return result;",
    "}",
    "// Time: O(sum_roots + |sentence|)   Space: O(sum_root_lengths * 26)",
]))
story.append(sp(0.8))

story.append(h2("10.3  Search Suggestions System  (LC 1268)  — Medium"))
story.append(body(
    "After each character typed, suggest up to 3 products with the matching prefix, lexicographically sorted. "
    "Sort products first. For each prefix, find matching products using Trie or binary search."
))
story.append(CppBlock([
    "// Binary search approach — simpler and same complexity",
    "vector<vector<string>> suggestedProducts(",
    "        vector<string>& products, string searchWord) {",
    "    sort(products.begin(), products.end());",
    "    vector<vector<string>> result;",
    "    string prefix = \"\";",
    "    for (char c : searchWord) {",
    "        prefix += c;",
    "        // Lower bound: first product >= prefix",
    "        auto lo = lower_bound(products.begin(), products.end(), prefix);",
    "        vector<string> suggestions;",
    "        for (int i=0; i<3 && lo!=products.end(); i++, lo++) {",
    "            // Check if still has this prefix",
    "            if (lo->substr(0, prefix.size()) == prefix)",
    "                suggestions.push_back(*lo);",
    "            else break;",
    "        }",
    "        result.push_back(suggestions);",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n log n + L * (log n + 3))   Space: O(L) for prefix string",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 11 — TRIE ADVANCED
# ══════════════════════════════════════════════════════════════
story.append(Banner("11","Trie — Advanced Applications",NAVY,RED))
story.append(sp(1))

story.append(h2("11.1  Maximum XOR of Two Numbers  (LC 421)  — Medium"))
story.append(body(
    "Find the maximum XOR of any two numbers in an array. "
    "Build a binary Trie of all numbers (bit by bit from MSB to LSB). "
    "For each number, greedily choose the opposite bit at each level to maximise XOR."
))
story.append(CppBlock([
    "// LC 421 — Maximum XOR of Two Numbers in an Array",
    "struct XorTrieNode {",
    "    XorTrieNode* ch[2] = {};",
    "};",
    "",
    "int findMaximumXOR(vector<int>& nums) {",
    "    XorTrieNode* root = new XorTrieNode();",
    "    // Insert all numbers into binary Trie (bit 31 to bit 0)",
    "    for (int x : nums) {",
    "        XorTrieNode* cur = root;",
    "        for (int i=31; i>=0; i--) {",
    "            int bit = (x>>i) & 1;",
    "            if (!cur->ch[bit]) cur->ch[bit] = new XorTrieNode();",
    "            cur = cur->ch[bit];",
    "        }",
    "    }",
    "    // For each number, query maximum XOR",
    "    int ans = 0;",
    "    for (int x : nums) {",
    "        XorTrieNode* cur = root;",
    "        int xorVal = 0;",
    "        for (int i=31; i>=0; i--) {",
    "            int bit = (x>>i) & 1;",
    "            int want = 1-bit;          // want opposite bit for max XOR",
    "            if (cur->ch[want]) {",
    "                xorVal |= (1<<i);      // this bit of XOR = 1",
    "                cur = cur->ch[want];",
    "            } else {",
    "                cur = cur->ch[bit];    // must take same bit",
    "            }",
    "        }",
    "        ans = max(ans, xorVal);",
    "    }",
    "    return ans;",
    "}",
    "// Time: O(n * 32)   Space: O(n * 32)",
]))
story.append(sp(0.8))

story.append(h2("11.2  Map Sum Pairs  (LC 677)  — Medium"))
story.append(body(
    "Insert key-value pairs. Find the sum of all values with keys starting with a given prefix. "
    "Store the sum at each node of the prefix that contributes to it."
))
story.append(CppBlock([
    "// LC 677 — Map Sum Pairs",
    "class MapSum {",
    "    struct Node { Node* ch[26]={}; int val=0; };",
    "    Node* root;",
    "    unordered_map<string,int> map;   // store inserted values",
    "public:",
    "    MapSum() { root = new Node(); }",
    "    void insert(string key, int val) {",
    "        int delta = val - map[key];  // change in value (handles updates)",
    "        map[key]  = val;",
    "        Node* cur = root;",
    "        for (char c : key) {",
    "            if (!cur->ch[c-'a']) cur->ch[c-'a'] = new Node();",
    "            cur = cur->ch[c-'a'];",
    "            cur->val += delta;       // each node on path gets delta",
    "        }",
    "    }",
    "    int sum(string prefix) {",
    "        Node* cur = root;",
    "        for (char c : prefix) {",
    "            if (!cur->ch[c-'a']) return 0;",
    "            cur = cur->ch[c-'a'];",
    "        }",
    "        return cur->val;             // sum of all values with this prefix",
    "    }",
    "};",
    "// insert: O(L)   sum: O(L)   Space: O(total_key_length * 26)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 12 — CHEAT SHEET
# ══════════════════════════════════════════════════════════════
story.append(Banner("12","Complexity Cheat Sheet & LeetCode Map",NAVY,RED))
story.append(sp(1))

story.append(h2("12.1  Backtracking Complexity Summary"))
bt_data = [
    ["Problem Type",              "Time Complexity",   "Space",    "Pruning Key"],
    ["Subsets of n elements",     "O(n * 2^n)",        "O(n)",     "Sort + skip dup at same level"],
    ["Permutations (distinct)",   "O(n * n!)",         "O(n)",     "used[] array prevents reuse"],
    ["Permutations (duplicates)", "O(n * n!)",         "O(n)",     "Sort + skip if !used[i-1] & dup"],
    ["Combinations nCk",          "O(k * C(n,k))",    "O(k)",     "start index avoids reversed dups"],
    ["Combination Sum",           "O(n^(T/M))",       "O(T/M)",   "Sort + break if cand > remaining"],
    ["N-Queens",                  "O(n!)",             "O(n)",     "Bitmask O(1) conflict check"],
    ["Sudoku Solver",             "O(9^empty)",        "O(1)",     "Bitmask available digits"],
    ["Palindrome Partition",      "O(n * 2^n)",        "O(n^2)",   "Precompute isPalin table"],
    ["Word Search I",             "O(m*n * 4^L)",     "O(L)",     "In-place visited marking"],
    ["Word Search II (Trie)",     "O(m*n * 4^L)",     "O(W*L)",   "Trie guides DFS, prune no-prefix"],
]
story.append(mtbl(bt_data,[50*mm,30*mm,16*mm,62*mm]))
story.append(cap("Table 1: Backtracking complexity summary"))
story.append(sp(0.5))

story.append(h2("12.2  Trie Complexity Summary"))
trie_data = [
    ["Operation",         "Time",    "Space",          "Notes"],
    ["Insert word",       "O(L)",    "O(L * Σ)",       "Σ = alphabet size (26 for lowercase)"],
    ["Search word",       "O(L)",    "O(1)",           "Exact match"],
    ["Prefix search",     "O(L)",    "O(1)",           "startsWith"],
    ["Delete word",       "O(L)",    "O(L)",           "Recursive cleanup"],
    ["Count words",       "O(W*L)",  "O(W*L)",         "Build then query"],
    ["Wildcard search",   "O(26^w*L)","O(L)",          "w = number of wildcards"],
    ["XOR Trie insert",   "O(32)",   "O(32*n)",        "32-bit integers"],
    ["XOR Trie query",    "O(32)",   "O(1)",           "Greedy opposite bit"],
    ["Space (array)",     "—",       "O(Σ * W * avgL)","Array of children pointers"],
    ["Space (hashmap)",   "—",       "O(W * avgL)",    "HashMap children; slower access"],
]
story.append(mtbl(trie_data,[30*mm,22*mm,26*mm,80*mm]))
story.append(cap("Table 2: Trie operations complexity (L=word length, W=number of words)"))
story.append(sp(0.5))

story.append(h2("12.3  Pattern Decision Guide"))
story.append(CppBlock([
    "/*",
    " * PROBLEM SIGNAL                             → APPROACH",
    " * ─────────────────────────────────────────────────────────────────────",
    " * Generate all subsets                       → Backtracking (include/exclude)",
    " * Generate all permutations                  → Backtracking + used[] array",
    " * Generate all combinations                  → Backtracking with start index",
    " * Find all solutions satisfying constraint   → Backtracking + pruning",
    " * Constraint satisfaction (Sudoku, N-Queens) → Backtracking + bitmask pruning",
    " * Path-finding in 2D grid                   → DFS backtracking with in-place mark",
    " * Multiple words in grid                     → Trie + DFS backtracking",
    " * Prefix search / autocomplete               → Trie",
    " * Replace words with shortest root           → Trie (prefix query)",
    " * Count strings with prefix                  → Trie with counts at each node",
    " * Wildcard matching over dictionary          → Trie with DFS for '.'",
    " * Maximum XOR of two numbers                 → Binary Trie (greedy opposite bit)",
    " * Duplicate subsets/permutations             → Sort + skip dup at same level",
    " * Deduplication with sets                    → Sort first, then skip == prev",
    " */",
]))
story.append(sp(0.5))

story.append(h2("12.4  LeetCode Problem Map"))
lc_data = [
    ["#",   "Problem",                               "Pattern",                    "Diff"],
    ["17",  "Letter Combinations of Phone Number",    "Backtracking",               "Medium"],
    ["22",  "Generate Parentheses",                   "Backtracking + validity",    "Medium"],
    ["37",  "Sudoku Solver",                          "Backtracking + bitmask",     "Hard"],
    ["39",  "Combination Sum",                        "BT + unlimited reuse",       "Medium"],
    ["40",  "Combination Sum II",                     "BT + skip duplicates",       "Medium"],
    ["46",  "Permutations",                           "BT + used[] array",          "Medium"],
    ["47",  "Permutations II",                        "BT + !used[i-1] skip",       "Medium"],
    ["51",  "N-Queens",                               "BT + diag sets",             "Hard"],
    ["52",  "N-Queens II",                            "BT + bitmask optimization",  "Hard"],
    ["77",  "Combinations",                           "BT with start index",        "Medium"],
    ["78",  "Subsets",                                "BT include/exclude",         "Medium"],
    ["79",  "Word Search",                            "DFS + backtrack in grid",    "Medium"],
    ["90",  "Subsets II",                             "BT + skip dup same level",   "Medium"],
    ["93",  "Restore IP Addresses",                   "BT + pruning",               "Medium"],
    ["131", "Palindrome Partitioning",                "BT + isPalin table",         "Medium"],
    ["212", "Word Search II",                         "Trie + DFS backtracking",    "Hard"],
    ["208", "Implement Trie",                         "Trie insert/search/prefix",  "Medium"],
    ["211", "Design Add and Search Words",            "Trie + DFS wildcard",        "Medium"],
    ["421", "Maximum XOR of Two Numbers in Array",    "Binary Trie",                "Medium"],
    ["472", "Concatenated Words",                     "Trie + DP",                  "Hard"],
    ["588", "Design In-Memory File System",           "Trie",                       "Hard"],
    ["648", "Replace Words",                          "Trie prefix replacement",    "Medium"],
    ["677", "Map Sum Pairs",                          "Trie with prefix sum",       "Medium"],
    ["1268","Search Suggestions System",              "Trie / Binary Search",       "Medium"],
]
dc={"Easy":GREEN,"Medium":ORANGE,"Hard":RED}
le=[]
for i,r in enumerate(lc_data[1:],1):
    col=dc.get(r[3],DARK)
    le+=[("TEXTCOLOR",(3,i),(3,i),col),("FONTNAME",(3,i),(3,i),"Helvetica-Bold")]
story.append(mtbl(lc_data,[13*mm,68*mm,48*mm,19*mm],extra=le))
story.append(cap("Table 3: 23 LeetCode problems — Backtracking & Trie"))
story.append(sp(0.8))

story.append(InfoBox([
    "1.  Backtracking = DFS on decision tree. CHOOSE → EXPLORE → UNCHOOSE. Always restore state.",
    "2.  Deduplication: SORT the input first. Skip if i > start && nums[i] == nums[i-1].",
    "3.  Permutations vs Combinations: Permutations use used[] (no start). Combinations use start (no used[]).",
    "4.  Combination Sum reuse: pass i (same index). No reuse: pass i+1.",
    "5.  N-Queens bitmask: avail = ~(cols|d1|d2) & full. Pick lowest bit: bit = avail & (-avail).",
    "6.  Pruning is EVERYTHING in backtracking. Sort + break when candidate exceeds remaining = huge speedup.",
    "7.  Word Search II: build Trie from word list. DFS uses Trie node to guide search and prune dead branches.",
    "8.  Trie insert/search: O(L) per operation. Never O(n) — independent of number of stored words.",
    "9.  XOR Trie: build bit-by-bit from MSB. For max XOR, greedily choose opposite bit if available.",
    "10. In-place visited marking (board[r][c]='#'): saves O(m*n) extra space vs a separate visited array.",
], title="🏆 Golden Rules — Backtracking & Trie", color=NAVY, bg=LIGHT))

# ── BUILD ───────────────────────────────────────────────────────
out = "DSA_Notes_Backtracking_Trie.pdf"
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=34*mm,  bottomMargin=18*mm,
    title="DSA Notes — Backtracking & Trie",
    author="DSA Revision Planner",
    subject="Complete Backtracking and Trie Notes with C++",
)
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"\n✅  Done!  →  {out}")
print(f"   Open the PDF in the same folder where you ran this script.")