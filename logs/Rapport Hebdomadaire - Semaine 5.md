# Rapport Hebdomadaire - Semaine 5

**Date :** 18/02/2025  

---

## 1. Tâches réalisées cette semaine  

### i. Faire un script utilitaire `TrackUtils` qui est utilisé pour sauvegarder et plot des valeurs de track et agent_path pour n'importe quelle simulation. Cela forme partie de la factorisation du code.

`TrackUtils` contient une finction `plot_track` qui quand elle est appelé pour n'importe quelle simulation, dessine le graph `plotly` avec centre de la track, nodes et agent_path (voir le script `tests/track_data/agent_path.py` comme exemple d'utilisation)

**Explication de l'organisaton des fichiers:**

-> Le dossier `/src/customAgents` contient les fichiers des agents que nous avons développés :

`AutoAgent.py` était une première tentative d'un agent automatisé qui suit la piste mais EST A IGNORER POUR L'INSTANT.

#### `MedianAgent.py` : L’agent que nous avons développé cette semaine et qui est à considérer.

-> Le dossier /src/utils contient des utilitaires pour analyser et visualiser les données :

`TrackUtils.py` : Contient les fonctions compute_curvature(nodes) et compute_slope(nodes), utilisées pour analyser la courbure et la pente de la piste.

`plot.py` : Permet la génération des graphiques et visualisations.
    
`csvRW.py` : Utilitaire pour lire et écrire des fichiers CSV.

mais ces 2 derniers fichiers sont à revoir. Il ne fait considérer que `TrackUtils.py`  pour l'instant.

-> Le dossier `/tests/custom_agents` contient toutes les implémentations des agents définis dans `/src/customAgents`

Par exemple, `MedianAgent` qu'on a impléménté cette semaine est testé dans `test_MedianAgent.py` ici.


On a remarqué que factoriser du code est toujours une tache continue chaque semaine et qu'on ne pourra jamais vraiment la mettre en "terminé".

---

### ii. Visualiser les nodes et la piste sur le même graphique en superposant les informations et en ajustant si nécessaire.
Le problème avec notre approche initale de visualisation de la track venait du fait que `self.obs` exprime les positions relatives au kart, tandis que `env.unwrapped.track.path_nodes` donne des positions en coordonnées absolues dans l’environnement de SuperTuxKart.

---
### iii.Chercher ou trouver le bon agent_path (penser aux coordonees relatifs et absolu) et tracer ainsi les graphes corrigés
On a découvert que la position actuelle du kart  est dans `env.unwrapped.world.karts[0].location`, qui est une variable dans un référentiel absolu.

Les graphes sont beaucoup plus logiques:

*Eg1: Lighthouse*
![image](https://github.com/user-attachments/assets/5a699144-ff0b-4688-9fd7-f5bbf6b5d36c)

*Eg2: xr591*
![image](https://github.com/user-attachments/assets/946cf849-5aae-4e4e-ae35-29ea16dc7239)
Ces images montrent que la les nodes et le centre sont bien alignés(pusique les nodes représentent le centre!) et en plus, le agent_path est correctement pris, donc nous voyons pour une simulation avec AI que le path suivi par l'agent est bien logique avec la forme de la track.

---
### iv. Faire la ligne 𝓵 entre la postion du kart et le n-ième prochain node : 
C'est la ligne tracé entre la position absolu du kart et la position du n-ième noeud.

Donné que `agent_abs_pos`, la position absolu de l'agent dans l'environnement est donné par `env.unwrapped.world.karts[0].location`, et que 
la liste de tous les noeuds du circuit est obtenue avec `env.unwrapped.track.path_nodes`. Pour chaque `node` de cette liste, on suit les étapes suivantes:

(i) 
```Python
agent_front = np.array(env.unwrapped.world.karts[0].front)
movement_vector = agent_front - agent_abs_pos
movement_vector /= np.linalg.norm(movement_vector)  # Normalisation
```
Détermine où l’agent "regarde" (`agent_front`).
Calcule le vecteur de mouvement (`movement_vector`), qui est la différence entre la position actuelle et la direction en face.
Normalisation du vecteur de mouvement pour garder uniquement la direction.

(ii)
```Python
track_nodes = [np.array(segment[0]) for segment in env.unwrapped.track.path_nodes] #path_start & path_end
```
Liste tous les nœuds de la piste (`track_nodes`).
Chaque `segment[0]` représente le point de départ d'un segment de la piste.


(iii) Filtrage des noeuds devant l'agent
```Python
nodes_ahead = []
for node in track_nodes:
    direction_to_node = node - agent_abs_pos
    node_distance = np.linalg.norm(direction_to_node)

    # Normalisation du vecteur direction
    if node_distance > 0:
        direction_to_node /= node_distance

    dot_product = np.dot(movement_vector, direction_to_node)

    # Vérifier la différence de hauteur
    height_diff = abs(node[1] - agent_abs_pos[1])

    # Vérifier si le nœud est devant l'agent et à une hauteur raisonnable
    if dot_product > 0 and height_diff < 5.0:
        nodes_ahead.append((i, node, node_distance))


direction_to_node = node - agent_abs_pos # Calcule le vecteur de direction entre l’agent et le nœud.
dot_product = np.dot(movement_vector, direction_to_node)
```
Vérifie si l’angle entre le mouvement de l’agent et la direction vers le nœud est positif.
Si dot_product > 0, cela signifie que le nœud est devant l’agent.
Filtrage des nœuds trop éloignés en hauteur (height_diff < 5.0).
Empêche la sélection de nœuds qui sont trop hauts ou trop bas par rapport à l’agent.

(iv) Tri des nœuds restants par distance
```Python
nodes_ahead.sort(key=lambda x: (x[0], x[2]))  # Tri par distance croissante
```
Trie la liste nodes_ahead en fonction de la distance entre l’agent et chaque nœud.
L’objectif est de sélectionner le deuxième nœud le plus proche.


(v) Sélection du deuxième nœud le plus proche
```Python
if len(nodes_ahead) > 1:
    second_node_pos = nodes_ahead[1][1]  # Sélection du deuxième nœud le plus proche
elif len(nodes_ahead) == 1:
    second_node_pos = nodes_ahead[0][0]  # Si un seul nœud disponible, on le prend
else:
    second_node_pos = agent_abs_pos  # Si aucun nœud valide, on garde la position de l’agent
```
Si plusieurs nœuds sont disponibles, on prend le deuxième (nodes_ahead[1][1]).
Si un seul nœud est disponible, on le garde.
Si aucun nœud n’est valide, on garde la position de l’agent (agent_abs_pos).

(vi) Calcul du vecteur entre l’agent et le deuxième nœud
```Python
vector = second_node_pos - agent_abs_pos
```

**Résulats obtenus**:

*Track xr591 avec 2 noeuds devant soi*:
![image](https://github.com/user-attachments/assets/e23eb19c-bcb5-4d47-aa5a-47bec7dd7597)

*mais si on prend 3 noeuds devant soi, l'algorithme peut prendre des noeuds qui ne sont pas sur le meme segment de track ou on est:*
![image](https://github.com/user-attachments/assets/e2fe4561-5911-4a21-9350-38daf42685a2)
Ceci est du au fait qu'on ne considère que la distance et le fait que le noeud est devant lui, mais ne prend pas en compte si le noeud est sur a un autre segment de piste.
C'est pour cela qu'on a introduit le test `height_diff` mais c'est à corriger car cela ne marche pas vraiment pour l'instant. 
C'est un début, mais à corriger...

---
### v. Faire un agent qui suit le n-ième prochain node 
On l'a appelé `MedianAgent`

Objectif: L’agent doit rester au centre de la piste en utilisant les données de `paths_end` de `self.obs`. 

Il ajuste la direction (steer), l’accélération et active le drift ou le nitro en fonction de la courbure de la piste.

On a d'abord tenté une approche en utilisant les positions absolues des nodes( `env.unwrapped.track.path_nodes`) mais on a réalisé que c'était mieux d'utiliser les 
positions relatives(dans `self.obs`) car pas besoin de convertir les données de env en "`kart_view()`".

On a découvert que utiliser le `path_end` et `path_start` du dict `self.obs` d'un kart revenait à accéder aux nodes.

Le path_start et path_end dépendent de la position acutuelle du kart et on peu récupérer le k-ième node devant nous avec `self.obs["paths_end"][k]` d'où 
```Python
path_end = self.obs["paths_end"][self.path_lookahead - 1]
```
dans le code, où `path_lookahead` est un param passé par l'utilisateur qui indique combien noeud devant le kart je veux considérer.

Ça marche assez bien car notre agent fait bien un tour de circuit, mais le steer n'était pas parfait. Il tournait un peu trop tard ou tot dans certains virages, ce qui nous a ammené à la prochaine tache, qui a été rajoutée en semaine:

---
### vi. Faire une fonction `compute_curvature` qui étant donné une liste de nodes calcule la courbure k entre les nodes
Elle estime la courbure en analysant les différences d’angle entre les nodes consécutifs.

Si la liste passée `nodes` est vide ou contient moins de 2 points, on ne peut pas calculer de courbure.

La technique utilisé pour le calcule est la suivante:
```Python
direction_changes = []
for i in range(len(nodes) - 1):
    dx = nodes[i + 1][0] - nodes[i][0]  # Différence en X
    dy = nodes[i + 1][1] - nodes[i][1]  # Différence en Y
    angle = np.arctan2(dy, dx)
    direction_changes.append(angle)
```
On parcourt tous les pairs de nodes consécutifs pour calculer l’angle qu’ils forment.
`dx` et `dy` sont les différences de coordonnées entre deux points consécutifs.
`np.arctan2(dy, dx)` donne l’angle d’orientation du segment (direction du vecteur reliant les deux points).
On stocke ces angles dans direction_changes.

`direction_changes`, lui, représente la liste contenant tous les angles formés entre les segments de la piste.
Plus les angles varient fortement entre les segments, plus la piste est courbée.

À la fin, on fait:
```Python
if len(direction_changes) > 1:
    curvature = np.mean(np.diff(direction_changes)) * 10  # Sensibilité ajustée avec *10
else:
    curvature = 0
```
On utilise `np.diff(direction_changes)` pour calculer la différence entre chaque angle → Cela donne l’intensité du changement de direction entre les segments.
Plus cette différence est grande, plus la courbure est forte.

On a ensuite cette fonction `compute_curvature` dans `MedianAgent` pour adapter le steer à la courbure de la piste.

Cela nous a donné un agent assez performant qui complète des tours de circuits. Toutefois, on a réalisé après quelques tests que l'agent n'arrivait pas à avoir assez de vitesse dans les pentes montantes avec virages car on lui demandait déjà de décélérer dans les virages.

C'est pour cela que nous a aussi rajouté la prochaine tache de:


---
### vii. Faire une fonction `compute_slope` qui étant donné une liste de nodes calcule la pente entre les nodes
Cette fonction calcule la pente (slope) d'un segment de piste en analysant la variation d'altitude (axe Z) entre deux nodes consécutifs.

Le but était de déterminer si le kart est en montée (pente positive) ou en descente (pente négative) afin de fournir cette information pour ajuster l’accélération de l’agent (plus d'accélération en montée, moins en descente).

Le calul ici était plutot logique également:
```Python
dz = node2[2] - node1[2]  # Différence de hauteur (axe Z)
dx = node2[0] - node1[0]  # Différence sur l’axe X
dy = node2[1] - node1[1]  # Différence sur l’axe Y
distance = np.sqrt(dx**2 + dy**2)  # Distance horizontale entre les deux nodes
```
`dz` : Différence d'altitude entre les deux nodes (axe Z).<br>
`dx` et `dy` : Différences horizontales (X et Y).<br>
`distance` : Distance horizontale entre les deux nodes, calculée avec le **théorème de Pythagore** :

$`distance = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}`$

Si distance == 0, cela signifie que les deux nodes ont la même position horizontale.
La pente serait infinie donc pour éviter une erreur (division par zéro), on retourne simplement 0.

On fait finalement le calcul de la pente:
Pente = variation verticale / distance horizontale
```Python
slope = dz / distance  
```
car  
 $`slope = \frac{z_2 - z_1}{distance}`$

La fonction retourne une valeur positive en montée(uphill) et une valeur négative en descente(downhill).

Cette fonction a été utilisé dans `MedianAgent` comme un des paramètres pour ajuster l'accélération:
```Python
acceleration = max(0.1, 1 - abs(curvature) + max(0, slope))
```

La performance de notre agent s'est améliorer car on a réglé les porblèmes sur les pentes, mais il y avait toujours des problèmes de steering dans certains virages sérrés pour certaines pistes.
On s'est alors dit que pour garder une bonne accélération et ne pas devoir choisir entre vitesse et rester sur la piste, on était obligé d'activer le drift dans les virages:

---
### viii. Activer Drift dans les virages et Nitro dans les lignes droites pour corriger `MedianAgent`
On a impléménté un threshold qui est le seuil minimum pour activer le drfit et nitro:
```Python
nitro_threshold = 0.02  # Define curvature threshold for nitro activation
use_nitro = abs(curvature) < nitro_threshold  # Use nitro if curvature is below threshold
drift_threshold = 40  # Define curvature threshold for drift activation
use_drift = abs(curvature) > drift_threshold  # Enable drift if curvature is high
```

---

Toutes ces modifications ont été concluentes pour faire un agent qui arrive sur la grande majorité des circuits à compléter un tour de piste. 

Toutefois, on a observé que pour certaines track, notre agent faisait un virage abrupte juste avant la ligne d'arrivé. 

On a compris que: La liste des nodes qu'on a est composée de plusieurs parties: il y a d'abord dans une suite continue les nodes d'une route par défault dans la track.
Ensuite, à la fin, les différentes options de routes(qui divergent dans le circuits) sont placés à la fin. 

C'est pour cela que notre agent qui regarde les n prochains nodes finit toujours pas un grand virage à la fin. La solution parait assez simple: 
elle est juste de continuer tout droit à la fin du circuit car la fin est toujours en lignes droites. La fin est connue car le dernier node correspond au tout premier node.
Cette observation a été observée en analysant les csv. (On peut le vor dans les csv appelés `{track_name}_track_nodes.csv`, qui sont disponibles dans `tests/records_csv/track_nodes`.
On essayera de le corriger au plus vite.

---

## 2. Apprentissage & Documentation  
> Cette semaine, on s'est concentré sur plus sur le code.

---

## 3. Questions 

Si on doit faire du reinforcement learning sur notre `MedianAgent`, quel critère peut-t-on prendre pour l'instant?

---


**Rapport rédigé par :** Wilson 

**Vérifié par :** Badr, Mahmoud  
