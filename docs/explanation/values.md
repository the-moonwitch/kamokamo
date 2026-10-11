# absence, failure, and Python values

{py:type}`~kamokamo.Option` represents a value that may be missing.
{py:type}`~kamokamo.Result` represents a computation that may fail in an
expected way. the separate types let callers decide whether to supply a
default, recover from an error, or report it.

## absence and truthiness

Python often uses `None` as a missing-value sentinel. Option can also hold a
present None, so the value model has room for both cases:

```{doctest}
>>> from kamokamo import Nothing, Ok, Some, from_optional
>>> Some(None).is_some
True
>>> from_optional(None) is Nothing
True
>>> bool(Some(False))
True
>>> bool(Ok(False))
True
```

truth tests inspect the variant. Some and Ok are true; Nothing and Err are
false. the payload does not decide the wrapper's truth.

{py:meth}`~kamokamo.Option.to_optional` maps both Some(None) and Nothing to
None. that conversion is useful at a nullable Python boundary, but it loses
information. keep the Option while the distinction matters.

## expected errors and exceptions

an Err is a value the caller can inspect or transform. it does not have to
contain an exception. a parser might return an error string; a larger
application might return a domain record with a location and error kind.

callbacks passed to {py:meth}`~kamokamo.Result.map` or
{py:meth}`~kamokamo.Result.and_then` can still raise. those exceptions
propagate. converting exceptions to Err belongs at a boundary that can name
the expected failure; see [recovering from errors](../how-to/errors.md).

{py:meth}`~kamokamo.Result.unwrap` raises {py:exc}`ValueError` when given an
Err. use it when success is a precondition. use a fallback or recovery method
when failure belongs to the normal path.

## eager arguments and lazy callbacks

Python evaluates ordinary arguments before making a call. an expression
passed to {py:meth}`~kamokamo.Option.unwrap_or` therefore runs even on Some.
{py:meth}`~kamokamo.Option.unwrap_or_else` accepts a function and calls it
only on Nothing.

Option fallback factories receive no arguments. Result fallback functions
receive the error payload. this lets recovery depend on the failure.

## narrowing and pattern matching

Option and Result are union aliases, not runtime base classes. use their
concrete variants in `isinstance` checks and class patterns.

`is_some`, `is_none`, `is_ok`, and `is_err` are boolean attributes. ordinary
truth tests choose a branch. explicit identity checks also narrow the variant
consistently in BasedPyright, mypy, and Pyright/Pylance:

```{testcode}
from typing import assert_type

from kamokamo import Err, Nothing, NothingType, Ok, Option, Result, Some


def describe_option(value: Option[int]) -> str:
    if value.is_some is True:
        assert_type(value, Some[int])
        return str(value.value)
    assert_type(value, NothingType)
    return "missing"


def describe_result(result: Result[int, str]) -> str:
    match result:
        case Ok(value):
            assert_type(value, int)
            return str(value)
        case Err(error):
            assert_type(error, str)
            return error


assert describe_option(Some(0)) == "0"
assert describe_option(Nothing) == "missing"
assert describe_result(Err("bad")) == "bad"
```

use `case NothingType()` to match absence. a bare `case Nothing` captures a
name under Python's pattern rules; it does not compare with the shared value.

payload types are covariant. a mixed collection may need an explicit
`list[Option[T]]` or `list[Result[T, E]]` annotation to state the intended
union. constructors usually infer their payload types; explicit forms such
as `Some[int](value=1)` and `Err[str](error="bad")` also work.

## immutable wrappers

Some, Ok, and Err each hold one frozen payload slot and have no instance
dictionary. Nothing has no payload. the variants are marked final for type
checkers; additional domain state belongs in the payload.

freezing the wrapper does not freeze that payload:

```{doctest}
>>> items = Some([1])
>>> items.value.append(2)
>>> items
Some([1, 2])
```

equality compares the variant and payload. hashing requires a hashable
payload. {py:func}`copy.copy`, {py:func}`copy.deepcopy`,
{py:func}`dataclasses.replace`, and pickle are supported. shallow copies
share their payload; deep copies preserve cycles and shared references.

explicit constructor aliases such as `Some[int]` are cached
{py:class}`types.GenericAlias` objects. {py:func}`typing.get_origin` and
{py:func}`typing.get_args` expose their origin and parameters. frozen wrappers
do not store `__orig_class__`.
