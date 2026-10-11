# API reference

```{py:module} kamokamo
:synopsis: typed optional values, expected errors, and lazy pipelines.
```

import the public API from {py:mod}`kamokamo`:

```python
from kamokamo import Err, Iter, Nothing, NothingType, Ok, Option, Peekable
from kamokamo import Result, Some, from_optional
```

```{toctree}
:maxdepth: 1

reference/option
reference/result
reference/iter
reference/peekable
```

## version

```{py:data} __version__
:type: str

the installed distribution's version. metadata is loaded and cached when
this attribute is first requested.
```

## conventions

`T`, `E`, `U`, `V`, `F`, `S`, and `R` name type parameters.
the Option and Result method signatures describe a receiver annotated with
the union alias. a concrete variant can infer a narrower return type.

callbacks run only on the relevant variant. exceptions raised by callbacks
propagate. methods do not turn exceptions into {py:class}`~kamokamo.Err`.

use the {ref}`genindex` to look up a documented type or method by name.
