# Compte Rendu de Réunion - Semaine 5

**Date :** 13/02/2025  

---

## 1. Organisation
- **Trello :** 
    - Toutes les taĉhes doivent être en 'terminé' avant la réunion avec le client.
    - Quand on travaille sur le Trello, on prend une tâche, une personne la vérifie et on la met en terminé avant la réunion avec le client.
    - La tâche diagramme de classe devrait être en 'terminé'
    
- **GitHub :** 
    - Pas besoin d'avoir un fichier d'archive car github archive déjà automatiquement.
    - Les noms des fichiers doivent être explicites et pas par eg. test0_0.py
    - Il doit y avoir que du code dans src et test, donc il y a encore de la factroisation à faire.


---

## 2. Points abordés
-> **Référentiel des nodes et problème d’alignement:**  
- Les nodes viennent de `env(track_data)`.
- Le centre du circuit est généré par rapport à l’agent. Les nodes sont extraits depuis `self.obs`.
- Ils sont définis par rapport au kart (référentiel relatif).
- L’agent ne démarre pas à l’origine du circuit → décalage.
- Solution : ajouter l’offset de la position initiale de l’agent.
- Position des nodes sur le circuit: Les nodes semblent être au centre du circuit. On pourra vérifier si c’est le centre exact ou une approximation quand le problème sera réglé.
    

 
-> **Wrappers :**  

- Un wrapper est une couche intermédiaire qui encapsule un environnement (`env`) afin de modifier ou d’ajouter des fonctionnalités sans changer directement le code de l’environnement original. Cette approche est similaire à l'utilisation du Design Pattern Decorator.

- Dans Gymnasium, les wrappers permettent de modifier la manière dont l'agent interagit avec l’environnement sans modifier directement l’implémentation de l’environnement. 

- En général, dans un environnement Gym, un agent interagit selon une boucle typique:
    - L’agent initialise l’environnement avec `reset()`, ce qui lui fournit un état initial.
    - À chaque étape, l’agent choisit une action via sa fonction de décision (`agent.predict_action()`).
    - L’environnement met à jour son état en fonction de cette action et renvoie :
        - Le nouvel état (`next_state`)
        - Le `reward` associée à cette transition
        - Un indicateur de fin d’épisode (`done`)
        - Des informations supplémentaires (`info`)
        
    Ce processus continue jusqu'à ce que l'épisode se termine (`done = True`).


- Les wrappers implémentent `reset()` et `step()`, mais appellent ensuite les mêmes méthodes de l’environnement original après y avoir appliqué des modifications.

- Un exemple de wrapper peut être un module qui, à chaque étape, enregistre les informations de l’agent dans un fichier pour analyser ses performances.(au lieu de nos scripts tests comme fait présentement)

- Dans notre projet, les wrappers sont utilisés pour créer des environnements adaptés aux besoins spécifiques des agents. 

- Exemples Concrets d’Utilisation des Wrappers à explorer dans le code ou essayer ultérieurement:
    - Suppression des pièges dans la piste
    - Enregistrement des données
    - Transformation des observations
    - Modification des actions possibles
        On peut restreindre l’espace des actions en supprimant celles qui ne sont pas pertinentes.

- Dans Gymnasium, `register` est un mécanisme qui permet d’enregistrer un environnement pour qu'il soit reconnu par Gym. Il sert à maintenir un registre des environnements existants afin que Gym puisse les appeler par leur nom.


## 3. Apprentissage RL
Différence entre la fonction V et Q:
- (V^π)(s) est un vecteur : il associe une unique valeur à chaque état s.
(Q^π)(s,a) est une matrice : elle associe une valeur à chaque couple (état, action).

- Choix des actions :
    Avec Q, il est plus simple de choisir une action optimale car on compare directement les valeurs associées à chaque action dans un état donné.
    
    Avec V, il faut d'abord déterminer quelle action a conduit à la valeur V(s), ce qui peut nécessiter un calcul supplémentaire.

- Valeurs et normalisation :
    Les normes de Q sont généralement plus grandes que celles de V car Q(s,a) contient des informations plus détaillées sur chaque action, alors que V(s) est une agrégation.
    
    On s’intéresse souvent à la norme des valeurs car des valeurs plus élevées indiquent des récompenses plus importantes sur le long terme.

- Gestion des valeurs égales :
    Lorsque plusieurs valeurs de Q(s,a)Q(s,a) sont identiques pour un même état, une action peut être choisie aléatoirement ou selon un critère externe.



| Tâche à réaliser la semaine prochaine pour l'apprentissage RL  | 
|---------|
| 02-2-tabular-rl.student.ipynb  |

---


---

## 4. Tâches à réaliser la semaine prochaine

| Tâches  | 
|---------|
| Compléter la refactorisation du code. src et test ne doivent avoir que du code  |
| Pour régler le problème des nodes, calculer et appliquer l’offset de départ de l’agent pour garantir un bon alignement. Le faire pour plusieurs circuits |
| Trouver une formule changer le refentiel relatif de la track avec un referentiel absolu des nodes en comparant les coordonnées des nodes avant et après application de l'offset.  |
| Chercher ou trouver le bon agent_path (penser aux coordonees relatifs et absolu) et tracer ainsi les graphes corrigés  |
| Visualiser les nodes et la piste sur le même graphique en superposant les informations et en ajustant si nécessaire.   |
| Faire un agent qui suit le 2e prochain node  |
| Faire la ligne l entre la postion du kart et le 2e prochain node   | 

---

## 5. Nb d'heures de travail cette semaine par membre


|  Nom   |  Nombres d'heures prévues   |
|-----|-----|
| Badr  | 8  |
| Wilson  | 8  |
| Mahmoud  | 7 |
| Safa  | 2 |

---

**Rédigé par :** Wilson  
**Vérifié par :** Mahmoud & Badr  
