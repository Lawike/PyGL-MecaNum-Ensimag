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

from termios import IXANY
import numpy as np

from .abstract_dynamic_system import AbstractDynamicSystem


class SpiningSquareDynamicSystem(AbstractDynamicSystem):

    def __init__(self, squareMesh):
        # Constructor
        # @param self
        # @param squareMesh
        super().__init__()
        self.squareMesh = squareMesh
        l = 10

        self.it = 0
        self.delta = 1
        self.period = 120
        self.M = 10
        self.theta = 0

        # TODO Absolute positions (temporary) we will calculate locally the positions of the vertexs later
        self.positions = [[-l/2.,  l/2, 0],
                          [ l/2.,  l/2, 0],
                          [ l/2., -l/2, 0],
                          [-l/2., -l/2, 0]]
        # self.currentPositions = self.positions
        
        # mk is the mass at a specific vertex position
        # In our case we admit that each vertex has the same mass (a fraction of the global mass)
        # The mass is uniformly distributed between each vertex
        self.mk = self.M / len(self.positions)

        # self.currentDoF = [0, 0]
        # self.currentDDoF = [0, 0]
        self.omegaN = 0
        self.aN = 0
        self.J = 0

        # Initializing Omega (angular velocity)
        self.omega = 1

        
    
    def S(x, y, z):
        return [[0, -z, y],
                [z, 0, -x],
                [-y, x, 0]]

    def JPoint(x, y, z, m):
        Jx = m * (y**2 + z**2)
        Jy = m * (x**2 + z**2)
        Jz = m * (x**2 + y**2)
        Ixy = m * x * y
        Ixz = m * x * z
        Iyz = m * y * z
        return [[Jx, -Ixy, -Ixz],
                [-Ixy, Jy, -Iyz],
                [-Ixz, -Ixz, Jz]]

    def J(self):
        return sum([self.JPoint(x, y, z, self.mk) for [x, y, z] in self.positions])

    def step(self):
        oldOmega= self.omegaN
        self.omegaN = np.linalg.inv(self.J()) * np.exp(-self.delta * self.S(self.theta)) * (self.J() * self.omegaN + self.delta * np.transpose(self.rotation) * self.M)

        self.aN = (self.omegaN - oldOmega) / self.delta
        self.theta = self.omegaN + self.delta / 2 * self.aN
        
        self.rotation *= np.exp(self.delta * self.theta)
        print(self.rotation)

        for point in self.positions:
            point = self.rotation * point

        self.squareMesh.positions = self.positions
        
