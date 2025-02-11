# Rapport Hebdomadaire - Semaine 4

**Date :** 11/02/2025  



## 1. Tâches réalisées cette semaine  
> Liste des tâches complétées et de leur statut.

- **Factoriser les codes de Test :** <br>
   Nous avons créé un répertoire « utils » qui contient 2 fichiers. Un fichier « csvRW.py » qui contient des codes servant à lire et écrire dans un fichier csv. 
   L’autre fichier « plot.py » contient des codes servant à dessiner des graphes pour des agents uniques et également pour les multi-agents. 
   Nous avons importé ces fonctions refactorisé dans nos fichiers test pour les raccourcir. Nous avons factorisé les tests pour les simulations à agent multiple et unique. 
   Il nous reste à factoriser le test pour les agents « custom » et pour les tests qui utilisent plotly au lieu de matplotlib. 
   C’est-à-dire les agents avec des comportements spéciaux : Les agents qui suivent les nodes et les agents effectuent la course en essayant de rester uniquement au milieu de la piste.

- **Compréhension du fonctionnement de la création de l'environnement:** <br>
  On a cherché dans le code comment étaient instanciés les différents environnements pré-enregistrés dans register et comment créer notre propre environnement de toute pièce. 
  La tentative de création d'environnement fut un échec mais nous avons quand même bien avancé sur la compréhension de leur fonctionnement.
  Note : Cette partie nous a pris le plus de temps cette semaine même s'il n'y a pas de résultat visible.
  Par contre, le diagramme de classe généré avec Pyreverse (voir prochain point) nous a pas mal éclairé sur la manière dont pystk2_gymnasium était organisé.
  
- **Diagramme de Classe** <br>
  Procédure : Installation de Pylint et utilisation de pyreverse pour faire le reverse engineering automatique de l'UML des classes et packages dans pystk2_gymnasium. <br>
  Note : on a préféré faire ça de manière automatique pour la scalability.


## 2. Apprentissage & Documentation  
> Ressources consultées, formations suivies, ou découvertes techniques.

| Sujet | Source |
|------------|------------|
| 02-1-dynamic_programming| Notebook

---

## 3. Questions & Problèmes rencontrés  
> Liste des blocages ou questions soulevées.

Est-ce que les wrappers valent le coup d'être étudiés, utilisera-t-on des environnements prédéfinis ou devrons-nous créer des environnements particuliers?

Nous ne comprenons pas comment superposer les nodes à la track associée, nous aimerions avoir les explications de Benjamin Piwowarski, sur quel référentiel se basent les nodes et la track.

---

**Rapport rédigé par :** Badr <br>
**Vérifié par :** Mahmoud, Wilson, Safa
