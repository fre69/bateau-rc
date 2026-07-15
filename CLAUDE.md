# CLAUDE.md — Catamaran RC à hélices aériennes

Générateur paramétrique de pièces imprimables pour un catamaran à tunnel, propulsé par
deux hélices aériennes, construit à partir de la récup d'une voiture-jouet **Nikko N-Blaster**.
Design v2 (juillet 2026) : refonte complète — étraves inclinées, tonture classique, spray-rails,
capsule cockpit sur plinthe plane, pylônes profilés, anneaux-conduits.

## Contexte matériel (non négociable, c'est de la récup)

- **2 moteurs brossés** (un par côté, skid-steer) sortis de leurs réducteurs. **Pignon
  métallique Ø7 conservé sur l'axe (2,3 mm)** : il sert d'accouplement d'hélice (moyeu broche
  à froid, alésage Ø6,4 sous-coté — voir `make_prop` et `PIGN_D`/`GRIP_I`). Pas de méplat ni colle.
- **Carte RC 27/40 MHz** : commande **tout-ou-rien**, pas de proportionnel. Pièce irremplaçable.
- **Pack 6 V NiMH mort** → 5× AA NiMH + pile factice imprimée (support 6 piles).
- Pas d'achat en ligne : imprimante FDM, PETG, TPU 95A, visserie M3, rilsan.
- Imprimante : **Elegoo Neptune 4 Plus**, plateau 320 × 320.

Conséquence : **pilotage différentiel** (deux hélices, pas de gouvernail), hélices
**contre-rotatives** (une CW, une CCW, fils inversés sur un moteur), sinon les couples
s'additionnent et le bateau part en lacet en ligne droite.

## Fichiers

| Fichier | Rôle |
|---|---|
| `generate_pieces.py` | **Source unique de vérité.** Génère les 24 STL, l'assemblage, les rendus et les vérifications. Tout est paramétrique. |
| `stl/` | Sortie (pièces en orientation d'impression). Ne pas éditer à la main. |
| `stl/_assemblage/` | STL en repère bateau + `assemblage.scad` + vues PNG (régénéré à chaque run). |
| `apercu_assemblage.scad` | À ouvrir dans OpenSCAD pour orbiter autour du bateau complet. |
| `apercu_catamaran.png` | Planche de contrôle 4 vues. |
| `MONTAGE.md` | Notice utilisateur (impression, collage, câblage, mise à l'eau). |

Régénérer : `python generate_pieces.py` (Windows, Python 3.14).
Deps : `trimesh manifold3d shapely numpy scipy networkx rtree pillow mapbox_earcut`.
Rendus via **OpenSCAD Nightly** (`C:\Program Files\OpenSCAD (Nightly)\openscad.exe`) ; sans lui
le script génère quand même tous les STL.

## Repères et conventions

- **X** = étrave (0) → tableau arrière (300). **Y** = travers. **Z** = haut, 0 = quille. Cotes en **mm**.
- Coque par **loft de sections** (`sect_nose` ×2 miroir en avant de `XJ=95`, `sect_full` avec
  tunnel en arrière), puis `coque = extérieur − cavité_intérieure`.
- **Plan de montage commun** `ZMOUNT=88.5` : plateaux des pylônes et pastilles des anneaux
  sont des assises PLANES générées dans le pont. La plinthe du capot est un plan incliné
  (`Z0SEAT`, `KSEAT`) qui suit la tonture. **Jamais de bride plate posée sur le bouge du pont.**
- Axe hélices = `ZMOUNT + MOT_Z` = 164,5 au-dessus de la quille.

## Paramètres principaux (en tête de `generate_pieces.py`)

```
L=300        longueur ; SY=55.5 axe sponson (entraxe 111) ; BS=32.5 demi-largeur
CH=20        bouchain (plafonné près de l'étrave par ch_eff) ; CFL spray-rail ; FL flare
T=1.6        paroi (4 périmètres) ; DKT=2.2 pont ; LIP=6 lèvre d'emboîtement
SH_AFT=82 / SH_BOW=94   tonture (haute à l'étrave) ; STEMH/XSTEM étrave inclinée
tunz()       plafond de tunnel 70→58 ; ARCH=11 cambrure
HX=155       écoutille 108×72 ; plinthe SEATA/SEATB ; vis capot ±52/±34
PYX=240, PYY=66   pylônes (ce sont EUX qui écartent les hélices) ; MOT_Z=76
GDX=275      anneaux ; SADDLE_ID=32.4 berceau (bagues TPU 24/27.7/30)
```

## Pièges déjà rencontrés — à ne pas refaire

1. **La cavité intérieure doit être retraitée en X aussi.** Si elle va de 0 à L comme
   l'enveloppe, la soustraction emporte l'étrave et le tableau. Actuel : cavité de 22 à L−2,6,
   pont de 26 à 296,5 (la lèvre ne doit jamais descendre dans une zone pleine).

2. **Pour ouvrir le dessus de la cuve : montant VERTICAL, pas un étirement** (`raise_top`).
   Étirer le point haut change la pente de toute la muraille → éclats sur le livet.

3. **`is_watertight` / `open_edges` ne prouvent RIEN sur la validité de la pièce.**
   Un solide auquel il manque le tableau arrière est parfaitement fermé et manifold.
   **Toujours regarder la pièce** — y compris en coupe (voir piège 9).

4. **matplotlib `Poly3DCollection` ment sur les formes concaves.** Ne jamais conclure d'un
   rendu matplotlib. Utiliser les rendus OpenSCAD du script (ou le slicer).

5. **`fix_normals()` après un booléen qui crée une cavité fermée** retourne les normales de
   la cavité → volume faux, cavité perdue. Manifold sort des normales correctes, ne pas « corriger ».

6. **Miroir** : `apply_scale([1,-1,1])` inverse les faces → `fix_normals()` obligatoire,
   sinon « Not all meshes are volumes ».

7. **`trimesh.creation.revolve` peut sortir un solide à normales inversées** (volume négatif)
   selon l'orientation du profil. Tester `volume < 0` → `invert()`.

8. **Points consécutifs dupliqués dans une section = loft non manifold.** `seg()` exclut son
   premier point ; toute liste inversée réinjecte son extrémité → la tronquer (`[1:]`).
   Symptôme : « Not all meshes are volumes » sur l'union des lofts.

9. **OpenSCAD en preview (F5) rend BLANC les booléens sur des STL importés.**
   Pour les coupes de contrôle : `--render --backend=Manifold`. Les imports simples passent en preview.

10. **Étrave haute** : près de la pointe, la quille remonte → le bouchain (`kz+CH`) passerait
    au-dessus de la zone liston → sections auto-intersectées. D'où `ch_eff(x)`.

11. **Toute interface plane (bride capot, pied de pylône, patte d'anneau) exige une assise
    plane dans le pont** (plinthe, plateau, pastille) — posée sur le bouge, elle bascule de 2-3 mm.
    La v1 avait aussi les trous de vis du capot HORS de sa bride (jamais vérifiés) : recouper
    les positions de vis avec l'empreinte réelle des deux pièces.

12. **Vérifier l'accessibilité OUTIL des fixations, pas seulement leur position.** Les vis
    avant du capot v2.0 étaient géométriquement correctes mais dans le congé bride/dôme :
    aucun tournevis ne passait. Même piège sur les vis arrière des pylônes, sous les flancs
    du berceau. D'où le système actuel : capot = languettes avant + 2 boutons moletés ;
    pylône = griffe arrière + 2 vis avant ; anneaux vissés AVANT de monter les hélices.

13. **L'écoutille elliptique ne laisse passer à plat qu'un rectangle a√2 × b√2**
    (76 × 51 pour 108 × 72). Le boîtier 6 piles de 95 × 50 n'entre que sur chant, par le
    puits d'un sponson. Vérifier le passage de TOUT objet embarqué ; les piles, elles, se
    changent boîtier en place (son dessus affleure l'écoutille).

14. **Boucher un loft par un éventail depuis le centroïde est interdit sur une section
    CONCAVE** (tunnel, raise_top, lèvre du pont) : les triangles du bouchon se chevauchent
    et se retournent dans le plan, et manifold3d ressort du bruit déchiqueté sur TOUTE la
    dernière travée du loft (paroi pincée < 0,5 mm → trous au slicing, vus à l'arrière,
    à XJ et aux pointes d'étraves). `loft()` triangule ses bouchons par earcut
    (`mapbox_earcut`), orienté par aire signée. Les solides d'entrée paraissaient sains
    (coupes propres, watertight) : le défaut n'apparaissait qu'APRÈS le booléen.

15. **Le tableau COLLISIONS D'ASSEMBLAGE du run doit rester à ~0** (seuil 0,05 cm³).
    C'est lui qui a attrapé : la muraille à double épaisseur (offset `o` soustrait deux fois
    dans `ye`), la plinthe plongeant dans les murs d'étraves, les bouts de pattes d'anneau
    raclant le bouge, et les bossages d'anneaux dans la muraille (d'où `GFY=16`).

## Contraintes de conception à respecter

- **Pont imprimé à part**, collé (époxy), lèvre de 6 mm ; joint à 36-48 mm au-dessus de la
  flottaison, jamais immergé.
- **Coque quille en bas** : supports uniquement dans le tunnel + sous les pointes d'étraves.
- **Aucun perçage traversant** vers l'eau : toutes les vis (pylônes, anneaux, capot) vont dans
  des **trous borgnes** d'assises du pont. Pas de nable de vidange (séchage par l'écoutille).
- **Pattes d'anneau** : le long de l'anneau à l'extérieur du disque balayé, elles ne rentrent
  qu'une fois passées **sous** les pales.
- Anneaux exportés **à plat** (posés sur chant ils sont inimprimables).
- Après toute modif, relire la sortie du script : **garde sous tunnel > 10 mm**,
  **franc-bord arrière > 35 mm**, delta CG–CB raisonnable (compensable en glissant le pack).
- Valeurs de référence v2 : tirant ≈45 mm, garde ≈13 mm, franc-bord 49/37 mm, ~1150 g.

## Style de travail attendu

L'utilisateur est technique, va droit au but, et **repère les défauts géométriques mieux que
les contrôles automatiques**. Quand il signale un problème visuel, le croire et aller regarder
la pièce — pas répondre avec des statistiques de maillage.
