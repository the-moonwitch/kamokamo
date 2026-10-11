# recover from expected errors

return {py:class}`~kamokamo.Err` at the boundary that knows which failures
are expected. let unexpected exceptions propagate.

## return a useful error

```{doctest}
>>> from kamokamo import Err, Ok, Result
>>> def parse_integer(text: str) -> Result[int, str]:
...     try:
...         return Ok(int(text))
...     except ValueError:
...         return Err(f"invalid integer: {text!r}")
...
>>> parse_integer("42")
Ok(42)
>>> parse_integer("duck")
Err("invalid integer: 'duck'")
```

## compose validation

use {py:meth}`~kamokamo.Result.and_then` for a second check that can fail:

```{doctest}
>>> def positive(number: int) -> Result[int, str]:
...     return Ok(number) if number > 0 else Err("must be positive")
...
>>> parse_integer("42").and_then(positive)
Ok(42)
>>> parse_integer("0").and_then(positive)
Err('must be positive')
```

a previous Err skips the callback. use {py:meth}`~kamokamo.Result.map` for
a transformation that returns a plain value.

## recover or describe the error

supply a fallback Result with {py:meth}`~kamokamo.Result.or_else`:

```{doctest}
>>> parse_integer("duck").or_else(lambda error: Ok(0))
Ok(0)
```

use {py:meth}`~kamokamo.Result.map_err` to add context while retaining the
failure:

```{doctest}
>>> parse_integer("duck").map_err(lambda error: f"count: {error}")
Err("count: invalid integer: 'duck'")
```

Result fallback callbacks receive the error payload. Option fallback factories
receive no arguments.

## stop a stream at its first error

use {py:meth}`~kamokamo.Iter.collect_result` when all items must succeed:

```{doctest}
>>> from kamokamo import Iter
>>> values = Iter(["1", "duck", "3"]).map(parse_integer)
>>> values.collect_result()
Err("invalid integer: 'duck'")
>>> values.collect_result()
Ok([3])
```

only the failing input was consumed at the stopping point. use a loop when
all errors should be retained; [the configuration reader](../configuration.md)
shows that pattern.
