# SUDOKU

## Description

Ce projet a pour but de résoudre des grilles de Sudoku en python, sans dépendance et le plus rapidement possible.
<br>La philosophie est d'utiliser un minimum d'itérations sur la grille pour réduire le temps d'execution.

## Exécution

`python run.py`

## Architecture

Le code s'articule autour de 3 classes :

- **GridCell**

Responsable de la position et des possibilités d'une cellule du Sudoku.
<br>Lorsqu'il ne reste plus que 1 possibilité, `GridCell` notifie `GridProcessor`.

- **Grid**

Responsable de la grille du Sudoku.
<br>Cette classe propose des méthodes pour filtrer la grille, par ligne, par colonne, par bloc 3x3 et par valeur.
<br>`Grid.grid` représente la grille du sudoku.
<br>`Grid.possibilities` représente le brouillon utilisé pour résoudre la grille. 
<br>Pour chaque cellule non résolue, `Grid.possibilities` contient une instance de `GridCell` qui sera retirée dès que la valeur de la cellule est trouvée.

- **GridProcessor**

Responsable de la résolution du Sudoku.
<br>Cette classe traite les notifications envoyées par les instances de `GridCell`. Tant qu'une nouvelle cellule est résolue, l'ensemble des stratégies pour réduire des possibilités sont exécutées. Ces stratégies utilisent un ensemble de filtres mis à disposition par les méthodes de `Grid`.
