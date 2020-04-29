# sympathor - symbolic path extractor

[![CircleCI](https://img.shields.io/circleci/build/github/asteinh/sympathor/master?style=flat-square)](https://circleci.com/gh/asteinh/sympathor)
[![codecov](https://img.shields.io/codecov/c/github/asteinh/sympathor/master?style=flat-square)](https://codecov.io/gh/asteinh/sympathor)
[![License](https://img.shields.io/github/license/asteinh/sympathor?style=flat-square)](https://github.com/asteinh/sympathor/blob/master/LICENSE)

sympathor has compassion with those trying to obtain a symbolic description of paths described by the [SVG 2 specification](https://www.w3.org/TR/SVG/paths.html).

At reasonable size, sympathor enables you to extract a fully symbolic description of paths from MIME types `text/plain` or `image/svg+xml`. Based on this symbolic description, you can obtain a sampled path for further numerical processing, the path's natural parametrization, its Frenet frame, etc.

In short, sympathor seeks to single-handedly provide properties and quantities of differential geometry at high precision.

## First steps
For a quick start guide, documented examples and details on the API of sympathor see the [documentation](https://asteinh.github.io/sympathor/).
