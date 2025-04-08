# Rapport Hebdomadaire - Semaine 9

**Date :** 9/4/2025  

---

**TL;DR**  
Cette semaine, nous avons enrichi notre environnement en développant un wrapper d'observation pour mieux détecter et classifier les items et powerups, ce qui a permis d'améliorer l'ItemsAgent. L'agent ajuste désormais sa trajectoire en fonction des items et utilise stratégiquement ses powerups. Nous avons également constaté que le boost de départ est impossible à exploiter dans notre environnement, et nous avons réglé le problème de fin de course.


## A. Ce que nous avons compris  
> D'après la documentation STK & les ressources qu'on a eu le temps de bien analyser de Nazim et Nassim B.

### 1. Concernant les items
On a enfin compris le mapping.
Ils sont séparés en 3 sortes:

- **Obstacles**  
 ```python
  {
    'BONUS_BOX': <Type.BONUS_BOX: 0>,
    'BANANA': <Type.BANANA: 1>,
    'NITRO_BIG': <Type.NITRO_BIG: 2>,
    'NITRO_SMALL': <Type.NITRO_SMALL: 3>,
    'BUBBLEGUM': <Type.BUBBLEGUM: 4>,
    'EASTER_EGG': <Type.EASTER_EGG: 6>
  }
```
    
- **Powerups**
```python
{
  'NOTHING': <Type.NOTHING: 0>,
  'BUBBLEGUM': <Type.BUBBLEGUM: 1>,
  'CAKE': <Type.CAKE: 2>,
  'BOWLING': <Type.BOWLING: 3>,
  'ZIPPER': <Type.ZIPPER: 4>,
  'PLUNGER': <Type.PLUNGER: 5>,
  'SWITCH': <Type.SWITCH: 6>,
  'SWATTER': <Type.SWATTER: 7>,
  'RUBBERBALL': <Type.RUBBERBALL: 8>,
  'PARACHUTE': <Type.PARACHUTE: 9>,
  'ANVIL': <Type.ANVIL: 10>
}
```

- **Attachments**
```python
{
  'NOTHING': <Type.NOTHING: 9>,
  'PARACHUTE': <Type.PARACHUTE: 0>,
  'ANVIL': <Type.ANVIL: 1>,
  'BOMB': <Type.BOMB: 2>,
  'SWATTER': <Type.SWATTER: 3>,
  'BUBBLEGUM_SHIELD': <Type.BUBBLEGUM_SHIELD: 6>
}
```

Ces indications nous ont permis de définir clairement les types d’items considérés comme **"bons"** (par exemple, `BONUS_BOX`, `NITRO_BIG`, `NITRO_SMALL`, `EASTER_EGG`) et ceux considérés comme **"mauvais"** (par exemple, `BANANA`, `BUBBLEGUM`).


Pour les powerups, nous avons distingué deux grandes catégories :
- Powerups de boost (ex. `ZIPPER`) qui doivent être utilisés sur des portions droites de la piste.
- Powerups d’attaque (ex. `BOWLING`, `PLUNGER`, `SWATTER`) qui doivent être déclenchés lorsqu’un adversaire est proche.

### 2. Concernant le boost du départ (tâche de compréhension de code/documentation)
L'objectif initial de la tâche était d'exploiter le startup boost au lancement de chaque course. Ce boost, activé par une accélération maximale synchronisée avec la phase `SET (valeur 1)` du départ, devait offrir un avantage de vitesse dès le début de la course, similaire au comportement observé dans le jeu. L'hypothèse de départ reposait sur la possibilité d'intervenir pendant la phase `SET` pour déclencher ce boost. En parallèle, nous avons également étudié le rapport fourni par _Nassim B._ et _Nazim B._, lequel suggérait que l'exploitation du boost de départ pourrait être vouée à l'échec.

#### Problèmes rencontrés et défis techniques
Lors de nos expérimentations, plusieurs difficultés majeures ont été identifiées :
- Timing et gestion des phases
La simulation SuperTuxKart segmente la course en **quatre phases (READY, SET, GO, RACE)**. Nous avons constaté que, malgré nos modifications dans les méthodes de warmup et reset, l'agent ne reçoit que des observations indiquant la phase `RACE (valeur 3)`. Ainsi, même si la simulation passe techniquement par la phase `SET`, le système ne permet pas d'exécuter d'actions pendant cette période.

- Absence de contrôle précoce
Le système de simulation ne donne pas la possibilité d'intervenir avant la phase `RACE`. Autrement dit, le contrôle du kart n'est accordé à l'agent qu'après que la phase `SET` a été dépassée, ce qui empêche de tirer profit d'un startup boost. Nos logs, qui affichent systématiquement la valeur 3 pour la phase, confirment cette limitation.

#### Solutions apportées
Nous avons exploré plusieurs solutions dans le but de capturer et d'exploiter le startup boost :
- Modification de la boucle de warmup
Nous avons modifié la méthode warmup_race() dans le module pystk_process.py pour arrêter la simulation dès que la phase SET était détectée. L'objectif était de figer la simulation à ce moment critique.

- Forçage de la phase SET dans reset()
Dans la méthode reset() de STKRaceEnv, nous avons tenté de forcer la phase à SET (valeur 1) en interceptant et en modifiant l'observation initiale, dans l'espoir que l'agent puisse ainsi agir pendant cette phase.

    
**Malheureusement**, toutes ces approches se sont heurtées à la même réalité : le système de simulation ne donne le contrôle du kart qu'à partir de la phase `RACE`. Nos logs, qui affichent constamment la phase comme étant 3, témoignent que les modifications apportées n'ont pas permis de capturer la fenêtre temporelle de la phase `SET`. Ainsi, le boost de départ, tel qu'il est défini dans le jeu, s'avère inexploitables dans notre environnement. Face à cette contrainte technique majeure et après avoir exploré sans succès, les pistes mentionné précédemment, nous avons décidé d'abandonner l'utilisation du startup boost dans notre environnement.

---

## B. Tâches réalisées cette semaine  

### 1. ItemObservationWrapper

#### Objectif  
L'objectif du wrapper est d'enrichir les observations fournies par l'environnement en ajoutant des variables cruciales concernant les items.  
Ces variables sont les suivantes :
- **`target_item_position`** : Vecteur 3D indiquant la position de l'item ciblé.
- **`target_item_distance`** : Distance euclidienne entre le kart et l'item.
- **`target_item_angle`** : Angle (en degrés) entre la direction "avant" du kart et l'item.
- **`target_item_type`** : Code entier représentant le type de l'item, ce qui permet ensuite de l'interpréter grâce à une correspondance (par exemple, BANANA, BONUS_BOX, etc.).

#### Implémentation  
Le fichier `ItemObservationWrapper.py` consiste à :
- Récupérer les listes d’items brutes (`items_position` et `items_type`) issues des observations.
- S'assurer que la forme des données est correcte (pour obtenir un tableau de dimensions (N, 3)).
- Calculer pour chaque item :
  - La distance en utilisant `np.linalg.norm`.
  - L'angle en projetant le vecteur sur le plan XZ (par exemple avec `np.arctan2`).
- Sélectionner l'item cible par exemple en privilégiant les items dits « bons » (BONUS_BOX, NITRO_BIG, NITRO_SMALL, EASTER_EGG) s'ils sont à proximité, ou sinon ceux dits « mauvais » (BANANA, BUBBLEGUM).
- Affecter les valeurs calculées aux nouvelles clés de l'observation.

Ainsi, toutes les informations enrichies sont directement intégrées à l'observation, permettant aux agents de prendre des décisions plus fines.

### 2. Décorateur d'Agents : Chaîne de Décorateurs

Afin de rendre le code plus réutilisable, nous avons utilisé le **decorator design pattern** pour construire une chaîne de comportements :

1. **MedianAgent**  
   - **Fonctionnalité :**  
     Implémente la trajectoire de base en suivant le centre de la piste.  
   - **Implémentation :**  
     Calcule la différence entre le point de la piste (`paths_end`) et la position du kart (`front`).  
     Utilise des fonctions utilitaires comme `compute_curvature` et `compute_slope` pour ajuster l'accélération, la direction (steer), et même décider du drift/nitro de base.

2. **EulerAgent**  
   - **Fonctionnalité :**  
     Décore le MedianAgent pour ajouter un ajustement basé sur la courbure de la piste, via une méthode (ici `euler_spiral_curvature`) qui calcule une mesure de la courbure à partir des segments de trajectoire.  
   - **Implémentation :**  
     Intervient dans `calculate_action` pour recalculer le steer en fonction du résultat de la fonction de courbure.  
     EulerAgent récupère ainsi l'action de base produite par le MedianAgent et la modifie en fonction des conditions locales de la piste (courbure, pente).

3. **ItemsAgent**   (voir plus de détails dans la section B3 de ce rapport)
   - **Fonctionnalité :**  
     Décore un agent existant (généralement un EulerAgent) pour ajouter la prise en compte des items et des powerups.  
   - **Implémentation :**  
     Divise sa méthode `calculate_action` en trois parties :
      - Obtenir l'action de base à partir de l'agent décoré.
      - Appliquer un ajustement sur la direction en fonction des informations enrichies des items (provenant de l’ItemObservationWrapper).
      - Implémenter une stratégie pour l’utilisation des powerups : par exemple, utiliser des boosts uniquement sur des portions droites, ou déclencher un powerup d’attaque lorsque des adversaires sont proches.
   - Une correspondance (mapping) est utilisée pour traduire les codes de type d’item en noms lisibles, facilitant le debug.

#### Intégration dans les Scripts de Test

Nous avons mis à jour plusieurs scripts de test pour refléter cette nouvelle architecture.

#### -> test_MedianAgent.py  
Ce script initialise l'environnement en mode "human" et exécute un agent de base (MedianAgent) qui suit la trajectoire centrale. Le script :
- Crée un AgentSpec simple.
- Lance un environnement de course solo sur la piste "black_forest".
- Instancie et exécute MedianAgent.

#### -> test_EulerAgent.py  
Ce script montre à présent comment l’EulerAgent peut **décorer un MedianAgent**. En complément du suivi de base de la trajectoire, EulerAgent ajuste le steer en tenant compte de la courbure de la piste. Aussi, il ne drift pas, donc la trajectoire est effectivement meilleure.

#### -> test_ItemsAgent.py  
Ce script utilise un ItemsAgent **décorant un EulerAgent** qui **lui-même décore un MedianAgent**. Pour enrichir les observations, l’environnement est enveloppé avec le `ItemObservationWrapper`.  
- L’ItemsAgent ajuste le steer en fonction des données sur l’item cible (position, distance, angle et type).
- Il implémente également une stratégie de powerup (utilisation conditionnelle du boost ou d’une arme en fonction de la situation).

### 3. Implémentation de ItemsAgent
ItemsAgent est conçu comme un décorateur pour enrichir le comportement d’un agent de base (comme un MedianAgent ou un EulerAgent). Ce design s’inscrit dans le pattern décorateur, permettant de constituer des chaînes de comportements où chaque agent ajoute une couche de décision supplémentaire. Dans notre cas, l’ItemsAgent :

- **Récupère l’action de base** (suivi de trajectoire, ajustée par le MedianAgent ou l’EulerAgent),
- **Ajuste cette action en fonction des informations sur les items** (provenant du ItemObservationWrapper),
- **Applique une stratégie d’utilisation des powerups** en fonction des conditions observées.

En combinant le suivi de trajectoire avec des ajustements basés sur les items et une stratégie d’utilisation des powerups, nous obtenons un agent capable de prendre des décisions plus fines et adaptées aux situations de course.

-> Nous avons tenté d'incorporer une stratégie d'utilisation des powerups pour envoyer des items à nos adversaires, mais l'agent n'arrive pas encore à les lancer de manière efficace contre ses concurrents. Des améliorations supplémentaires seront nécessaires, notamment en ajustant le timing et les critères de déclenchement, afin de rendre la manipulation et le ciblage des powerups plus performants.

Ces étapes nous ont permis d’améliorer l’expertise de notre ItemsAgent en exploitant efficacement les informations sur les items, et nous ouvrent la voie à des stratégies encore plus sophistiquées dans le futur.


### 4. Lancement de plusieurs agents dans une même simulation

Notre objectif était de lancer simultanément plusieurs agents sur la même course pour comparer différentes stratégies de pilotage (`MedianAgent`, `EulerAgent` et `ItemAgent`). L’idée initiale était de lancer 2 agents sur une même course en utilisant l’environnement standard `STKRaceEnv` pour les agents solos. Toutefois, nous avons rencontré plusieurs obstacles lors de la mise en place d’une course multi‑agent.

#### Problèmes rencontrés et défis techniques

#### a. Lancement parallèle de 2 courses avec `STKRaceEnv`
Au départ, chaque agent (EulerAgent et MedianAgent) instancié créait son propre environnement `STKRaceEnv`. Ce comportement induisait le lancement de 2 courses en parallèle, ce qui ne permettait pas de faire courir 2 agents sur la même piste, puisque chacune de ces instances opérait de manière totalement indépendante.

#### b. Passage à un environnement multi‑agent
Pour pouvoir réunir plusieurs agents sur une seule course, il était nécessaire d’utiliser l’environnement `STKRaceMultiEnv` qui permet de configurer et de contrôler plusieurs karts dans le même déploiement. Cependant, les versions initiales d’EulerAgent et de MedianAgent étaient conçues pour créer un `STKRaceEnv` individuel. Cette approche ne permettait pas de passer une liste d’agents à l’environnement et donc de synchroniser la course entre plusieurs agents.

#### c. Difficulté avec l’implémentation de ItemAgent pour 3 agents
Une fois ItemAgent implémenté – il s’agit d’un décorateur qui enrichit la stratégie de pilotage avec la gestion des items – nous avons tenté de lancer une course avec 3 agents (MedianAgent, EulerAgent, ItemAgent) sur une même piste.

Le problème rencontré était une incohérence dans la configuration des contrôles :
-> L’environnement `STKRaceMultiEnv`, initialisé avec 3 agents humains (`use_ai=False` pour chacun), se positionne pour recevoir 3 actions externes. Toutefois, le code du STK sous-jacent attendait un nombre fixe d’actions (par exemple seulement 2), ce qui provoquait l’erreur `« Expected 2 actions, got 3 »`.
    
Face à cette situation, nous n’avons pas réussi à faire cohabiter 3 agents sur une seule course dans cette configuration. La solution immédiate fut de décomposer la course en duels afin de comparer deux agents à la fois.

#### Solutions apportées

#### a. Modification des agents pour le multi‑agent
Pour résoudre le problème du lancement parallèle de courses, nous avons modifié les classes EulerAgent et MedianAgent afin qu’elles ne créent plus un `STKRaceEnv` en interne. Au lieu de cela, le fichier de test instancie directement un `STKRaceMultiEnv` en passant une liste de spécifications d’agents (`AgentSpec`). Cela permet de :
    • Configurer un environnement commun (une seule course) pour tous les agents.
    • Préciser le nombre total de karts (par exemple, `num_kart=2 ou 3`) dans la course.
    • Synchroniser les observations et les actions pour chaque agent via un dictionnaire.
    
#### b. Passage en paramètre d’une liste d’agents dans le fichier de test
La solution mise en œuvre fut de centraliser la création de l’environnement dans un fichier de test unique qui instancie `STKRaceMultiEnv`. Dans ce fichier, nous définissons une liste d’`AgentSpec` pour les agents désirés. Ainsi, l’environnement reçoit l’ensemble des agents et peut mettre en correspondance chaque observation à son agent respectif via des clés (par exemple « 0 », « 1 » pour 2 agents).

#### c. Expérimentation en duel pour résoudre le problème à 3 agents
Après avoir implémenté ItemAgent, nous avons tenté de lancer une course avec 3 agents. Le problème rencontré (l’erreur indiquant que le système attendait 2 actions alors que 3 étaient fournies) semble être lié à la limitation du nombre d’actions externes attendues par le moteur STK ou une incompatibilité dans la configuration des contrôles des agents.

En conséquence, nous avons choisi de décomposer les tests en duels (matchs individuels) :
    • Duel Euler vs Median
    • Duel Euler vs Items
    • Duel Median vs Items
    
Cette séparation permet d’éviter le conflit dans la configuration du nombre de joueurs contrôlés et facilite le débogage des stratégies entre chaque paire d’agents.

-> Pour résumer, nous avons réussi à lancer 2 agents sur la même course en adaptant le code des agents pour utiliser directement `STKRaceMultiEnv` avec une liste d’agents. Le problème initial – chaque agent créant son propre environnement `STKRaceEnv` et donc lançant plusieurs courses parallèles – a été résolu en centralisant la création de l’environnement dans un fichier de test unique.

Suite à l’implémentation de ItemAgent, une tentative de course avec 3 agents a montré une incompatibilité (le moteur STK attendait un nombre d’actions différent du nombre d’agents fournis), ce qui nous a amenés à séparer les duels en face-à-face. Ces tests en duel nous permettent de comparer les stratégies (Items vs Median, Items vs Euler et Euler vs Median) sans entrer en conflit avec les contraintes du système.

### 5. Problème de fin de course réglé

Suite aux différentes modifications mentionnées plus tôt, il a également fallu adapter le comportement de fin de course pour chacun des agents étudiés. Pour cela, nous avons pris en compte le fait que nous utilisons désormais des décorateurs pour définir les actions des différents agents. Nous avons donc choisi de définir le comportement initial dans le MedianAgent, qui constitue notre agent de base (non décoré), puis nous avons mis en place des conditions spécifiques dans les différents décorateurs, ce qui permet de ne pas modifier l'action retournée si ce n’est pas nécessaire.


---

## C. Prochaines étapes 
> La partie code est quasi-complète à ce stade
1. Améliorer l'ItemsAgent pour lancer des attachments quand il y a d'autres karts. L'objectif sera de lancer stratégiquement des attachments pour gêner les adversaires.
2. Réaliser des graphiques d'analyse des performances lors des tests multi-agents afin de visualiser et comparer les stratégies en termes de trajectoire, de vitesse, et de taux de réussite des powerups.
3. Potentiellement **commencer** à intégrer du reinforcement learning pour optimiser automatiquement les paramètres de décision (gains, seuils, timing d'utilisation des powerups) en fonction des résultats de course. **(⚠️Discussion pendant la réunion)**



---

**Rapport rédigé par :** Wilson  
**Vérifié par :** Mahmoud, Badr, Safa  
