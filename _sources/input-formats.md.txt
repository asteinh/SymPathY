# Input formats

As stated, sympathor is able to parse various inputs. The following list gives an overview of possible input formats:

## SVG file
This is probably the most convenient input format for sympathor. As long as the format follows [SVG 2 specification](https://www.w3.org/TR/SVG/paths.html), sympathor will parse *all* paths found in the file.

A somewhat minimal example of an SVG file would be:
```bash
$ cat input.svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
  <path d="M 0 0 C 10 10, 20 10, 30 0 Z" />
</svg>
```
And the corresponding code to parse it into a path is
```python
from sympathor import ParsePaths

path = ParsePaths('input.svg')
```

## Text file
The possibility to parse a path description from a plain text file is mainly provided for compatibility and exchanging data.
Assume you have a file ``input.txt`` that contains a path description:
```bash
$ cat input.txt
<path d="M 0 0 C 10 10, 20 10, 30 0 Z" />
```
A minimal example parsing this file into a path would be:
```python
from sympathor import ParsePaths

path = ParsePaths('input.txt')
```
Alternatively, you can also parse a text file without any XML tags, formatted like
```bash
$ cat input.txt
M 0 0 C 10 10, 20 10, 30 0 Z
```

## Plain string
The possibility to parse plain strings is essentially the same as reading a text file.
A simple path could be described and parsed as shown below:

```python
from sympathor import ParsePaths

curve = "M 0 0 C 10 10, 20 10, 30 0 Z"
path = ParsePaths(curve)
```

Note that the description in this case must always be provided as plain data, i.e., without any XML tags.
