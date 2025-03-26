# Rapport Hebdomadaire - Semaine 7

**Date :** 26/03/2025

---

## 1. Tâches réalisées cette semaine

### i. Duel entre EulerAgent et MedianAgent

Nous avons essayé de lancer une simulation avec ces deux agents sur une même course. Nous avons rencontré plusieurs problèmes :

1. **Visuel du bot** : Quel bot doit être affiché visuellement dans la simulation ?
2. **Gestion des simulations simultanées** : Chaque agent lance sa propre simulation, ce qui a conduit à un double lancement et a provoqué un crash des PCs.

**Prochaine étape :** Revoir tout le code de `MedianAgent` et `EulerAgent` pour permettre un lancement unique et éviter ces conflits.

---

### ii. Problème de fin de parcours, bot qui fait du hors-piste

Après plusieurs tests infructueux avec différentes approches, nous avons identifié un problème dans la gestion des `nodes` :

- Lorsqu’un circuit présente une intersection, le second chemin est stocké en fin de tableau.
- À la fin de la course, le bot cible souvent le premier `node` de l’intersection, qui se situe généralement à gauche de sa trajectoire.
- Cela cause des collisions avec le mur ou des sorties de piste.

**Solution envisagée :** Comparer les distances des `nodes` à `n` et `n+1`. Si la différence est trop grande, entrer dans un état de « foncer tout droit » pour éviter les erreurs de trajectoire.

---

### iii. Intégrer un boost de départ

Un boost consiste à enclencher l’accélération à un moment précis avant le départ afin de bénéficier d’un gain de vitesse initial.

**Hypothèse :**

D’après des informations collectées sur le forum officiel de _SuperTuxKart_, le boost s’active en pressant le bouton d’accélération immédiatement après l’apparition de la phase `SET`, juste avant la transition vers `GO_PHASE` (feu vert).

**Mise en œuvre :**

L’agent a été programmé pour appuyer sur l’accélérateur uniquement pendant la phase `SET_PHASE`.

**Résultats :**

Le boost ne s’est pas manifesté visiblement dans la simulation. Cela suggère que nous devons encore déterminer :

- La durée optimale d’appui sur l’accélérateur.
- Si un tapotement rapide (appui-relâché puis ré-appui) est nécessaire.
- Si une simple pression continue au bon moment suffit.

**Prochaine étape :** Tester différentes durées et types d’appuis pour valider l’hypothèse du boost de départ.

---

### iv. Compréhension des objets dans SuperTuxKart

En analysant le code C++ (`state.cpp`) ainsi que la documentation (`ItemState`, `ItemType`, etc.), on comprend que chaque objet sur la piste est représenté sous forme d’une **structure `PyItem`** côté C++, exposée au Python via les bindings. Chaque objet possède :

- une **position 3D** (`location`),
- une **taille** (`size`),
- un **type** (`type`) défini par une énumération (`ItemType`) qui distingue les objets bénéfiques (`NITRO_SMALL`, `NITRO_BIG`, `EASTER_EGG`) des objets à éviter (`BANANA`, `BUBBLEGUM`, etc.).

Cependant, côté Python (dans `self.obs`), on ne reçoit **pas directement ces objets riches**. À la place, on a :

- `items_position` → une simple liste des positions des objets,
- `items_type` → une liste d'entiers correspondant aux types d’objets.

Les identifiants de type sont des entiers (par exemple, `0 = BANANA`, `1 = NITRO_SMALL`, etc.), ce qui explique pourquoi au départ l’agent ne comprenait pas les types — il fallait mapper manuellement les entiers vers les types nommés.

Enfin, certaines méthodes utiles comme `getAvoidancePoint()` existent dans le backend C++ pour aider les IA à contourner proprement les objets, mais ne sont **pas exposées dans l’interface Python**. Cela limite les possibilités d’évitement précis à moins de recompiler le binding.

### Étapes de mise en œuvre

1. **Observation des objets**

   - Extraction en temps réel de `items_position` depuis `self.obs`.
   - Chaque position est convertie dans le référentiel du kart (`to_kart_frame`).

2. **Vision périphérique**

   - Calcul d’une **distance d’anticipation (`look_radius`)** autour du kart.
   - Filtrage des objets proches de l’agent.

3. **Analyse latérale**

   - Détermination du nombre d’objets à gauche et à droite du kart (basé sur `x` local).
   - Aucune supposition rigide (pas de “toujours à gauche”).
   - Décision : si un côté est plus encombré, on tourne légèrement de l’autre côté.

4. **Action de pilotage**
   - Combinaison de la **direction du chemin principal** (centerline) et de l’ajustement latéral.
   - Pas de drift, pas de nitro : on garde un contrôle simple pour observer le comportement.

### Difficultés rencontrées

- **Profondeur des objets dans `np.digitize`**

  - Erreur `object too deep for desired array` due à un mauvais format des coordonnées ou des bords de bin.
  - Résolu en forçant le flattening de `bin_edges` et la conversion des coordonnées en `float`.

- **Surcharge de steering**

  - Au départ, l’évitement était trop agressif (déviation excessive même pour de petits obstacles).
  - Corrigé avec un `steering` plus doux et des ajustements latéraux plus subtils.

- **Vision trop tardive**

  - Les items étaient détectés trop tard → stratégie de prévision renforcée avec `look_radius` étendu.

- **Essai non concluant d’un plan global**
  - Tentative de prétraiter tous les chemins au début de la course (planification) abandonnée car trop rigide.
  - Retour à une logique adaptative temps réel, plus efficace.

---

**Rapport rédigé par :** Safa  
**Vérifié par :** Badr, Wilson et Mahmoud
