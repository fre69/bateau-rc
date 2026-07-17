# -*- coding: utf-8 -*-
# Catamaran RC a helices aeriennes -- generateur parametrique v2
# Recup Nikko N-Blaster : 2 moteurs brosses (skid-steer), carte RC 27/40 MHz tout-ou-rien.
# Usage : python generate_pieces.py   ->  stl/*.stl + stl/_assemblage/ + apercu_catamaran.png
import os, math, shutil, subprocess
import numpy as np, trimesh, mapbox_earcut
from trimesh.creation import box, cylinder, extrude_polygon, icosphere, revolve
from shapely.geometry import Polygon, LineString

HERE = os.path.dirname(os.path.abspath(__file__))
STL  = os.path.join(HERE, "stl")
ASM  = os.path.join(STL, "_assemblage")
os.makedirs(STL, exist_ok=True)

RX = trimesh.transformations.rotation_matrix
TR = trimesh.transformations.translation_matrix
U, D, I = trimesh.boolean.union, trimesh.boolean.difference, trimesh.boolean.intersection

# ---------------------------------------------------------------- parametres
L      = 300.0   # longueur coque
SY     = 55.5    # axe d'un sponson (entraxe 111)
BS     = 32.5    # demi-largeur max d'un sponson
CH     = 20.0    # hauteur de bouchain
CFL    = 2.5     # meplat de bouchain (spray-rail) -- s'efface vers l'etrave
FL     = 6.0     # debord du livet (flare) -- s'efface vers l'etrave
T      = 1.6     # paroi (4 perimetres)
XJ     = 95.0    # etraves separees en avant de XJ
SH_AFT = 82.0    # livet au tableau
SH_BOW = 94.0    # livet a l'etrave (tonture classique : haut devant)
STEMH  = 74.0    # hauteur de l'etrave inclinee
XSTEM  = 66.0    # l'etrave rejoint la quille a x=XSTEM
ARCH   = 11.0    # cambrure du plafond de tunnel
DKT    = 2.2     # epaisseur du pont
CRN    = 5.0     # bouge du pont
LIP    = 6.0     # levre d'emboitement du pont
M3     = 3.4

HX, HA, HB    = 155.0, 54.0, 36.0   # ecoutille : centre + demi-axes (108x72)
FA, FB        = 76.0, 58.0          # bride du capot (demi-axes)
SEATA, SEATB  = 78.0, 59.5          # plinthe cockpit (demi-axes, deborde la bride du capot)
Z0SEAT, KSEAT = 93.7, -0.037        # plan de la plinthe : z = Z0SEAT + KSEAT*(x-HX)
SCRX, SCRY    = 52.0, 34.0          # vis du capot (sur la bride ET sur la plinthe)
CANH          = 26.0                # hauteur de la capsule

PYX, PYY  = 240.0, 66.0             # pylones : position x, ecartement y des helices
ZMOUNT    = 88.5                    # plan de montage commun pylones + anneaux
MOT_Z     = 76.0                    # axe moteur au-dessus de ZMOUNT
SADDLE_ID = 32.4                    # berceau moteur (bague 24 mm : corps moteur Ø24)
NAC_R, NAC_L, NAC_X = 19.0, 36.0, 10.0  # nacelle : rayon, longueur, decalage x local
# --- accouplement helice sur le pignon metallique CONSERVE sur l'axe (broche a froid) ---
PIGN_D  = 7.0     # diametre exterieur du pignon (mesure ~7 mm au pied a coulisse)
PIGN_L  = 8.0     # longueur du pignon le long de l'axe (mesure)
GRIP_I  = 0.6     # interference de broche : alesage = PIGN_D-GRIP_I, dents mordent GRIP_I/2 au rayon
SHAFT_D = 2.3     # arbre nu (sert de pilote de centrage / trou d'ejection)
HOUS_L  = 14.0    # longueur de la coiffe arriere-moteur (bloc 30 mm + deparasitage ~5 mm = 35 mm total)
GDX, GFY  = 275.0, 16.0             # anneaux : centre x, demi-ecart des pieds (16 : pas plus,
                                    # sinon les bossages exterieurs percutent la muraille)
WIREX, WIREY = 254.0, 22.0          # passe-fils dans le pont

# ---------------------------------------------------- etanchement de l'etrave (piege n.16)
# La cuve s'ouvre des x=22 (XNi) alors que le pont v2 ne commencait qu'a x=26 -> trou de
# 4 mm en travers de chaque etrave (+ 0.9 mm a l'arriere). Deux facons de le traiter :
#
#   BOW_PATCH = True   RUSTINE -- geometrie du bateau DEJA IMPRIME (juillet 2026).
#                      Pont court (26 -> 296.5) + 2 bouchons TPU rapportes (piece 11).
#                      Ne PAS toucher tant qu'on veut des STL compatibles avec ces coques.
#
#   BOW_PATCH = False  CORRECTIF -- pour une NOUVELLE impression complete.
#                      Pont rallonge (22.3 -> 297.1) : il couvre toute la cuve, avec le
#                      meme jeu de collage de 0.3 mm au bout qu'il a deja sur les cotes.
#                      Pas de bouchons -- ils entreraient en collision.
BOW_PATCH  = True
XPL0, XPL1 = 22.0, 26.0             # le trou : debut de la cavite -> debut du pont v2
XPLC       = 20.0                   # la collerette deborde vers l'avant sur l'etrave PLEINE
PLD        = 4.0                    # profondeur du teton dans la cuve
PLCAP      = 1.4                    # collerette : affleure le nez du pont (93.23 vs 93.24)
PLW        = 1.2                    # debord de la collerette sur le livet (livet = T = 1.6)
PLGAP      = 0.3                    # JEU de montage. La v2.1 sortait un booleen sur la cavite,
                                    # donc un ajustement EXACT : ca ne tenait que parce que la
                                    # piece etait en TPU cense absorber. Elle est en PETG (soudable,
                                    # comme la coque) -> il FAUT un jeu reel. 0.3 par face, comble
                                    # a la soudure au fer + filament PETG.
XD0 = XPL1 if BOW_PATCH else XPL0 + 0.3        # debut du pont
XD1 = 296.5 if BOW_PATCH else L - 2.6 - 0.3    # fin du pont (cavite = L-2.6)

# ------------------------------------------ cloison d'etrave a XJ (piege n.18)
# A XJ, les etraves separees rejoignent la section a tunnel. XA (enveloppe) ET XAi (cavite)
# demarrent tous deux exactement a XJ -> la soustraction ne laisse AUCUNE cloison sur la face
# avant du pont-bras : le compartiment est ouvert plein nez (5 cm2, verifie au lance-rayons).
# Meme bug que le piege n.16 : deux lofts qui demarrent au meme x, l'un soustrait de l'autre.
# Piece rapportee, COLLEE en meme temps que le pont (elle est structurelle et etanche).
BKX0, BKX1 = 95.0, 110.0            # travee de la cloison, de XJ vers l'arriere.
                                    # 15 mm et pas 4 : ce n'est pas la largeur qui manquait mais
                                    # l'aire collee. 979 mm2 sur l'arche contre 259 a 4 mm, pour
                                    # 8 g de plus -- et elle S'ASSOIT sur l'arche au lieu de tenir
                                    # sur un chant. Son dos ressort sous l'ecoutille : inspectable.
                                    # Ne PAS l'elargir a travers les sponsons : ca fermerait
                                    # l'etrave, toute infiltration y serait piegee et invidangeable.
BKGAP      = 0.3                    # jeu lateral pour le cordon de colle.
                                    # La demi-largeur N'EST PAS constante : le tunnel se retrecit
                                    # vers l'arriere (30.41 a x=95, 28.6 a x=110). Une valeur figee
                                    # deborde dans les sponsons et fait pousser deux pattes jusqu'a
                                    # la quille -> la cloison SUIT yi_cav(x). Verifier la bbox : ~16
                                    # mm de haut, pas 66.

# ------------------------------------------------------------------- profils
def sheer(x):   # tonture : haute a l'etrave, creuse, plate a l'arriere
    return SH_AFT + (SH_BOW-SH_AFT)*(1.0-x/L)**2.2

def keelz(x):   # etrave inclinee puis fond plat (flotteur planant)
    return STEMH*((XSTEM-x)/XSTEM)**1.5 if x < XSTEM else 0.0

def bsx(x):     # plan : entree fine, maitre-bau a 0.62L, leger retrecissement arriere
    xi = x/L
    w = (1.0-(1.0-xi/0.62)**2)**0.72 if xi < 0.62 else 1.0-0.10*((xi-0.62)/0.38)**2
    return max(BS*w, 1.6)

def tunz(x):    # plafond de tunnel : haut a l'entree, bas au tableau
    return 58.0 + 12.0*(1.0-(x-XJ)/(L-XJ)) if x >= XJ else 70.0

def fl_eff(x):   # le flare s'efface vers la pointe -> etraves fines
    return FL*(0.30+0.70*min(1.0, x/70.0))

def cfl_eff(x):  # le spray-rail aussi
    return CFL*min(1.0, x/55.0)

def crown(y, ye):
    return CRN*(1.0-min(abs(y)/ye, 1.0)**2)**1.2

def seat_z(x):  # plan incline de la plinthe cockpit
    return Z0SEAT + KSEAT*(x-HX)

def seg(p, q, n):
    return [(p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t) for t in np.linspace(0, 1, n)[1:]]

# ------------------------------------------------------------------ sections
def side_out(sh, kz, yo, ye, sg, detail, CH, x):
    """muraille exterieure d'un sponson, du livet au bouchain, cote sg=+1/-1.
    detail=True : liston + spray-rail. Renvoie la liste de points (descendante)."""
    yc = yo + cfl_eff(x)
    lst = min(1.4, 0.3+0.25*(ye-yo))
    p = []
    if detail:
        p += [(sg*(ye+lst), sh-1.2), (sg*(ye+lst), sh-4.2), (sg*ye, sh-5.8)]
        p += seg((sg*ye, sh-5.8), (sg*yc, kz+CH+1.2), 7)
        p += [(sg*yc, kz+CH), (sg*yo, kz+CH)]
    else:
        p += seg((sg*ye, sh), (sg*yo, kz+CH), 9)
    return p

def ch_eff(x):  # pres de l'etrave la quille remonte : le bouchain doit rester sous le liston
    return min(CH, 0.42*(sheer(x)-keelz(x)))

def sect_full(x, o=0.0, raise_top=False, detail=True):
    bs = max(bsx(x)-o, 0.6); kz = keelz(x)+1.25*o; sh = sheer(x); CH = ch_eff(x)
    yi, yo = SY-bs, SY+bs; ye = yo+fl_eff(x)   # bs porte deja l'offset o : ne pas re-soustraire
    tz = tunz(x)+1.05*o
    arch = lambda y: tz + ARCH*(1.0-(y/yi)**2)
    top = sh+30.0 if raise_top else sh
    p = [(ye, top)]
    if raise_top: p += [(ye, sh)]                       # montant vertical (piege n.2)
    p += side_out(sh, kz, yo, ye, +1, detail, CH, x)
    p += [(SY+bs*u, kz+CH*abs(u)**1.5) for u in np.linspace(1, -1, 20)][1:]
    p += seg((yi, kz+CH), (yi, arch(yi)), 5)
    p += [(y, arch(y)) for y in np.linspace(yi, -yi, 16)][1:]
    p += seg((-yi, arch(yi)), (-yi, kz+CH), 5)
    p += [(-SY+bs*u, kz+CH*abs(u)**1.5) for u in np.linspace(1, -1, 20)][1:]
    p += list(reversed(side_out(sh, kz, yo, ye, -1, detail, CH, x)))[1:]
    p += [(-ye, sh)]
    if raise_top: p += [(-ye, top)]
    p += seg((-ye, top), (ye, top), 18)[:-1]
    return [(x, y, z) for y, z in p]

def sect_nose(x, o=0.0, raise_top=False, detail=True):
    bs = max(bsx(x)-o, 0.6); kz = keelz(x)+1.25*o; sh = sheer(x); CH = ch_eff(x)
    yi, yo = SY-bs, SY+bs; ye = yo+fl_eff(x)   # idem : un seul offset
    top = sh+30.0 if raise_top else sh
    p = [(yi, top)]
    if raise_top: p += [(yi, sh)]
    p += seg((yi, sh), (yi, kz+CH), 8)
    p += [(SY+bs*u, kz+CH*abs(u)**1.5) for u in np.linspace(-1, 1, 20)][1:]
    p += list(reversed(side_out(sh, kz, yo, ye, +1, detail, CH, x)))[1:]
    p += [(ye, sh)]
    if raise_top: p += [(ye, top)]
    p += seg((ye, top), (yi, top), 10)[:-1]
    return [(x, y, z) for y, z in p]

def loft(secs):
    S = [np.asarray(s, float) for s in secs]; n, m = len(S[0]), len(S)
    V = np.vstack(S); F = []
    for i in range(m-1):
        a, b = i*n, (i+1)*n
        for j in range(n):
            k = (j+1) % n; F.append([a+j, a+k, b+j]); F.append([a+k, b+k, b+j])
    # bouchons : earcut, PAS un eventail depuis le centroide -- sur une section
    # concave (tunnel, raise_top, levre du pont) l'eventail s'auto-intersecte et
    # manifold ressort du bruit sur toute la derniere travee (parois trouees au slicing)
    for idx, sg in ((0, -1), (m-1, 1)):
        base = idx*n; sec = S[idx]
        ax = int(np.argmin(np.ptp(sec, axis=0)))     # axe constant de la section
        u, v = (ax+1) % 3, (ax+2) % 3                # ordre cyclique : CCW en (u,v) = normale +ax
        ring = np.ascontiguousarray(sec[:, (u, v)])
        tris = mapbox_earcut.triangulate_float64(ring, np.array([n], dtype=np.uint32)).reshape(-1, 3)
        for t in tris:
            p = ring[t]
            ccw = (p[1,0]-p[0,0])*(p[2,1]-p[0,1]) - (p[1,1]-p[0,1])*(p[2,0]-p[0,0]) > 0
            F.append(list(base+t) if ccw == (sg > 0) else list(base+t[::-1]))
    mm = trimesh.Trimesh(vertices=V, faces=np.array(F), process=True)
    mm.fix_normals(); return mm

XN  = np.linspace(2, XJ, 26);  XA  = np.concatenate([np.linspace(XJ, 150, 12), np.linspace(155, L, 22)])
XNi = np.linspace(22, XJ, 22); XAi = np.concatenate([np.linspace(XJ, 150, 12), np.linspace(155, L-2.6, 20)])

def solid(o=0.0, raise_top=False, detail=True):
    xn, xa = (XN, XA) if o == 0 else (XNi, XAi)
    nose = loft([sect_nose(x, o, raise_top, detail) for x in xn])
    n2 = nose.copy(); n2.apply_scale([1, -1, 1]); n2.fix_normals()   # piege n.6
    aft = loft([sect_full(x, o, raise_top, detail) for x in xa])
    return U([nose, n2, aft])

def make_hull():
    return D([solid(0.0, False, True), solid(T, True, False)])      # pieges n.1 et n.5

# ------------------------------------------------------------------- le pont
def deck_loop(sh, y0, y1, cf, n=26, fair=1.0):
    a = y0+T+0.3; b = y1-T-0.3
    ys = np.linspace(a, b, n)
    p  = [(y, sh+(DKT+cf(y))*fair) for y in ys]
    p += [(b, sh)]
    p += [(b-1.4, sh), (b-1.4, sh-LIP), (b-2.9, sh-LIP), (b-2.9, sh)]
    p += [(y, sh+cf(y)*fair) for y in np.linspace(b-2.9, a+2.9, n)][1:-1]
    p += [(a+2.9, sh), (a+2.9, sh-LIP), (a+1.4, sh-LIP), (a+1.4, sh)]
    p += [(a, sh)]
    return p

def deck_sect_aft(x):
    ye = SY+bsx(x)+fl_eff(x); sh = sheer(x)
    return [(x, y, z) for y, z in deck_loop(sh, -ye, ye, lambda y: crown(y, ye))]

def deck_sect_nose(x):
    bs = bsx(x); yi = SY-bs; ye = SY+bs+fl_eff(x); sh = sheer(x)
    if ye-yi < 12: ye = yi+12
    c = (yi+ye)/2; hw = (ye-yi)/2
    fair = min(1.0, 0.30+0.70*(x-XD0)/40.0)    # l'avant du pont s'efface dans la coque
    return [(x, y, z) for y, z in deck_loop(sh, yi, ye, lambda y: crown(y-c, hw)*0.5, fair=fair)]

def ell(a, b, z0, z1, cx=0.0, cy=0.0, res=72):
    th = np.linspace(0, 2*np.pi, res, endpoint=False)
    e = Polygon([(cx+a*math.cos(t), cy+b*math.sin(t)) for t in th])
    m = extrude_polygon(e, z1-z0); m.apply_translation([0, 0, z0]); return m

def rrect(w, h, r, z0, z1, cx=0.0, cy=0.0):
    p = Polygon([(-w/2+r, -h/2+r), (w/2-r, -h/2+r), (w/2-r, h/2-r), (-w/2+r, h/2-r)]).buffer(r, resolution=24)
    m = extrude_polygon(p, z1-z0); m.apply_translation([cx, cy, z0]); return m

def cut_plane(m, normal, origin):
    return trimesh.intersections.slice_mesh_plane(m, plane_normal=normal, plane_origin=origin, cap=True)

# vis : (x, y, z_haut_du_plat)  --  toutes borgnes, aucune ne traverse la coque
# capot : 2 languettes AVANT (poches dans la plinthe) + 2 boutons moletes ARRIERE.
# (les vis avant v2.0 etaient dans le conge du dome -> inaccessibles au tournevis)
SCREWS_CANOPY = [(HX+SCRX, sy) for sy in (-SCRY, SCRY)]
TABY = 26.0                          # ecartement des languettes avant
# pylone : 2 vis AVANT seulement (les vis arriere etaient sous les flancs du berceau,
# inaccessibles au tournevis) ; l'arriere de la bride glisse sous une griffe du plateau
SCREWS_PYLON  = [(PYX-22, sg*PYY+sy) for sg in (1, -1) for sy in (-13, 13)]
SCREWS_GUARD  = [(GDX+14, sg*(PYY+e)) for sg in (1, -1) for e in (-GFY, GFY)]

def make_deck():
    nose = loft([deck_sect_nose(x) for x in np.linspace(XD0, XJ, 18)])
    n2 = nose.copy(); n2.apply_scale([1, -1, 1]); n2.fix_normals()
    aft = loft([deck_sect_aft(x) for x in np.concatenate([np.linspace(XJ, 150, 10), np.linspace(155, XD1, 18)])])
    d = U([nose, n2, aft])
    # plinthe cockpit : dalle de 6.5 entre deux plans inclines (un bas PLAT plongerait
    # dans le haut des murs d'etraves a l'avant)
    seat = ell(SEATA, SEATB, 80.0, 110.0, cx=HX)
    ears = [rrect(18, 18, 5, 80.0, 110.0, cx=HX-72.0, cy=sy) for sy in (-TABY, TABY)]
    seat = U([seat]+ears)
    kn = np.array([KSEAT, 0.0, -1.0]); kn /= np.linalg.norm(kn)
    seat = cut_plane(seat, kn, [HX, 0, Z0SEAT])
    seat = cut_plane(seat, -kn, [HX, 0, Z0SEAT-6.5])
    # plateaux plans pour les pylones et pastilles pour les pieds d'anneaux
    pads = [rrect(60, 44, 8, ZMOUNT-9, ZMOUNT, cx=PYX, cy=sg*PYY) for sg in (1, -1)]
    # griffe centrale a l'arriere de chaque plateau : l'arriere de la bride glisse dessous
    pads += [rrect(9, 13, 2, ZMOUNT-12, ZMOUNT+8.5, cx=PYX+30.5, cy=sg*PYY) for sg in (1, -1)]
    pads += [cylinder(radius=6.0, height=12, transform=TR([x, y, ZMOUNT-6])) for x, y in SCREWS_GUARD]
    d = U([d, seat]+pads)
    # cloison avant VENUE DE FONDERIE quand on reimprime le pont (piege n.18) : plus de piece 13,
    # plus de collage sur 3 faces, position garantie. Unie AVANT les decoupes -> l'ecoutille la
    # retaille de x=101 a 110 et reste donc entierement ouverte ; la face qui etanche est a x=95,
    # en avant de l'ecoutille, elle n'est pas touchee.
    if not BOW_PATCH:
        d = U([d, make_bow_bulkhead(up=1.5)])   # pas de `deck=` ici : elle mord dans la dalle -> corps=1
    # ecoutille + passe-fils
    cuts = [ell(HA, HB, 60, 140, cx=HX)]
    cuts += [cylinder(radius=2.75, height=60, transform=TR([WIREX, sg*WIREY, 85])) for sg in (1, -1)]
    # poches des languettes du capot (ouverture + contre-depouille vers l'avant)
    # BORGNES : fond a zp-5.5, la dalle descend a zp-6.5 -> pas de fuite vers le compartiment
    for sy in (-TABY, TABY):
        zp = seat_z(HX-72.0)
        cuts.append(box([8.0, 12.5, 8.5], transform=TR([HX-68.5, sy, zp-1.25])))   # ouverture
        cuts.append(box([6.5, 12.5, 3.5], transform=TR([HX-75.75, sy, zp-3.25])))  # contre-depouille
    # gueule des griffes des pylones (la bride entre par l'avant, 0.4 de jeu vertical)
    cuts += [box([9.2, 14.0, 4.45], transform=TR([PYX+26.0, sg*PYY, ZMOUNT+2.2])) for sg in (1, -1)]
    # trous de vis borgnes (0.5-1.0 de fond conserve : rien ne traverse)
    for x, y in SCREWS_CANOPY:
        cuts.append(cylinder(radius=1.35, height=7, transform=TR([x, y, seat_z(x)-2.5])))
    for x, y in SCREWS_PYLON:
        cuts.append(cylinder(radius=1.35, height=9, transform=TR([x, y, ZMOUNT-3.5])))
    for x, y in SCREWS_GUARD:
        cuts.append(cylinder(radius=1.35, height=11, transform=TR([x, y, ZMOUNT-4.5])))
    return D([d, U(cuts)])

# ------------------------------------------------ bouchons d'etrave (rustine)
def make_bow_plug():
    """Bouche le trou laisse a l'avant de chaque cuve (piege n.16) : la cavite s'ouvre
    des x=XPL0 alors que le pont ne commence qu'a x=XPL1. Se pose sur des coques DEJA
    imprimees ; a supprimer si le pont est un jour rallonge jusqu'a XPL0.
      - teton : booleen sur la cavite RETREINTE de PLGAP -> 0.3 de jeu par face ;
      - collerette : a cheval sur les 2 livets ET sur l'etrave pleine en avant de XPL0.
        Indispensable -- les parois de la cuve y sont quasi verticales (21.95 -> 21.33 mm
        sur 6 mm de fond) : un teton seul tomberait dans la coque.
    Dessous sur la tonture, dessus PLAT (z=zc) -> s'imprime collerette sur le plateau,
    teton en l'air, sans support. PETG : meme matiere que la coque, donc SOUDABLE au fer +
    filament (le TPU ne se soude pas au PETG : 30-50 degres d'ecart de fusion)."""
    cav = solid(T + PLGAP, True, False)
    zc  = sheer(XPL1) + PLCAP
    def bsec(x):                                     # bande qui suit la tonture
        sh = sheer(x)
        return [(x, -200.0, sh-PLD), (x, 200.0, sh-PLD), (x, 200.0, sh), (x, -200.0, sh)]
    spig = I([cav, loft([bsec(x) for x in np.linspace(XPL0+PLGAP, XPL1-PLGAP, 6)])])
    def csec(x):
        sh = sheer(x); ym = SY-max(bsx(x)-T, 0.6)-PLW; yp = SY+max(bsx(x)-T, 0.6)+fl_eff(x)+PLW
        return [(x, ym, sh), (x, yp, sh), (x, yp, zc), (x, ym, zc)]
    c1 = loft([csec(x) for x in np.linspace(XPLC, XPL1-PLGAP, 8)])
    c2 = c1.copy(); c2.apply_scale([1, -1, 1]); c2.fix_normals()      # piege n.6
    return U([spig, c1, c2])

# ----------------------------------------------- cloison d'etrave a XJ (piege n.18)
def make_bow_bulkhead(deck=None, up=0.0):
    """Le dessous du pont N'EST PAS a `sheer` : la dalle est bombee, son intrados est a
    `sheer + crown(y)` (jusqu'a +5 dans l'axe). Une cloison arretee a `sheer` laisse un jour
    de 5 mm sur 60 de large -- 3 cm2 d'ecope, invisible aux rayons tires sous le livet.
    D'ou : on ne DEVINE pas ou s'arrete le pont, on le SOUSTRAIT.
      deck != None -> piece rapportee 13 : epouse l'intrados reel, aucune collision.
      deck == None -> version integree : elle MORD de `up` dans la dalle. Indispensable, sinon
                      les surfaces se touchent sans se recouvrir et l'union ne fusionne pas
                      (corps=2 : la cloison sort en piece separee sur le plateau)."""
    """Ferme la face avant du compartiment, ouverte plein nez a XJ (piege n.18).
    Booleen sur la cavite REELLE, donc l'emprise epouse exactement l'arche du tunnel en
    dessous et les murailles internes des sponsons sur les cotes ; le dessus arrive pile
    au dessous du pont. Se pose par le DESSUS, pont non colle, et se colle avec lui.
"""
    cav = solid(T, True, False)
    # On monte FRANCHEMENT au-dessus de l'intrados (CRN = bombement max, +2 de marge) : le loft
    # de la bande interpole en lignes droites entre ses stations et passerait sinon SOUS la courbe
    # du livet (91.86 mesure contre 92.19 vise). C'est la soustraction du pont qui donne la cote
    # exacte, pas ce plafond -- il doit juste etre trop haut partout.
    zt = lambda x: sheer(x) + CRN + 2.0 + up
    bsec = lambda x: [(x, -200.0, 0.0), (x, 200.0, 0.0), (x, 200.0, zt(x)), (x, -200.0, zt(x))]
    band = loft([bsec(x) for x in np.linspace(BKX0, BKX1, 8)])
    def ysec(x):    # suit la muraille interne du tunnel, qui se retrecit vers l'arriere
        yl = SY - max(bsx(x)-T, 0.6) - BKGAP
        return [(x, -yl, 0.0), (x, yl, 0.0), (x, yl, 200.0), (x, -yl, 200.0)]
    ylim = loft([ysec(x) for x in np.linspace(BKX0-2.0, BKX1+2.0, 10)])
    b = I([cav, band, ylim])
    return D([b, deck]) if deck is not None else b

# -------------------------------------------------------------------- capot
def half_teardrop(af, ar, b, h, zc):
    """dome = 2 demi-ellipsoides (avant long = pare-brise incline, arriere court).
    Coupe a z>=zc : sans elle, la moitie basse de la lentille pend SOUS la bride."""
    big = 500.0
    f = icosphere(subdivisions=4, radius=1.0); f.apply_scale([af, b, h]); f.apply_translation([0, 0, zc])
    f = I([f, box([big, big, big], transform=TR([-big/2, 0, zc]))])
    r = icosphere(subdivisions=4, radius=1.0); r.apply_scale([ar, b, h]); r.apply_translation([0, 0, zc])
    r = I([r, box([big, big, big], transform=TR([big/2, 0, zc]))])
    d = U([f, r])
    return I([d, box([big, big, big], transform=TR([0, 0, zc+big/2]))])

def make_canopy():
    # dome recentre dans la bride : nez a 6 du bord avant, queue effilee couvrant TOUTE
    # l'ecoutille (x+54), boutons arriere au degage lateral de la queue
    AF, AR, BC, XO = 62.0, 70.0, 46.0, -8.0
    fl = ell(FA, FB, 0, 2.5)
    out = half_teardrop(AF, AR, BC, CANH, 2.5); out.apply_translation([XO, 0, 0])
    inn = half_teardrop(AF-2.2, AR-2.2, BC-2.2, CANH-2.2, 2.5); inn.apply_translation([XO, 0, 0])
    tabs = []
    for sy in (-TABY, TABY):         # languettes avant : plat + jambe + pied vers l'avant
        tabs.append(box([15.0, 11.0, 2.5], transform=TR([-69.5, sy, 1.25])))
        tabs.append(box([3.5, 11.0, 6.0],  transform=TR([-70.15, sy, -3.0])))
        tabs.append(box([4.0, 11.0, 2.5],  transform=TR([-73.9, sy, -4.75])))
    c = U([fl, out]+tabs)
    c = D([c, inn, ell(56, 40, -2, 2.51)])           # ouvre le dessous vers l'ecoutille
    cuts = [cylinder(radius=1.75, height=12, transform=TR([SCRX, sy, 1.25]))
            for sy in (-SCRY, SCRY)]                 # 2 vis ARRIERE seulement (boutons moletes)
    return D([c, U(cuts)])

def make_gasket():
    return D([ell(64, 44, 0, 2.0), ell(56, 38, -1, 4)])

def make_knob():
    """bouton molete : une vis M3 collee dedans -> serrage du capot a la main"""
    body = cylinder(radius=8.0, height=9.0, transform=TR([0, 0, 4.5]))
    cuts = [cylinder(radius=2.5, height=11, transform=TR([9.6*math.cos(a), 9.6*math.sin(a), 4.5]))
            for a in np.linspace(0, 2*np.pi, 8, endpoint=False)]
    cuts.append(cylinder(radius=3.2, height=7, transform=TR([0, 0, 9.0-2.4])))   # logement tete
    cuts.append(cylinder(radius=1.7, height=30, transform=TR([0, 0, 0])))        # passage vis
    return D([body, U(cuts)])

# ------------------------------------------------------------------- pylone
def foil_pts(c, th, n=22):
    """profil symetrique type NACA00, corde c, epaisseur th, BA a x=-c/2"""
    up = []
    for u in np.linspace(0.002, 1.0, n):
        yt = th/0.2*(0.2969*math.sqrt(u)-0.1260*u-0.3516*u**2+0.2843*u**3-0.1036*u**4)
        up.append((u*c-c/2, yt/2))
    lo = [(x, -y) for x, y in reversed(up[:-1])]
    return up+lo

def make_pylon():
    fl = rrect(56, 38, 5, 0, 4)     # coins peu arrondis : l'arriere droit entre dans la griffe
    secs = []
    for t in np.linspace(0, 1, 8):
        z = 4+t*(MOT_Z-16-4); c = 46-8*t; th = 12-2*t; xoff = -2+12*t*t
        secs.append([(x+xoff, y, z) for x, y in foil_pts(c, th)])
    fin = loft(secs)
    out = cylinder(radius=NAC_R, height=NAC_L, transform=RX(np.pi/2, [0, 1, 0]))
    inn = cylinder(radius=SADDLE_ID/2, height=NAC_L+10, transform=RX(np.pi/2, [0, 1, 0]))
    sad = D([out, inn]); sad.apply_translation([NAC_X, 0, MOT_Z])
    sad = I([sad, box([120, 120, 120], transform=TR([NAC_X, 0, MOT_Z-60]))])   # demi-coquille
    # casquette / capot arriere-moteur INTEGRE : coiffe fermee sur le flasque arriere (cote etrave)
    # qui CACHE et protege le deparasitage (2 selfs + condo). Meme Ø que la nacelle, face avant
    # pleine (deflecteur), OUVERTE EN BAS -> sortie fils + egouttage + un filet d'air (pas de
    # surchauffe, pas de caisson etanche). Prealable : couper les oreilles triangulaires du flasque.
    fx0  = NAC_X - NAC_L/2                                       # nez du berceau (x=-8)
    fout = cylinder(radius=NAC_R, height=HOUS_L, transform=RX(np.pi/2, [0, 1, 0]))
    fout.apply_translation([fx0 - HOUS_L/2 + 3, 0, MOT_Z])       # tube exterieur
    fbor = cylinder(radius=SADDLE_ID/2, height=HOUS_L, transform=RX(np.pi/2, [0, 1, 0]))
    fbor.apply_translation([fx0 - HOUS_L/2 + 6, 0, MOT_Z])       # alesage decale -> face AVANT pleine (~3 mm)
    fair = D([fout, fbor])
    fair = I([fair, box([HOUS_L+8, 60, 60], transform=TR([fx0 - HOUS_L/2 + 3, 0, MOT_Z+30-9]))])  # bas ouvert
    p = U([fl, fin, sad, fair])
    cuts = [box([4, 60, 20], transform=TR([NAC_X-12, 0, MOT_Z-13])),           # fentes rilsan
            box([4, 60, 20], transform=TR([NAC_X+12, 0, MOT_Z-13]))]
    cuts += [cylinder(radius=1.75, height=12, transform=TR([-22, sy, 2]))
             for sy in (-13, 13)]                     # 2 vis AVANT ; l'arriere sous la griffe
    return D([p, U(cuts)])

def make_shim(md):
    out = cylinder(radius=SADDLE_ID/2-0.15, height=20)
    inn = cylinder(radius=md/2+0.2, height=26)
    slot = box([20, 4.5, 26]); slot.apply_translation([SADDLE_ID/2, 0, 0])
    r = D([out, inn, slot]); r.apply_translation([0, 0, 10]); return r

# ----------------------------------------------------- anneau de protection
def make_guard(pd=100.0):
    ri, ro = pd/2+5.0, pd/2+10.5
    prof = Polygon([(ri, -4.5), (ro, -4.5), (ro, 4.5), (ri, 4.5)]).buffer(-1.6).buffer(1.6)
    ring = revolve(np.array(prof.exterior.coords), sections=96)
    if ring.volume < 0: ring.invert()
    ring.apply_transform(RX(np.pi/2, [0, 1, 0])); ring.apply_translation([0, 0, MOT_Z])
    parts = [ring]; cuts = []
    a = math.radians(42)
    for sg in (1, -1):
        end = (sg*ro*math.sin(a), MOT_Z-ro*math.cos(a))
        leg = LineString([(sg*22, 6), end]).buffer(5.5, resolution=16)   # bout bas a z=0.5
        lg = extrude_polygon(leg, 7.0)
        lg.apply_transform(RX(np.pi/2, [1, 0, 0])); lg.apply_transform(RX(np.pi/2, [0, 0, 1]))
        lg.apply_translation([3.5, 0, 0])          # plaque yz, epaisseur x -3.5..3.5
        pad = rrect(24, 16, 4, 0, 6, cx=7, cy=sg*GFY)
        parts += [lg, pad]
        cuts.append(cylinder(radius=1.75, height=16, transform=TR([14, sg*GFY, 3])))
    return D([U(parts), U(cuts)])

# ------------------------------------------------------------------ helices
def blade_sec(r, Dm):
    R = Dm/2; P = 0.72*Dm
    beta = min(math.atan2(P, 2*np.pi*max(r, 6.0)), math.radians(46))
    tt = (r-9)/(R-9); ch = 21-11*tt**1.15; th = 2.5-1.4*tt
    swp = -0.5-7.0*tt**1.8                        # fleche -> pale en cimeterre
    pts = []
    for s in np.linspace(-0.5, 0.5, 12): pts.append((ch*s+swp, th/2*math.sqrt(max(1-(2*s)**2, 0))**0.8))
    for s in np.linspace(0.5, -0.5, 14)[1:-1]: pts.append((ch*s+swp, -th/2*math.sqrt(max(1-(2*s)**2, 0))**0.8))
    # beta = calage depuis le PLAN DE ROTATION -> corde = cos(beta) sur le tangentiel (x),
    # sin(beta) sur l'axial (z). Inverser les deux donne un calage 90-beta (piege n.19).
    return [(c*math.cos(beta)-t*math.sin(beta), r, c*math.sin(beta)+t*math.cos(beta)) for c, t in pts]

def make_prop(Dm, ccw=False):
    R = Dm/2
    bl = loft([blade_sec(r, Dm) for r in np.linspace(9, R-1.0, 22)])
    parts = []
    for k in range(3):
        b = bl.copy(); b.apply_transform(RX(k*2*np.pi/3, [0, 0, 1])); parts.append(b)
    grip_h = PIGN_L + 2.0                                       # profondeur de prise sur le pignon
    HUB_H  = grip_h + 6.0                                       # + fond plein derriere le pignon
    parts.append(cylinder(radius=9.5, height=HUB_H))            # moyeu Ø19
    p = U(parts)
    # --- accouplement broche a froid sur le pignon conserve (Ø PIGN_D) ---
    # trou rond sous-cote : en pressant, les dents du pignon taillent leurs
    # cannelures dans le PETG -> entrainement positif, auto-centre, sans colle.
    zf   = -HUB_H/2                                             # face moteur (bas du moyeu)
    grip = cylinder(radius=(PIGN_D-GRIP_I)/2, height=grip_h)
    grip.apply_translation([0, 0, zf+grip_h/2])
    lead = cylinder(radius=(PIGN_D+1.0)/2, height=2.0)          # lamage d'amorce a l'entree
    lead.apply_translation([0, 0, zf+1.0])
    pilot = cylinder(radius=(SHAFT_D+0.3)/2, height=HUB_H+2)    # pilote centrage / ejection (traversant)
    p = D([p, grip, lead, pilot])
    if ccw: p.apply_scale([1, -1, 1]); p.fix_normals()
    return p

def make_dummy():
    d = D([cylinder(radius=7.05, height=49.5), cylinder(radius=1.9, height=60)])
    d.apply_translation([0, 0, 49.5/2]); return d

# ------------------------------------------------------------------- export
def save(m, n):
    m.export(os.path.join(STL, n+".stl"))
    import collections
    cnt = collections.Counter(map(tuple, m.edges_sorted)); op = sum(1 for v in cnt.values() if v == 1)
    print("%-34s ouvertes=%-3d corps=%-2d vol=%7.1f cm3 bbox=%s" %
          (n, op, m.body_count, m.volume/1000, np.round(m.extents, 1)))
    return m

def grounded(m):
    g = m.copy(); g.apply_translation([0, 0, -g.bounds[0][2]]); return g

def plugs_flat(m):
    """les 2 bouchons d'etrave : retournes collerette sur le plateau, teton en l'air."""
    g = m.copy(); g.apply_transform(RX(np.pi, [1, 0, 0]))
    out = []
    for i, b in enumerate(sorted(g.split(), key=lambda k: k.centroid[1])):
        b = grounded(b)
        b.apply_translation([-b.centroid[0], -b.centroid[1] + (i-0.5)*32.0, 0])
        out.append(b)
    return trimesh.util.concatenate(out)

if __name__ == "__main__":
    for f in os.listdir(STL):
        fp = os.path.join(STL, f)
        if f.endswith(".stl"): os.remove(fp)
    if os.path.isdir(ASM): shutil.rmtree(ASM, ignore_errors=True)
    os.makedirs(ASM, exist_ok=True)

    hull   = save(make_hull(),  "01_coque")
    deck   = save(make_deck(),  "02_pont")           # reste en repere bateau (le slicer posera)
    canopy = save(grounded(make_canopy()), "03_capot")
    gasket = save(grounded(make_gasket()), "04_joint_capot_TPU")
    pylon  = save(make_pylon(), "05_pylone_moteur_x2")
    save(make_shim(24.0), "06_bague_moteur_24_0mm")             # corps moteur Ø24 (mesure)
    guards = {}
    for pd in (100.0, 90.0):
        g = make_guard(pd)
        gp = g.copy(); gp.apply_transform(RX(-np.pi/2, [0, 1, 0]))   # anneau a plat sur le plateau
        guards[pd] = g
        save(grounded(gp), "07_anneau_protection_D%d_x2" % pd)
    props = {}
    for Dm in (100.0, 90.0):                                         # D100 (6 V) / D90 (option 7,2 V)
        pr = save(grounded(make_prop(Dm, False)), "08_helice_D%d_pignon7_CW" % Dm)
        save(grounded(make_prop(Dm, True)),  "08_helice_D%d_pignon7_CCW" % Dm)
        props[Dm] = pr
    save(make_dummy(), "09_pile_factice_AA")
    save(make_knob(),  "10_bouton_capot_x2")
    plugs = make_bow_plug() if BOW_PATCH else None     # rustine seulement (piege n.16)
    if plugs is not None:
        save(plugs_flat(plugs), "11_bouchon_etrave_x2")
    # piece rapportee SEULEMENT en mode rustine : si on reimprime le pont, elle y est integree
    bulk = make_bow_bulkhead(deck=deck) if BOW_PATCH else None
    if bulk is not None:
        bf = bulk.copy(); bf.apply_transform(RX(np.pi/2, [0, 1, 0]))   # a plat : croissant sur le plateau
        save(grounded(bf), "13_cloison_avant")

    # ------------------------------------------------------------ assemblage
    print("\n=== ASSEMBLAGE (rendu) ===")
    AX = MOT_Z + ZMOUNT                       # axe helices (z bateau)
    asm = {}
    asm["coque"]    = hull
    asm["pont"]     = deck
    if bulk is not None: asm["cloison"] = bulk
    if plugs is not None: asm["bouchons"] = plugs
    beta = math.atan(-KSEAT)
    cano = make_canopy(); cano.apply_transform(RX(beta, [0, 1, 0])); cano.apply_translation([HX, 0, Z0SEAT+2.0])
    asm["capot"] = cano
    py = make_pylon()
    p1 = py.copy(); p1.apply_translation([PYX, PYY, ZMOUNT])
    p2 = py.copy(); p2.apply_translation([PYX, -PYY, ZMOUNT])
    asm["pylones"] = U([p1, p2])
    gu = make_guard(100.0)
    g1 = gu.copy(); g1.apply_translation([GDX, PYY, ZMOUNT])
    g2 = gu.copy(); g2.apply_translation([GDX, -PYY, ZMOUNT])
    asm["anneaux"] = U([g1, g2])
    mots = []
    for sg in (1, -1):
        mo = cylinder(radius=12, height=30, transform=RX(np.pi/2, [0, 1, 0]))   # corps moteur Ø24 x 30
        mo.apply_translation([PYX+NAC_X, sg*PYY, AX])
        sh_ = cylinder(radius=1.6, height=26, transform=RX(np.pi/2, [0, 1, 0]))
        sh_.apply_translation([PYX+NAC_X+NAC_L/2+8, sg*PYY, AX])
        mots += [mo, sh_]
    asm["moteurs"] = U(mots)
    prs = []
    for sg, ccw in ((1, False), (-1, True)):
        pr = make_prop(100.0, ccw)
        pr.apply_transform(RX(np.pi/2, [0, 1, 0]))
        pr.apply_transform(RX(sg*0.5, [1, 0, 0]))
        pr.apply_translation([GDX, sg*PYY, AX])
        prs.append(pr)
    asm["helices"] = U(prs)
    for k, m in asm.items():
        m.export(os.path.join(ASM, k+".stl"))

    COLORS = {"coque": "#f2f0e9", "pont": "#3a3f44", "capot": "#20242a", "bouchons": "#8a1f1f",
              "cloison": "#b8860b",
              "pylones": "#c8ccd0", "anneaux": "#c8ccd0", "moteurs": "#54585e", "helices": "#e8641b"}
    with open(os.path.join(ASM, "assemblage.scad"), "w") as f:
        for k in asm:
            f.write('color("%s") import("%s.stl", convexity=6);\n' % (COLORS[k], k))
    scad_gui = os.path.join(HERE, "apercu_assemblage.scad")
    with open(scad_gui, "w") as f:
        f.write("// Assemblage complet -- ouvrir dans OpenSCAD pour orbiter\n")
        for k in asm:
            f.write('color("%s") import("stl/_assemblage/%s.stl", convexity=6);\n' % (COLORS[k], k))

    # ---------------------------------------------------------- verification
    print("\n=== VERIFICATION ===")
    out = solid(0.0, False, True)
    mh = hull.volume/1000*1.27; md = deck.volume/1000*1.27
    mcap = canopy.volume/1000*1.27
    mpy = 2*pylon.volume/1000*1.27*0.62; mgu = 2*guards[100].volume/1000*1.27*0.62
    mpr = 2*props[100].volume/1000*1.27*0.62
    comps = [("coque", mh, out.center_mass[0]), ("pont", md, deck.center_mass[0]),
             ("capot+joint", mcap+8, HX), ("pylones", mpy, PYX), ("anneaux", mgu, GDX),
             ("helices", mpr, GDX), ("moteurs", 140.0, PYX+NAC_X), ("pack 5xAA+support", 175.0, HX),
             ("carte RC+fils", 70.0, HX-20), ("visserie", 20.0, 230.0)]
    mt = sum(c[1] for c in comps)
    xg = sum(c[1]*c[2] for c in comps)/mt
    print("masses : " + " | ".join("%s %.0f g" % (c[0], c[1]) for c in comps))
    print("total %.0f g  --  CG a x=%.0f" % (mt, xg))
    draft = None
    for Tt in np.arange(2, 70, 0.25):
        sl = cut_plane(out, [0, 0, -1], [0, 0, Tt])
        if sl.volume/1000.0 >= mt:
            draft = Tt; xb = sl.center_mass[0]; break
    print("hors-tout coque : %.0f x %.0f x %.0f mm | envergure anneaux %.0f mm" %
          (*out.extents, 2*(PYY+62)))
    print("tirant d'eau %.1f mm | CB a x=%.0f (delta CG-CB %.0f mm, corriger en glissant le pack)" % (draft, xb, xg-xb))
    print("garde sous tunnel %.1f mm | franc-bord AV %.1f / AR %.1f mm" %
          (tunz(L)-draft, sheer(0)-draft, sheer(280)-draft))
    print("joint pont/coque a %.0f-%.0f mm au-dessus de la flottaison" % (SH_AFT-draft, SH_BOW-draft))
    print("axe helices z=%.1f | bas du disque D100 a %.1f au-dessus de ZMOUNT" % (AX, MOT_Z-50))
    print("\n=== COLLISIONS D'ASSEMBLAGE (les contacts plans comptent 0) ===")
    for a, b in [("coque", "pont"), ("pont", "pylones"), ("pont", "anneaux"),
                 ("pont", "capot"), ("coque", "pylones"), ("coque", "anneaux"),
                 ("pylones", "anneaux"), ("capot", "pylones"),
                 ("helices", "anneaux"), ("helices", "pylones"),
                 ] + ([("coque", "cloison"), ("pont", "cloison")] if bulk is not None else []) + \
                ([("coque", "bouchons"), ("pont", "bouchons")] if plugs is not None else []):
        try:
            v = I([asm[a], asm[b]]).volume/1000.0
        except Exception:
            v = 0.0
        print("%-18s %8.3f cm3 %s" % (a+" / "+b, v, "ok" if v < 0.05 else "<<< COLLISION"))

    # --------------------------------------------------------------- apercus
    print("\n=== RENDUS ===")
    OPENSCAD = r"C:\Program Files\OpenSCAD (Nightly)\openscad.exe"
    views = [("3/4 avant",   (-190, -300, 260)),
             ("profil",      (150, -560, 100)),
             ("dessus",      (149.9, 0, 600)),
             ("3/4 arriere", (520, 260, 240))]
    ctr = (150, 0, 90)
    imgs = []
    if os.path.isfile(OPENSCAD):
        for i, (lab, eye) in enumerate(views):
            png = os.path.join(ASM, "v%d.png" % i)
            cam = ",".join(str(v) for v in eye)+","+",".join(str(v) for v in ctr)
            r = subprocess.run([OPENSCAD, "-o", png, "--imgsize=1500,950", "--camera="+cam,
                                "--viewall", "--projection=p", "--colorscheme=Tomorrow",
                                os.path.join(ASM, "assemblage.scad")],
                               capture_output=True, text=True, cwd=ASM)
            ok = os.path.isfile(png)
            print("vue %-12s -> %s" % (lab, "ok" if ok else r.stderr[-300:]))
            if ok: imgs.append((lab, png))
        try:
            from PIL import Image, ImageDraw, ImageChops
            tiles = []
            for _, p in imgs:
                im = Image.open(p).convert("RGB")
                bg = Image.new("RGB", im.size, im.getpixel((3, 3)))
                bb = ImageChops.difference(im, bg).getbbox()
                if bb:
                    m = 30
                    bb = (max(bb[0]-m, 0), max(bb[1]-m, 0), min(bb[2]+m, im.width), min(bb[3]+m, im.height))
                    im = im.crop(bb)
                tiles.append(im)
            cw = max(t.width for t in tiles); chh = max(t.height for t in tiles)
            grid = Image.new("RGB", (cw*2+30, chh*2+30), "#f7f7f7")
            dr = ImageDraw.Draw(grid)
            for i, im in enumerate(tiles):
                ox, oy = (i % 2)*(cw+10)+10, (i//2)*(chh+10)+10
                grid.paste(im, (ox+(cw-im.width)//2, oy+(chh-im.height)//2))
                dr.text((ox+10, oy+6), imgs[i][0], fill="#222")
            grid.thumbnail((2200, 1500))
            grid.save(os.path.join(HERE, "apercu_catamaran.png"))
            print("apercu_catamaran.png ecrit")
        except Exception as e:
            print("composition PNG impossible :", e)
    else:
        print("OpenSCAD introuvable -- pas de rendu")
