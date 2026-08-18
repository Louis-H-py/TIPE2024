# TIPE Louis H.

###### Titre | MCOT | DOT

---

### Titre :

**Maîtriser informatiquement le jeu de l'Othello sans connaissances humaines.**

### Ancrage dans le thème de l'année :

Le projet de TIPE **Othello AI** s'intéresse à la possibilité d'utiliser de l'intelligence artificielle dans le but
d'améliorer les méthodes informatiques traditionnelles de résolution des jeux de plateau comme l'Othello. Il s'encre
donc
dans la sous-catégorie "Jeux" du thème de l'année.

*41 mots*

### Motivations :

Mon TIPE reprend les travaux menés par Google DeepMind concernant AlphaGo Zero qui m'ont marqués plus jeune. Il
correspond
également à mon souhait d'orientation dans certains milieux de l'intelligence artificielle, et me permet de comprendre
et de
recréer simplement le fonctionnement d'AlphaGo appliqué au jeu de l'Othello.

*47 mots*

# MCOT

### Positionnement thématique :

**Informatique (pratique)** ; **Informatique (théorique)** ; *Mathématiques (Probabilités)*

### Mots clés :

| **Français**                    | **Anglais**               |
|---------------------------------|---------------------------|
| Intelligence artificielle       | Artificial intelligence   |
| Jeux de plateau                 | Board game                |
| Réseaux de neurones artificiels | Artificial neural network |
| Apprentissage par renforcement  | Reinforcement learning    |
| Arbre de recherche              | Search tree               |

### Bibliographie commentée :

En 1997, le superordinateur *Deep Blue* [1] bat aux échecs Garry Kasparov, alors meilleur joueur au monde. Dès
lors, il ne reste plus que le jeu de Go qui peut résister aux machines. Étant donné sa complexité combinatoire, il
semblait impossible de parvenir un jour à maîtriser le jeu, en effet le nombre de parties de Go possibles s’élève à
$10^{600}$, contre $10^{120}$ pour les échecs.

Habituellement pour maîtriser un jeu de plateau comme les échecs ou l’Othello, on a recours à un arbre de
recherche*MinMax*. Pour l’optimiser, on utilise des méthodes telles que les *bitboard*, l’élagage *Alpha-beta* et des
tables de transposition [2]. Malgré ses optimisations, cela reste insuffisant pour le jeu de Go. Une solution est alors
d’utiliser un arbre de recherche de Monte-Carlo [3], permettant une exploration plus profonde de l’arbre moyennant une
recherche plus incomplète. Cette méthode associée à celles énumérées plus haut permet de maîtriser correctement le Go
face à un débutant sur un petit plateau.

En 2016, c’est la filière *DeepMind* de *Google* qui réussit l’impossible à l’aide de son programme *AlphaGo* [3].
Leur approche consiste à utiliser un arbre de recherche de Monte-Carlo, guidé par deux réseaux de neurones qui
optimisent l’exploration de l’arbre. Le fonctionnement des réseaux vise à reproduire informatiquement le comportement du
cerveau humain. Ils reposent sur de l’apprentissage profond [4] et ont été entraînés sur plus de 150.000 parties de Go
humaines.

L’idée de *DeepMind* est de construire deux réseaux de neurones résiduels par blocs [5] : Un réseau politique
(_policy_) et un réseau de valeur (_value_) [3]. Le premier permettra de prédire quels coups sont les plus pertinents à
explorer dans l’arbre et le second jouera le rôle d’une heuristique, indiquant la probabilité de gagner sur un plateau
donné. On peut par ailleurs assembler les deux réseaux de neurones pour n’en former qu’un dans le but de diminuer le
temps de calcul, c’est ce que fera *DeepMind* plus tard avec *Alpha Zero* [6].

En 2017, *DeeMind* décide de pousser *AlphaGo* plus loin, ils conçoivent *AlphaGo Zero* [7]. Elle a la
particularité de s’être entraînée sans données humaines, mais en utilisant de l’apprentissage par
renforcement, [8] qui repose sur de nombreuses méthodes mathématiques et informatiques permettant de faire apprendre aux
réseaux de neurones sans données extérieures, notamment en les faisant jouer contre eux-mêmes [9].

Pour entraîner  *AlphaGo Zero*, les chercheurs de *DeepMind* l'ont fait jouer contre plusieurs versions d'elle-même,[9] mais certains
de ses coups sont aléatoires, dans le but de lui faire découvrir des stratégies. Ils passent ensuite à l’apprentissage par
renforcement [8] qui vise, en fonction de chaque configuration de plateau, à entraîner le réseau à prédire les prochains
plateaux et à estimer leur valeur. Puis, on compare le modèle entraîné avec sa version précédente. S’il est meilleur,
il est considéré comme le nouveau modèle de référence, sinon il devra continuer de s’entraîner. De cette manière, on
garantit à la fois que le modèle découvre des nouvelles stratégies, mais aussi que sa maîtrise du jeu reste toujours
croissante au cours de l'apprentissage.

L’Othello quant à lui est un candidat parfait pour mettre en application et adapter les
travaux de *DeepMind* dans le but d’observer le gain de maîtrise du jeu. C'est un jeu de plateau plus simple que les
échecs d’un point de vue combinatoire avec seulement $10^{58}$ parties possibles. Ce jeu à la particularité d'avoir 
un plateau qui évolue beaucoup au cours du temps par rapport à d’autres jeux, ce
qui rend une partie difficilement prévisible pour l’Homme. Il se prête donc parfaitement à la comparaison entre
la méthode naïve et celle utilisant de l'intelligence artificielle.

Au-delà de la simple résolution d'un jeu de plateau, ses méthodes d'apprentissage par renforcement sur des réseaux
de neurones trouvent des applications notamment pour les véhicules autonomes, dans le milieu médical, en finance [10] 
et dans l'industrie.

*629 mots*

### Problématique retenue :

Comment concevoir un programme informatique capable d’apprendre à jouer au jeu de l’Othello en utilisant des réseaux de
neurones artificiels entraînés sans données humaines, dans le but d’optimiser et de surpasser les méthodes
habituellement utilisées pour résoudre ce jeu ?

*41 mots*

### Objectif du TIPE :

Le TIPE se décompose en plusieurs objectifs :

1. Conception d'un algorithme "naïf" de résolution de l'Othello qui servira de point de comparaison dans le futur.
2. Conception du programme de résolution qui utilise les réseaux de neurones pour sa résolution.
3. Construction de l'environnement d'entraînement qui va permettre l'apprentissage par renforcement des modèles.
4. Entraînement des modèles, évaluation de leur niveau et modification de la structure des réseaux de neurones.
5. Comparaison avec des humains et avec l'algorithme "naïf".

On pourra donc conclure sur l'amélioration apportée par le/les réseau(x) de neurones sur la maîtrise de l'Othello.

*97 mots*

### Références bibliographiques :

**[1]** M. Campbell, A. Hoane, and F.-H. Hsu, <u>"Deep blue,"</u>*Artificial Intelligence*, vol. 134, no. 1-2, pp.
57–83, 2002.

**[2]** Pascal Pons. <u>Solving connect 4: how to build a perfect
ai. </u> [http://blog.gamesolver.org/](http://blog.gamesolver.org/) *Consulté le 2 Avril 2023*

**[3]** Silver, D., Huang, A., Maddison, C.*et al.*<u>"Mastering the game of Go with deep neural networks and tree
search."</u>*Nature***529**, 484–489 (2016).

**[4]** LeCun, Y., Bengio, Y. & Hinton, G. <u>"Deep learning."</u>*Nature***521**, 436–444 (2015).

**[5]** Cazenave, T. <u>"Residual Networks for Computer Go"</u>. IEEE Transactions on Computational Intelligence and AI
in Games. PP. 1-1. (2017).

**[6]** David Silver *et al.* <u>"A general reinforcement learning algorithm that masters chess, shogi, and Go through
self-play."</u> Science **362**,1140-1144 (2018).

**[7]** Silver, D., Schrittwieser, J., Simonyan, K.*et al.*<u>"Mastering the game of Go without human knowledge.</u>"
*Nature***550**, 354–359 (2017).

**[8]** Hessel, M., <u>"Rainbow: Combining Improvements in Deep Reinforcement Learning"</u>, <i>arXiv e-prints
1710.02298</i>, 2017.

**[9]** Baker, B., <u>"Emergent Tool Use From Multi-Agent Autocurricula"</u>, *arXiv e-prints* 1909.07528, 2019.

**[10]** Du, Jiayi & Jin, Muyang & Kolm, Petter & Ritter, Gordon & Wang, Yixuan & Zhang, Bofei. (2020).
Deep Reinforcement Learning for Option Replication and Hedging. The Journal of Financial Data Science. 2. 44-57

# DOT

[ ] 7 - 12 mars 2023 : Conception du jeu d'Othello et test de premières approches en utilisant une recherche en arbre de
Monte-Carlo en Python, HTML, CSS et Javascript.

[ ] 2 - 8 avril 2023 : Conception de l'algorithme de résolution 'naïf' de l'Othello en C++ utilisant des*bitboard*, une
table de*hashage*et un algorithme min-max.

[ ] 10 - 11 avril 2023 : Conception des premiers réseaux de neurones (*policy*et*value*) en Python avec Tensorflow et
Keras. Ce sont au départ de simples réseaux de neurones à convolution (CNN).

[ ] 16 - 17 avril 2023 : Conception du système d'entrainement des modèles, dans un premier temps à*thread*unique puis
ensuite sur plusieurs*threads*pour accélérer l'entrainement et de jouer plus de parties en même temps.

[ ] 19 - 21 avril 2023 : Passage à des réseaux résiduels par bloc pour accélérer l'entrainement et augmenter la
précision des prédictions. Hésitation quant au nombre de blocs (entre 5 et 10) pour finalement choir 7 blocs.

[ ] 21 avril - 20 mai 2023 : Entrainement des réseaux de neurones par renforcement. La probabilité d'un coup aléatoire
est régressive au cours du temps.

[ ] 3 mai : Correction d'une erreur majeure entachant la progression correcte des modèles. Le meilleur coup renvoyé par
le modèle n'était pas celui de l'arbre mais celui du*policy network*.

[ ] 17 - 18 mai 2023 : Passage à un unique réseau de neurones. Entrainement 'classique' sur la base de 2.000.000 de
parties jouées par le modèle à deux réseaux de neurones puis retour à un entrainement par renforcement.
