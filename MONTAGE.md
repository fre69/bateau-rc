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
| `05_pylone_moteur` | **2** | PETG | Debout (bride en bas), **support sous la nacelle**. 4 périmètres, 40 %. |
| `06_bague_moteur_XX` | 2 (ta taille) | TPU | 100 % — souple et adhérente. Berceau Ø32,4 ; bagues pour moteurs Ø24 / 27,7 / 30. |
| `07_anneau_protection_D100` ou `_D90` | **2** | PETG | Exporté **à plat** : anneau et pattes sur le plateau, les deux tours de fixation montent verticalement. 4 périmètres, 40 %. Prends le diamètre assorti à tes hélices. |
| `08_helice_*_CW` + `*_CCW` | 1 de chaque | PETG | À plat, 4 périmètres, 40 %, couches 0,12 mm. |
| `09_pile_factice_AA` | 1 | PETG | 100 %. |
| `10_bouton_capot` | **2** | PETG | À plat, 100 %. Vis M3 (~16 mm) collée dedans à la cyano → bouton moleté. |

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

Alésage : mesure l'axe moteur (2,0 / 2,3 / 3,17 mm) et prends le fichier correspondant.
En cas de doute, prends l'alésage en dessous et alèse au foret.

**Jamais de rotation sans les anneaux** — une hélice PETG à plusieurs milliers de tr/min coupe.

---

## 5. Montage mécanique

**Récupération sur la voiture** (photographie la carte avant de dessouder, garde du fil) :
2 moteurs sortis de leurs réducteurs (**pignon retiré**), carte RC + antenne + connecteur batterie.

1. **Pont sur coque** (§3), laisse sécher.
2. **Pylônes** : glisse l'arrière de la bride sous la **griffe** du plateau (x = 240), puis
   **2 vis M3 à l'avant** — elles sont volontairement devant la nacelle, là où le tournevis
   passe verticalement. Toutes les vis du bateau sont **borgnes** : rien ne traverse vers l'eau.
3. **Anneaux** : 2 vis M3 chacun dans les pastilles du pont (x = 289) — à faire **avant** de
   monter les hélices. Les pattes longent l'extérieur du disque et ne rentrent qu'**sous** les pales.
4. **Moteur** dans le berceau : bague `06` à ta taille, 2 colliers rilsan dans les fentes.
   **Fais glisser le moteur** dans le berceau pour centrer l'hélice dans l'anneau (x ≈ 280).
5. **Hélice** sur l'axe, à force (goutte de cyano si lâche).
6. **Câblage** : fils moteurs le long du bord de fuite du pylône (collier), puis dans les
   **passe-fils Ø5,5** du pont (x = 254, ±22) → noix de silicone. Antenne : ressortie par le
   même passe-fils, scotchée en zigzag sous le livet ou le long du pont.
7. **Batterie + carte RC** par l'écoutille (108 × 72), **capot + joint TPU** : présente le
   capot incliné du nez (~20°), engage les **2 languettes avant** dans les poches de la
   plinthe, rabats, serre les **2 boutons moletés** arrière à la main. **Aucun outil.**

---

## 6. Batterie — le pack 6 V est mort

Le pack d'origine = 5 cellules NiMH 1,2 V. Tu n'as que des supports 6 ou 8 piles.

**Solution : support 6 piles + 5 AA NiMH + la pile factice** (`09`) dans le 6ᵉ logement,
avec une **vis M3 traversante** (ou fil rigide) dans son perçage axial pour fermer le circuit.
6 V nominal, aucun risque pour la carte RC. Avec des AA 2000 mAh : ~35 min de navigation.

**Si tu tentes 7,2 V** (6 piles réelles) : poussée +44 % mais échauffement ×2. Le risque n'est
pas les moteurs (refroidis par l'hélice) mais **la carte RC**, seule pièce irremplaçable.
Si tu le fais : hélices **D90** + anneaux D90, et contrôle 30 s plein gaz main sur le moteur.
**Jamais 8 piles (9,6 V).**

**Équilibrage :** le calcul donne un centre de gravité ~6 mm en arrière du centre de poussée →
**pack de piles à fond en AVANT du compartiment**. Ajuste ensuite sur l'eau : la ligne de
flottaison doit être parallèle (une légère assiette arrière est acceptable, elle aide au déjaugeage).

---

## 7. Protection de l'électronique — et accès piles sans outil

Compartiment central entre le plafond du tunnel et le pont, fermé par la capsule.

- Le capot repose sur une **plinthe plane** moulée dans le pont (inclinée avec la tonture) :
  joint TPU `04` entre les deux. Verrouillage **sans outil** : 2 languettes avant + 2 boutons
  moletés `10` à l'arrière (vis M3 borgnes dans la plinthe).
- **L'électronique ne se démonte jamais** : carte RC collée au velcro à demeure ; boîtier de
  piles sur son propre velcro, relié par le **connecteur récupéré du pack Nikko**. Les 2 fils
  fragiles du boîtier : un **rilsan autour du boîtier** en anti-traction, à 2 cm des soudures —
  c'est le connecteur qu'on débranche, jamais les fils.
- **Routine recharge** : 2 boutons à la main → capot basculé → les 5 AA se retirent **une à
  une, boîtier en place** (son dessus affleure l'écoutille ; laisse la factice à sa place).
  Recharge au chargeur de piles, remontage inverse. Aucun outil, aucun fil sollicité.
- **Le boîtier lui-même** ne sort qu'au premier montage ou pour réparation : à plat il ne
  passe PAS par l'écoutille (le plus grand rectangle qui passe à plat fait 76 × 51 mm).
  Méthode : **sur chant** (95 × 19), descendu le long du bord latéral de l'écoutille dans le
  puits du sponson, puis basculé à plat sur l'arche. Brancher le connecteur après.
- La bride déborde le joint de tous côtés : l'eau ruisselle, ne rentre pas par la tranche.
- Hauteur utile : support 6 piles (17 mm) + carte RC empilée passent large (~30 mm de marge).
- Après chaque sortie : capot ouvert, éponge s'il le faut — pas de nable de vidange, c'est voulu
  (aucun perçage sous la flottaison).

---

## 8. À quoi t'attendre

- **Poussée modeste** : une hélice aérienne pousse bien moins qu'une immergée. Vif, pas puissant.
- **Tout-ou-rien** (27/40 MHz) : pas de dosage, virages secs, ligne droite en léger zigzag.
- **Il dérape en virage.** C'est le charme du truc.
- **Marche arrière inutile** : pales profilées dans un sens, la poussée s'effondre en reculant.
  Sers-t'en pour pivoter, pas pour naviguer.
