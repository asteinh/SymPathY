.. toctree::
    :maxdepth: 2
    :hidden:
    :glob:
    :caption: Docs

    quick-start
    input-formats

.. toctree::
    :maxdepth: 2
    :hidden:
    :glob:
    :caption: API

    api/index

Welcome to sympathor's documentation!
==========================================

sympathor has compassion with those trying to obtain a symbolic description of paths described by the `SVG 2 specification <https://www.w3.org/TR/SVG/paths.html>`_.
It enables you to extract a fully symbolic description of paths from MIME types ``text/plain`` or ``image/svg+xml``.

sympathor enables you to ...

- obtain a sampled path, e.g. for further (numerical) processing

- transform the path, e.g. translate, rotate or scale

- derive properties and quantities of differential geometry, e.g. its natural parametrization, its Frenet frame or its curvature

- retrieve all symbolic expressions as `CasADi objects <https://web.casadi.org/>`_, e.g. for use in subsequent software

Looking for an easy way to get started? Check out the `quick start guide <quick-start.html>`_.

.. _Compatibility:

Compatibility
-------------
sympathor is written for Python 3 - we suggest you use Python 3.5 or newer.

.. _License:

License
-------
sympathor is a free and open-source package, licensed under the permissive `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_.
