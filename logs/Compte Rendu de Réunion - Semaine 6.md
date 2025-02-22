---
title: Compte Rendu de Réunion - Semaine 6

---

# Compte Rendu de Réunion - Semaine 6

**Date :** 20/02/2025  

---

## 1. Organisation
    
- **GitHub :** 
    - Ne pas upload des fichiers de code dans le répertoire du projet. Utiliser plutôt les git add, git add et git push.


---

## 2. Points abordés
-> **Fonctionnement du Bot:**  
- Le Bot est un peu lent par rapport au Bot utilisant l'IA de difficulté 2
- Il ne considere pas les piege de la track ainsi que les objet bonus
- Le Bot essaye d'utilisé le drift mais ca ne l'aide pas a surpassé le Bot de dificulté 2
- Il utilise sa connaisance de la courbure de la tarck avec la fonction `compute_curvature`
- Le Bot a des probleme a la fin de certaines track ou il part dans le mur

->  **Choix des objectifs:**
- Trois choix s'offrent à nous:
    1. Tout d'abord, on peut se concentrer sur le perfectionnement du bot actuel.
    2. On peut aussi décider d'utiliser le RL dans des actions discrètes comme la détection de piège (en utilisant Q-Learning, SARSA ou actor critic).
    3. Au final, on peut aussi repartir de 0 pour se concentrer uniquement sur la création d'un bot utilisant le RL pour faire varier les hypervariables.

- On a choisi de se diriger vers le premier choix dans un premier temps, et lorsque l'on sera satisfait de nos résultats, on essaiera de peaufiner le bot avec du RL pour les actions discrètes

---

## 3. Objectifs

| Tâches à réaliser les prochaines semaines pour l'apprentissage RL  | 
|---------|
| Faire le NoteBook Q-Learning  |
| Faire le NoteBook SARSA  |

| Tâches à réaliser les prochaines semaines  | 
|---------|
| Regler le probleme rencontré a la fin de certaines track  |
| donnée un comportement basique par rapport au items rencontré par terre  |
| arranger le dossier des agent pour garder une trace de chacun d'entre eux avec leur avantage et leurs inconvénient  |
| regarder comment fonctionne les bot de base de STK  |
| faire que le bot puisse esquiver les pieges  |
| Trouver un moyen de se debloquer en reculant  |
| faire differents tests avec des agents de niveau 0 et 1 pour voir l'efficacité de notre bot  |
| Récupérer le `ActionTimeExtensionWrapper` des élèves NazimB et NassimB de M2 et l'integrer dans notre code  |
| Récupérer le `ExpertObservationWrapper` des élèves NazimB et NassimB de M2 et l'integrer dans notre code  |
| Récupérer le 'Expert agent function'(Algorithm1-section 3.3.1) des élèves NazimB et NassimB de M2 et l'integrer dans notre code  |
| quand on aura plusieurs agents, faire une course avec les différents agents  |
| Améliorer les virages (Recherche et Implementation)  |

| Tâches pour le rapport intermediaire OverLeaf  |
|---------|
| Ecrire l'algorithme de MedianAgent en PseudoCode  |
| A chaque verification de tache, si la tache est approuvé par l'ensembre de l'equipe, faire une description de la tache. Temps totale de la tache = `t+1h` |

---

**Rédigé par :** Mahmoud  
**Vérifié par :** Wilson, Badr & Safa  