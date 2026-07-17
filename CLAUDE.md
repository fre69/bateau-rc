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
- **Pack 6 V NiMH mort** → 5× AA NiMH + pile factice imprimée dans un support 6 piles
  **du commerce (90×55×15)**, coincé à ~45° dans un puits de sponson (piège 17).
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
PROP_ALPHA=30  hélices : pale fine posée sur son bord de fuite (rampe) ; PROP_TH=2.8 épaisseur ;
             PROP_CH0/CH1 corde emplanture/bout ; PROP_SWEEP flèche ; PROP_FOOT méplat. Support court. Piège 19.
BOW_PATCH    True = bateau déjà imprimé (pont 26→296.5 + bouchons PETG pièce 11) ;
             False = nouvelle impression (pont rallongé 22.3→297.1, pas de bouchons). Piège 16.
BKX0/BKX1=95→110, BKGAP=0.3   cloison avant (pièce 13) : ferme le compartiment, ouvert
             plein nez à XJ. Sa largeur SUIT yi_cav(x) — pas de valeur figée. Piège 18.
Piles : AUCUNE pièce. Le support 6 piles du commerce se coince à 45° dans un puits de
             sponson, contrepoids en face. Le compartiment central fait 5 mm. Piège 17.
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

16. **Le pont ne couvrait pas toute la cuve — et AUCUN contrôle ne l'a vu.** La cavité s'ouvre
    dès `x=22` (`XNi`) alors que le pont ne commençait qu'à `x=26` (`make_deck`) : il restait un
    **trou de 4 mm en travers de chaque étrave**, plus 0,9 mm à l'arrière (pont 296,5 / tableau
    297,4). Coque et pont étaient chacun parfaitement manifold, et **le tableau du piège 15 ne
    teste que les RECOUVREMENTS, jamais les MANQUES** : un trou ne déclenche rien. C'est
    l'utilisateur qui l'a vu à l'œil, une fois les pièces imprimées.
    Corollaire : **quand une pièce en couvre une autre, comparer leurs emprises** — un `bounds`
    des deux pièces l'aurait attrapé en une ligne (`pont X 26→296.5` vs `cavité X 22→297.4`).
    Les deux traitements sont câblés sur l'interrupteur **`BOW_PATCH`** (en tête du script) —
    ils **s'excluent**, ne jamais les cumuler :
    - **`True` (défaut) = le bateau déjà imprimé (juillet 2026).** Pont court (26 → 296,5) +
      `11_bouchon_etrave_x2`, dessiné **par booléen sur la cavité**, en PETG (même matière que
      la coque → soudable) avec `PLGAP=0.3` de jeu par face. ⚠️ **Ne jamais livrer un booléen sur
      la cavité SANS jeu** : c'était le cas en v2.1, « justifié » par un TPU censé absorber — sauf
      qu'un TPU 95A à 100 % dans un bloc trapu est rigide, et qu'il **ne se soude pas au PETG**. Ne pas y toucher tant qu'on veut des STL compatibles avec
      ces coques. Sa collerette porte sur les livets **et** sur l'étrave pleine : les parois de
      la cuve y sont quasi verticales (21,95 → 21,33 mm sur 6 mm), un téton seul tomberait dedans.
    - **`False` = nouvelle impression complète.** Pont rallongé (22,3 → 297,1), jours ramenés à
      **0,30 mm** — soit le jeu de collage que le pont a déjà sur les côtés, donc un trait de
      colle et non un trou. Pas de bouchons (ils percuteraient le pont). Vérifié : `pont/coque`
      = 0, et le garde-fou `ye-yi < 12` de `deck_sect_nose` ne se déclenche pas (25,4 mm à x=22,3).

17. **Le « compartiment central » du MONTAGE v2 n'existait pas — et j'ai perdu une demi-journée
    à essayer de le remplacer.** Le texte décrivait un logement « entre le plafond du tunnel et le
    pont » pour le pack et la carte RC. Mesuré : **4,6 à 6,5 mm de haut** dans l'axe. Rien n'y entre.
    **Ce que le tableau COLLISIONS ne teste pas :** il ne voit que les pièces **générées**. Pack,
    carte RC, connecteur, câbles, **et même le joint `04`** (jamais mis dans `asm`) échappent à
    toute vérification. La notice a donc pu décrire pendant des mois un montage impossible.
    **Modéliser les objets embarqués, ne serait-ce qu'en boîtes, et les passer au tableau.**
    **Les erreurs de méthode à ne pas refaire (toutes commises ici) :**
    - **N'avoir mesuré que l'axe `y=0`.** L'arche y remonte à 79 → « 5 mm, rien ne rentre ». Faux :
      le volume est **à côté de la bosse**. Sous l'écoutille, à `|y|≈30`, le fond tombe à **z≈17** —
      75 mm sous la plinthe. **Cartographier le vide sur une grille (x,y) AVANT de dessiner.**
    - **Avoir posé l'assise SUR l'écoutille** alors que c'est un **trou traversant** : 9,3 mm de
      puits (plinthe 93,7 → dessous du pont 84,4) purement gaspillés.
    - **Avoir jugé des affleurements avec un seuil réglé pour des collisions franches.** À 0,05 cm³,
      une pièce qui mord 0,3 mm dans la plinthe passe pour « ok ». Pour un contact plan, afficher
      le volume réel, pas un verdict.
    - **Avoir validé un carter sans modéliser les contacts.** Gorges de 50,9 pour des piles de 50,5
      → 1,75 mm par bout, un ressort en demande 5-6. Collisions à zéro parce que seules les piles
      étaient modélisées.
    **Solution retenue (v2.1) :** aucune pièce imprimée. Le support 6 piles du commerce entre par
    l'écoutille et se **coince incliné à ~45° dans un puits de sponson**, contrepoids dans l'autre.
    C'est l'utilisateur qui l'a trouvée pendant que je cherchais à tout poser à plat.
    Cotes utiles si le sujet revient : dôme du capot = 87 × 59 au mieux (à +13 mm de la plinthe),
    **longueur max 75 mm** ; rebord de plinthe porteur = **2,0 mm** ; l'écoutille ne passe à plat
    qu'un rectangle **76 × 51**.

18. **Le compartiment était OUVERT PLEIN NEZ à `XJ` — le pire défaut du lot, et le même que le
    n°16.** À `XJ=95`, les étraves séparées rejoignent la section à tunnel : `XA` (enveloppe)
    **et** `XAi` (cavité) démarrent tous deux exactement à `XJ`, donc la soustraction ne laisse
    **aucune cloison** sur la face avant du pont-bras. Trou de **60,8 × 4,5-15,5 mm ≈ 5 cm²**,
    orienté vers l'avant. Fermé par `13_cloison_avant` (booléen sur la cavité réelle), à coller
    avec le pont.
    - **La leçon qui compte : j'avais corrigé le n°16 sans vérifier l'AUTRE raccord de lofts.**
      Un bug de ce type n'est jamais isolé — il y a un raccord à `XJ` et un à chaque bout. Après
      toute correction de ce genre, **passer en revue TOUS les raccords** (`XN/XA`, `XNi/XAi`,
      nez/arrière du pont).
    - **L'INTRADOS DU PONT N'EST PAS A `sheer`.** `deck_loop` pose le dessous a `sheer + crown(y)`
      — la dalle est bombee, elle remonte de **5 mm dans l'axe**. Une piece butee sur `sheer`
      laisse un jour de 5 mm sur 60 de large. **Ne pas DEVINER ou s'arrete le pont : le
      SOUSTRAIRE** (`D([piece, deck])`). Corollaire pour l'integrer au pont : il faut au contraire
      qu'elle MORDE dedans (`up>0`), sinon les surfaces se touchent sans se recouvrir et l'union
      ne fusionne pas -> `corps=2`, la piece sort separee sur le plateau. **Toujours verifier
      `corps=1` apres une union censee fusionner.**
    - Piege dans le piege : un loft interpole **en lignes droites** entre ses stations et passe
      donc SOUS la courbe visee (91,86 mesure contre 92,19). Viser franchement trop haut et
      laisser la soustraction donner la cote.
    - **MES OUTILS DE CONTROLE ONT TOUS MENTI ICI, chacun pour une raison differente. A relire
      avant d'en refaire un :**
      * **Rayons / `contains` sur `U([coque, pont])`** : les deux solides se **touchent sans se
        recouvrir** -> union degeneree -> resultats incoherents (`contains`=PLEIN la ou les rayons
        disent VIDE). **Ne jamais unir des solides jointifs pour tester ; tester chaque maillage
        separement** (`a.contains(p) | b.contains(p)`).
      * **Rayons tires seulement sous le livet** (z=83-87) : ils ont declare « bouche » un trou qui
        beait de 87 a 92. **Balayer TOUTE la hauteur du compartiment, bouge compris.**
      * **Diffusion sans le capot** : l'ecoutille est un trou par construction, l'eau y entre
        toujours -> « ouvert » quoi qu'on fasse. **Boucher l'ecoutille avec un couvercle fictif**
        pour isoler la question posee.
      * **Diffusion au pas de 1,5 mm sur des parois de 1,6 mm** : elle traverse les murailles sans
        les voir. **Le pas doit etre tres inferieur a `T`.**
      * **Volume residuel booleen** : comptait comme « trou » le vide **au-dessus** du pont.
    - **Ce qui a marche, a chaque fois : le RENDU en coupe** (piege 9). Les trois defauts trouves
      ce jour-la l'ont ete a l'oeil — deux par l'utilisateur, sur photo. **Regarder la piece.**
    - Correctif propre pour une v2 (non implémenté) : faire démarrer `XAi` à `XJ+T` **et**
      prolonger `XNi` jusqu'à `XJ+T`, de sorte que seule la région pont-bras (|y| < yi) reste
      pleine → cloison de 1,6 mm venue de fonderie, sponsons toujours creux. Vérifier alors que
      `13` est bien supprimée (elle entrerait en collision).

19. **Les hélices — TROIS refontes, et la leçon = ne pas passer d'un extrême à l'autre.**
    Chaque étape a un piège distinct ; c'est l'utilisateur qui a recadré à chaque fois.
    - **Étape 0 — calage inversé (`sin`/`cos`).** `beta = atan2(P, 2πr)` est mesuré **depuis le
      plan de rotation** : la corde se projette en `cos(beta)` sur le tangentiel, `sin(beta)` sur
      l'axial. Le code faisait l'inverse → calage `90−beta`, 77° en bout au lieu de 13°, pas réel
      de 1310 mm pour 72 visés. Maillage watertight, 1 corps, volume plausible : **rien** ne l'a
      vu, et le tableau COLLISIONS n'avait **aucune paire `helices/*`**. Vu par l'utilisateur dans
      le slicer. Test qui tue : recalculer `2πr·tan(calage)` depuis la géométrie et comparer à
      `0.72·D`.
    - **Étape 1 — le vrai problème était le PROFIL, pas le calage.** La pale était une **lentille
      dont l'épaisseur tombe à ZÉRO au bord** (`th/2·sqrt(1-(2s)²)`). À 1 mm du BF en bout :
      **0,73 mm**, < 2 extrusions → ni périmètre ni remplissage → trous, cordons, arête sale,
      balourd. **Ce n'est pas le support qui perçait les pales : il n'y avait rien à percer.** Deux
      impressions ratées. Leçon : **une pale FDM se juge à l'épaisseur de ses bords** — tout bord
      < ~0,9 mm (≈2 extrusions) est un trou en puissance.
    - **Étape 2 — MA SUR-CORRECTION : le coin plein.** J'ai fait un `blade_wedge_sec` à **fond
      plat 100 % posé sur le plateau**. Zéro support, oui, mais **dessous rugueux** (plateau
      texturé) et pale pleine. L'utilisateur : « tu vas d'un extrême à l'autre » — la lentille
      était 100 % en l'air, le coin 100 % sur le plateau. **Piège de méthode : quand on corrige un
      défaut, viser le POINT MILIEU, pas le défaut opposé.**
    - **Étape 3 (RETENUE) — pale FINE posée sur son BORD DE FUITE.** `blade_ramp_sec` : plaque
      mince (`PROP_TH=2.8` vert. ≈ 2,4 mm perp.) dont le BF est une **ligne à z=0** sur toute
      l'envergure ; la pale monte en rampe au calage `PROP_ALPHA=30°`, petit méplat `PROP_FOOT`
      sous le BF pour la 1re couche. **Seule l'arête touche le plateau** ; le dessous (à 30°)
      demande **un peu de support COURT (≤11 mm)**, mais les bords épais et francs font qu'il
      **se détache sans déchirer**. C'est l'entre-deux voulu. Volume ~10 cm³ (entre 7 lentille et
      13 coin). `PROP_ALPHA→45°` = zéro support (pas grossier) ; `→20°` = pas fin, plus de support.
    - Paires `helices/anneaux` et `helices/pylones` désormais dans le tableau COLLISIONS (garde
      bout de pale ≈5 mm, `ri=pd/2+5`). ⚠️ Le `except: v=0.0` du tableau affiche « ok » quand le
      booléen **échoue** : un contrôle qui ne peut pas échouer ne contrôle rien.

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
