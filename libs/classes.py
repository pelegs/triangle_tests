import numpy as np
from .mathlib import *


class Side:
    """
    Represents a side of a polygon in 3D space.
    It is defined by two edges, such that edges[0] is the start point
    and edges[1] is the end point. The direction is given by the unit vector
    from the start pointing towards the end.
    NOTE: it is best to input the edges as a 2x3 numpy array: first row is edges[0],
    second row is edges[1].
    """
    def __init__(self, edges):
        self.edges = edges
        self.direction = unit(self.edges[1] - self.edges[0])

    def point_on(self, t):
        """
        The (parametric) line equation for the side is given by
        L(t) = start + direction*t. This function returns a point on the
        line given the parameter t.
        """
        return self.edges[0] + t * self.direction

    def __str__(self):
        return f"Start: {self.edges[0]}, end: {self.edges[1]}, direction: {self.direction}"


class Plane:
    """
    Represents a plane in 3D space.
    The plane is constructed from a direction (given by the normal vector)
    and a point on the plane. The normal form is a 4-vector with components
    (a, b, c, d), such that they solve the equation ax+by+cz+d=0.
    """
    def __init__(self, normal, point):
        self.normal = normal
        self.point = point
        self.get_normal_form()

    def get_normal_form(self):
        a, b, c = self.normal
        px, py, pz = self.point
        d = -(a*px + b*py + c*pz)
        self.normal_form = np.array([a, b, c, d])

    def __str__(self):
        normal_txt = ",".join(map(str, self.normal))
        return f"Normal: {normal_txt}"


class Triangle:
    """
    Represents a triangle in 3D space.
    It takes three 3D points as vertices, preferably as a 3x3 numpy array
    (s.t. each row represents a vertex). From this it creates the appropriate
    three sides of the triangle and the plane it lies on.
    """
    def __init__(self, vertices):
        self.vertices = vertices
        self.create_sides()
        self.create_plane()

    def create_sides(self):
        # TODO: add case where sides are colinear
        pairs = np.array([
            (a, b)
            for idx, a in enumerate(self.vertices)
            for b in self.vertices[idx+1:]
        ])
        self.sides = [Side(pair) for pair in pairs]

    def create_plane(self):
        self.v1 = self.vertices[1] - self.vertices[0]
        self.v2 = self.vertices[2] - self.vertices[0]
        normal = unit(np.cross(self.v1, self.v2))
        point = self.vertices[2]
        self.plane = Plane(normal, point)

    def point_inside(self, p):
        """ Checks whether a given point p is inside the triangle. """
        trans_triangle = self.vertices - p
        u = np.cross(trans_triangle[1], trans_triangle[2])
        v = np.cross(trans_triangle[2], trans_triangle[0])
        w = np.cross(trans_triangle[0], trans_triangle[1])
        if np.dot(u, v) < 0:
            return False
        if np.dot(u, w) < 0:
            return False
        return True

    def __str__(self):
        return f"""
        Vertices: {self.sides[0]}, {self.sides[1]}, {self.sides[2]}.
        Basis: {self.v1}, {self.v2}
        Plane: normal: {self.plane.normal}, point: {self.plane.point}.
        """


if __name__ == "__main__":
    pass
