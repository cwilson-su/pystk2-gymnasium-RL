# Rapport Hebdomadaire - Semaine 6

**Date :** 13/03/2025  

---

## 1. Tâches réalisées cette semaine  

### i. Faire le rapport de Projet intermediaire.

On a tout d'abord décidé de rédiger un rapport qui se rapprocherait le plus possible de ce qu'un chercheur aurait écrit. On a choisi de ne pas inclure trop de code inutile et de se limiter à fournir du pseudocode, ce qui rendra les explications plus claires lors de la relecture.


### Explication du fonctionnement du rapport:



#### -> On a d'abord le rapport principal, qui est composé des lignes directrices du projet et de toutes les informations et définitions utiles à la compréhension du projet :

Ce rapport introduit tout d'abord le contexte du projet dans la section `Introduction`, mais aussi l'idée générale et les grandes lignes. Il permet de donner au lecteur les informations les plus importantes pour qu'il n'ait pas à les chercher plus loin.

On a ensuite une section `Definitions` qui, comme son nom l'indique, définit les différentes notions utilisées afin que même un lecteur ayant peu ou pas de connaissances sur le sujet puisse en comprendre le fonctionnement global.

On a aussi une section `Analysis of Provided Scripts` où l'on décrit le fonctionnement de l'environnement de départ.

Enfin, on a une section `Selecting the Node to target` où l'on explique tout le cheminement que nous avons suivi en travaillant avec les nœuds, qui est une partie centrale du projet actuel.



#### -> On a ensuite décidé de s'orienter vers la création de fiches techniques pour les agents du projet.

Les fiches techniques, comme leur nom l’indique, présentent la partie technique d’un agent spécifique de notre projet (par exemple : le MedianAgent). 
Elles détaillent en profondeur le fonctionnement de l'agent, les raisons qui ont motivé nos choix de conception et le cheminement qui nous a conduits à ces décisions. Nous y indiquons également les différentes approches qui se sont révélées peu ou pas fructueuses.




### La section `reports` a été ajoutée dans le GitHub.

Cette section contiendra toutes les fiches techniques futures, ainsi que le rapport intermédiaire et le rapport final.
**/!\ On a upload une fiche technique du `MedianAgent` mais elle n'est pas final /!\\**

---

### ii. Implémentation du TrackPathWrapper

Le module `TrackPathWrapper` a été implémenté pour permettre la visualisation du tracé du circuit, du chemin suivi par l'agent et des items présents sur la piste.

## Fonctionnalités
- **`plot_agent_path_with_track`** : Affiche le tracé du circuit et le chemin suivi par l'agent.
- **`plot_agent_path_with_items`** : En plus du tracé et du chemin de l'agent, cette fonction affiche également les items avec leur type (0, 1, 2 ou 3).

Les items sont représentés par de petits points rouges avec leur type indiqué à côté pour faciliter l'analyse visuelle. Cette visualisation est à amémiorer pour linstant car il y a un problème de coordonnées.

## Utilisation
1. Importer le wrapper :
```python
from utils.TrackPathWrapper import plot_agent_path_with_track, plot_agent_path_with_items
```

2. Pour afficher le tracé et le chemin de l'agent :
```python
plot_agent_path_with_track(agent, env, "nom_du_circuit")
```

3. Pour afficher le tracé, le chemin de l'agent et les items :
```python
plot_agent_path_with_items(agent, env, "nom_du_circuit")
```

- Le wrapper utilise la classe `TrackVisualizer`(fait avant) pour tracer les données du circuit.
- Pour convertir les coordonnées des items de `self.obs` (coordonnées relatives) en coordonnées globales, la fonction `local_to_global_coordinates` est appelée. C'est cette fonction qui contient certainement un problème de logique.
- Le wrapper gère les deux types d'agents :
  - Les agents personnalisés (comme `MedianAgent` ou `ItemsAgent`).
  - Les agents donnés (comme ceux utilisant `AgentSpec`).

Les items et leur positions relatives se trouvent dans `self.obs`
**On n'est pas surs mais on pense que** Les items sont classifiés comme suit :
- `0` : Nitro
- `1` : Banana
- `2` : Cake
- `3` : Bomb


## Prochaines étapes
- Améliorer la stratégie de l'agent pour réagir efficacement face aux items dangereux ou bonus.
- Ajouter une option permettant de zoomer sur certaines parties du tracé pour une analyse plus détaillée.
- Optimiser la vitesse d'exécution du wrapper pour les simulations complexes.

--> Début de l'`ItemsAgent`
Un nouvel agent, nommé `ItemsAgent`, a été commencé cette semaine. Il repose sur la logique du MedianAgent mais ajoute une capacité à éviter les pièges (comme les bananes ou les bombes) et à se diriger vers les items positifs (comme le Nitro ou le Cake). Pour l'instant, son comportement n'est pas encore parfaitement optimisé : l'agent ne parvient pas toujours à éviter les obstacles efficacement. On espère finaliser cette fonctionnalité d'ici la fin de la semaine.








---

## 2. Apprentissage & Documentation  
> Cette semaine aussi, on s'est concentré sur plus sur le code et le rapport intermediaire.

---




**Rapport rédigé par :** Mahmoud 

**Vérifié par :** Badr, Wilson et Safa  