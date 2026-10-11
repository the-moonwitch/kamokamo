# handle missing values

use {py:class}`~kamokamo.Some` when a value is present and
{py:data}`~kamokamo.Nothing` when it is absent. use
{py:func}`~kamokamo.from_optional` at a boundary where Python's `None` means
missing.

## convert a nullable lookup

```{doctest}
>>> from kamokamo import Nothing, Some, from_optional
>>> settings = {"name": "  duck  "}
>>> name = from_optional(settings.get("name"))
>>> name.map(str.strip).unwrap_or("anonymous")
'duck'
>>> from_optional(settings.get("nickname")).unwrap_or("anonymous")
'anonymous'
```

{py:meth}`~kamokamo.Option.map` changes a present value. use
{py:meth}`~kamokamo.Option.and_then` when your callback already returns an
Option:

```{doctest}
>>> from kamokamo import Option
>>> def nonempty(text: str) -> Option[str]:
...     return Some(text) if text else Nothing
...
>>> name.map(str.strip).and_then(nonempty)
Some('duck')
>>> Some("  ").map(str.strip).and_then(nonempty)
Nothing
```

## delay an expensive default

pass a zero-argument function to {py:meth}`~kamokamo.Option.unwrap_or_else`
so it runs only when the value is missing:

```{doctest}
>>> def default_name() -> str:
...     return "anonymous"
...
>>> Nothing.unwrap_or_else(default_name)
'anonymous'
>>> name.unwrap_or_else(default_name)
'  duck  '
```

use {py:meth}`~kamokamo.Option.map_or_else` when you need a transformed
value and a lazy fallback, without constructing an intermediate Option.

## treat absence as an error

when a value is required, convert absence into an error with
{py:meth}`~kamokamo.Option.ok_or`:

```{doctest}
>>> name.ok_or("name is required")
Ok('  duck  ')
>>> Nothing.ok_or("name is required")
Err('name is required')
```

use {py:meth}`~kamokamo.Option.ok_or_else` to construct the error only when
needed. continue with [expected errors](errors.md) to validate the value.

## keep a present None

construct `Some(None)` when `None` is a real payload. calling
{py:meth}`~kamokamo.Option.to_optional` converts both it and Nothing to
`None`. keep the Option when you need to distinguish them; see
[absence and truthiness](../explanation/values.md#absence-and-truthiness).
