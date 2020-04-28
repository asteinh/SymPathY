"""sympathor brings differential geometry to SVG paths.

sympathor enables you to extract a fully symbolic description of paths from \
MIME types `text/plain` or `image/svg+xml`. Based on this symbolic \
description, you can obtain a sampled path for further numerical processing, \
the path's natural parametrization, its Frenet frame, etc.

  Typical usage example:

  .. code-block:: python

      path = ParsePaths('path/to/file.svg')[0]
      t = path.tangent()
      c = path.curvature()
"""

from sympathor.parser import ParsePaths  # noqa
