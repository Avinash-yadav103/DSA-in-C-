"""
DSA Notes — Graphs: BFS, DFS & Union-Find
Run:  python Graphs_BFS_DFS_UnionFind_Notes.py
Output: DSA_Notes_Graphs_BFS_DFS_UnionFind.pdf  (same folder)
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
    c.setFillColor(TEAL);  c.rect(0, H-28*mm, W, 2*mm,  fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, H-16*mm, "DSA Notes — Graphs: BFS, DFS & Union-Find")
    c.setFont("Helvetica", 9)
    c.drawRightString(W-15*mm, H-16*mm, "Topic 8 of 13")
    c.setFillColor(NAVY);  c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(TEAL);  c.rect(0, 12*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica", 8)
    c.drawString(15*mm, 4*mm, "DSA Revision Planner  •  C++ Code Edition")
    c.drawRightString(W-15*mm, 4*mm, f"Page {doc.page}")
    c.restoreState()

first_page  = lambda c, doc: _chrome(c, doc)
later_pages = lambda c, doc: _chrome(c, doc)

# ── Flowables ──────────────────────────────────────────────────
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
    def __init__(self, lines, title="", color=TEAL, bg=TEAL_BG, width=None):
        super().__init__()
        self.lines = lines if isinstance(lines, list) else [lines]
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


class GraphDiagram(Flowable):
    """
    Draws a graph given as:
      nodes: list of (id, label, x, y)  — x,y in [0,1] relative coords
      edges: list of (u, v, label, directed)
      highlights: {node_id: fill_color}
    """
    def __init__(self, nodes, edges, highlights=None, label="",
                 color=TEAL, width=None, height=55*mm):
        super().__init__()
        self.nodes      = nodes
        self.edges      = edges
        self.highlights = highlights or {}
        self.label      = label
        self.color      = color
        self._w         = width or (W-30*mm)
        self._h         = height
        self.r          = 6*mm

    def wrap(self,*a):
        return self._w, self._h + (5*mm if self.label else 0)

    def _node_pos(self, x, y):
        return x * (self._w - 2*self.r) + self.r, \
               y * (self._h - 2*self.r - (5*mm if self.label else 0)) + self.r

    def draw(self):
        c = self.canv
        r = self.r

        # draw edges first
        for edge in self.edges:
            if len(edge) == 4:
                u, v, elabel, directed = edge
            else:
                u, v, elabel = edge[0], edge[1], edge[2] if len(edge)>2 else ""
                directed = False
            nu = next((n for n in self.nodes if n[0]==u), None)
            nv = next((n for n in self.nodes if n[0]==v), None)
            if nu is None or nv is None: continue
            x1,y1 = self._node_pos(nu[2], nu[3])
            x2,y2 = self._node_pos(nv[2], nv[3])
            dx,dy  = x2-x1, y2-y1
            dist   = math.sqrt(dx*dx+dy*dy) or 1
            ux,uy  = dx/dist, dy/dist
            sx, sy = x1+ux*r, y1+uy*r
            ex, ey = x2-ux*r, y2-uy*r
            c.setStrokeColor(MUTED); c.setLineWidth(1.2)
            c.line(sx, sy, ex, ey)
            if directed:
                c.setFillColor(MUTED)
                p=c.beginPath()
                p.moveTo(ex,ey)
                p.lineTo(ex-ux*3*mm+uy*1.5*mm, ey-uy*3*mm-ux*1.5*mm)
                p.lineTo(ex-ux*3*mm-uy*1.5*mm, ey-uy*3*mm+ux*1.5*mm)
                p.close(); c.drawPath(p,fill=1,stroke=0)
            if elabel:
                mx,my = (sx+ex)/2, (sy+ey)/2
                c.setFillColor(ORANGE); c.setFont("Helvetica-Bold",8)
                ew = c.stringWidth(elabel,"Helvetica-Bold",8)
                c.setFillColor(white)
                c.roundRect(mx-ew/2-1*mm, my-2.5*mm, ew+2*mm, 5*mm, 1*mm, fill=1, stroke=0)
                c.setFillColor(ORANGE)
                c.drawString(mx-ew/2, my-2*mm, elabel)

        # draw nodes
        for node in self.nodes:
            nid, lbl, nx, ny = node
            x,y   = self._node_pos(nx, ny)
            fill  = self.highlights.get(nid, self.color)
            c.setFillColor(fill); c.setStrokeColor(fill); c.setLineWidth(1.5)
            c.circle(x,y,r,fill=1,stroke=1)
            c.setFillColor(white); c.setFont("Helvetica-Bold",9)
            sw = c.stringWidth(str(lbl),"Helvetica-Bold",9)
            c.drawString(x-sw/2, y-3*mm, str(lbl))

        if self.label:
            c.setFillColor(MUTED); c.setFont("Helvetica-Oblique",8)
            lw = c.stringWidth(self.label,"Helvetica-Oblique",8)
            c.drawString(self._w/2-lw/2, 0.5*mm, self.label)


class BFSStepsViz(Flowable):
    """Visualise BFS queue state at each step."""
    def __init__(self, steps, color=TEAL, width=None):
        super().__init__()
        self.steps = steps   # list of (visited_set, queue_list, note_str)
        self.color = color
        self._w    = width or (W-30*mm)
        self.row_h = 8*mm

    def wrap(self,*a):
        return self._w, len(self.steps)*self.row_h + 10*mm

    def draw(self):
        c = self.canv
        n = len(self.steps)
        col_w = [12*mm, 62*mm, 62*mm, self._w-136*mm]
        headers = ["Step","Visited","Queue","Action"]
        # header
        x = 0
        c.setFillColor(NAVY)
        c.rect(0, n*self.row_h+2*mm, self._w, 8*mm, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold",8)
        for i,(h,cw) in enumerate(zip(headers,col_w)):
            c.drawString(x+2*mm, n*self.row_h+4.5*mm, h); x+=cw
        for si,(visited,queue,note) in enumerate(self.steps):
            y = (n-1-si)*self.row_h + 2*mm
            fill = ALT_ROW if si%2==0 else white
            c.setFillColor(fill); c.rect(0,y,self._w,self.row_h,fill=1,stroke=0)
            c.setStrokeColor(BORDER); c.setLineWidth(0.3); c.rect(0,y,self._w,self.row_h,fill=0,stroke=1)
            x=0
            c.setFillColor(DARK); c.setFont("Helvetica-Bold",8)
            c.drawString(x+3*mm, y+2.5*mm, str(si+1)); x+=col_w[0]
            c.setFont("Helvetica",7.5)
            c.setFillColor(GREEN)
            c.drawString(x+2*mm, y+2.5*mm, "{"+", ".join(str(v) for v in sorted(visited))+"}"); x+=col_w[1]
            c.setFillColor(TEAL)
            c.drawString(x+2*mm, y+2.5*mm, "["+", ".join(str(v) for v in queue)+"]"); x+=col_w[2]
            c.setFillColor(DARK)
            c.drawString(x+2*mm, y+2.5*mm, note)


class UnionFindViz(Flowable):
    """Shows union-find parent array state."""
    def __init__(self, n, parent, rank=None, label="", color=PURPLE, width=None):
        super().__init__()
        self.n      = n
        self.parent = parent
        self.rank   = rank
        self.label  = label
        self.color  = color
        self._w     = width or (W-30*mm)
        self.cell_h = 9*mm

    def wrap(self,*a):
        rows = 2 if self.rank else 1
        return self._w, rows*self.cell_h + 14*mm

    def draw(self):
        c    = self.canv
        n    = self.n
        cw   = min(16*mm, (self._w-28*mm)/n)
        sx   = (self._w - n*cw) / 2
        base = 8*mm if self.rank else 3*mm

        # header row
        headers = [("Index", NAVY), ("Parent", self.color)]
        if self.rank: headers.append(("Rank", ORANGE))

        row_labels = ["index", "parent"]
        if self.rank: row_labels.append("rank")
        data_rows  = [list(range(n)), self.parent]
        if self.rank: data_rows.append(self.rank)

        for ri, (row_lbl, row_data) in enumerate(zip(row_labels, data_rows)):
            y = base + (len(data_rows)-1-ri)*self.cell_h
            c.setFillColor(MUTED); c.setFont("Helvetica-Bold",7.5)
            c.drawString(2*mm, y+2.5*mm, row_lbl)
            for i, val in enumerate(row_data):
                x = sx + i*cw
                # highlight root nodes (parent[i]==i)
                is_root = (self.parent[i] == i)
                fill = self.color if is_root else HexColor("#1E293B")
                c.setFillColor(fill); c.setStrokeColor(self.color); c.setLineWidth(0.8)
                c.rect(x, y, cw, self.cell_h-1*mm, fill=1, stroke=1)
                c.setFillColor(white); c.setFont("Helvetica-Bold" if is_root else "Helvetica",8)
                sv = str(val); sw = c.stringWidth(sv,"Helvetica",8)
                c.drawString(x+cw/2-sw/2, y+2.5*mm, sv)

        # draw tree arrows from child to parent
        y_parent = base + (len(data_rows)-1 - row_labels.index("parent"))*self.cell_h
        for i, p in enumerate(self.parent):
            if p != i:
                x1 = sx + i*cw + cw/2
                x2 = sx + p*cw + cw/2
                ay = y_parent + self.cell_h
                c.setStrokeColor(self.color); c.setLineWidth(0.8)
                c.line(x1, ay, x1, ay+3*mm)
                c.line(x1, ay+3*mm, x2, ay+3*mm)
                c.line(x2, ay+3*mm, x2, ay+0.5*mm)
                pp=c.beginPath()
                pp.moveTo(x2, ay)
                pp.lineTo(x2-1.5*mm, ay+2*mm)
                pp.lineTo(x2+1.5*mm, ay+2*mm)
                pp.close(); c.setFillColor(self.color); c.drawPath(pp,fill=1,stroke=0)

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
        'typename','unsigned','size_t','NULL','function','numeric_limits',
        'sort','max','min','swap','reverse','push_back','pop_back','emplace_back',
        'begin','end','empty','size','insert','erase','count','clear','find',
        'front','back','top','push','pop','INT_MAX','INT_MIN','LLONG_MAX',
        'double','float','long long','abs','greater','less',
    }
    def __init__(self, lines, width=None):
        super().__init__()
        self.lines=lines; self._w=width or (W-30*mm)
        self.lh=4.1*mm; self.hh=6.5*mm; self.pad=3.5*mm
    def wrap(self,*a):
        return self._w, self.hh+self.pad+len(self.lines)*self.lh+self.pad
    def draw(self):
        c=self.canv
        th=self.hh+self.pad+len(self.lines)*self.lh+self.pad
        c.setFillColor(CODE_BG); c.roundRect(0,0,self._w,th,3*mm,fill=1,stroke=0)
        c.setFillColor(CODE_HDR); c.roundRect(0,th-self.hh,self._w,self.hh,3*mm,fill=1,stroke=0)
        c.rect(0,th-self.hh,self._w,self.hh/2,fill=1,stroke=0)
        c.setFillColor(CPP_TYPE); c.setFont("Helvetica-Bold",7.5)
        c.drawString(4*mm,th-self.hh+2*mm,"C++")
        for i,col in enumerate([HexColor("#FF5F57"),HexColor("#FEBC2E"),HexColor("#28C840")]):
            c.setFillColor(col); c.circle(self._w-(3-i)*5.5*mm,th-self.hh/2,1.4*mm,fill=1,stroke=0)
        y=th-self.hh-self.pad-self.lh
        for idx,raw in enumerate(self.lines):
            c.setFillColor(HexColor("#3D444D")); c.setFont("Courier",7.5)
            c.drawString(3*mm,y+1.2*mm,f"{idx+1:2d}")
            stripped=raw.lstrip(); indent=len(raw)-len(stripped)
            x=12*mm+indent*2.2*mm
            self._line(c,stripped,x,y+1.2*mm)
            y-=self.lh
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

# ── Style helpers ───────────────────────────────────────────────
def S(name,**kw):
    base=dict(fontName="Helvetica",fontSize=9.5,textColor=DARK,leading=14,spaceBefore=3,spaceAfter=3)
    base.update(kw); return ParagraphStyle(name,**base)

ST={
    "body":    S("body",alignment=TA_JUSTIFY,leading=15),
    "bullet":  S("bullet",leftIndent=12,firstLineIndent=-8,leading=13,spaceBefore=2,spaceAfter=2),
    "caption": S("caption",fontName="Helvetica-Oblique",fontSize=8.5,textColor=MUTED,spaceBefore=2,spaceAfter=6),
    "toc_h":   S("toc_h",fontName="Helvetica-Bold",fontSize=11,textColor=NAVY,spaceBefore=5,spaceAfter=2,leading=15),
    "toc_i":   S("toc_i",fontSize=9.5,textColor=DARK,spaceBefore=1,spaceAfter=1,leftIndent=8,leading=13),
    "cover_t": S("ct",fontName="Helvetica-Bold",fontSize=34,textColor=white,leading=40,alignment=TA_CENTER),
    "cover_s": S("cs",fontName="Helvetica-Bold",fontSize=19,textColor=HexColor("#A0E4EE"),leading=26,alignment=TA_CENTER),
    "cover_d": S("cd",fontName="Helvetica",fontSize=11,textColor=HexColor("#CBD5E1"),leading=16,alignment=TA_CENTER),
    "h2": S("h2",fontName="Helvetica-Bold",fontSize=14,textColor=BLUE,leading=20,spaceBefore=10,spaceAfter=4),
    "h3": S("h3",fontName="Helvetica-Bold",fontSize=11.5,textColor=TEAL,leading=16,spaceBefore=8,spaceAfter=3),
    "h4": S("h4",fontName="Helvetica-Bold",fontSize=10,textColor=NAVY,leading=14,spaceBefore=6,spaceAfter=2),
}

def sp(n=1):  return Spacer(1,n*4*mm)
def body(t):  return Paragraph(t,ST["body"])
def cap(t):   return Paragraph(f"<i>{t}</i>",ST["caption"])
def h2(t,col=BLUE): return Paragraph(t,ParagraphStyle("_h2",parent=ST["h2"],textColor=col))
def h3(t,col=TEAL): return Paragraph(t,ParagraphStyle("_h3",parent=ST["h3"],textColor=col))
def h4(t,col=NAVY): return Paragraph(t,ParagraphStyle("_h4",parent=ST["h4"],textColor=col))
def bl(t,col="#1F7A8C"): return Paragraph(f'<font color="{col}">▸</font>  {t}',ST["bullet"])

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
    [Paragraph("Topic 8 — Graphs: BFS, DFS &amp; Union-Find",ST["cover_s"])],
    [Paragraph(
        "Graph representations · BFS/DFS templates · Connected components<br/>"
        "Cycle detection · Topological sort · Union-Find · 25+ C++ examples",
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
    Paragraph('<b><font color="#1A3C5E">30+</font></b><br/><font size="8" color="#64748B">C++ Examples</font>',
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
story.append(Banner("TOC","Table of Contents",NAVY,TEAL))
story.append(sp(1))
toc=[
    ("1.", "Graph Fundamentals"),
    ("",   "→ Definitions · Types · Representations · Properties"),
    ("",   "→ Adjacency matrix · Adjacency list · Edge list comparison"),
    ("2.", "Breadth-First Search (BFS)"),
    ("",   "→ Algorithm · Queue-based template · Step-by-step trace"),
    ("",   "→ Shortest path in unweighted graph · Multi-source BFS"),
    ("",   "→ 0-1 BFS with deque"),
    ("3.", "BFS — Classic Problems"),
    ("",   "→ Number of Islands · Rotting Oranges · Word Ladder"),
    ("",   "→ Shortest Path in Binary Matrix · Pacific Atlantic"),
    ("4.", "Depth-First Search (DFS)"),
    ("",   "→ Recursive & iterative templates"),
    ("",   "→ DFS timestamps · Discovery/finish times"),
    ("",   "→ DFS tree: tree/back/forward/cross edges"),
    ("5.", "DFS — Cycle Detection"),
    ("",   "→ Undirected graph: visited + parent check"),
    ("",   "→ Directed graph: white-grey-black colouring"),
    ("6.", "Topological Sort"),
    ("",   "→ Kahn's algorithm (BFS-based)"),
    ("",   "→ DFS-based topological sort"),
    ("",   "→ Course Schedule I & II"),
    ("7.", "DFS — Connected Components & SCC"),
    ("",   "→ Connected components · Bipartite check"),
    ("",   "→ Kosaraju's SCC algorithm"),
    ("",   "→ Articulation points & bridges"),
    ("8.", "Union-Find (Disjoint Set Union)"),
    ("",   "→ Quick Find · Quick Union · Weighted Union"),
    ("",   "→ Path compression · Union by rank"),
    ("",   "→ Full optimised implementation"),
    ("9.", "Union-Find — Classic Problems"),
    ("",   "→ Redundant Connection · Number of Provinces"),
    ("",   "→ Accounts Merge · Satisfiability of Equality Equations"),
    ("10.","Grid Problems — BFS & DFS on 2D Arrays"),
    ("",   "→ 4-directional template · Flood fill · Surrounded Regions"),
    ("11.","Shortest Path Algorithms"),
    ("",   "→ Dijkstra's · Bellman-Ford · BFS for unweighted"),
    ("12.","Complexity Cheat Sheet & LeetCode Map"),
]
for num,title in toc:
    if num:
        story.append(Paragraph(f'<b><font color="#1A3C5E">{num}</font></b>  <b>{title}</b>',ST["toc_h"]))
    else:
        story.append(Paragraph(f'<font color="#64748B">        {title}</font>',ST["toc_i"]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 1 — GRAPH FUNDAMENTALS
# ══════════════════════════════════════════════════════════════
story.append(Banner("1","Graph Fundamentals",NAVY,TEAL))
story.append(sp(1))

story.append(h2("1.1  Core Definitions"))
terms=[
    ("Vertex (Node)","A point in the graph. G = (V, E) where V = vertices, E = edges."),
    ("Edge",         "A connection between two vertices. Can be directed or undirected."),
    ("Degree",       "Number of edges incident to a vertex. In-degree (incoming) / out-degree (outgoing) for directed."),
    ("Path",         "Sequence of vertices where consecutive pairs are connected by edges."),
    ("Cycle",        "A path that starts and ends at the same vertex."),
    ("DAG",          "Directed Acyclic Graph. Used for topological sort, dependency resolution."),
    ("Connected",    "Undirected: path exists between every pair of vertices. Directed: strongly/weakly connected."),
    ("Tree",         "Connected undirected graph with V-1 edges (no cycles). A special case of graph."),
    ("Spanning Tree","A subgraph that is a tree and includes all vertices of the original graph."),
    ("Weight",       "A value assigned to an edge representing cost, distance, or capacity."),
    ("Bipartite",    "Graph whose vertices can be coloured with 2 colours such that no edge connects same-colour vertices."),
]
for term,defn in terms:
    story.append(bl(f"<b>{term}:</b>  {defn}"))
story.append(sp(0.5))

story.append(h2("1.2  Graph Representations"))
story.append(h3("Adjacency List — Most Common for Sparse Graphs"))
story.append(CppBlock([
    "#include <vector>",
    "#include <unordered_map>",
    "using namespace std;",
    "",
    "// ── Unweighted undirected graph ────────────────────────",
    "int n = 5;  // vertices 0..4",
    "vector<vector<int>> adj(n);",
    "// Add edge 0--1",
    "adj[0].push_back(1);",
    "adj[1].push_back(0);   // undirected: add both directions",
    "",
    "// ── Weighted directed graph ─────────────────────────── ",
    "vector<vector<pair<int,int>>> wadj(n);  // {neighbour, weight}",
    "wadj[0].push_back({1, 5});   // edge 0→1 with weight 5",
    "wadj[1].push_back({2, 3});   // edge 1→2 with weight 3",
    "",
    "// ── Graph with string nodes ──────────────────────────── ",
    "unordered_map<string, vector<string>> graph;",
    "graph[\"A\"].push_back(\"B\");",
    "graph[\"A\"].push_back(\"C\");",
    "",
    "// Space: O(V + E)   Access neighbour: O(degree)   Check edge: O(degree)",
]))
story.append(sp(0.5))

story.append(h3("Adjacency Matrix — Dense Graphs / Fast Edge Lookup"))
story.append(CppBlock([
    "// Adjacency matrix: O(V^2) space",
    "int n = 5;",
    "vector<vector<int>> mat(n, vector<int>(n, 0));",
    "mat[0][1] = 1; mat[1][0] = 1;   // undirected edge 0--1",
    "mat[2][3] = 7;                   // directed weighted edge 2→3 weight 7",
    "",
    "// Check if edge exists: O(1) — mat[u][v] != 0",
    "// But: O(V^2) space even if graph is sparse!",
    "// Use for: Floyd-Warshall, dense graphs, small V (V <= 1000)",
]))
story.append(sp(0.5))

rep_data=[
    ["Property",             "Adjacency List",          "Adjacency Matrix",      "Edge List"],
    ["Space",                "O(V + E)",                "O(V²)",                 "O(E)"],
    ["Add edge",             "O(1)",                    "O(1)",                  "O(1)"],
    ["Check edge (u,v)",     "O(degree(u))",            "O(1)",                  "O(E)"],
    ["Iterate neighbours",   "O(degree(u))",            "O(V)",                  "O(E)"],
    ["Best for",             "Sparse graphs, BFS/DFS",  "Dense graphs, APSP",    "MST algorithms"],
    ["Memory",               "Compact",                 "Wasteful if sparse",    "Very compact"],
    ["Weighted edges",       "pair<int,int>",           "Store weight in cell",  "tuple<u,v,w>"],
]
story.append(mtbl(rep_data,[38*mm,44*mm,38*mm,38*mm]))
story.append(cap("Table 1: Graph representation comparison"))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 2 — BFS
# ══════════════════════════════════════════════════════════════
story.append(Banner("2","Breadth-First Search (BFS)",TEAL,NAVY))
story.append(sp(1))

story.append(h2("2.1  Algorithm & Intuition"))
story.append(body(
    "BFS explores all vertices at distance d before any vertex at distance d+1. "
    "A <b>queue (FIFO)</b> naturally achieves this level-by-level order. "
    "Mark vertices as visited <b>before enqueuing</b> (not after dequeuing) "
    "to prevent the same vertex being added multiple times."
))
story.append(sp(0.5))

# Graph diagram for BFS trace
story.append(GraphDiagram(
    nodes=[(0,"0",0.5,0.85),(1,"1",0.15,0.55),(2,"2",0.85,0.55),
           (3,"3",0.05,0.2),(4,"4",0.35,0.2),(5,"5",0.65,0.2),(6,"6",0.95,0.2)],
    edges=[(0,1,""),(0,2,""),(1,3,""),(1,4,""),(2,5,""),(2,6,"")],
    highlights={0:NAVY},
    label="Graph: start BFS from node 0",
    color=TEAL, height=52*mm
))
story.append(sp(0.3))

story.append(BFSStepsViz([
    ({0},      [1,2],    "Visit 0 → enqueue neighbours 1,2"),
    ({0,1,2},  [3,4,5,6],"Dequeue 1 → enqueue 3,4 | Dequeue 2 → enqueue 5,6"),
    ({0,1,2,3,4,5,6},[],  "Dequeue 3,4,5,6 → no new neighbours → done"),
]))
story.append(sp(0.5))

story.append(h2("2.2  BFS Template — Adjacency List"))
story.append(CppBlock([
    "#include <queue>",
    "#include <vector>",
    "using namespace std;",
    "",
    "// ── Generic BFS Template ────────────────────────────────",
    "void bfs(int start, vector<vector<int>>& adj) {",
    "    int n = adj.size();",
    "    vector<bool> visited(n, false);",
    "    queue<int> q;",
    "    visited[start] = true;   // mark BEFORE enqueue",
    "    q.push(start);",
    "    while (!q.empty()) {",
    "        int node = q.front(); q.pop();",
    "        // --- process node here ---",
    "        for (int nb : adj[node]) {",
    "            if (!visited[nb]) {",
    "                visited[nb] = true;  // mark BEFORE enqueue",
    "                q.push(nb);",
    "            }",
    "        }",
    "    }",
    "}",
    "// Time: O(V + E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("2.3  BFS Shortest Path — Unweighted Graph"))
story.append(body(
    "BFS gives the <b>shortest path in hops</b> for unweighted graphs. "
    "Maintain a distance array: dist[v] = dist[u] + 1 when edge u→v is traversed in BFS."
))
story.append(CppBlock([
    "vector<int> bfsShortestPath(int src, int dst, vector<vector<int>>& adj) {",
    "    int n = adj.size();",
    "    vector<int>  dist(n, -1);",
    "    vector<int>  prev(n, -1);   // for path reconstruction",
    "    queue<int> q;",
    "    dist[src] = 0;",
    "    q.push(src);",
    "    while (!q.empty()) {",
    "        int u = q.front(); q.pop();",
    "        if (u == dst) break;   // early exit",
    "        for (int v : adj[u]) {",
    "            if (dist[v] == -1) {",
    "                dist[v] = dist[u] + 1;",
    "                prev[v] = u;",
    "                q.push(v);",
    "            }",
    "        }",
    "    }",
    "    if (dist[dst] == -1) return {};   // unreachable",
    "    // Reconstruct path",
    "    vector<int> path;",
    "    for (int v = dst; v != -1; v = prev[v]) path.push_back(v);",
    "    reverse(path.begin(), path.end());",
    "    return path;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("2.4  Multi-Source BFS"))
story.append(body(
    "When multiple starting points exist (e.g., multiple 0s in a grid), "
    "push all sources into the queue initially with distance 0. "
    "BFS naturally propagates the shortest distance from any source."
))
story.append(CppBlock([
    "// Multi-source BFS — e.g., Rotting Oranges (LC 994)",
    "void multiSourceBFS(vector<vector<int>>& grid) {",
    "    int m = grid.size(), n = grid[0].size();",
    "    queue<pair<int,int>> q;",
    "    // Enqueue ALL sources first",
    "    for (int r = 0; r < m; r++)",
    "        for (int c = 0; c < n; c++)",
    "            if (grid[r][c] == 2)   // source condition",
    "                q.push({r, c});",
    "    int dr[] = {-1,1,0,0};",
    "    int dc[] = {0,0,-1,1};",
    "    while (!q.empty()) {",
    "        auto [r, c] = q.front(); q.pop();",
    "        for (int d = 0; d < 4; d++) {",
    "            int nr = r+dr[d], nc = c+dc[d];",
    "            if (nr>=0 && nr<m && nc>=0 && nc<n && grid[nr][nc]==1) {",
    "                grid[nr][nc] = 2;   // mark visited/updated",
    "                q.push({nr, nc});",
    "            }",
    "        }",
    "    }",
    "}",
    "// Time: O(m*n)   Space: O(m*n)",
]))
story.append(sp(0.8))

story.append(h2("2.5  0-1 BFS — Deque for Edge Weights 0 or 1"))
story.append(body(
    "When edge weights are only 0 or 1, use a <b>deque</b> instead of a queue or full Dijkstra. "
    "Weight-0 edges: push to <b>front</b>. Weight-1 edges: push to <b>back</b>. "
    "This gives O(V+E) vs O((V+E) log V) for Dijkstra."
))
story.append(CppBlock([
    "#include <deque>",
    "",
    "vector<int> zeroOneBFS(int src, vector<vector<pair<int,int>>>& adj) {",
    "    int n = adj.size();",
    "    vector<int> dist(n, INT_MAX);",
    "    deque<int> dq;",
    "    dist[src] = 0;",
    "    dq.push_back(src);",
    "    while (!dq.empty()) {",
    "        int u = dq.front(); dq.pop_front();",
    "        for (auto [v, w] : adj[u]) {",
    "            if (dist[u] + w < dist[v]) {",
    "                dist[v] = dist[u] + w;",
    "                if (w == 0) dq.push_front(v);   // 0-weight: front",
    "                else        dq.push_back(v);     // 1-weight: back",
    "            }",
    "        }",
    "    }",
    "    return dist;",
    "}",
    "// Time: O(V + E)   Space: O(V)",
    "// Use case: LC 1368 Minimum Cost to Make at Least One Valid Path in Grid",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 3 — BFS CLASSIC PROBLEMS
# ══════════════════════════════════════════════════════════════
story.append(Banner("3","BFS — Classic Problems",TEAL,NAVY))
story.append(sp(1))

story.append(h2("3.1  Number of Islands  (LC 200)  — Medium"))
story.append(body(
    "Count connected components of '1's in a 2D grid. "
    "For each unvisited '1', BFS/DFS and mark all connected '1's as visited. "
    "Each BFS/DFS call = one island."
))
story.append(CppBlock([
    "int numIslands(vector<vector<char>>& grid) {",
    "    int m = grid.size(), n = grid[0].size(), islands = 0;",
    "    int dr[]={-1,1,0,0}, dc[]={0,0,-1,1};",
    "    for (int r = 0; r < m; r++) {",
    "        for (int c = 0; c < n; c++) {",
    "            if (grid[r][c] == '1') {",
    "                islands++;",
    "                // BFS to mark all connected land",
    "                queue<pair<int,int>> q;",
    "                grid[r][c] = '0';   // mark visited immediately",
    "                q.push({r,c});",
    "                while (!q.empty()) {",
    "                    auto [cr,cc] = q.front(); q.pop();",
    "                    for (int d=0;d<4;d++) {",
    "                        int nr=cr+dr[d], nc=cc+dc[d];",
    "                        if (nr>=0&&nr<m&&nc>=0&&nc<n&&grid[nr][nc]=='1'){",
    "                            grid[nr][nc]='0';",
    "                            q.push({nr,nc});",
    "                        }",
    "                    }",
    "                }",
    "            }",
    "        }",
    "    }",
    "    return islands;",
    "}",
    "// Time: O(m*n)   Space: O(min(m,n)) — max queue size is diagonal",
]))
story.append(sp(0.8))

story.append(h2("3.2  Word Ladder  (LC 127)  — Hard"))
story.append(body(
    "Find minimum transformations from beginWord to endWord changing one letter at a time, "
    "using only words in wordList. Model as graph: nodes = words, edges = one-letter-apart words. "
    "BFS gives shortest path. Key trick: generate all 26-letter variations at each step."
))
story.append(CppBlock([
    "#include <unordered_set>",
    "",
    "int ladderLength(string begin, string end, vector<string>& wordList) {",
    "    unordered_set<string> wordSet(wordList.begin(), wordList.end());",
    "    if (!wordSet.count(end)) return 0;",
    "    queue<string> q;",
    "    q.push(begin);",
    "    int steps = 1;",
    "    while (!q.empty()) {",
    "        int sz = q.size();",
    "        for (int i = 0; i < sz; i++) {",
    "            string word = q.front(); q.pop();",
    "            if (word == end) return steps;",
    "            // Try all single-letter changes",
    "            for (int j = 0; j < (int)word.size(); j++) {",
    "                char orig = word[j];",
    "                for (char c = 'a'; c <= 'z'; c++) {",
    "                    word[j] = c;",
    "                    if (wordSet.count(word)) {",
    "                        q.push(word);",
    "                        wordSet.erase(word);  // remove = mark visited",
    "                    }",
    "                }",
    "                word[j] = orig;",
    "            }",
    "        }",
    "        steps++;",
    "    }",
    "    return 0;",
    "}",
    "// Time: O(M^2 * N)  M=word length, N=wordList size   Space: O(M*N)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 4 — DFS
# ══════════════════════════════════════════════════════════════
story.append(Banner("4","Depth-First Search (DFS)",PURPLE,TEAL))
story.append(sp(1))

story.append(h2("4.1  DFS — Recursive & Iterative Templates"))
story.append(body(
    "DFS explores as far as possible along each branch before backtracking. "
    "Natural with recursion (implicit call stack). "
    "Iterative version uses an explicit stack. "
    "DFS assigns <b>discovery time</b> and <b>finish time</b> to each vertex — useful for cycle detection and SCC."
))
story.append(CppBlock([
    "// ── Recursive DFS ───────────────────────────────────────",
    "void dfsRec(int u, vector<vector<int>>& adj, vector<bool>& vis) {",
    "    vis[u] = true;",
    "    // --- pre-process u here ---",
    "    for (int v : adj[u]) {",
    "        if (!vis[v]) dfsRec(v, adj, vis);",
    "    }",
    "    // --- post-process u here (after all descendants) ---",
    "}",
    "",
    "// Call for all components:",
    "void dfsAll(vector<vector<int>>& adj) {",
    "    int n = adj.size();",
    "    vector<bool> vis(n, false);",
    "    for (int i = 0; i < n; i++)",
    "        if (!vis[i]) dfsRec(i, adj, vis);",
    "}",
    "// Time: O(V+E)   Space: O(V) stack + O(V) visited",
]))
story.append(sp(0.5))
story.append(CppBlock([
    "// ── Iterative DFS (using explicit stack) ───────────────",
    "void dfsIter(int start, vector<vector<int>>& adj) {",
    "    int n = adj.size();",
    "    vector<bool> vis(n, false);",
    "    stack<int> st;",
    "    st.push(start);",
    "    while (!st.empty()) {",
    "        int u = st.top(); st.pop();",
    "        if (vis[u]) continue;   // skip if already visited",
    "        vis[u] = true;",
    "        // --- process u ---",
    "        for (int v : adj[u]) {",
    "            if (!vis[v]) st.push(v);",
    "        }",
    "    }",
    "}",
    "// NOTE: iterative DFS may visit neighbours in reverse order vs recursive",
    "// For exact same order: push neighbours in reverse",
]))
story.append(sp(0.8))

story.append(h2("4.2  DFS Timestamps — Discovery & Finish Times"))
story.append(body(
    "Assign each vertex a <b>discovery time</b> (when first visited) and <b>finish time</b> "
    "(when all descendants processed). These timestamps classify edges and enable "
    "cycle detection, SCC, and topological sort."
))
story.append(CppBlock([
    "int timer = 0;",
    "vector<int> disc, finish;",
    "",
    "void dfsTimestamp(int u, vector<vector<int>>& adj, vector<bool>& vis) {",
    "    vis[u] = true;",
    "    disc[u] = ++timer;        // record discovery time",
    "    for (int v : adj[u]) {",
    "        if (!vis[v]) dfsTimestamp(v, adj, vis);",
    "    }",
    "    finish[u] = ++timer;      // record finish time",
    "}",
    "",
    "// Edge classification in directed graph:",
    "// Tree edge:    disc[u] < disc[v] < finish[v] < finish[u]  (v unvisited when traversed)",
    "// Back edge:    disc[v] < disc[u] < finish[u] < finish[v]  (v is ancestor → CYCLE)",
    "// Forward edge: disc[u] < disc[v], finish[v] < finish[u]   (v is descendant)",
    "// Cross edge:   finish[v] < disc[u]                        (no ancestor relation)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 5 — CYCLE DETECTION
# ══════════════════════════════════════════════════════════════
story.append(Banner("5","DFS — Cycle Detection",RED,TEAL))
story.append(sp(1))

story.append(h2("5.1  Undirected Graph — Visited + Parent Check"))
story.append(body(
    "In an undirected graph, a cycle exists if DFS encounters a visited neighbour that is NOT the parent "
    "we came from. Pass the parent vertex to avoid treating the edge we just came from as a back-edge."
))
story.append(CppBlock([
    "bool hasCycleUndirected(int u, int parent,",
    "                         vector<vector<int>>& adj, vector<bool>& vis) {",
    "    vis[u] = true;",
    "    for (int v : adj[u]) {",
    "        if (!vis[v]) {",
    "            if (hasCycleUndirected(v, u, adj, vis)) return true;",
    "        } else if (v != parent) {",
    "            return true;   // visited neighbour that's not parent → cycle",
    "        }",
    "    }",
    "    return false;",
    "}",
    "",
    "bool containsCycle(vector<vector<int>>& adj) {",
    "    int n = adj.size();",
    "    vector<bool> vis(n, false);",
    "    for (int i = 0; i < n; i++)",
    "        if (!vis[i] && hasCycleUndirected(i, -1, adj, vis)) return true;",
    "    return false;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("5.2  Directed Graph — White/Grey/Black Colouring"))
story.append(body(
    "For directed graphs, we need 3 colours: <b>white</b> (unvisited), "
    "<b>grey</b> (in current DFS path / recursion stack), <b>black</b> (fully processed). "
    "A back-edge — encountering a grey node — indicates a cycle."
))
story.append(InfoBox([
    "0 = WHITE: not yet visited",
    "1 = GREY:  currently in the recursion stack (processing)",
    "2 = BLACK: fully processed (all descendants done)",
    "Cycle condition: DFS reaches a neighbour v where color[v] == GREY",
    "Why not just 'visited'? A visited-but-finished (BLACK) node in a directed graph",
    "does NOT create a cycle — the current path doesn't go through it.",
],title="🎨 3-Color DFS for Directed Graphs",color=RED,bg=RED_BG))
story.append(sp(0.5))
story.append(CppBlock([
    "// color: 0=white, 1=grey (in stack), 2=black (done)",
    "bool hasCycleDirected(int u, vector<vector<int>>& adj, vector<int>& color) {",
    "    color[u] = 1;   // grey: start processing",
    "    for (int v : adj[u]) {",
    "        if (color[v] == 1) return true;   // back-edge to grey = cycle",
    "        if (color[v] == 0) {",
    "            if (hasCycleDirected(v, adj, color)) return true;",
    "        }",
    "    }",
    "    color[u] = 2;   // black: finished",
    "    return false;",
    "}",
    "",
    "bool containsCycleDirected(vector<vector<int>>& adj) {",
    "    int n = adj.size();",
    "    vector<int> color(n, 0);",
    "    for (int i = 0; i < n; i++)",
    "        if (color[i] == 0 && hasCycleDirected(i, adj, color)) return true;",
    "    return false;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 6 — TOPOLOGICAL SORT
# ══════════════════════════════════════════════════════════════
story.append(Banner("6","Topological Sort",ORANGE,TEAL))
story.append(sp(1))

story.append(h2("6.1  What is Topological Sort?"))
story.append(body(
    "A <b>linear ordering</b> of vertices of a DAG such that for every directed edge u→v, "
    "vertex u appears before vertex v. Only possible for DAGs (no cycles). "
    "Used for: task scheduling, build systems, dependency resolution, course prerequisites."
))
story.append(sp(0.5))

story.append(h2("6.2  Kahn's Algorithm — BFS-based  (LC 207/210)"))
story.append(body(
    "Repeatedly remove vertices with in-degree 0 (no dependencies). "
    "After removing a vertex, decrement in-degree of its neighbours. "
    "If topological order contains all V vertices, graph is a DAG. Otherwise, cycle exists."
))
story.append(CppBlock([
    "// Kahn's Algorithm — O(V+E)",
    "vector<int> topoSort(int n, vector<vector<int>>& adj) {",
    "    vector<int> indegree(n, 0);",
    "    // Compute in-degree for all vertices",
    "    for (int u = 0; u < n; u++)",
    "        for (int v : adj[u]) indegree[v]++;",
    "    // Enqueue all vertices with in-degree 0",
    "    queue<int> q;",
    "    for (int i = 0; i < n; i++)",
    "        if (indegree[i] == 0) q.push(i);",
    "    vector<int> order;",
    "    while (!q.empty()) {",
    "        int u = q.front(); q.pop();",
    "        order.push_back(u);",
    "        for (int v : adj[u]) {",
    "            indegree[v]--;",
    "            if (indegree[v] == 0) q.push(v);",
    "        }",
    "    }",
    "    // If order.size() != n → cycle exists",
    "    return order;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("6.3  DFS-based Topological Sort"))
story.append(body(
    "In DFS: when a vertex finishes (all descendants processed), push to a stack. "
    "At the end, pop the stack — this gives topological order. "
    "Why? A vertex pushed first (finishes first) must come AFTER all its dependencies."
))
story.append(CppBlock([
    "void dfsTopoSort(int u, vector<vector<int>>& adj,",
    "                  vector<bool>& vis, stack<int>& st) {",
    "    vis[u] = true;",
    "    for (int v : adj[u])",
    "        if (!vis[v]) dfsTopoSort(v, adj, vis, st);",
    "    st.push(u);   // push AFTER all descendants are processed",
    "}",
    "",
    "vector<int> topoSortDFS(int n, vector<vector<int>>& adj) {",
    "    vector<bool> vis(n, false);",
    "    stack<int> st;",
    "    for (int i = 0; i < n; i++)",
    "        if (!vis[i]) dfsTopoSort(i, adj, vis, st);",
    "    vector<int> order;",
    "    while (!st.empty()) { order.push_back(st.top()); st.pop(); }",
    "    return order;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("6.4  Course Schedule I & II  (LC 207, 210)"))
story.append(CppBlock([
    "// LC 207 — Can finish all courses? (cycle detection in directed graph)",
    "bool canFinish(int numCourses, vector<vector<int>>& prereqs) {",
    "    vector<vector<int>> adj(numCourses);",
    "    for (auto& e : prereqs) adj[e[1]].push_back(e[0]);",
    "    // Use Kahn's: if topo order has all courses → no cycle",
    "    vector<int> indeg(numCourses,0);",
    "    for (int u=0;u<numCourses;u++) for (int v:adj[u]) indeg[v]++;",
    "    queue<int> q;",
    "    for (int i=0;i<numCourses;i++) if(indeg[i]==0) q.push(i);",
    "    int count=0;",
    "    while(!q.empty()){",
    "        int u=q.front();q.pop();count++;",
    "        for(int v:adj[u]) if(--indeg[v]==0) q.push(v);",
    "    }",
    "    return count==numCourses;",
    "}",
    "",
    "// LC 210 — Return one valid order (or empty if impossible)",
    "vector<int> findOrder(int n, vector<vector<int>>& prereqs) {",
    "    vector<vector<int>> adj(n);",
    "    vector<int> indeg(n,0);",
    "    for (auto& e : prereqs) { adj[e[1]].push_back(e[0]); indeg[e[0]]++; }",
    "    queue<int> q;",
    "    for(int i=0;i<n;i++) if(indeg[i]==0) q.push(i);",
    "    vector<int> order;",
    "    while(!q.empty()){",
    "        int u=q.front();q.pop(); order.push_back(u);",
    "        for(int v:adj[u]) if(--indeg[v]==0) q.push(v);",
    "    }",
    "    return order.size()==n ? order : vector<int>{};",
    "}",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 7 — CONNECTED COMPONENTS & SCC
# ══════════════════════════════════════════════════════════════
story.append(Banner("7","Connected Components, Bipartite & SCC",BLUE,TEAL))
story.append(sp(1))

story.append(h2("7.1  Connected Components  (LC 323)"))
story.append(CppBlock([
    "// Count connected components in undirected graph",
    "int countComponents(int n, vector<vector<int>>& edges) {",
    "    vector<vector<int>> adj(n);",
    "    for (auto& e : edges) {",
    "        adj[e[0]].push_back(e[1]);",
    "        adj[e[1]].push_back(e[0]);",
    "    }",
    "    vector<bool> vis(n, false);",
    "    int components = 0;",
    "    for (int i = 0; i < n; i++) {",
    "        if (!vis[i]) {",
    "            components++;",
    "            // BFS/DFS marks entire component",
    "            queue<int> q; vis[i]=true; q.push(i);",
    "            while(!q.empty()){",
    "                int u=q.front();q.pop();",
    "                for(int v:adj[u]) if(!vis[v]){vis[v]=true;q.push(v);}",
    "            }",
    "        }",
    "    }",
    "    return components;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("7.2  Bipartite Check  (LC 785)  — Medium"))
story.append(body(
    "A graph is bipartite iff it can be 2-coloured with no two adjacent vertices sharing a colour. "
    "Equivalently: it contains no odd-length cycle. Use BFS/DFS colouring."
))
story.append(CppBlock([
    "bool isBipartite(vector<vector<int>>& graph) {",
    "    int n = graph.size();",
    "    vector<int> color(n, -1);   // -1=unvisited, 0/1=colours",
    "    for (int start = 0; start < n; start++) {",
    "        if (color[start] != -1) continue;",
    "        queue<int> q;",
    "        color[start] = 0;",
    "        q.push(start);",
    "        while (!q.empty()) {",
    "            int u = q.front(); q.pop();",
    "            for (int v : graph[u]) {",
    "                if (color[v] == -1) {",
    "                    color[v] = 1 - color[u];  // opposite colour",
    "                    q.push(v);",
    "                } else if (color[v] == color[u]) {",
    "                    return false;   // same colour → not bipartite",
    "                }",
    "            }",
    "        }",
    "    }",
    "    return true;",
    "}",
    "// Time: O(V+E)   Space: O(V)",
]))
story.append(sp(0.8))

story.append(h2("7.3  Kosaraju's Algorithm — Strongly Connected Components"))
story.append(body(
    "An SCC is a maximal subgraph where every vertex is reachable from every other. "
    "Kosaraju's: (1) DFS on original graph, record finish order. "
    "(2) Transpose the graph. (3) DFS in reverse finish order on transposed graph — each DFS = one SCC."
))
story.append(CppBlock([
    "void dfs1(int u, vector<vector<int>>& adj,",
    "          vector<bool>& vis, stack<int>& st) {",
    "    vis[u] = true;",
    "    for (int v : adj[u]) if (!vis[v]) dfs1(v, adj, vis, st);",
    "    st.push(u);   // push after all descendants",
    "}",
    "void dfs2(int u, vector<vector<int>>& radj, vector<bool>& vis) {",
    "    vis[u] = true;",
    "    for (int v : radj[u]) if (!vis[v]) dfs2(v, radj, vis);",
    "}",
    "int kosaraju(int n, vector<vector<int>>& adj) {",
    "    // Step 1: DFS on original graph",
    "    vector<bool> vis(n, false); stack<int> st;",
    "    for (int i=0;i<n;i++) if(!vis[i]) dfs1(i,adj,vis,st);",
    "    // Step 2: Transpose graph",
    "    vector<vector<int>> radj(n);",
    "    for (int u=0;u<n;u++) for(int v:adj[u]) radj[v].push_back(u);",
    "    // Step 3: DFS on transposed in reverse finish order",
    "    fill(vis.begin(),vis.end(),false);",
    "    int scc=0;",
    "    while(!st.empty()){",
    "        int u=st.top();st.pop();",
    "        if(!vis[u]){scc++;dfs2(u,radj,vis);}",
    "    }",
    "    return scc;",
    "}",
    "// Time: O(V+E)   Space: O(V+E)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 8 — UNION-FIND
# ══════════════════════════════════════════════════════════════
story.append(Banner("8","Union-Find (Disjoint Set Union — DSU)",PURPLE,TEAL))
story.append(sp(1))

story.append(h2("8.1  Core Idea & Evolution"))
story.append(body(
    "Union-Find maintains a collection of <b>disjoint sets</b>. "
    "Two operations: <b>find(x)</b> — which set does x belong to? "
    "<b>union(x,y)</b> — merge the sets containing x and y. "
    "Optimisations: <b>path compression</b> (flatten tree on find) and "
    "<b>union by rank</b> (always attach smaller tree under larger). "
    "Together they give <b>nearly O(1) amortised</b> per operation — O(α(n)) where α is the inverse Ackermann function."
))
story.append(sp(0.5))

# Show union-find state
story.append(h3("State after union(0,1), union(2,3), union(1,2)"))
story.append(UnionFindViz(
    n=6, parent=[0,0,0,2,4,5], rank=[2,0,1,0,0,0],
    label="After merging: {0,1,2,3} in one component, {4} and {5} separate. Root of {0,1,2,3} = 0",
    color=PURPLE
))
story.append(sp(0.5))

story.append(h2("8.2  Full Optimised Implementation"))
story.append(CppBlock([
    "class UnionFind {",
    "    vector<int> parent, rank_;",
    "public:",
    "    UnionFind(int n) : parent(n), rank_(n, 0) {",
    "        iota(parent.begin(), parent.end(), 0);  // parent[i] = i",
    "    }",
    "    // Find with PATH COMPRESSION — O(α(n)) amortised",
    "    int find(int x) {",
    "        if (parent[x] != x)",
    "            parent[x] = find(parent[x]);  // path compression: flatten",
    "        return parent[x];",
    "    }",
    "    // Union by RANK — attach smaller tree under larger",
    "    bool unite(int x, int y) {",
    "        int rx = find(x), ry = find(y);",
    "        if (rx == ry) return false;   // already same set",
    "        if (rank_[rx] < rank_[ry]) swap(rx, ry);",
    "        parent[ry] = rx;              // attach ry under rx",
    "        if (rank_[rx] == rank_[ry]) rank_[rx]++;",
    "        return true;",
    "    }",
    "    bool connected(int x, int y) { return find(x) == find(y); }",
    "};",
    "// find: O(α(n)) ≈ O(1) amortised   unite: O(α(n))",
    "// α(n) < 5 for all practical n — effectively constant",
]))
story.append(sp(0.8))

story.append(h2("8.3  Union-Find with Size Tracking"))
story.append(CppBlock([
    "class UnionFindSz {",
    "    vector<int> parent, sz;",
    "    int components;",
    "public:",
    "    UnionFindSz(int n) : parent(n), sz(n,1), components(n) {",
    "        iota(parent.begin(), parent.end(), 0);",
    "    }",
    "    int find(int x) {",
    "        return parent[x]==x ? x : parent[x]=find(parent[x]);",
    "    }",
    "    bool unite(int x, int y) {",
    "        x=find(x); y=find(y);",
    "        if(x==y) return false;",
    "        if(sz[x]<sz[y]) swap(x,y);",
    "        parent[y]=x; sz[x]+=sz[y];  // attach smaller under larger",
    "        components--;",
    "        return true;",
    "    }",
    "    int size(int x)   { return sz[find(x)]; }",
    "    int numComponents() { return components; }",
    "    bool connected(int x,int y){ return find(x)==find(y); }",
    "};",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 9 — UNION-FIND PROBLEMS
# ══════════════════════════════════════════════════════════════
story.append(Banner("9","Union-Find — Classic Problems",PURPLE,TEAL))
story.append(sp(1))

story.append(h2("9.1  Redundant Connection  (LC 684)  — Medium"))
story.append(body(
    "Find the edge that, when removed, makes an undirected tree. "
    "Process edges in order: if both endpoints are already in the same component, "
    "this edge creates a cycle — it's the answer."
))
story.append(CppBlock([
    "vector<int> findRedundantConnection(vector<vector<int>>& edges) {",
    "    int n = edges.size();",
    "    UnionFind uf(n + 1);   // 1-indexed",
    "    for (auto& e : edges) {",
    "        if (!uf.unite(e[0], e[1]))",
    "            return e;   // already connected → this edge is redundant",
    "    }",
    "    return {};",
    "}",
    "// Time: O(n * α(n)) ≈ O(n)   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("9.2  Number of Provinces  (LC 547)  — Medium"))
story.append(CppBlock([
    "int findCircleNum(vector<vector<int>>& isConnected) {",
    "    int n = isConnected.size();",
    "    UnionFindSz uf(n);",
    "    for (int i = 0; i < n; i++)",
    "        for (int j = i+1; j < n; j++)",
    "            if (isConnected[i][j]) uf.unite(i, j);",
    "    return uf.numComponents();",
    "}",
    "// Time: O(n^2 * α(n))   Space: O(n)",
]))
story.append(sp(0.8))

story.append(h2("9.3  Accounts Merge  (LC 721)  — Medium"))
story.append(body(
    "Merge accounts sharing at least one email. "
    "Union-Find: map each email to its first-seen account index. "
    "If email already seen, union the two accounts. "
    "Finally, group all emails by their root account."
))
story.append(CppBlock([
    "vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {",
    "    int n = accounts.size();",
    "    UnionFind uf(n);",
    "    unordered_map<string, int> emailToAcc;",
    "    // Union accounts that share emails",
    "    for (int i = 0; i < n; i++) {",
    "        for (int j = 1; j < (int)accounts[i].size(); j++) {",
    "            string& email = accounts[i][j];",
    "            if (emailToAcc.count(email))",
    "                uf.unite(i, emailToAcc[email]);",
    "            else",
    "                emailToAcc[email] = i;",
    "        }",
    "    }",
    "    // Group emails by root account",
    "    unordered_map<int, set<string>> groups;",
    "    for (auto& [email, acc] : emailToAcc)",
    "        groups[uf.find(acc)].insert(email);",
    "    // Build result",
    "    vector<vector<string>> result;",
    "    for (auto& [root, emails] : groups) {",
    "        vector<string> merged = {accounts[root][0]};  // account name",
    "        merged.insert(merged.end(), emails.begin(), emails.end());",
    "        result.push_back(merged);",
    "    }",
    "    return result;",
    "}",
    "// Time: O(n*k*α(n))  k=avg emails per account   Space: O(n*k)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 10 — GRID PROBLEMS
# ══════════════════════════════════════════════════════════════
story.append(Banner("10","Grid Problems — BFS & DFS on 2D Arrays",GREEN,TEAL))
story.append(sp(1))

story.append(h2("10.1  4-Directional Grid Template"))
story.append(CppBlock([
    "// Standard 4-directional movement template",
    "int dr[] = {-1, 1, 0, 0};   // up, down, left, right",
    "int dc[] = {0, 0, -1, 1};",
    "",
    "// In-bounds check",
    "auto inBounds = [&](int r, int c) {",
    "    return r >= 0 && r < rows && c >= 0 && c < cols;",
    "};",
    "",
    "// 8-directional (including diagonals)",
    "int dr8[] = {-1,-1,-1,0,0,1,1,1};",
    "int dc8[] = {-1, 0, 1,-1,1,-1,0,1};",
]))
story.append(sp(0.8))

story.append(h2("10.2  Surrounded Regions  (LC 130)  — Medium"))
story.append(body(
    "Capture all 'O' regions not connected to the border. "
    "Key insight: instead of finding surrounded regions, find all 'O's connected to border "
    "(these are NOT surrounded) and mark them safe. Then flip the rest."
))
story.append(CppBlock([
    "void solve(vector<vector<char>>& board) {",
    "    int m = board.size(), n = board[0].size();",
    "    int dr[]={-1,1,0,0}, dc[]={0,0,-1,1};",
    "    // BFS from all border 'O's to find safe cells",
    "    queue<pair<int,int>> q;",
    "    for (int r=0;r<m;r++) for(int c:{0,n-1})",
    "        if(board[r][c]=='O'){board[r][c]='S';q.push({r,c});}",
    "    for (int c=0;c<n;c++) for(int r:{0,m-1})",
    "        if(board[r][c]=='O'){board[r][c]='S';q.push({r,c});}",
    "    while (!q.empty()) {",
    "        auto [r,c]=q.front();q.pop();",
    "        for(int d=0;d<4;d++){",
    "            int nr=r+dr[d],nc=c+dc[d];",
    "            if(nr>=0&&nr<m&&nc>=0&&nc<n&&board[nr][nc]=='O'){",
    "                board[nr][nc]='S'; q.push({nr,nc});",
    "            }",
    "        }",
    "    }",
    "    // Flip: 'O'→'X' (surrounded), 'S'→'O' (safe)",
    "    for(int r=0;r<m;r++) for(int c=0;c<n;c++)",
    "        board[r][c] = board[r][c]=='S' ? 'O' : 'X';",
    "}",
    "// Time: O(m*n)   Space: O(m*n)",
]))
story.append(sp(0.8))

story.append(h2("10.3  Pacific Atlantic Water Flow  (LC 417)  — Medium"))
story.append(body(
    "Find cells from which water can flow to BOTH Pacific and Atlantic oceans. "
    "Reverse approach: BFS from each ocean's border. "
    "A cell is in the answer if it's reachable from both oceans."
))
story.append(CppBlock([
    "vector<vector<int>> pacificAtlantic(vector<vector<int>>& h) {",
    "    int m=h.size(), n=h[0].size();",
    "    int dr[]={-1,1,0,0}, dc[]={0,0,-1,1};",
    "    auto bfs=[&](queue<pair<int,int>> q)->vector<vector<bool>>{",
    "        vector<vector<bool>> reach(m,vector<bool>(n,false));",
    "        while(!q.empty()){",
    "            auto[r,c]=q.front();q.pop();",
    "            reach[r][c]=true;",
    "            for(int d=0;d<4;d++){",
    "                int nr=r+dr[d],nc=c+dc[d];",
    "                if(nr>=0&&nr<m&&nc>=0&&nc<n&&!reach[nr][nc]",
    "                   &&h[nr][nc]>=h[r][c]){  // water flows UP in reverse",
    "                    reach[nr][nc]=true; q.push({nr,nc});",
    "                }",
    "            }",
    "        }",
    "        return reach;",
    "    };",
    "    queue<pair<int,int>> pac,atl;",
    "    for(int i=0;i<m;i++){pac.push({i,0});  atl.push({i,n-1});}",
    "    for(int j=0;j<n;j++){pac.push({0,j});  atl.push({m-1,j});}",
    "    auto rp=bfs(pac), ra=bfs(atl);",
    "    vector<vector<int>> res;",
    "    for(int r=0;r<m;r++) for(int c=0;c<n;c++)",
    "        if(rp[r][c]&&ra[r][c]) res.push_back({r,c});",
    "    return res;",
    "}",
    "// Time: O(m*n)   Space: O(m*n)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 11 — SHORTEST PATH
# ══════════════════════════════════════════════════════════════
story.append(Banner("11","Shortest Path Algorithms",RED,TEAL))
story.append(sp(1))

story.append(h2("11.1  Dijkstra's Algorithm — Weighted, Non-negative Edges"))
story.append(body(
    "Greedy shortest-path algorithm using a min-priority queue. "
    "At each step, extract the unvisited vertex with minimum tentative distance and relax its edges. "
    "<b>Does NOT work with negative edge weights.</b>"
))
story.append(CppBlock([
    "#include <queue>",
    "",
    "vector<int> dijkstra(int src, vector<vector<pair<int,int>>>& adj) {",
    "    int n = adj.size();",
    "    vector<int> dist(n, INT_MAX);",
    "    // min-heap: {distance, node}",
    "    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<>> pq;",
    "    dist[src] = 0;",
    "    pq.push({0, src});",
    "    while (!pq.empty()) {",
    "        auto [d, u] = pq.top(); pq.pop();",
    "        if (d > dist[u]) continue;   // stale entry — skip",
    "        for (auto [v, w] : adj[u]) {",
    "            if (dist[u] + w < dist[v]) {",
    "                dist[v] = dist[u] + w;",
    "                pq.push({dist[v], v});",
    "            }",
    "        }",
    "    }",
    "    return dist;   // dist[i] = shortest distance from src to i",
    "}",
    "// Time: O((V+E) log V)   Space: O(V)",
    "// LC 743 Network Delay Time, LC 1514 Path with Max Probability",
]))
story.append(sp(0.8))

story.append(h2("11.2  Bellman-Ford — Handles Negative Edges"))
story.append(body(
    "Relax ALL edges V-1 times. Each iteration guarantees shortest paths using at most k edges after k iterations. "
    "Run one more pass: if any distance still decreases → negative cycle detected."
))
story.append(CppBlock([
    "// Edge list format: {u, v, weight}",
    "vector<int> bellmanFord(int src, int n,",
    "                         vector<tuple<int,int,int>>& edges) {",
    "    vector<int> dist(n, INT_MAX);",
    "    dist[src] = 0;",
    "    // Relax all edges V-1 times",
    "    for (int iter = 0; iter < n-1; iter++) {",
    "        for (auto& [u, v, w] : edges) {",
    "            if (dist[u] != INT_MAX && dist[u]+w < dist[v])",
    "                dist[v] = dist[u]+w;",
    "        }",
    "    }",
    "    // Check for negative cycles",
    "    for (auto& [u, v, w] : edges)",
    "        if (dist[u] != INT_MAX && dist[u]+w < dist[v])",
    "            return {};   // negative cycle exists",
    "    return dist;",
    "}",
    "// Time: O(V*E)   Space: O(V)",
    "// LC 787 Cheapest Flights Within K Stops (Bellman-Ford with k iterations)",
]))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
#  SECTION 12 — CHEAT SHEET
# ══════════════════════════════════════════════════════════════
story.append(Banner("12","Complexity Cheat Sheet & LeetCode Map",NAVY,TEAL))
story.append(sp(1))

story.append(h2("12.1  Algorithm Complexity Summary"))
cx_data=[
    ["Algorithm",            "Time",          "Space",   "Key Condition / Notes"],
    ["BFS",                   "O(V+E)",        "O(V)",    "Shortest path (unweighted), level-order"],
    ["DFS",                   "O(V+E)",        "O(V)",    "Component detection, cycle, topo sort"],
    ["Multi-source BFS",      "O(V+E)",        "O(V)",    "Push all sources first"],
    ["0-1 BFS",               "O(V+E)",        "O(V)",    "Edge weights 0 or 1 only"],
    ["Topological Sort",      "O(V+E)",        "O(V)",    "DAG only (Kahn's or DFS post-order)"],
    ["Cycle Detection",       "O(V+E)",        "O(V)",    "3-colour for directed, parent for undirected"],
    ["SCC (Kosaraju)",        "O(V+E)",        "O(V+E)", "Two DFS passes + transpose"],
    ["Union-Find (optimised)","O(α(n)) each",  "O(n)",   "Path compression + union by rank"],
    ["Dijkstra",              "O((V+E) log V)","O(V)",   "Non-negative weights only"],
    ["Bellman-Ford",          "O(V*E)",        "O(V)",   "Handles negative weights, detects neg cycles"],
    ["Floyd-Warshall",        "O(V³)",         "O(V²)",  "All-pairs shortest path, dense graphs"],
    ["Prim's MST",            "O((V+E) log V)","O(V)",   "Min-heap based"],
    ["Kruskal's MST",         "O(E log E)",    "O(V)",   "Sort edges + Union-Find"],
]
cx_extra=[]
for i in range(1,len(cx_data)):
    v=cx_data[i][1]
    col=GREEN if "(V+E)" in v and "log" not in v else \
        (ORANGE if "log" in v else (RED if "V³" in v or "V*E" in v else DARK))
    cx_extra+=[("TEXTCOLOR",(1,i),(1,i),col),("FONTNAME",(1,i),(1,i),"Helvetica-Bold")]
story.append(mtbl(cx_data,[42*mm,30*mm,20*mm,76*mm],extra=cx_extra))
story.append(cap("Table 2: Graph algorithm complexities"))
story.append(sp(0.5))

story.append(h2("12.2  Algorithm Selection Guide"))
story.append(CppBlock([
    "/*",
    " * PROBLEM SIGNAL                           → ALGORITHM",
    " * ─────────────────────────────────────────────────────────────────────",
    " * Shortest path (unweighted graph)         → BFS",
    " * Shortest path (non-negative weights)     → Dijkstra",
    " * Shortest path (negative weights)         → Bellman-Ford",
    " * All-pairs shortest path                  → Floyd-Warshall",
    " * Minimum spanning tree                    → Prim's / Kruskal's + UF",
    " * Connected components                     → BFS/DFS or Union-Find",
    " * Cycle detection (undirected)             → DFS + parent, or UF",
    " * Cycle detection (directed)               → DFS 3-colour (white/grey/black)",
    " * Topological ordering                     → Kahn's BFS or DFS post-order",
    " * Strongly connected components            → Kosaraju / Tarjan",
    " * Bipartite check                          → BFS/DFS 2-colouring",
    " * Dynamic connectivity (online merges)     → Union-Find",
    " * Grid flood fill / island count           → BFS/DFS 4-directional",
    " * Shortest path with exactly k edges       → Bellman-Ford k iterations",
    " * Path with maximum probability            → Dijkstra (negate log probs)",
    " * Articulation points & bridges            → Tarjan DFS low-link values",
    " */",
]))
story.append(sp(0.5))

story.append(h2("12.3  Complete LeetCode Problem Map"))
lc_data=[
    ["#",   "Problem",                                   "Algorithm",                  "Diff"],
    ["127", "Word Ladder",                                "BFS word graph",             "Hard"],
    ["130", "Surrounded Regions",                         "BFS from border",            "Medium"],
    ["200", "Number of Islands",                          "BFS/DFS grid",               "Medium"],
    ["207", "Course Schedule",                            "Kahn's topo sort",           "Medium"],
    ["210", "Course Schedule II",                         "Kahn's topo sort",           "Medium"],
    ["261", "Graph Valid Tree",                           "Union-Find / DFS",           "Medium"],
    ["269", "Alien Dictionary",                           "Topo sort BFS",              "Hard"],
    ["286", "Walls and Gates",                            "Multi-source BFS",           "Medium"],
    ["310", "Minimum Height Trees",                       "Topo sort (trim leaves)",    "Medium"],
    ["323", "Number of Connected Components",             "DFS / Union-Find",           "Medium"],
    ["399", "Evaluate Division",                          "BFS weighted graph",         "Medium"],
    ["417", "Pacific Atlantic Water Flow",                "BFS from both oceans",       "Medium"],
    ["433", "Minimum Genetic Mutation",                   "BFS",                        "Medium"],
    ["547", "Number of Provinces",                        "DFS / Union-Find",           "Medium"],
    ["684", "Redundant Connection",                       "Union-Find cycle detect",    "Medium"],
    ["695", "Max Area of Island",                         "DFS grid",                   "Medium"],
    ["721", "Accounts Merge",                             "Union-Find + HashMap",       "Medium"],
    ["743", "Network Delay Time",                         "Dijkstra",                   "Medium"],
    ["785", "Is Graph Bipartite?",                        "BFS 2-colouring",            "Medium"],
    ["787", "Cheapest Flights Within K Stops",            "Bellman-Ford k iters",       "Medium"],
    ["802", "Find Eventual Safe States",                  "DFS / Kahn's reverse",       "Medium"],
    ["994", "Rotting Oranges",                            "Multi-source BFS",           "Medium"],
    ["1091","Shortest Path in Binary Matrix",             "BFS",                        "Medium"],
    ["1202","Smallest String With Swaps",                 "Union-Find groups",          "Medium"],
    ["1319","Number of Operations to Connect Network",    "Union-Find",                 "Medium"],
    ["1584","Min Cost to Connect All Points",             "Kruskal / Prim MST",         "Medium"],
    ["1631","Path With Minimum Effort",                   "Dijkstra / Binary Search",   "Medium"],
]
dc={"Easy":GREEN,"Medium":ORANGE,"Hard":RED}
le=[]
for i,r in enumerate(lc_data[1:],1):
    col=dc.get(r[3],DARK)
    le+=[("TEXTCOLOR",(3,i),(3,i),col),("FONTNAME",(3,i),(3,i),"Helvetica-Bold")]
story.append(mtbl(lc_data,[13*mm,70*mm,50*mm,15*mm],extra=le))
story.append(cap("Table 3: 26 LeetCode problems — Graphs: BFS, DFS & Union-Find"))
story.append(sp(0.8))

story.append(InfoBox([
    "1.  BFS = shortest path in unweighted graphs. DFS = deep exploration, cycle, topo, components.",
    "2.  Always mark visited BEFORE enqueuing in BFS (not after dequeuing) to prevent duplicates.",
    "3.  For directed cycle detection: use 3-colours (white/grey/black). Grey = currently in stack = cycle.",
    "4.  Topological sort only works on DAGs. Kahn's detects cycles: if output size < V → cycle exists.",
    "5.  Union-Find: path compression + union by rank → O(α(n)) per operation — essentially O(1).",
    "6.  Dijkstra requires non-negative weights. Negative weights → Bellman-Ford.",
    "7.  Multi-source BFS: push ALL sources initially. BFS naturally computes dist from nearest source.",
    "8.  0-1 BFS: weight=0 → push_front (deque), weight=1 → push_back. O(V+E) vs O((V+E) log V).",
    "9.  Grid problems: store visited state IN the grid (mark as visited) to save O(m*n) extra space.",
    "10. SCC: Kosaraju needs two DFS passes + graph transpose. Simpler: check if reverse graph agrees.",
],title="🏆 Golden Rules — Graphs: BFS, DFS & Union-Find",color=NAVY,bg=LIGHT))

# ── BUILD ───────────────────────────────────────────────────────
out = "DSA_Notes_Graphs_BFS_DFS_UnionFind.pdf"
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=34*mm, bottomMargin=18*mm,
    title="DSA Notes — Graphs: BFS, DFS & Union-Find",
    author="DSA Revision Planner",
    subject="Complete Graph BFS DFS Union-Find Notes with C++",
)
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"\n✅  Done!  →  {out}")
print(f"   Open the PDF in the same folder where you ran this script.")