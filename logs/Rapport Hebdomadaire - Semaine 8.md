
# Rapport Hebdomadaire - Semaine 8

**Date :** 1/04/2025

---

## 1. Tâches réalisées cette semaine

### i. Duel entre EulerAgent et MedianAgent

Cette semaine, notre objectif principal était de faire cohabiter deux agents personnalisés (MedianAgent et EulerAgent) dans une même instance de course SuperTuxKart. L'idée est d’observer leur comportement en situation réelle, sur un même circuit, avec des conditions strictement identiques. 

- Avancées
Mise en place d’un script de test unique (test_dual_agents.py) capable d’instancier deux agents dans un seul environnement STKRaceEnv. Modification des agents pour leur permettre de recevoir directement leur propre observation via un index (obs[kart_index]) et d'utiliser l’environnement partagé (env injecté depuis l’extérieur). Mise à jour de l'environnement pour activer deux karts avec num_kart=2.  

- Problèmes rencontrés 
L’appel à env.reset() ne retourne qu’un seul dictionnaire d’observation au lieu d’une liste d’observations (une par kart). Cela entraîne une erreur KeyError: 0 au moment de l'accès à obs[i] pour le deuxième agent. Comportement incohérent de l’environnement pystk2, qui ne différencie pas bien les karts dans les observations, bien que deux karts soient visibles à l’écran.  
- Étapes suivantes 
Identifier précisément pourquoi l’environnement ne retourne pas les observations séparées pour chaque kart. Explorer si une modification du wrapper STKRaceEnv ou des wrappers internes (ex : BaseSTKRaceEnv) est nécessaire pour corriger ce comportement. Une fois ce problème résolu, intégrer la génération de fichiers CSV et de graphiques pour comparer les trajectoires des deux agents.

---

### ii. Problème de fin de parcours, bot qui fait du hors-piste
- Pour la fin du parcours : 
Suite à la réunion précédente, ou on avais discuté du fonctionnement du rangement des nodes et de la façon dont notre agent décidait de la direction qu’il devait prendre, on a appliqué la méthode que nous avions évoqué et cela a bien fonctionné pour toutes les tracks concernés par le problème. 

- Pour le blocage sur les murs : 
Suite à plusieurs tentatives d’invocation de l’oiseau qui ont résulté en des échecs, on a compris que pour pouvoir utiliser l’oiseau, il nous faudrait modifier plus de code que prévue ce qui n’est pas envisageable au vu des objectifs primaires du projet. On a décidé d’opter pour une approche un peu moins élégante, mais qui peut tout de même marcher tout aussi bien. L’idée serait que l’agent prenne les virages trop serrés un peu plus large. Pour l’appliquer, on a ajouté au calcul du steer une petite variable qui va varier en fonction de la courbure de la track. Cette tache n’est pas encore complète, car on n’a pas pu faire des tests approfondis, mais elle semble offrir une bonne option pour régler le problème. On a aussi implémenté une mécanique de recul suite à un blocage, mais elle n’est pas encore exploitée correctement.

---

### iii. Intégrer un boost de départ


L'objectif était d'implémenter un startup boost dans l'environnement de simulation en synchronisant l'accélération maximale avec la phase SET (valeur 1 dans envs.py), afin d'obtenir un avantage de départ similaire à celui observé dans le jeu.

**Méthodologie**

-   **Environnement**  
    L'environnement est défini dans STKRaceEnv, qui segmente la course en différentes phases (READY, SET, GO, RACE) et communique via PySTKProcess avec le moteur SuperTuxKart. Les méthodes telles que reset_race() et warmup_race() sont utilisées pour initialiser la course et faire avancer la simulation jusqu'à une phase donnée.
    
-   **Gestion du Contrôle et du Timing**  
    L'analyse a porté sur la possibilité d'intervenir durant la phase SET afin de déclencher le startup boost en appliquant une accélération maximale (1.0). Pour ce faire, plusieurs modifications ont été apportées dans les méthodes de warmup et reset pour forcer la première observation à refléter la phase SET.
    

**Résultats et Analyse**

-   **Observations**  
    Lors de la simulation, la valeur de la phase a été affichée à chaque step, et il a été constaté que cette valeur est toujours 3 (phase RACE), sans aucune occurrence de la phase SET (1).
    
-   **Interprétation**  
    Cela indique que, bien que la simulation traverse en interne les phases READY et SET, le système ne permet pas d'exécuter d'actions avant d'atteindre la phase RACE. Autrement dit, le contrôle du kart est attribué uniquement à partir de la phase 3, empêchant ainsi toute intervention durant la phase SET nécessaire pour déclencher le startup boost.
    
**Conclusion et Perspectives**

-   **Bilan**  
    Le système de simulation de SuperTuxKart attribue le contrôle du kart uniquement à partir de la phase RACE. Cette contrainte empêche d'intervenir durant la phase SET et, par conséquent, d'appliquer le startup boost tel qu'il se produit dans le jeu.
    
-   **Perspectives**  
    Pour reproduire fidèlement le comportement du boost de départ, il serait nécessaire de modifier le fonctionnement interne de l'environnement, par exemple en :
    
    -   Modifiant le moment où le contrôle est transféré à l'agent (en retardant la transition automatique vers la phase RACE).
        
    -   Introduisant un mécanisme pour intercepter ou figer l'état de la course pendant la phase SET afin de permettre l'exécution d'une action de boost.

---

## iv. Compréhension des objets dans SuperTuxKart

Lors de notre précédent rapport, nous avions établi que l’ItemsAgent utilisait des observations simplifiées (positions d’items et types d’items) pour éviter les objets sur la piste en se basant sur une vision périphérique. Nous avions constaté que l’agent évitait systématiquement les items en se décalant latéralement, mais que ce comportement était parfois trop rigide (toujours vers la gauche, par exemple). En plus, on est pas sur du mapping des items de cpp à Python.


### Simulation et amélioration en Python

Comme nous n’avons pas accès directement aux méthodes C++ via le wrapper Python (pystk2), nous avons commencé l'implémentation une classe ItemWrapper en Python pour simuler ces fonctions. Cette classe permet de :

  - Renvoyer la position via `getPosition()`.

  - Calculer un point d’évitement avec `getAvoidancePoint()` en appliquant un décalage fixe.

   - Simuler la mesure de la distance par rapport au centre, etc.

->Depuis le dernier rapport, nous avons donc :

  - Amélioré la compréhension du code source en examinant la documentation et le dépôt GitHub.

  - Simulé en Python des fonctions clés de la version C++ (comme `getAvoidancePoint`) pour permettre à l’agent de réagir de manière plus intelligente.

   - Mise en place d’ajustements dynamiques qui font varier la direction en fonction de l’encombrement latéral plutôt que de toujours se décaler d’un côté fixe.

Les prochaines étapes consisteront à affiner les paramètres (facteurs de pondération, distances, décalages) et, si possible, à intégrer des éléments de la véritable IA de SuperTuxKart si les fonctions C++ deviennent entièrement accessibles via le wrapper `pystk2`.


## 2. Question 

Pourriez vous nous mettre en relation avec des élèves de M2?
Nous avons tenté de contacter les élève figurant sur le rapport que vous nous avez envoyé mais nous sommes resté sans réponse.

---
**Rapport rédigé par :** Badr
**Vérifié par :** Safa, Wilson et Mahmoud