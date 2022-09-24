#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of SimulationTeachingElan, a python code used for teaching at Elan Inria.
#
# Copyright 2020 Mickael Ly <mickael.ly@inria.fr> (Elan / Inria - Université Grenoble Alpes)
# SimulationTeachingElan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SimulationTeachingElan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SimulationTeachingElan.  If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
import matplotlib.pyplot as plt

from .abstract_dynamic_system import AbstractDynamicSystem

## Dummy dynamic system just to test
class PendulumDynamicSystem(AbstractDynamicSystem):

    def __init__(self, rod):
        ## Constructor
        # @param self
        # @param rod  
        super().__init__()
        self.rod = rod

        # Animations parameters
        self.colours = np.copy(self.rod.constColours)

        # Euler explicit
        self.g = 9.81
        self.l = 0.5
        self.theta = np.pi / 6.
        self.thetaDot = 0.
        self.M = 1.
        self.h = 0.01
        self.cin = 0.
        self.pot = 0.
        self.meca = 0.
        self.i = 0
        self.thetas = []

    def step(self):
        # Vertex Position update 
        self.rod.positions[0] = self.l * np.sin(self.theta)
        self.rod.positions[1] = - self.l * np.cos(self.theta)

        # Theta update
        oldTheta = self.theta
        self.theta += self.h * self.thetaDot
        self.thetaDot += self.h * -(self.g/self.l) * np.sin(oldTheta)

        # Data visualization
        self.i += 1
        sampleSize = 1000
        self.thetas.append(self.theta)
        indexes = [j for j in range(sampleSize)]
        if self.i == sampleSize:
            fig, ax = plt.subplots()
            ax.plot(indexes, self.thetas)
            plt.show()

        # Energy calculation
        self.cin = 1/2 * self.M * np.power((self.l * self.thetaDot), 2)
        self.pot = self.M * self.g * (- np.cos(self.theta) * self.l)
        self.meca = self.cin + self.pot
        # print(self.meca)
