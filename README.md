# <img src="https://github.com/hampusborgos/country-flags/raw/main/svg/fr.svg" width="40"> TIPE 2024 - Jeux et Sport

Travail d'initiative personnelle encadré (TIPE) réalisé en classe préparatoire, filière MP, en 2024.

Ce projet se situe à la croisée de l'informatique pratique, de l'intelligence artificielle et de l'apprentissage par renforcement.

**Auteur :** Louis H.

**Stack :** 🐍 Python | ⚙️ C++ | 🧠 Keras | 📊 NumPy | 🌐 Flask

## Maîtriser informatiquement le jeu de l'Othello sans connaissances humaines.

> Comment concevoir un programme informatique capable d’apprendre à jouer au jeu de l’Othello en utilisant des réseaux de neurones artificiels entraînés sans données humaines, dans le but d’optimiser et de surpasser les méthodes habituellement utilisées pour résoudre ce jeu ?

## Description du problème

Le jeu d'Othello présente un espace d'états extrêmement vaste et une complexité combinatoire élevée. 

L'objectif de ce projet est de concevoir un agent capable d'apprendre et d'améliorer progressivement son niveau de jeu de manière autonome, en simulant des parties contre ses propres versions précédentes (*self-play*), jusqu'à surpasser les méthodes de recherche traditionnelles.

## Implémentation et Résolution

Le projet combine plusieurs briques technologiques et algorithmiques :

- **Moteur de jeu et interface :** Développement complet d'Othello en Python avec une interface web interactive (**Flask / HTML / CSS / JavaScript**).
- **Moteur Minimax (C++) :** Implémentation d'un premier moteur de référence basé sur l'algorithme Minimax, utilisant des *bitboards*, une table de hachage et une recherche en profondeur (profondeur 8, atteignant 2 à 3 millions de coups par seconde).
- **Réseaux de neurones :** Conception de deux architectures (un réseau séparant politique et valeur, puis une architecture unifiée à tronc partagé de 7 blocs résiduels) pour estimer la pertinence des coups et la probabilité de victoire.
- **Apprentissage par renforcement (*Self-play*) :** Génération automatique de millions de positions et entraînement itératif sans aucune intervention ni donnée humaine.

## Résultats

- **Version 1 :** Environ 32 800 parties jouées sur 15 jours ; première victoire contre le moteur C++ après environ 20 000 parties.
- **Version 2 :** Entraînement sur un jeu de données initial de 5,35 millions de positions (100 000 parties), suivi de 26 000 parties en *self-play* (10 jours) ; première victoire contre le moteur C++ après environ 8 000 parties.

### Présentation

> [**Présentation.pdf**](https://github.com/Louis-H-py/TIPE2024/blob/main/documents/presentation.pdf)

**Score :** 18.6/20 (top 5% among 7,000 candidates)

---

# <img src="https://github.com/hampusborgos/country-flags/raw/main/svg/gb.svg" width="40"> TIPE 2024 - Game and sport

Year-long Research Project completed in 2024 as part of the French preparatory program (MP track).

This project combines **Applied Computer Science**, **Artificial Intelligence**, and **Reinforcement Learning**.

**Author:** Louis H.

**Stack :** 🐍 Python | ⚙️ C++ | 🧠 Keras | 📊 NumPy | 🌐 Flask

## Mastering Othello Computationally Without Human Knowledge.

> How can we design a computer program capable of learning how to play Othello using artificial neural networks trained without human data, with the goal of optimizing and outperforming standard methods traditionally used to solve this game?

## Problem Description

Othello features an extremely vast state space and high combinatorial complexity.

The objective of this project is to design an agent capable of learning and progressively improving its playing strength autonomously by simulating games against its previous versions (*self-play*), eventually outperforming traditional search methods.

## Implementation and Approach

The project combines several technological and algorithmic components:

- **Game Engine and Interface:** Complete implementation of Othello in Python with an interactive web interface (**Flask / HTML / CSS / JavaScript**).
- **Minimax Engine (C++):** Development of a baseline engine using the Minimax algorithm with *bitboards*, transposition tables, and tree search (depth 8, reaching 2 to 3 million evaluated moves per second).
- **Neural Networks:** Design of two architectures (a separated policy/value network, then a unified architecture with a shared backbone of 7 residual blocks) to estimate move relevance and win probability.
- **Reinforcement Learning (Self-play):** Automatic generation of millions of board positions and iterative training without any human data.

## Results

- **Version 1:** Approximately 32,800 games played over 15 days; first victory against the C++ engine after roughly 20,000 games.
- **Version 2:** Trained on an initial dataset of 5.35 million positions (100,000 games), followed by 26,000 self-play games (10 days); first victory against the C++ engine after about 8,000 games.

> [**Présentation.pdf**](https://github.com/Louis-H-py/TIPE2024/blob/main/documents/presentation.pdf)

**Score :** 18.6/20 (top 5% among 7,000 candidates)
