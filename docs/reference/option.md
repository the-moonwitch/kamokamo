# Option

```{py:currentmodule} kamokamo
```

an optional value is either {py:class}`Some` or {py:data}`Nothing`.
presence is independent of the payload's truthiness: `Some(None)` and
`Some(False)` are both present.

## types and constructors

```{py:type} Option[T]
:canonical: Some[T] | NothingType

an annotation for the two variants. construct Some or use Nothing;
Option is a type alias, so it is not a runtime base class.
```

```{py:class} Some[T](value: T)
:final:

a present value. the wrapper is immutable; the payload keeps its own mutability.
```

```{py:attribute} Some.value
:type: T

the present payload. this attribute cannot be reassigned.
```

```{py:data} Nothing
:type: NothingType

the shared absence value. use it directly, without parentheses.
```

```{py:class} NothingType
:final:

the absence class, useful in annotations, `isinstance`, and
`case NothingType()` patterns. additional instances compare equal to Nothing.
```

```{py:function} from_optional(value) -> Option[T]

convert None to Nothing and any other value to Some. this conversion cannot
represent a present None; construct `Some(None)` explicitly when needed.
```

## presence tests

```{py:attribute} Option.is_some
:type: bool

True on Some and False on Nothing. this is an attribute, not a method.
```

```{py:attribute} Option.is_none
:type: bool

False on Some and True on Nothing. this is an attribute, not a method.
```

```{py:method} Option.is_some_and(predicate) -> bool

call `predicate(value)` on Some; return False on Nothing.
```

```{py:method} Option.is_none_or(predicate) -> bool

call `predicate(value)` on Some; return True on Nothing.
```

## read a value

```{py:method} Option.unwrap() -> T

return the payload. raise {py:exc}`ValueError` on Nothing.
```

```{py:method} Option.expect(message) -> T

return the payload. on Nothing, raise {py:exc}`ValueError` with `message`.
```

```{py:method} Option.unwrap_or(default) -> T | U

return the payload or `default`. Python evaluates the default argument
before this method is called.
```

```{py:method} Option.unwrap_or_else(default) -> T | U

return the payload or call the zero-argument `default` function.
the callback runs only on Nothing.
```

## transform a value

```{py:method} Option.map(function) -> Option[U]

apply `function(value)` on Some and wrap the output in Some.
return Nothing without calling the function on absence.
```

```{py:method} Option.map_or(default, function) -> U | V

return `function(value)` on Some or `default` on Nothing.
the output is a plain value, without an Option wrapper.
```

```{py:method} Option.map_or_else(default, function) -> U | V

return `function(value)` on Some or call the zero-argument
`default` function on Nothing. the output is a plain value.
```

```{py:method} Option.inspect(function) -> Option[T]

call `function(value)` on Some and return the original wrapper.
skip the callback on Nothing. its return value is ignored.
```

```{py:method} Option.filter(predicate) -> Option[T]

retain a Some when `predicate(value)` is true; otherwise return Nothing.
the predicate is skipped on Nothing.
```

```{py:method} Option.flatten() -> Option[U]

remove one layer from `Option[Option[U]]`. Some returns its inner Option;
Nothing stays absent.
```

## combine optional values

```{py:method} Option.and_(other) -> Option[U]

return `other` on Some or Nothing on absence.
use {py:meth}`Option.and_then` to delay the second computation.
```

```{py:method} Option.and_then(function) -> Option[U]

call `function(value)` on Some. the callback must return an Option.
return Nothing without calling it on absence.
```

```{py:method} Option.or_(other) -> Option[T | U]

retain the original Some or return `other` on absence.
use {py:meth}`Option.or_else` to delay the fallback.
```

```{py:method} Option.or_else(default) -> Option[T | U]

retain the original Some or call a zero-argument Option factory on Nothing.
```

```{py:method} Option.xor(other) -> Option[T | U]

retain the present input when exactly one input is Some.
return Nothing when both or neither are present.
```

```{py:method} Option.zip(other) -> Option[tuple[T, U]]

combine two present payloads into `Some((left, right))`.
return Nothing if either input is absent.
```

```{py:method} Option.zip_with(other, function) -> Option[V]

call `function(left, right)` only when both inputs are present and
wrap its output in Some. otherwise return Nothing.
```

```{py:method} Option.unzip() -> tuple[Option[U], Option[V]]

split an `Option[tuple[U, V]]` into two Options.
Nothing returns `(Nothing, Nothing)`.
```

## convert to another representation

```{py:method} Option.to_optional() -> T | None

return the payload on Some or None on Nothing.
this loses the distinction between Some(None) and Nothing.
```

```{py:method} Option.ok_or(error) -> Result[T, E]

convert Some to {py:class}`Ok` and Nothing to {py:class}`Err` with
the supplied error. the error argument is evaluated eagerly.
```

```{py:method} Option.ok_or_else(error) -> Result[T, E]

convert Some to {py:class}`Ok`. on Nothing, call the zero-argument
error factory and wrap its output in {py:class}`Err`.
```

```{py:method} Option.transpose() -> Result[Option[U], E]

exchange the layers of `Option[Result[U, E]]`. a present error is returned
as an Err; Nothing becomes `Ok(Nothing)`.
```

```{py:method} Option.iter() -> collections.abc.Iterator[T]

return a fresh Python iterator over the payload of Some, or an empty
iterator on Nothing. `iter(option)` has the same behavior.
```

## examples

```{doctest}
>>> from kamokamo import Err, Nothing, Ok, Some
>>> Some(4).map(lambda value: value * 2)
Some(8)
>>> Nothing.unwrap_or(0)
0
>>> Some(1).zip(Some("duck"))
Some((1, 'duck'))
>>> Some(Err("bad")).transpose()
Err('bad')
>>> Nothing.transpose()
Ok(Nothing)
```

see [handling missing values](../how-to/optional.md) for practical use and
[the value model](../explanation/values.md) for matching, typing, and Python
protocols.
