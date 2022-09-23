
# PyGLViewer

This is a simple python OpenGL viewer designed to have a quick visualization of the results of the simulations. The goal is *not* to do efficient/marvelous renderings, although you can tune a bit the viewer if you want.

## Authors

* Mickaël LY
* Thibaut METIVET

## How to use

### Dependencies 

* Python3
* GLFW3
* OpenGL

To install them (on Ubuntu) :
```
sudo apt-get install freeglut3 freeglut3-dev mesa-utils python3 python3-setuptools libglfw3-dev libassimp-dev python3-pip
pip3 install numpy Pillow PyOpenGL PyOpenGL-accelerate glfw scipy
```

### Test

Running
```
python3 main.py
```
should play one of the default base scenarios.

### Making your own scenarios

The examples of the file `scene.py` are quite self explanatory. 


### Comment qu'on fait

Classe Square 2D
    On fait une classe avec la description d'un carré en 2D
    Soit on défini une position absolue pour chaque vertex
    Soit on part sur une pos relative (plus simple pour les calculs après) on définit juste le centre et on calcul.
    On doit calculer M (la matrice) et J (le moment d'inertie)
    (vertex, longueur...)

Classe RigidBody
    On doit décrire xg et theta
