\subsection{Taxonomie}
Si nous regardons sur la figure \ref{fig:interface}, nous voyons que la première demande concerne la taxonomie. Concernant ce sujet-là, un éventail de choix peut être fait. Une fois le niveau de taxonomie choisi, un nouveau panel de choix s'ouvre afin de permettre la sélection d'une espèce. Par exemple, si nous choisissons de nous limiter aux embranchements, il faut par la suite sélectionner l'embranchement que nous souhaitons projeter sur la carte. Lors de la sélection du niveau de taxonomie, la projection fera abstraction des autres choix dans les autres niveaux. Il n'y a qu'une seule spécificité, elle se situe au niveau des espèces. En effet, nous pouvons choisir une ou deux espèces différentes à projeter sur la carte. Celles-ci seront visualisées avec des couleurs différentes.
\subsection{Année}
Sur notre interface, nous avons la possibilité de choisir un intervalle d'années. Sachant que les années sélectionnées sont inclues dans la sélection. 

\subsection{Groupement}
La fonction groupement sert, comme son nom l'indique, à grouper des observations qui sont proches l'une de l'autre. Prenons les observations d'hirondelles (Delichon urbicum) en 2015 pour illustrer cela. 
\begin{figure*}[h]
    \centering
    \begin{subfigure}[b]{0.475\textwidth}
        \centering
        \includegraphics[width=\textwidth]{hirondelle_non_groupe.png}  
        \caption{Sans l'option groupement}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.475\textwidth}  
        \centering 
        \includegraphics[width=\textwidth]{hirondelle_groupe.png}
        \caption{Avec l'option groupement}
    \end{subfigure}
    \caption{Effet de l'option groupement sur la carte}
    \label{fig:graphique}
\end{figure*}

Avec l'option groupement, nous pouvons cliquer sur une zone et nous allons tout de suite avoir un zoom sur celle-ci. Si nous zoomons par nous-mêmes, les bulles avec le nombre d'observations vont se multiplier en plus petites bulles.

\subsection{Dynamique}
\subsubsection{Désactivé}
\begin{itemize}
    \item \textbf{Nom} : La dernière option à choisir est le nom que nous voulons donner à notre carte. Effectivement, l'interface va générer une carte en html, celle-ci va être enregistrée à l'endroit souhaité ou par défaut, là où le code se situe. Après avoir appuyé sur \textit{Ok}, la carte va s'ouvrir d'elle même dans un navigateur. 
    \item \textbf{Carte} : Quelques informations supplémentaires concernant la carte, il y a une fonctionnalité de zoom, de dézoom. De plus, nous pouvons nous déplacer dans l'espace. 
\begin{figure}[H]
    \centering
    \includegraphics[height=5cm, width=4cm]{legende.png}
    \caption{Fonctionnalité de notre carte}
    \label{fig:legende}
\end{figure}

Nous avons aussi différentes cartes possibles qui peuvent être changées au moment de l'analyse. Par défaut, c'est le fond de carte openstreetmap qui va être sélectionné au moment de l'ouverture. Toujours dans ce panel d'options, si nous avons décidé de mettre plusieurs années ou même plusieurs espèces sur la carte, nous pouvons cocher ou décocher les années pour chaque espèce afin d'enlever ou ajouter les données intéressantes. Chaque année de l'interval choisi correspondra à une couleur sur la carte pour une meilleure visibilité.\\
\\
Enfin, le dernier choix que nous avons fait pour la carte concerne les cartes qui n'ont pas l'option groupement. Comme nous l'avons précisé plus haut, les données de localisation sont mises sur un quadrillage, et plusieurs données sont amenées à se superposer. C'est pour cela que la colonne \textit{num\_obs} a été créé au moment de la transformation des données. Pour visualiser les observations sur la carte, nous avons mis des cercles à chaque point d'observation, et le diamètre de celui-ci dépend du nombre d'observations de l'espèce sélectionnée à cet endroit précis. Le diamètre est décidé selon une échelle logarithmique en base 10, du nombre d 'observations faites. Pour chaque pointeur (sans groupement) ou cercle (avec groupement), en cliquant dessus, une fenêtre d'information apparaît avec l'année de l'observation, le nombre d'observations (pour le sans groupement) et le nombre d'individus comptés. 
\end{itemize}


\subsubsection{Activé}
Le principe de cette option va être de pouvoir observer un mouvement d'évolution des observations au niveau du temps. Pour cela, nous allons générer une vidéo qui va montrer cette évolution sur une période de temps défini. 
\begin{itemize}
    \item \textbf{Nom} : c'est le même principe lorsque l'option dynamique n'est pas activée. Cependant, ici, ce sera le nom de la vidéo.

    \item \textbf{Carte} : étant dans une vidéo, nous n'avons plus autant de liberté que sur la carte. Le zoom est prédéfini pour visualiser la Belgique dans son ensemble et une seule couleur est utilisée car les années vont s'enchaîner.
\end{itemize}

Grâce à cette option, nous pouvons être témoin si une espèce se déplace, d'années en années, sur le territoire, ou encore si une espèce augmente la taille de son territoire dans le temps.


\subsection{Implémentation}
Cette interface a été implémentée en Python 3.9 et a fait appel à différentes librairies :

\begin{itemize}
    \item panda : est utilisé pour la gestion de la base de données.
    \item tkinter\cite{tinker} : cette librairie nous permet de construire notre interface.
    \item folium\cite{folium} : permet de générer la carte et toutes les fonctionnalités sur celle-ci.
    \item numpy :  utilisé seulement pour l'échelle logarithmique sur les cartes.
    \item webbrowser et os : produit, enregistre et ouvre notre nouveau fichier html.
    \item html2image, cv2, shutil : permet de transformer nos cartes en images, puis de les réunir en une vidéo.

\end{itemize}
