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
| Hélices | 3 pales cimeterre, D100 (6 V) ou D90 (7,2 V), pas 0,72 D |
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
| `07_anneau_protection_D100` ou `_D90` | **2** | PETG | Exporté **à plat** : anneau et pattes sur le plateau, les deux tours de fixation montent verticalement. 4 périmètres, 40 %. Prends le diamètre assorti à tes hélices. |
| `08_helice_*_CW` + `*_CCW` | 1 de chaque | PETG | Exporté **à plat, gros alésage Ø6,4 (face moteur) contre le plateau** — garde ce sens. 4 périmètres, 40 %, couches 0,12 mm. Le dessous des pales est un surplomb de 13° (bout) à 46° (pied) : **inévitable sur toute hélice**, aucune orientation n'y échappe. Le retourner ne change rien à l'aire en surplomb (2012 vs 2010 mm² — le profil de pale est symétrique, retourner échange les deux faces sans changer une pente) et coûte **27 % de support en plus** (11 995 vs 9 480 mm³). **Réglages qui décident du démoulage, en PETG :** **couches d'interface = 0** (l'interface est quasi pleine et se soude à la pale — c'est *la* raison des supports impossibles à retirer) et **distance Z supérieure = 0,24 mm**, pas 0,2 : le slicer arrondit cet écart à un multiple de la couche, et 0,2 retombe à 0,12 = une seule couche de vide, qui colle. Support « sur le plateau uniquement » (sans effet ici — rien ne surplombe une autre pale — mais c'est la ceinture) ; XY 0,35-0,4 ; densité 8-10 %. Colonnes ≤ 12 mm : elles cassent au doigt. |
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
Si tu le fais : hélices **D90** + anneaux D90, et contrôle 30 s plein gaz main sur le moteur.
**Jamais 8 piles (9,6 V).**

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
