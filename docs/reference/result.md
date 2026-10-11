# Result

```{py:currentmodule} kamokamo
```

a Result is either a successful {py:class}`Ok` or an expected {py:class}`Err`.
an error can hold any payload, including a string, exception, or domain value.

## types and constructors

```{py:type} Result[T, E]
:canonical: Ok[T] | Err[E]

an annotation for the two variants. construct Ok or Err;
Result is a type alias, so it is not a runtime base class.
```

```{py:class} Ok[T](value: T)
:final:

a successful value. the wrapper is immutable; the payload keeps its own mutability.
```

```{py:attribute} Ok.value
:type: T

the successful payload. this attribute cannot be reassigned.
```

```{py:class} Err[E](error: E)
:final:

an expected failure. the wrapper is immutable; the error keeps its own mutability.
```

```{py:attribute} Err.error
:type: E

the error payload. this attribute cannot be reassigned.
```

## variant tests

```{py:attribute} Result.is_ok
:type: bool

True on Ok and False on Err. this is an attribute, not a method.
```

```{py:attribute} Result.is_err
:type: bool

False on Ok and True on Err. this is an attribute, not a method.
```

```{py:method} Result.is_ok_and(predicate) -> bool

call `predicate(value)` on Ok; return False on Err.
```

```{py:method} Result.is_err_and(predicate) -> bool

call `predicate(error)` on Err; return False on Ok.
```

## read a payload

```{py:method} Result.unwrap() -> T

return the successful payload. on Err, raise {py:exc}`ValueError`
including the error representation.
```

```{py:method} Result.expect(message) -> T

return the successful payload. on Err, raise {py:exc}`ValueError`
including the supplied message and error representation.
```

```{py:method} Result.unwrap_err() -> E

return the error payload. on Ok, raise {py:exc}`ValueError`
including the successful value representation.
```

```{py:method} Result.expect_err(message) -> E

return the error payload. on Ok, raise {py:exc}`ValueError`
including the supplied message and successful value representation.
```

```{py:method} Result.unwrap_or(default) -> T | U

return the successful payload or `default` on Err.
Python evaluates the default argument before the call.
```

```{py:method} Result.unwrap_or_else(default) -> T | U

return the successful payload or call `default(error)` on Err.
```

## transform or observe

```{py:method} Result.map(function) -> Result[U, E]

apply `function(value)` on Ok and wrap its output in Ok.
retain the original Err without calling the function.
```

```{py:method} Result.map_err(function) -> Result[T, F]

apply `function(error)` on Err and wrap its output in Err.
retain the original Ok without calling the function.
```

```{py:method} Result.map_or(default, function) -> U | V

return `function(value)` on Ok or `default` on Err, without a Result wrapper.
```

```{py:method} Result.map_or_else(default, function) -> U | V

return `function(value)` on Ok or `default(error)` on Err,
without a Result wrapper.
```

```{py:method} Result.inspect(function) -> Result[T, E]

call `function(value)` on Ok and return the original wrapper.
skip the callback on Err. its return value is ignored.
```

```{py:method} Result.inspect_err(function) -> Result[T, E]

call `function(error)` on Err and return the original wrapper.
skip the callback on Ok. its return value is ignored.
```

```{py:method} Result.flatten() -> Result[U, E | F]

remove one layer from `Result[Result[U, F], E]`.
Ok returns its inner Result; an outer Err is retained.
```

## sequence or recover

```{py:method} Result.and_(other) -> Result[U, E | F]

return `other` on Ok or retain the original Err.
use {py:meth}`Result.and_then` to delay the next computation.
```

```{py:method} Result.and_then(function) -> Result[U, E | F]

call the Result-returning `function(value)` on Ok.
retain the original Err without calling it.
```

```{py:method} Result.or_(other) -> Result[T | U, F]

retain the original Ok or return `other` on Err.
use {py:meth}`Result.or_else` to delay recovery.
```

```{py:method} Result.or_else(default) -> Result[T | U, F]

retain the original Ok or call the Result-returning `default(error)` on Err.
```

## convert to another representation

```{py:method} Result.ok() -> Option[T]

convert Ok to {py:class}`Some` and Err to {py:data}`Nothing`.
```

```{py:method} Result.err() -> Option[E]

convert Err to {py:class}`Some` and Ok to {py:data}`Nothing`.
```

```{py:method} Result.transpose() -> Option[Result[U, E]]

exchange the layers of `Result[Option[U], E]`.
`Ok(Nothing)` becomes Nothing; Err becomes a present Err.
```

```{py:method} Result.iter() -> collections.abc.Iterator[T]

return a fresh iterator over the successful payload, or an empty iterator
on Err. `iter(result)` has the same behavior.
```

## examples

```{doctest}
>>> from kamokamo import Err, Nothing, Ok, Some
>>> Ok(4).map(lambda value: value * 2)
Ok(8)
>>> Err("bad").map(str)
Err('bad')
>>> Err("bad").unwrap_or_else(len)
3
>>> Ok(Some(4)).transpose()
Some(Ok(4))
>>> Ok(Nothing).transpose()
Nothing
```

see [recovering from expected errors](../how-to/errors.md) for practical use
and [the value model](../explanation/values.md) for matching and Python
protocols.
