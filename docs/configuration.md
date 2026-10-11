# read configuration sections and keep all errors

use {py:meth}`~kamokamo.Iter.map_while` to end a section at a blank line.
return an Option of Result for each line: Nothing ends the section, Ok holds
an entry, and Err holds a malformed-entry error.

this example runs from a checkout or source distribution, where the
`examples` package is available. copy the two functions below into your
application when using an installed wheel.

## parse one line

```{literalinclude} ../examples/configuration.py
:language: python
:start-at: from kamokamo import
:end-before: def read_section
```

the first `=` separates key and value. keys must be nonempty; values may be
empty or contain more `=` characters. whitespace around each is stripped.

```{doctest}
>>> from examples.configuration import parse_entry, read_section
>>> parse_entry("port = 8080")
Some(Ok(('port', '8080')))
>>> parse_entry("broken")
Some(Err("invalid entry: 'broken'"))
>>> parse_entry("\n")
Nothing
```

## collect a section

accumulate successful entries and errors in one pass. the last duplicate
key wins:

```{literalinclude} ../examples/configuration.py
:language: python
:start-at: def read_section
```

## read consecutive sections

keep the input file open while consuming it. the reader consumes each blank
line delimiter and leaves later lines for the next call:

```{doctest}
>>> from io import StringIO
>>> from kamokamo import Iter
>>> with StringIO("port=8080\nbroken\n\nnext=yes\n") as source:
...     lines = Iter(source)
...     print(read_section(lines))
...     print(read_section(lines))
...     print(source.closed)
...
({'port': '8080'}, ["invalid entry: 'broken'"])
({'next': 'yes'}, [])
False
>>> source.closed
True
```

kamokamo does not close the input. the context manager owns that resource;
see [resource ownership](explanation/iteration.md#resource-ownership).
