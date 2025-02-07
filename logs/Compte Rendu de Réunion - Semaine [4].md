# Compte Rendu de Réunion - Semaine [4]

**Date :** [07/02/2025]  

---

## 1. Organisation
- **Trello :**
- Mettre les tâches non finies dans "tâche à reprendre" ou "à corriger".
- Les tâches doivent être mises en archive après la réunion et non avant.
- Les tâches “réunion” ne sont pas très utiles, mais on peut laisser un compte rendu de nos réunions sur GitHub.
- Rappel de la Méthode agile : on définit ce qui doit être fait et on le découpe en petites tâches. 
  N’importe qui peut prendre n’importe quelle tâche. Pas de réunion pour dispatcher les tâches.


- **GitHub :**
  - GitHub peut contenir plusieurs sections, par exemple :
    - Une pour les documents,
    - Une pour les résultats expérimentaux,
    - Une partie "tools" pour permettre de tester facilement les fichiers et créer des graphes en suivant notre tutoriel.
  - Suivre les règles imposées par "The Figure Checklist" pour éviter tout problème juridique.


## 2. Réponses aux questions de la semaine
> Liste des problèmes rencontrés et des réponses apportées.

Problèmes
-  1) Lorsque les nœuds ont été tracés sur le même graphique que la
  piste, ils apparaissaient décalés. Ce décalage suggère que les
  coordonnées des nœuds et celles de la piste ne sont pas dans le
  même référentiel ou qu'il y a un problème d'échelle ou de
  transformation des coordonnées.
-  2) Nous avons tenté de générer un graphe représentant la trajectoire
   parcourue par un agent. Cependant, le graphe obtenu n’a aucun sens :
   l’agent n’est pas du tout sur la piste. Nous ne comprenons pas
   notre résultat. Peut-être que notre compréhension ou notre
   écriture du code est incorrecte. Pouvez-vous nous éclairer sur ce
   point ?

Réponses
- 1) Tenter de calculer l'offset entre les nodes et le centre du circuit de facon generique.
- 2) Les coordonnées sont peut être relative à quelque chose ce qui provoque l’incohérence.



## 3. Points abordés
-> **Discussions principales :**  
  - Tache concernant l'angle Beta
     - La courbe de l’angle au cours du temps était une bonne initiative.
    - On remarque que l’angle était en moyenne à 90°, 
    mais cela représente le fait que le kart était perpendiculaire à la piste et non au centre.
    L’angle devrait être à 0°.
    - Cela pourrait être un début d’apprentissage par renforcement, 
    où la récompense serait l’inverse de l’angle. Pour maximiser la récompense, l’angle devrait tendre vers 0°.
  - Restructuration du code
    - Factoriser les codes de test, mettre à part les fonctions communes dans un fichier common.py par exemple.
    - Ne conserver que les nouvelles parties et éviter la redondance dans plusieurs fichiers, transformer les parties        répétitives en fonctions importables pour épurer les fichiers, afin d’éviter de chercher les parties
      intéressantes parmi les parties communes.    
---

## 4. Tâches à réaliser la semaine prochaine
> Assignation des tâches et objectifs.

| Tâche  | 
|---------|
|Organiser le GitHub en plusieurs parties |
|Reajuster les nodes sur le centre du circuit|
|Faire un agent qui suit les nodes reajuster |
|Faire un diagramme de classe de pystk-gymnasium|

---

## 5. Apprentissage RL
> Notebook et/ou Vidéos à faire cette semaine
  - Les tâches d’auto-formation pourraient se limiter aux cours portant sur DQN au cours des prochaines semaines, 
  car le projet semble se diriger dans cette direction.

| Tâche  | 
|---------|
| Prendre connaissance des notebooks sur Google Collab  |
| Tenter d’installer les différentes bibliothèques lié à actor_critic_study |
| Completer le Notebook Dynamic Programming|

**Quelque definitions lié au cours qui ont été evoqué durant la réunion :** 
- value_V : vecteur qui donne une valeur pour chaque état.
- value_Q : matrice qui donne une valeur pour chaque couple état-action.
- Policy : décision de la politique.
- Politique : action associée à chaque état.
- Policy iteration : on part d’une politique, on calcule la fonction de valeur associée à cette politique.
- Value iteration : pas de politique, uniquement des calculs sur les valeurs ; on peut ensuite en déduire une politique.
---

## 6. Nb d'heures de travail cette semaine par membre
> Combien d'heures de travail chaque membre de l'equipe prevoit cette semaine

|  Nom   |  Nombres d'heures prévues   |
|-----|-----|
| Badr  | 8  |
| Cedric  | 8  |
| Mahmoud  | 8 |
| Safa  | 8 |

---

**Rédigé par :** [Badr]  
**Vérifié par :** [Noms des verificateurs]  
