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
PROP_ALPHA0/1=30/15  hélices : pale fine posée sur son bord de fuite (rampe), VRILLÉE de
             l'emplanture au bout. PROP_TH=2.8 épaisseur ; PROP_CH0/CH1 corde ; PROP_SWEEP flèche ;
             PROP_FOOT méplat. Support court. Piège 19.
PROP_D=95    diamètre FIGÉ (le D100 tripale à calage constant tirait 3 A → carte RC en sécurité).
             Leviers de conso, dans l'ordre d'efficacité : PROP_NB (3→2 pales, le meilleur),
             PROP_ALPHA1, puis la TENSION (4×AA=4,8 V) qui seule garantit < 2 A. JAMAIS la corde
             (PROP_TH figée → t/c dégradé, gain nul). On n'exporte que 2 STL (CW+CCW) ;
             PROP_LADDER n'est qu'un affichage. Pièges 20 et 21.
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
      *(Depuis le piège 20, `PROP_ALPHA` est devenu `PROP_ALPHA0`/`PROP_ALPHA1` : calage vrillé.)*
    - Paires `helices/anneaux` et `helices/pylones` désormais dans le tableau COLLISIONS (garde
      bout de pale ≈5 mm, `ri=pd/2+5`). ⚠️ Le `except: v=0.0` du tableau affiche « ok » quand le
      booléen **échoue** : un contrôle qui ne peut pas échouer ne contrôle rien.

20. **Le calage CONSTANT était un pas de 1,36·D — 3 A par moteur, carte RC en sécurité.**
    Quatrième passe sur les hélices, et **le seul défaut trouvé par la MESURE ÉLECTRIQUE**, pas par
    l'œil ni par la géométrie. Une pale à calage constant de 30° donne `pas = 2πr·tan30` : ça monte
    linéairement avec le rayon, donc **pas/D = 1,36** à 75 % — 2 à 3 fois ce qu'encaisse un moteur
    de jouet en 6 V (une hélice aérienne de jouet vit entre 0,6 et 0,9).
    - **La leçon de fond : le piège 19 étape 3 a résolu l'IMPRIMABILITÉ et fait passer
      l'AÉRODYNAMIQUE à la trappe.** `PROP_ALPHA` était devenu un paramètre d'impression (pente de
      rampe) — plus personne ne le lisait comme un calage. Quand un paramètre sert **deux** métiers,
      celui qui n'est pas en train de faire mal se fait oublier. Le contrôle « pas réel » du piège
      19 étape 0 **existait dans la tête, pas dans le script** : rien ne l'affichait, donc 1,36 est
      passé. Corrigé : le run imprime un tableau **HÉLICES : pas et charge**, recalculé **depuis les
      sections réellement lofttées** (`blade_ramp_sec`), pas depuis les paramètres.
    - **Le bon levier n'est pas le diamètre, c'est le VRILLAGE.** Le couple absorbé est pondéré en
      **r³** : c'est le bout qui coûte. Réduire D perd deux fois — l'allure, et la **surface de
      disque**, donc la poussée à basse vitesse et l'autorité au différentiel (l'utilisateur :
      « la maniabilité à tourner des grandes pales »). Réduire le calage **du bout seulement** tape
      exactement où il faut. `PROP_ALPHA0=30` → `PROP_ALPHA1=15` à **D95** : pas/D 1,36 → **0,84**,
      couple **÷2,2** (la cible demandée) et 1,6-2,3 A. Chiffré ensuite au BEM : à couple ÉGAL, il
      aurait fallu descendre à **D81** en calage constant, qui pousse 11 % de moins et perd 38 %
      de surface de disque. Le gain du vrillage est réel mais modeste — le dire tel quel.
    - **⚠️ J'AI BOUGÉ DEUX PARAMÈTRES À LA FOIS — et c'est le vrai reproche de cette passe.**
      Premier jet : diamètre 100→90 **et** calage constant→vrillé, alors que la demande disait
      explicitement « la taille **ou** le pas ». Le résultat tombait juste (÷2,2) mais était
      **irréglable** : trop mou, on ne sait pas lequel des deux reculer, et chaque essai coûte une
      impression d'une heure. Corrigé en figeant `PROP_D` et en n'exportant que des variantes de
      `PROP_ALPHA1` (mêmes anneaux, même corde, même envergure — une seule chose diffère).
      **Règle : sur une pièce qu'on va régler par essais physiques, ne JAMAIS livrer deux
      variables changées ensemble. Et quand l'utilisateur écrit "A ou B", ce "ou" est exclusif.**
    - **Livrer l'ÉCHELLE dans le TABLEAU, le POINT dans les STL.** Un STL isolé n'apprend rien à
      qui l'imprime, d'où le tableau : sensibilité (**~4 % de couple par degré** de calage de bout)
      et bornes utiles (sous ~13° ça ne pousse plus, au-dessus de ~22° la conso repart). Mais
      j'avais d'abord exporté la variante de repli **en fichier** → 4 STL pour 2 hélices, et
      l'utilisateur : « j'ai 4 stl 95, 2 suffisent ». Il a raison : un STL de rechange sur le
      disque ne dit pas ce qu'il vaut, ne se distingue du bon que par son nom, et se régénère en
      changeant une ligne. **Une variante utile est une ligne de tableau, pas un fichier ; le
      dossier `stl/` ne contient QUE ce qu'on imprime.** Le tableau marque explicitement la ligne
      exportée. Il distingue aussi la mesure (3 A à l'ampèremètre) des **estimations** : un modèle
      en `Q^0.75` donne un ordre de grandeur, pas une promesse, et le dire évite qu'on le prenne
      pour une garantie.
    - **Le vrillage IMPROVE l'impression, il ne la dégrade pas** — contre-intuitif, et c'est
      pourquoi le piège 19 (« `→20°` = plus de support ») ne s'applique pas ici. Baisser le calage
      **global** allonge la rampe partout ; le baisser **au bout, là où la corde est étroite**,
      fait tomber la hauteur de rampe de 6,4 à 3,6 mm. L'emplanture (corde large, rampe de 12 mm)
      reste à 30°. Support plus COURT qu'avant.
    - Garde-fou : l'assemblage de contrôle monte `PROP_D` — un diamètre codé en dur ailleurs
      ferait tester au tableau COLLISIONS une hélice qu'on n'imprime plus. Même piège attrapé sur
      l'« envergure anneaux », qui était figée à `2*(PYY+62)` (valeur du D100).
    - **MON MODÈLE DE COUPLE ÉTAIT UN BRICOLAGE, et il a fallu que l'utilisateur demande « tu es
      sûr de ton calcul ? » pour que j'aille voir.** `Q ~ ∫c·r³·tan(β)dr` **mélangeait deux
      modèles sans le dire** : le `∫c·r³` vient de la théorie de l'élément de pale, le `tan(β)`
      d'une règle empirique (`P ∝ D⁴·pas`). Aucune dérivation ne donne ce produit. Vérifié après
      coup contre un vrai BEM : le rapport de couple tombait juste (0,49 contre 0,45 — la cible
      ÷2 tenait), mais **par chance** : la variante en `sin²β`, tout aussi défendable a priori,
      donnait 0,36. Un modèle dont on ne sait pas d'où il sort n'a pas d'incertitude connue.
    - **Le vrai coût de ce bricolage n'était pas l'imprécision, c'était le TROU.** Un indice de
      couple ne sait pas calculer la **poussée** — or c'est elle, pas le couple, qui répond à la
      seule question qui intéresse (« est-ce que ça va être trop mou ? »). J'ai passé quatre
      messages à optimiser une grandeur en ignorant celle dont dépendait la décision. Le BEM dit :
      poussée ×0,68 à ×0,9. **Quand on choisit une métrique à optimiser, vérifier qu'elle est
      celle sur laquelle porte la décision.**
    - **Et j'avais annoncé un COURANT sans modéliser le moteur — l'erreur la plus lourde.** Mon
      `I ~ Q^0.75` supposait implicitement un régime constant. Faux : une hélice plus légère fait
      **monter** le régime, la force contre-électromotrice suit, et **le courant ne retombe que
      lentement**. En résolvant le point de fonctionnement (moteur CC ancré sur les 3 A mesurés) :
      **2,0-2,6 A** pour le calage 15°, soit **-20 à -30 %**, alors que j'avais promis « ÷2 » puis
      « 1,8 A ». Diviser le couple par deux ne divise PAS le courant par deux.
    - **Le retournement complet : la poussée ne baisse quasiment pas (×0,87-1,13).** J'avais
      annoncé « -10 à -30 % » à l'utilisateur en lisant le rapport à **régime égal** — or le
      régime n'est jamais égal, c'est tout l'objet du couplage. L'ancienne hélice **étranglait**
      le moteur (30-40 % du régime à vide) : mauvais appariement, on perdait sur les deux tableaux.
      Conséquence pratique inversée : **baisser encore le calage coûte très peu de poussée**, donc
      la marge de manœuvre est bien plus grande que je ne le croyais.
      **Leçon : un rapport à régime égal ne veut rien dire sur une machine dont le régime est
      libre. Toujours résoudre le POINT DE FONCTIONNEMENT charge/moteur avant de conclure.**
    - **Paramétrer par une grandeur MESURABLE.** J'avais d'abord balayé un « rendement moteur »
      de 45 à 85 % — abstrait, et dont la borne haute était irréaliste pour un moteur de jouet
      tirant 3 A, ce qui tirait toute la fourchette vers le bas. Reparamétré par la **résistance
      série** : même physique, mais l'incertitude devient mesurable. Une incertitude qu'on sait
      mesurer vaut mieux qu'une moyenne.
    - **DEMANDER LES MESURES QU'ON A DEJA plutôt que d'en réclamer une nouvelle.** J'allais faire
      démonter un moteur pour un ohmmètre ; l'utilisateur avait mieux sous la main — **le courant
      à VIDE** (0,5 A, 0,25 A lubrifié). Il donne le couple de frottement, donc l'hélice absorbe
      `k(I-I0)` et non `k.I` ; en écrivant les deux points de fonctionnement, **`k` se simplifie**
      et la prédiction ne dépend plus du couple ABSOLU du BEM (le maillon faible) mais seulement
      de son RAPPORT (le maillon solide) et de `R`. Recoupement supplémentaire : le couple absolu
      du BEM + les 3 A impliquent un régime à vide ; n'ont été gardés que les `R` donnant un
      régime à vide et un courant de calage crédibles (9000-22000 tr/min, 3,5-9 A) → R = 0,7-1,3 Ω.
      **Constantes de la machine : `MOT_V/MOT_I0/MOT_IMES` en dur dans le script, sourcées.**
      Verdict : **2,0-2,5 A**, poussée ×0,82-1,04. Et le courant à vide s'avère quasi sans effet
      sur le résultat en charge (+0,03 A) : la lubrification soulage le moteur mais ne traite pas
      le problème d'hélice — le dire évite une fausse piste.
    - Ce que le script imprime maintenant : couple ET poussée, en **rapports** à la géométrie qui
      a réellement tiré 3 A (un rapport survit aux erreurs de modèle bien mieux qu'un absolu), et
      le courant en fourchette. Corde et calage sont **relus sur les sections lofttées**.
    - Deux bugs attrapés en intégrant le BEM, tous deux du même genre — **une variante de
      diamètre ne se fabrique pas par homothétie** : la corde est en mm ABSOLUS à tout diamètre,
      donc il faut régénérer les sections avec leur propre `Dm` (sinon la référence D100 sortait
      avec une corde étirée de 5 %) ; et le rayon à 75 % doit se prendre sur **le** diamètre de
      l'hélice évaluée, pas sur `PROP_D`.
    - `print("... 4 %% ...")` **sans argument de formatage** affiche `%%` littéralement. Fait deux
      fois dans la même session. Le `%%` ne s'échappe que dans une chaîne passée à `%`.

21. **« Sous 2 A sûr » : la géométrie d'hélice NE PEUT PAS le garantir — et le meilleur levier
    n'était pas celui que je poussais depuis quatre messages.**
    - **Le nombre de pales bat le calage, et je ne l'avais jamais testé.** À courant égal, une
      **bipale à 15° pousse plus qu'une tripale à 10°** (×0,69-0,95 contre ×0,64-0,85). Retirer
      une pale enlève de la solidité sans toucher à la géométrie des pales restantes ; baisser le
      calage fait travailler *toutes* les pales à mauvais rendement, parce que la traînée de
      profil ne baisse pas avec la portance. J'avais passé quatre passes à optimiser `PROP_ALPHA1`
      sans jamais remettre en cause `range(3)`, codé en dur depuis le début. **Ce qui n'est pas un
      paramètre n'est jamais remis en question : inventorier les constantes en dur AVANT
      d'optimiser celles qui portent déjà un nom.**
    - **Réduire la corde est un piège, et mon modèle l'encourageait.** `PROP_TH` est figée par
      l'impression : une corde plus étroite **épaissit** la pale en relatif (t/c 23 % → 33 %). Or
      mon BEM avait un `cd0` **constant**, donc il ne voyait que la surface qui diminue et
      recommandait joyeusement des pales-briques. Corrigé en `cd0(t/c)` : corde ×0,70 donne le
      *même* courant que la corde pleine, pour 20 % de poussée en moins — un pur perdant.
      **Un coefficient constant dans un modèle est une hypothèse cachée ; celui qui ne varie pas
      est celui qui ment quand on optimise justement dans sa direction.**
    - **Le levier qui garantit, c'est la TENSION.** Le courant vaut `(V-fem)/R` : la tension agit
      *directement* dessus, la géométrie seulement *indirectement* (via le régime, qui remonte et
      compense). D'où le plafond : au pire cas de `R`, aucune hélice ne descend sous 2 A à 6 V.
      À 4,8 V (4×AA + 2 factices, zéro réimpression, réversible) : 1,2-1,7 A. **Quand un objectif
      résiste à tous les leviers d'un même domaine, c'est que le bon levier est dans un autre.**
    - Méthode : à diamètre et puissance absorbée donnés, la poussée est fixée par la quantité de
      mouvement (`T ~ (2ρA·P²)^⅓ × FM`). Donc **peu importe par quel levier on retire la charge** —
      ce qui compte est de garder le DISQUE et un bon rendement de pale. Ça explique pourquoi tous
      les candidats d'une recherche en grille tombaient sur la même poussée à courant égal, et ça
      dit où chercher : la solidité et le rendement, pas le diamètre.
    - Conseil livré : **monter la bipale à 6 V et MESURER**. Une mesure lève toute l'incertitude
      d'un coup ; retirer une pile reste possible en 10 s si ça ne passe pas. Ne pas faire
      réimprimer sur la foi d'un pire cas modélisé quand une mesure est à portée de main.

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
