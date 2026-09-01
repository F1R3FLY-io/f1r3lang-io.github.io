import math, random
random.seed(20260828)
CX = CY = 500.0
P = []
def pt(r,a):
    ar = math.radians(a); return (CX + r*math.cos(ar), CY + r*math.sin(ar))

def pane(r0,r1,a0,a1,fill,op=1.0):
    x0,y0 = pt(r1,a0); x1,y1 = pt(r1,a1); x2,y2 = pt(r0,a1); x3,y3 = pt(r0,a0)
    lg = 1 if (a1-a0) % 360 > 180 else 0
    P.append(f'<path d="M{x0:.1f} {y0:.1f}A{r1:.1f} {r1:.1f} 0 {lg} 1 {x1:.1f} {y1:.1f}'
             f'L{x2:.1f} {y2:.1f}A{r0:.1f} {r0:.1f} 0 {lg} 0 {x3:.1f} {y3:.1f}Z"'
             f' fill="{fill}"' + (f' opacity="{op:.2f}"' if op<1 else '') + '/>')

def glass(r0,r1,approx_n,cols,splits=(1,2,3),wobble=.45,opr=(.72,1.0),start=0.0):
    """irregular subdivision: uneven wedge widths, uneven radial splits"""
    widths=[]; base=360.0/approx_n
    while True:
        widths.append(base*random.uniform(1-wobble,1+wobble))
        if sum(widths) >= 360: break
    s=360.0/sum(widths); widths=[w*s for w in widths]
    a=start
    for w in widths:
        a0,a1=a,a+w; a=a1
        k=random.choice(splits)
        cuts=[r0]+sorted(random.uniform(r0,r1) for _ in range(k-1))+[r1]
        cuts=[c+random.uniform(-2.5,2.5) for c in cuts]; cuts[0]=r0; cuts[-1]=r1
        for i in range(len(cuts)-1):
            if cuts[i+1]-cuts[i] < 7: continue
            pane(cuts[i],cuts[i+1],a0+.5,a1-.5,random.choice(cols),random.uniform(*opr))

def node(r,a,rad=3.2):
    x,y=pt(r,a); P.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="var(--lead)"/>')

STONE   = ["#1b1d21","#232529","#15171a","#2a2c30","#191b1f"]
STONE_HI= ["#33363b","#3b3e44"]
MATTER  = ["#2c4459","#365269","#22384a","#40607a","#294a5e","#1e3243","#375b6f","#4a6f86"]
MATTER_HI=["#5b829a","#6d94aa","#7ba3b8"]
LIFE    = ["#2f6b57","#3d7f5e","#275b52","#4a8f66","#356e63","#1f4f47","#437f72","#54996f"]
LIFE_HI = ["#7cb489","#8fc79a","#a3d4ab"]
MIND    = ["#b8861f","#d0a02c","#9e701a","#e0b845","#c79127","#a97d1d","#8f6415"]
MIND_HI = ["#f2d891","#f7e6b8","#ffefc6"]
EMBER   = ["#8c2a24","#a33a2c","#6e1f1b"]

# ---- stone frame ----------------------------------------------------------
glass(470,500,58,STONE,splits=(1,),wobble=.3,opr=(.92,1.0))
for _ in range(14):
    a=random.uniform(0,360); pane(472,498,a,a+random.uniform(2,4.5),random.choice(STONE_HI),random.uniform(.5,.8))
frame="".join(P); P.clear()

# ---- MATTER ---------------------------------------------------------------
glass(408,468,30,MATTER,splits=(2,3),wobble=.5)
for _ in range(11):
    a=random.uniform(0,360); pane(412+random.uniform(0,26),442+random.uniform(0,24),a,a+random.uniform(2.5,5),random.choice(MATTER_HI),random.uniform(.45,.8))
for i in range(30): node(438,i*12+random.uniform(-3,3),2.6)
matter="".join(P); P.clear()

# ---- threshold I: matter weaving into life --------------------------------
n=76; st=360.0/n
for i in range(n):
    t=(i%9)/8.0
    pane(382,404,i*st+.5,(i+1)*st-.5,random.choice(MATTER if t<.5 else LIFE),.55+.35*abs(t-.5))
thr1="".join(P); P.clear()

# ---- LIFE -----------------------------------------------------------------
glass(304,378,26,LIFE,splits=(2,3),wobble=.5)
for _ in range(9):
    a=random.uniform(0,360); pane(308+random.uniform(0,22),340+random.uniform(0,26),a,a+random.uniform(3,6),random.choice(LIFE_HI),random.uniform(.4,.75))
# gametes: paired forms meeting at a lead node and exchanging what they carry
for i in range(11):
    a=i*(360/11)+9
    for s in (-1,1):
        x1,y1=pt(341,a+s*8.5); x2,y2=pt(374,a+s*1.6); x3,y3=pt(341,a+s*0.7); x4,y4=pt(311,a+s*5.0)
        P.append(f'<path d="M{x1:.1f} {y1:.1f}Q{x2:.1f} {y2:.1f} {x3:.1f} {y3:.1f}'
                 f'Q{x4:.1f} {y4:.1f} {x1:.1f} {y1:.1f}Z" fill="{random.choice(LIFE_HI)}" opacity="0.62"/>')
    node(341,a,4.6)
life="".join(P); P.clear()

# ---- threshold II ---------------------------------------------------------
n=62; st=360.0/n
for i in range(n):
    t=(i%7)/6.0
    pane(268,300,i*st+.6,(i+1)*st-.6,random.choice(LIFE if t<.5 else MIND),.55+.35*abs(t-.5))
thr2="".join(P); P.clear()

# ---- MIND: radiating light, broken into glass-sized pieces ----------------
n=30; st=360.0/n
for i in range(n):
    a0,a1=i*st,(i+1)*st
    lead = (i%2==0)
    r_in = 68 if lead else 104
    cuts=[r_in,r_in+random.uniform(30,48)]
    while cuts[-1] < 176: cuts.append(cuts[-1]+random.uniform(30,46))
    cuts.append(200)
    for j in range(len(cuts)-1):
        if cuts[j+1]-cuts[j] < 9: continue
        col = random.choice(MIND_HI) if (lead and j%3==1) else random.choice(MIND)
        pane(cuts[j],cuts[j+1],a0+1.1,a1-1.1,col,random.uniform(.7,1.0))
    if not lead:
        pane(104,200,a0+3.4,a1-3.4,random.choice(EMBER),random.uniform(.18,.34))
for i in range(n): node(200,i*st,2.6)
mind="".join(P); P.clear()

# ---- SERPENT: dark glass, coiled around the light, taking its own tail -----
RS, W0, W1 = 230.0, 52.0, 18.0
A_HEAD, A_TAIL = 40.0, 392.0
BODY  = ["#1c2028","#242833","#171a21","#2b3040","#1f242e","#20252f"]
SHEEN = ["#4a4360","#6b5a3f","#3d4a52"]
segs = 140
def spiral(t): return RS + 7.0*math.sin(t*math.pi*2.4) - 14.0*t
for i in range(segs):                                   # dark under-body
    t=i/(segs-1.0); t2=(i+1)/(segs-1.0)
    a0=A_HEAD+t*(A_TAIL-A_HEAD); a1=A_HEAD+t2*(A_TAIL-A_HEAD)
    w=(W0*(1-t**1.3)+W1*(t**1.3))+9; rm=spiral(t)
    pane(rm-w/2, rm+w/2, a0, a1+.6, "#0a0c10", 1.0)
for i in range(segs):
    t=i/(segs-1.0); t2=(i+1)/(segs-1.0)
    a0=A_HEAD+t*(A_TAIL-A_HEAD); a1=A_HEAD+t2*(A_TAIL-A_HEAD)
    w=W0*(1-t**1.3)+W1*(t**1.3); rm=spiral(t)
    pane(rm-w/2, rm+w/2, a0, a1+.45, BODY[i%6], 1.0)
    for row,frac in ((0,-0.28),(1,0.02),(2,0.30)):      # staggered scales
        if (i+row)%3: continue
        rr=rm+w*frac; sw=w*0.32
        pane(rr-sw/2, rr+sw/2, a0+.3, a1+.2, SHEEN[row], [0.42,0.30,0.24][row])
tx,ty=pt(spiral(1.0), A_TAIL-3)
P.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="9" fill="#171a21"/>')
hx,hy=pt(RS+4, A_HEAD+5)
P.append(
  f'<g transform="translate({hx:.1f} {hy:.1f}) rotate({A_HEAD-92:.1f}) scale(1.34)">'
  f'<path d="M-82 -22 C-70 -54 -10 -62 34 -40 L66 -22 L24 -9 L-48 -7 Z" fill="#242833"/>'
  f'<path d="M-48 7 L22 9 L64 22 L32 37 C-8 39 -40 26 -52 13 Z" fill="#1c2028"/>'
  f'<path d="M24 -9 L64 -22 L62 21 L22 9 Z" fill="#8c2a24"/>'
  f'<path d="M40 -14 L58 -19 L57 6 L40 2 Z" fill="#c9a24a" opacity=".5"/>'
  f'<path d="M-74 -24 C-60 -48 -22 -54 6 -43 L12 -16 L-56 -14 Z" fill="#4a4360" opacity=".45"/>'
  f'<circle cx="-34" cy="-26" r="11.5" fill="#f7e6b8"/>'
  f'<ellipse cx="-34" cy="-26" rx="3.4" ry="9.5" fill="var(--lead)"/>'
  f'</g>')
serpent="".join(P); P.clear()

# ---- MEDALLION: the fixed point, the window inside the window -------------
glass(58,74,14,MIND,splits=(1,),wobble=.25,opr=(.8,1.0))
for i,(r0,r1,cnt,cols) in enumerate(((40,56,10,MATTER),(22,38,8,LIFE),(8,20,8,MIND_HI))):
    st=360.0/cnt
    for j in range(cnt):
        pane(r0,r1,j*st+1.4,(j+1)*st-1.4,random.choice(cols),.92)
P.append(f'<circle cx="{CX}" cy="{CY}" r="6.5" fill="#fff6dd"/>')
medallion="".join(P); P.clear()

# ---- fireflies ------------------------------------------------------------
ff="".join(
    f'<circle class="ff" cx="{pt(random.uniform(412,464),random.uniform(0,360))[0]:.1f}" '
    f'cy="{CY + (lambda a,r: r*math.sin(math.radians(a)))(0,0):.1f}" r="0"/>' for _ in range(0))
ffl=[]
for _ in range(18):
    a=random.uniform(0,360); r=random.uniform(412,464); x,y=pt(r,a)
    ffl.append(f'<circle class="ff" cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(2.6,4.4):.1f}"/>')
fireflies="".join(ffl)

svg=f'''<svg id="window" viewBox="0 0 1000 1000" role="img" aria-labelledby="win-t win-d" preserveAspectRatio="xMidYMid meet">
<title id="win-t">The Reflection Window</title>
<desc id="win-d">A stained-glass roundel in three concentric rings. Cold mineral shards for matter on the outside, cellular green forms that meet in pairs for life, and radiating gold light for mind at the centre. A serpent coils between life and mind and takes its own tail, and inside its coil a small medallion repeats the whole window again.</desc>
<defs>
<radialGradient id="corelight" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#ffeec2" stop-opacity=".92"/>
<stop offset="58%" stop-color="#f0c866" stop-opacity=".44"/>
<stop offset="100%" stop-color="#e0b845" stop-opacity="0"/>
</radialGradient>
<radialGradient id="lightfall" cx="50%" cy="44%" r="64%">
<stop offset="0%" stop-color="#fff6dd" stop-opacity=".30"/>
<stop offset="46%" stop-color="#ffe9b4" stop-opacity=".10"/>
<stop offset="100%" stop-color="#000" stop-opacity="0"/>
</radialGradient>
<clipPath id="disc"><circle cx="500" cy="500" r="500"/></clipPath>
</defs>
<g clip-path="url(#disc)" class="leaded">
<g id="ring-frame">{frame}</g>
<g id="ring-matter" class="ring">{matter}{thr1}{fireflies}</g>
<g id="ring-life" class="ring">{life}{thr2}</g>
<g id="ring-mind" class="ring">
<circle cx="500" cy="500" r="300" fill="url(#corelight)" class="corelight"/>
{mind}{serpent}{medallion}</g>
<circle cx="500" cy="500" r="500" fill="url(#lightfall)" class="lightfall"/>
</g>
</svg>'''
open("window.svg","w").write(svg)
print("paths:",svg.count("<path"),"bytes:",len(svg))
