# Compte Rendu de Réunion - Semaine 7

**Date :** 13/03/2025

---

_Le rapport de mi-semestre a été envoyé à Fabrice Kordon Vendredi 14 Mars._
_Nous avons essayé de suivre vos conseils pour améliorer notre rapport._
_Nous sommes vraiment débordé ces derniers temps entre le rapport de mi-projet, notre rapport de mi-projet en Technologie du web à rendre aujourd'hui(ce qui nous a pris une bonne partie de notre weekend) et notre TME solo en Génie Logiciel(jeudi après-midi). C'est pour cela qu'on ne pourra pas travaillé énormément cette semaine._

## 1. Organisation

- **GitHub :** Mise en ligne du rapport de mi-projet

---

## 2. Points abordés

-> **Décomposition du projet en trois étapes :**

1. **Pilotage efficace de l’agent en ignorant les objets** (déjà implémenté mais peut être améliorer avec EulerAgent)
2. **Collection et évitement des objets par l’agent**
   - Les positions des items sont directement accessibles depuis l’agent.
   - Si un item doit être récupéré, l’agent se dirige vers lui.
   - Sinon, un nouveau node est créé pour éviter l’item/obstacle.
   - Les items sont classés de 0 à 3, mais leur correspondance exacte est inconnue (Surprise box, Banane, Nitro, Bombe).
   - Demander à Benjamin P quel numéro d'item correspond à quoi
3. **Lancement des objets par l’agent**
   i) Lancer les objets dès leur récupération.
   ii) Lancer les objets en fonction de leur utilité :
   - Lancer une banane si un adversaire est derrière.
   - Utiliser le nitro en ligne droite.
   - Lancer une boule de bowling si un ennemi est dans la ligne de mire.

-> **Autres discussions :**

- Développement et comparaison entre EulerAgent et MedianAgent.
- Analyse des performances de départ de l’agent :
  - L’adversaire semble démarrer plus vite malgré une accélération constante de 100% de notre agent.
  - Deux hypothèses :
    1. L’agent n’accélère qu’après le top départ, tandis que l’adversaire utilise un "frein à main" pour pré-accélérer.
    2. Il existe un départ bonus similaire à Mario Kart qui offre un boost initial si certaines conditions sont remplies.
  - Il faut tester ces hypothèses et identifier la présence éventuelle d’un départ bonus.
- Mettre en compétition les agents crée et faire des graphes de vitesse pour comparer leur performance.

## 3. Tâches à réaliser les semaines à venir

> Objectifs

| Tâche                                                                                                 |
| ----------------------------------------------------------------------------------------------------- |
| Continuer à développer EulerAgent                                                                     |
| Tracer des graphs de position et de vélocité pour comparer EulerAgent et MedianAgent                  |
| Demander l’agent de l’étudiant de M2 pour comparer avec notre agent                                   |
| Tester le pré-accélération de l’agent                                                                 |
| Vérifier l’existence et les conditions du départ bonus                                                |
| Demander à Benjamin P la correspondance des items                                                     |
| Implémenter l’étape 2 : Collection et évitement des objets                                            |
| Implémenter l’étape 3 partie 1 : Lancer les objets dès leur récupération                              |
| Implémenter l’étape 3 partie 2 : Lancer les objets en fonction de leur utilité                        |
| Mettre en compétition les agents crée et faire des graphes de vitesse pour comparer leur performance. |

---

**Rédigé par :** Safa
**Vérifié par :** Badr, Mahmoud et Wilson
