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

from .abstract_dynamic_system import AbstractDynamicSystem


class SpiningSquareDynamicSystem(AbstractDynamicSystem):

    def __init__(self, squareMesh):
        # Constructor
        # @param self
        # @param squareMesh
        super().__init__()
        self.squareMesh = squareMesh
        l = 1

        self.it = 0
        self.delta = 1.
        self.period = 120
        self.M = 10
        self.theta = [0.,2.,0.]
        self.rotation = np.identity(3)

        # TODO Absolute positions (temporary) we will calculate locally the positions of the vertexs later
        self.positions = [[-l/2.,  l/2., 0.],
                          [ l/2.,  l/2., 0.],
                          [ l/2., -l/2., 0.],
                          [-l/2., -l/2., 0.]]
        # self.currentPositions = self.positions
        
        # mk is the mass at a specific vertex position
        # In our case we admit that each vertex has the same mass (a fraction of the global mass)
        # The mass is uniformly distributed between each vertex
        self.mk = self.M / len(self.positions)

        # self.currentDoF = [0, 0]
        # self.currentDDoF = [0, 0]
        self.omegaN = [0,0,0]
        self.aN = 0

        # Initializing Omega (angular velocity)
        self.omega = 1

        
    # Makes a vec3 into a matrix 3,3
    def S(self, x, y, z):
        return [[0., -z, y],
                [z, 0., -x],
                [-y, x, 0.]]

    # Inertia Tensor (of the whole solid)
    def J(self):
        result = np.zeros((3,3))
        for [x, y, z] in self.positions :
            result += self.JPoint(x, y, z, self.mk)
        return result

    # Inertia tensor (for a point in a solid)
    def JPoint(self, x, y, z, m):
        Jx = m * (y**2. + z**2.)
        Jy = m * (x**2. + z**2.)
        Jz = m * (x**2. + y**2.)
        Ixy = m * x * y
        Ixz = m * x * z
        Iyz = m * y * z
        return [[Jx, -Ixy, -Ixz],
                [-Ixy, Jy, -Iyz],
                [-Ixz, -Ixz, Jz]]


    def step(self):
        oldOmega = self.omegaN

        left = np.linalg.inv(self.J()) * np.exp(-self.delta * np.array(self.S(self.theta[0], self.theta[1], self.theta[2])))
        print('left : ', left)
        right = self.J() * self.omegaN + self.delta * np.transpose(self.rotation) * self.M
        print('right', right)

        self.omegaN = left * right

        # We get a 3x3 matrix but we should get a vec3 ...
        print('omega', self.omegaN)

        self.aN = (self.omegaN - oldOmega) / self.delta
        # Commented because omegaN should be a vec3 and it currently crash the code
        # self.theta = self.omegaN + self.delta / 2 * self.aN
        
        # self.rotation *= np.exp(self.delta * self.theta)
        for point in self.positions:
            point = self.rotation * point

        self.squareMesh.positions = self.positions
        
