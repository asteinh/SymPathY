import sympathor.elements as elements
from svg.path import Path
import casadi as cas
import numpy as np


class SymbolicPath(elements.SymbolicMixin, Path):
    """
    A symbolic path description extending `svg.path.Path`.

    This class mates various symbolic elements by building a composite path
    description. Based on this composite path, properties and quantities of
    differential geometry can be derived, e.g. tangent and normal vectors, or
    the curvature.
    This class also implements a convenient path-level access to SVG
    transforms, which are simply delegated to each element.

    Parameters
    ----------
    path : svg.path.Path
        An `svg.path.Path` object, e.g. parsed using `svg.path.parse_path()`,
        as done in `sympathor.ParsePaths()`.

    """
    def __init__(self, path):
        Path.__init__(self)
        elements.SymbolicMixin.__init__(self)

        # build path from segments
        for seg in path._segments:
            clss = 'Symbolic' + seg.__class__.__name__
            self._segments.append(getattr(elements, clss)(seg))

        self.__symbolic_setup()

    def __symbolic_setup(self):
        # build composite symbolic expression
        self._calc_lengths()
        expr = cas.MX.nan(2, 1)
        for i in range(len(self._segments)-1, -1, -1):
            s_max = self._fractions[i]
            s_min = self._fractions[i-1] if i > 0 else 0
            s_loc = (self._s - s_min) / self._lengths[i]
            expr = cas.if_else(self._s <= s_max, self._segments[i].point(s_loc), expr)
        self._point_expr = expr
        self._point = cas.Function('point', [self._s], [self._point_expr])

        dp_ds = cas.jacobian(self._point_expr, self._s)
        # unit tangent vector
        self._tangent_expr = cas.if_else(cas.norm_2(dp_ds) > 0, dp_ds / cas.norm_2(dp_ds), cas.DM([0, 0]))
        self._tangent = cas.Function('tangent', [self._s], [self._tangent_expr])
        dt_ds = cas.jacobian(self._tangent_expr, self._s)
        # unit normal vector
        self._normal_expr = cas.if_else(cas.norm_2(dt_ds) > 0, dt_ds / cas.norm_2(dt_ds), cas.DM([0, 0]))
        self._normal = cas.Function('normal', [self._s], [self._normal_expr])
        # curvature value
        self._curvature_expr = cas.if_else(cas.norm_2(dp_ds) > 0, cas.norm_2(dt_ds) / cas.norm_2(dp_ds), 0.0)
        self._curvature = cas.Function('curvature', [self._s], [self._curvature_expr])

    def __maybe_map_function(self, fcn, s):
        s_ = np.asarray(s).flatten()
        N = np.size(s_)
        fcn_ = fcn.map(N) if N > 1 else fcn
        return fcn_(s_)

    def __eq__(self, other):
        if not isinstance(other, SymbolicPath):
            return NotImplemented
        if len(self) != len(other):
            return False
        for s, o in zip(self._segments, other._segments):
            if not s == o:
                return False
        return True

    def set_natural_parametrization(self, new_state=True):
        """
        Toggle natural parametrization of path.

        Parameters
        ----------
        on : bool
            Activate natural parametrization
        """
        for seg in self._segments:
            seg.set_natural_parametrization(set=new_state)
        self.__symbolic_setup()

    def length(self):
        """
        Compute overall length of path.

        Returns
        -------
        length : numpy.float
            Length of path

        """
        return np.float(Path.length(self))

    def point(self, s=None):
        """
        Obtain point along the path.

        Parameters
        ----------
        s : float or list of float, optional
            The parameter value(s) at which the path should be sampled.

        Returns
        -------
        point : casadi.Function or numpy.ndarray
            Function of symbolic description of point if no parameter value
            was provided; otherwise an array of point coordinates
            corresponding to the given parameter values.

        """
        if s is None:
            return self._point_expr
        else:
            p = self.__maybe_map_function(self._point, s)
            return np.array(p)

    def tangent(self, s=None):
        """
        Obtain tangent vector along the path.

        Parameters
        ----------
        s : float or list of float, optional
            The parameter value(s) at which the tangent vector should be
            evaluated.

        Returns
        -------
        point : casadi.Function or numpy.ndarray
            Function of symbolic description of tangent vector if no parameter
            value was provided; otherwise an array of components of the
            tangent vector corresponding to the given parameter values.

        """
        if s is None:
            return self._tangent
        else:
            t = self.__maybe_map_function(self._tangent, s)
            return np.array(t)

    def normal(self, s=None):
        """
        Obtain normal vector along the path.

        Parameters
        ----------
        s : float or list of float, optional
            The parameter value(s) at which the normal vector should be
            evaluated.

        Returns
        -------
        point : casadi.Function or numpy.ndarray
            Function of symbolic description of normal vector if no parameter
            value was provided; otherwise an array of components of the normal
            vector corresponding to the given parameter values.

        """
        if s is None:
            return self._normal
        else:
            n = self.__maybe_map_function(self._normal, s)
            return np.array(n)

    def curvature(self, s=None):
        """
        Obtain curvature along the path.

        Parameters
        ----------
        s : float or list of float, optional
            The parameter value(s) at which the curvature should be evaluated.

        Returns
        -------
        point : casadi.Function or numpy.ndarray
            Function of symbolic description of curvature if no parameter
            value was provided; otherwise an array of curvature values
            corresponding to the given parameter values.

        """
        if s is None:
            return self._curvature
        else:
            c = self.__maybe_map_function(self._curvature, s)
            return np.array(c)

    # transforms
    def matrix(self, a, b, c, d, e, f):
        for seg in self._segments:
            seg.matrix(a=a, b=b, c=c, d=d, e=e, f=f)
        self.__symbolic_setup()

    def translate(self, dx, dy=0):
        for seg in self._segments:
            seg.translate(dx=dx, dy=dy)
        self.__symbolic_setup()

    def rotate(self, theta, x=0, y=0):
        for seg in self._segments:
            seg.rotate(theta=theta, x=x, y=y)
        self.__symbolic_setup()

    def scale(self, x, y=None):
        if y is None:
            y = x
        for seg in self._segments:
            seg.scale(x=x, y=y)
        self.__symbolic_setup()

    def skewX(self, theta):
        for seg in self._segments:
            seg.skewX(theta=theta)
        self.__symbolic_setup()

    def skewY(self, theta):
        for seg in self._segments:
            seg.skewY(theta=theta)
        self.__symbolic_setup()
