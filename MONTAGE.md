# Catamaran à tunnel, hélices aériennes — récup Nikko N-Blaster

Coque-cuve + pont sculpté collé, capot capsule vissé, deux hélices aériennes en pylônes,
**pilotage différentiel** (skid-steer). Les deux à fond = tout droit. Un seul = virage.
Un avant + un arrière = rotation sur place.

---

## 1. Chiffres (recalculés par `generate_pieces.py` — source de vérité)

| | |
|---|---|
| Coque | 298 × **191** × 94 mm — entraxe des flotteurs **111 mm** |
| Envergure anneaux | 256 mm — ce sont les **pylônes** qui écartent les hélices (±66 mm) |
| Carène | sponsons en V (deadrise 32°), spray-rail au bouchain, étraves inclinées, tunnel cambré |
| Tirant d'eau | **≈45 mm** (à 1150 g) — franc-bord 49 mm à l'étrave, 37 mm à l'arrière |
| Garde sous tunnel | **≈13 mm** au-dessus de la flottaison |
| Joint pont/coque | 37 à 49 mm au-dessus de la flottaison — jamais immergé |
| Masse estimée | **~1 150 g** |
| Hélices | **2** pales fines **vrillées** D95, posées sur le bord de fuite. Calage 30° à l'emplanture → **15°** au bout (pas/D 0,84) |
| Axe hélices | 164 mm au-dessus de la quille |

---

## 2. Impression (PETG sauf mention, buse 0,4)

| Pièce | Qté | Matière | Orientation / réglages |
|---|---|---|---|
| `01_coque` | 1 | PETG | **Quille en bas**, brim large. 4 périmètres, 0 % remplissage. Supports **dans le tunnel** (accessibles par-dessous) **et sous les pointes d'étraves** (l'étrave inclinée surplombe à ~45°). |
| `02_pont` | 1 | PETG | Dessus vers le haut, supports sous le pont (pièce séparée = supports faciles). 4 périmètres. |
| `03_capot` | 1 | PETG | Dôme vers le haut, aucun support (convexe). |
| `04_joint_capot_TPU` | 1 | TPU 95A | 100 %, pas d'ironing. |
| `05_pylone_moteur` | **2** | PETG | Debout (bride en bas), **support sous la nacelle + sous la coiffe arrière-moteur** (l'arche fermée surplombe le vide). 4 périmètres, 40 %. |
| `06_bague_moteur_24_0mm` | **2** | TPU | 100 % — souple et adhérente. Berceau Ø32,4, moteur Ø24, bague **fendue** (se clipse autour du corps). |
| `07_anneau_protection_D95` | **2** | PETG | Exporté **à plat** : anneau et pattes sur le plateau, les deux tours de fixation montent verticalement. 4 périmètres, 40 %. Un seul diamètre — les deux variantes d'hélice ont la même envergure. |
| `08_helice_*_CW` + `*_CCW` | 1 de chaque | PETG | Pale **fine posée sur son bord de fuite** : seule cette arête (+ un petit méplat) touche le plateau, la pale monte en rampe (30° à l'emplanture, 15° au bout — la pale est **vrillée**, c'est voulu ; le nom du fichier porte les deux calages). Orientation déjà bonne dans le STL, ne pas la coucher. 4 périmètres, 40-100 % (plus c'est dense, moins ça vibre), couches 0,12-0,16 mm. **Support « sur le plateau uniquement » activé** : il en faut un peu, COURT (≤11 mm), sous le dessous de la pale — jamais sur le dessus visible. Les bords sont épais et francs (~2,4 mm) : le support s'en détache sans déchirer (c'était ça le drame de la v1 à bords en lame). Distance Z sup. = 0,24 mm, interface 0. |
| `09_pile_factice_AA` | 1 | PETG | 100 %. Bouche le 6ᵉ logement du support (5 AA = 6 V), vis M3 traversante pour fermer le circuit. |
| `10_bouton_capot` | **2** | PETG | À plat, 100 %. Vis M3 (~16 mm) collée dedans à la cyano → bouton moleté. |
| `11_bouchon_etrave_x2` | **2** | PETG | 100 %, collerette sur le plateau et téton en l'air : **aucun support**. Les deux sont dans le fichier et sont **symétriques, pas identiques** — ne pas imprimer deux fois le même. Rustine, voir §3. |
| `13_cloison_avant` | 1 | PETG | **À plat (croissant sur le plateau), aucun support.** 4 périmètres, 100 %. Ferme l'avant du compartiment — **pièce d'étanchéité, à coller**, voir §3. |

**Logique matériaux :** PETG = tout ce qui est structurel/étanche (et même matériau des deux
côtés du joint époxy pont/coque). TPU 95A = uniquement les interfaces souples (joint, bagues).
**Ne cède pas à la tentation du TPU pour :** les **anneaux** (souples, ils s'ovalisent et un choc
les défléchit *dans* l'hélice) ni les **hélices** (les pales se dévrillent à haut régime →
plus de poussée, flottement). Un anneau PETG qui casse en crash se réimprime pour 15 g.

**Étanchéité de la coque :** 4 périmètres, 240-250 °C, flux 102-105 %, refroidissement faible,
couture Z aléatoire. Test avant mise à l'eau : coque remplie d'eau posée sur de l'essuie-tout, 15 min.

---

## 3. Le collage pont / coque

Le seul joint structurel du bateau. Le pont porte une **lèvre de 6 mm** qui s'emboîte à
l'intérieur des murailles : il se positionne tout seul et offre une grande surface de collage.

- Ponce légèrement, dégraisse à l'alcool.
- **Époxy** (pas de cyano : cassant, ne comble pas les jeux — le jeu lèvre/muraille de ~1,5 mm est prévu pour le cordon).
- Presse avec pinces/élastiques, essuie le surplus, 24 h.
- Cordon de silicone lissé au doigt sur le joint extérieur pour finir.

Le joint est à **36-48 mm au-dessus de la flottaison** : même s'il suinte, ça ne coule pas.

**Pas d'époxy ?** Un **mastic-colle MS Polymer / polyuréthane** (Sikaflex, Fix'All…) fait aussi
bien, voire mieux ici : il accroche mieux le PETG, comble le jeu de 1,5 mm, encaisse les
vibrations d'hélice au lieu de casser net, et laisse 15-20 min de temps ouvert — indispensable
vu qu'il y a ~1,5 m de lèvre à encoller. **Ni cyano ni colle chaude** : la colle chaude fige en
30 s (impossible sur 1,5 m), n'accroche pas le PETG et flue sous charge permanente.

### La cloison avant (`13`) — À NE PAS OUBLIER

**Défaut du dessin v2, le plus grave :** à `x=95`, là où les étraves séparées rejoignent la
section à tunnel, il n'y a **aucune cloison**. Le compartiment électronique est **ouvert plein
nez** : 60,8 mm de large, 4,5 mm de haut dans l'axe et jusqu'à 15,5 mm sur les bords, soit
**≈5 cm² face à la marche**. Vérifié au lance-rayons : un rayon tiré de l'avant à z=83
**traversait tout le bateau sans rien toucher**. Ce n'est pas une fuite, c'est une **écope** :
38-42 mm au-dessus de la flottaison, donc rien au mouillage, mais tous les embruns dedans dès
que ça avance — et il n'y a **pas de nable** pour vidanger.

La cloison `13` la ferme (booléen sur la cavité réelle : elle épouse le dos du tunnel dessous,
les murailles sur les côtés, et affleure le dessous du pont).

- **Pose-la AVANT de coller le pont** — elle descend par le dessus, tu ne peux plus le faire après.
- **Colle-la à l'époxy/mastic sur ses 3 faces** (arche + 2 murailles), puis colle le pont
  par-dessus : le cordon du pont soude aussi son arête supérieure. C'est une pièce d'étanchéité,
  ne la pose pas « à sec ».
- Le jeu latéral de 0,3 mm est prévu pour le cordon.

### Les 2 bouchons d'étrave (`11`) — rustine

Défaut du dessin v2 : la cuve s'ouvre dès **x=22** alors que le pont ne commence qu'à **x=26**
→ il restait un **trou de 4 mm en travers de chaque étrave**. Les 2 bouchons TPU le comblent
(générés par booléen sur la cavité réelle : l'emprise est exacte au centième).

- **Pose-les avant de coller le pont**, à sec d'abord : ils descendent dans leur logement par
  le dessus. La collerette porte sur les 2 livets **et** sur l'étrave pleine en avant de x=22 —
  ils ne peuvent pas tomber dans la coque. Le dessus affleure le nez du pont (93,23 vs 93,24).
- Jeu de montage **0,2 à 0,6 mm par face** : ils descendent à la main, et le cordon a où aller.
- **PETG = même matière que la coque → soudables** au fer + filament, ou au mastic. *(Ils étaient
  en TPU en v2.1 : erreur. Un TPU 95A à 100 % dans un bloc de 6 × 27 × 5 n'absorbe rien, et
  surtout il ne se soude PAS au PETG — 30 à 50 °C d'écart de fusion.)*

Il reste un **second jour de 0,9 mm à l'arrière**, entre le bout du pont (296,5) et le tableau
(297,4). À cette largeur c'est un joint de colle, pas un trou : le cordon de mastic du pont le
remplit seul — rien à imprimer, mais ne l'oublie pas au collage.

> ### Tu réimprimes le pont ?
>
> Mets **`BOW_PATCH = False`** en tête de `generate_pieces.py` et régénère. **Seul le pont est à
> réimprimer** — la coque, les pylônes, tout le reste est conservé. Tu obtiens d'un coup :
>
> - **le pont rallongé** (22,3 → 297,1) : il couvre toute la cuve, les jours tombent à 0,30 mm
>   (le jeu de collage normal, pas un trou) → **la pièce `11` disparaît** ;
> - **la cloison avant venue de fonderie** : plus de collage sur 3 faces, position garantie
>   → **la pièce `13` disparaît**.
>
> Vérifié : pont `corps=1` (la cloison est bien fusionnée, pas posée à côté), `watertight`,
> `pont/coque = 0`, écoutille toujours ouverte.
>
> **Conséquence à l'impression :** la cloison descend sous la lèvre, le pont passe de 21 à 26 mm
> de haut et sa nervure avant surplombe le vide → **supports sous la cloison** en plus de ceux
> déjà prévus sous le pont.
>
> À l'inverse, tant que tu montes le pont imprimé en juillet 2026, **laisse `True`** : il faut
> alors les pièces `11` et `13`. Les deux modes s'excluent.

---

## 4. Hélices — le point à ne pas rater

**Forme des pales.** Pales **fines posées sur leur bord de fuite** : cette arête court sur le
plateau sur toute la longueur, la pale monte en rampe à 30° de calage. Seule l'arête (et un petit
méplat d'accroche) touche le plateau — le reste est en l'air. Il faut donc **un peu de support
court sous la pale**, mais les bords sont **épais et francs (~2,4 mm)**, si bien que le support se
détache sans déchirer — c'était ça le vrai problème de la première version, dont les bords en lame
tombaient à épaisseur nulle (trous, cordons, arête sale, balourd). Calage, corde, flèche et
épaisseur se règlent en tête de `generate_pieces.py` (`PROP_ALPHA`, `PROP_CH0/CH1`, `PROP_SWEEP`,
`PROP_TH`). Monter `PROP_ALPHA` vers 45° supprime le support (mais pas plus grossier) ; le
descendre affine le pas au prix de plus de support. **Ne jamais revenir à une section type
lentille** : bords à épaisseur nulle = trous garantis (piège n°19).

Les deux moteurs sont identiques et tournent dans le même sens. Deux hélices identiques =
les couples s'additionnent → lacet permanent, même à fond tout droit.

**La parade :**
1. Inverse les deux fils sur **un seul** moteur.
2. Monte-lui l'hélice **miroir** (`_CCW` au lieu de `_CW`).
3. Contre-rotation : les couples s'annulent, les deux poussent vers l'avant.

**Vérification obligatoire avant l'eau :** commande « avant », main derrière chaque hélice —
les deux doivent souffler **vers l'arrière**.

**Accouplement (broche à froid sur le pignon).** On **garde** le pignon métallique (Ø ≈ 7 mm)
sur l'axe : le moyeu de l'hélice a un alésage rond légèrement sous-coté (Ø 6,4 mm). On **presse**
le moyeu sur le pignon (à l'étau ou au serre-joint, bien droit) : les dents taillent leurs
cannelures dans le PETG → entraînement positif, auto-centré, **sans colle** ni méplat. Un lamage
d'amorce Ø 8 guide l'entrée ; le petit trou Ø 2,6 traversant sert de pilote et permet d'éjecter
l'hélice au chasse-goupille. Astuce : tremper le moyeu 30 s dans l'eau chaude ramollit le PETG
et facilite la presse (il durcit en refroidissant). Si trop dur → agrandir un peu (`GRIP_I`) ;
si ça tourne fou → réduire l'alésage. Une goutte de cyano dans les cannelures verrouille l'axial.

**Jamais de rotation sans les anneaux** — une hélice PETG à plusieurs milliers de tr/min coupe.

---

## 5. Montage mécanique

**Récupération sur la voiture** (photographie la carte avant de dessouder, garde du fil) :
2 moteurs sortis de leurs réducteurs (**pignon métallique conservé** — il sert d'accouplement
d'hélice, cf. §4), carte RC + antenne + connecteur batterie.

1. **Pont sur coque** (§3), laisse sécher.
2. **Pylônes** : glisse l'arrière de la bride sous la **griffe** du plateau (x = 240), puis
   **2 vis M3 à l'avant** — elles sont volontairement devant la nacelle, là où le tournevis
   passe verticalement. Toutes les vis du bateau sont **borgnes** : rien ne traverse vers l'eau.
3. **Anneaux** : 2 vis M3 chacun dans les pastilles du pont (x = 289) — à faire **avant** de
   monter les hélices. Les pattes longent l'extérieur du disque et ne rentrent qu'**sous** les pales.
4. **Moteur** — préparer le flasque arrière (côté déparasitage) AVANT le montage :
   - **coupe les 2 oreilles triangulaires** du flasque (ancienne fixation du réducteur, inutile) ;
   - replie les 2 selfs contre le flasque, **noie les soudures dans une goutte de colle chaude ou
     d'époxy** (anti-casse + isolation + étanchéité), **garde le condensateur** (déparasitage
     indispensable : sans lui le moteur brouille le récepteur AM 27/40 MHz) ;
   - clipse la bague fendue `06` (Ø24) autour du corps.
   Puis **engage le moteur par l'arrière ouvert du berceau, flasque arrière EN PREMIER dans la
   coiffe** — elle cache et protège le déparasitage (côté hélice laissé ouvert = le moteur respire,
   refroidi par l'aspiration de l'hélice). 2 colliers rilsan dans les fentes. **Fais glisser le
   moteur** pour centrer l'hélice dans l'anneau (x ≈ 280). Les fils sortent par le **bas ouvert de
   la coiffe** puis descendent le long du pylône.
5. **Hélice** pressée sur le pignon (broche à froid, cf. §4) — bien droite, à l'étau.
6. **Câblage** : fils moteurs le long du bord de fuite du pylône (collier), puis dans les
   **passe-fils Ø5,5** du pont (x = 254, ±22) → noix de silicone. Antenne : ressortie par le
   même passe-fils, scotchée en zigzag sous le livet ou le long du pont.
7. **Batterie + carte RC** par l'écoutille (108 × 72), **capot + joint TPU** : présente le
   capot incliné du nez (~20°), engage les **2 languettes avant** dans les poches de la
   plinthe, rabats, serre les **2 boutons moletés** arrière à la main. **Aucun outil.**

---

## 6. Batterie — le pack 6 V est mort

Le pack d'origine = 5 cellules NiMH 1,2 V.

**Solution : ton support 6 piles ENTIER + 5 AA NiMH + la pile factice** (`09`) dans le 6ᵉ
logement, avec une **vis M3 traversante** dans son perçage axial pour fermer le circuit.
6 V nominal, aucun risque pour la carte RC. Avec des AA 2000 mAh : ~35 min de navigation.

**Où il va :** il **ne rentre nulle part à plat** — c'est mesuré, et ça a coûté cher à trouver.
Le « compartiment central » n'existe pas (4,6 à 6,5 mm de haut), et le dôme du capot ne laisse
que **75 mm** de long alors que le bloc en fait 90. La solution qui marche : **le bloc entre par
l'écoutille et se coince incliné à ~45° dans UN flotteur**, dans le puits de sponson. Pas
d'assise, pas de carter imprimé, pas de contacts à inventer : le bloc du commerce fait le travail.

**Si tu tentes 7,2 V** (6 piles réelles) : poussée +44 % mais échauffement ×2. Le risque n'est
pas les moteurs (refroidis par l'hélice) mais **la carte RC**, seule pièce irremplaçable.
Si tu le fais : regénère les hélices avec `PROP_ALPHA1 = 12` (jamais au-dessus de 15° en 7,2 V),
et contrôle 30 s plein gaz main sur le moteur.
**Jamais 8 piles (9,6 V).**

### Conso : pourquoi les hélices sont vrillées, et comment les régler

Les premières hélices D100 avaient un calage **constant de 30°** sur toute la pale. Comme le pas
vaut `2πr·tan(calage)`, un calage constant fait grimper le pas linéairement avec le rayon :
**pas/D = 1,36**, soit 2 à 3 fois ce qu'encaisse un moteur de jouet en 6 V. Mesuré **3 A par
moteur**, la carte RC se mettait en sécurité.

Le couple absorbé est pondéré en **r³** : c'est le bout de pale qui coûte, pas l'emplanture. Les
hélices sont donc **vrillées** — 30° au moyeu (corde large, la rampe d'impression doit y rester
franche), **15° au bout**. Pas/D ramené à **0,84**, couple **÷2,2**, courant estimé **2,0-2,5 A**.

Le modèle est **ancré sur trois mesures réelles** : 6 V, **0,5 A à vide** (0,25 A après
lubrification), **3 A avec l'ancienne hélice**. Le courant à vide donne le couple de frottement,
ce qui élimine une inconnue. Reste la résistance série, balayée de 0,7 à 1,3 Ω — d'où la
fourchette.

À noter : **lubrifier n'a quasiment aucun effet sur ce problème** (0,25 A au lieu de 0,5 A à vide
ne déplace le résultat en charge que de 0,03 A). Ça soulage le moteur et c'est toujours bon à
prendre, mais le problème est bien dans l'hélice.

⚠️ Ces chiffres sortent d'un modèle (élément de pale + quantité de mouvement, à l'arrêt). Les
**rapports** entre deux hélices sont fiables ; les valeurs absolues le sont moins. **Contrôle à
l'ampèremètre en série avec un moteur, plein gaz, bateau tenu à la main.**

**Le diamètre reste à 95 mm** — c'était un choix, pas un oubli. Rétrécir l'hélice aurait marché
aussi, mais on perd deux fois : l'allure du bateau, et la **surface de disque**, qui est ce qui
donne la poussée à basse vitesse et donc l'autorité au différentiel (c'est en tournant de
grandes pales qu'il manœuvre). À 95 mm le disque ne perd que 10 % contre le D100 d'origine.

**Un seul bouton de réglage : le calage de bout** (`PROP_ALPHA1`). Le diamètre, la corde et les
anneaux ne bougent pas — si tu changes quelque chose, tu sais exactement quoi.

| Hélice D95 | pas/D | couple | poussée | courant |
|---|---|---|---|---|
| *(ancienne, 3 pales D100, 30° const.)* | 1,37 | réf | réf | **3,0 A mesurés** ← coupait |
| 3 pales, bout 15° | 0,84 | ×0,45 | ×0,82–1,04 | 2,0–2,5 A |
| **2 pales, bout 15° ← imprimée** | 0,84 | **×0,35** | ×0,69–0,95 | **1,7–2,3 A** |
| 2 pales, bout 12° | 0,75 | ×0,31 | ×0,62–0,89 | 1,6–2,2 A |

**Pourquoi 2 pales et pas 3.** Contre-intuitif, mais vérifié : à courant égal, une **bipale à 15°
pousse plus qu'une tripale à 10°** (×0,69–0,95 contre ×0,64–0,85). Retirer une pale enlève de la
solidité sans dégrader la géométrie des deux qui restent, alors que baisser le calage fait
travailler les trois à mauvais rendement — la traînée de profil, elle, ne baisse pas avec la
portance. Moins de matière, moins de temps d'impression, et le moteur respire.
*Si l'allure bipale ne te plaît pas : `PROP_NB = 3` en tête du script et tu retrouves la tripale
(colonne ci-dessus), au prix de ~0,3 A.*

**⚠️ Ne réduis PAS la corde pour gagner du courant.** `PROP_TH` est figée par l'impression, donc
une corde plus étroite **épaissit** la pale en relatif (t/c 23 % → 33 %) et la traînée annule le
gain : corde ×0,70 donne le *même* courant que la corde pleine, avec 20 % de poussée en moins.

**Deux choses contre-intuitives de plus :**

**1. Tu ne perds quasiment pas de poussée en dépitchant.** Le moteur *accélère* en retour, ce qui
compense. L'ancienne hélice **étranglait** le moteur — trop de pas pour lui, il ne montait jamais
en régime. Mauvais appariement : on perdait sur les deux tableaux à la fois.

**2. Le courant ne baisse que de ~20–30 %, pas de moitié.** Pour la même raison : le moteur qui
accélère continue de tirer du courant. **Diviser le couple par deux ne divise pas le courant par
deux** — et c'est pour ça que la géométrie seule ne suffit pas à garantir moins de 2 A.

### Descendre sous 2 A de façon SÛRE : la tension

La forme de l'hélice ne peut pas le garantir : au pire cas de la plage de résistance, la bipale
15° reste à 2,3 A. Le seul levier qui agisse **directement** sur le courant (et non via le
régime), c'est la **tension**.

Passe le pack à **4 × AA + 2 piles factices** (4,8 V) au lieu de 5 + 1 :

| Config | courant | poussée |
|---|---|---|
| 2 pales 15° à **6,0 V** | 1,7–2,3 A | ×0,69–0,95 |
| 2 pales 15° à **4,8 V** | **1,2–1,7 A** | ×0,46–0,69 |
| 3 pales 15° à **4,8 V** | 1,5–1,9 A | ×0,53–0,70 |

Zéro réimpression (imprime juste une 2ᵉ `09_pile_factice_AA`), réversible en 10 secondes, et ça
passe sous 2 A quelle que soit la résistance réelle. Le prix : la poussée retombe à la moitié.

**L'ordre de marche que je recommande :** monte la bipale 15° à 6 V, **mesure**. Une seule mesure
lève toute l'incertitude du tableau. Si tu es en dessous de 2 A, tu as gardé le maximum de
poussée. Sinon, retire une pile — c'est immédiat et ça ne coûte rien.

Il n'y a **que 2 STL** (CW et CCW) : les autres lignes sont une échelle, pas des fichiers. Pour
en changer, modifie `PROP_ALPHA1` en tête de `generate_pieces.py` et relance. En dessous de ~13°
la pale ne pousse plus grand-chose, au-dessus de ~22° tu retournes vers les ennuis de conso.

Le tableau **HÉLICES** affiché à chaque run recalcule corde et calage **depuis la géométrie
réellement générée**, pas depuis les paramètres.

---

## 7. Équilibrage et électronique

Le pack étant dans **un seul flotteur**, il faut le contrepoids dans l'autre. Deux règles :

1. **Le roulis ne dépend QUE du bras horizontal `y`.** Descendre un poids ne compense **rien**
   en roulis (ça aide la stabilité, c'est un autre sujet). Seul `m × y` compte.
2. **Pousse tout le plus à l'extérieur possible** — c'est le seul levier dont tu disposes.

Ce qui compte, c'est le **bras `y` du CENTRE DE GRAVITÉ du pack** — pas la coque où il finit.
Coincé en travers, à cheval sur l'écoutille et le puits, une bonne moitié de sa masse est encore
au-dessus du centre : il est **bien moins excentré qu'il n'en a l'air**.

Contrepoids nécessaire (pack 175 g, carte RC + fils 70 g, entraxe flotteurs 111 mm) :

| CG du pack à y= | Contrepoids à y=70 | à y=85 | Avec la seule carte RC (70 g) à y=85 |
|---|---|---|---|
| 30 | 75 g | 62 g | sur-corrige de 0,7° |
| **35** | **88 g** | **72 g** | **il reste 0,2° — nul** |
| 40 | 100 g | 82 g | 1,0° |
| 55 | 138 g | 113 g | 3,4° |

**En pratique : l'électronique seule, calée le plus à l'extérieur possible, suffit.** Pas de lest
à prévoir tant que le pack reste à cheval sur l'écoutille. Si tu le pousses plus loin dans le
flotteur, ajoute ~20-40 g. **Le vrai contrôle, c'est l'eau** : mets-le à flot et regarde.

**Assiette longitudinale :** le CG tombe ~10 mm en arrière du centre de poussée. Ajuste sur
l'eau en glissant le pack ; la flottaison doit être parallèle (une légère assiette arrière est
acceptable, elle aide au déjaugeage).

**Câblage :** connecteur récupéré du pack Nikko — c'est **lui** qu'on débranche, jamais les fils.
Rilsan autour du boîtier en anti-traction, à 2 cm des soudures.

### Le joint de capot `04` — ne l'imprime pas

**Il ne sert à rien, deux raisons, toutes deux vérifiées :**

1. **Rien ne le loge.** La plinthe est un plan lisse, aucune rainure. Et la bride du capot
   (76 × 58) **déborde le joint de 12 mm** : elle ne le pince même pas latéralement. Il est posé
   libre entre deux plans — il glisse.
2. **Il force à la fermeture.** Le modèle prétend que ses 2 mm sont pris en compte, mais il reste
   un recouvrement pont/capot que le seuil de contrôle (0,05 cm³) classait « ok ».

Il n'a **jamais figuré dans le tableau des collisions** : jamais testé. Le capot ferme mieux sans.
Si tu veux un jour une vraie étanchéité de capot, il faut une **rainure dans la plinthe** — donc
réimprimer le pont.

- La bride déborde le joint de tous côtés : l'eau ruisselle, ne rentre pas par la tranche.
- Après chaque sortie : capot ouvert, éponge s'il le faut — pas de nable de vidange, c'est voulu
  (aucun perçage sous la flottaison).

---

## 8. À quoi t'attendre

- **Poussée modeste** : une hélice aérienne pousse bien moins qu'une immergée. Vif, pas puissant.
- **Tout-ou-rien** (27/40 MHz) : pas de dosage, virages secs, ligne droite en léger zigzag.
- **Il dérape en virage.** C'est le charme du truc.
- **Marche arrière inutile** : pales profilées dans un sens, la poussée s'effondre en reculant.
  Sers-t'en pour pivoter, pas pour naviguer.
