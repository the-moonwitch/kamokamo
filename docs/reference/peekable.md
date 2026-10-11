# Peekable

```{py:currentmodule} kamokamo
```

```{py:class} Peekable[T](iterable)
:final:

add one buffered item to an iterator. Peekable extends {py:class}`Iter` and
supports its adapters and consumers. it is also a Python iterator:
`iter(values) is values`, and `next(values)` returns a raw input.
```

use {py:meth}`Iter.peekable` to wrap an existing cursor. consume through the
Peekable once it has been introduced; an upstream alias bypasses its buffer.

## lookahead and consumption

```{py:method} Peekable.peek() -> Option[T]

fetch and buffer the next input once. repeated calls return the same Some,
including for a None payload. Nothing is cached permanently on exhaustion.
```

```{py:method} Peekable.next() -> Option[T]

consume the next input. return an existing buffered Some when available,
otherwise fetch an input and wrap it. return Nothing on exhaustion.
```

```{py:method} Peekable.next_if(predicate) -> Option[T]

consume the buffered input only if `predicate(value)` is true. rejection
returns Nothing and retains that input. callback exceptions also retain it.
the callback is skipped when exhausted.
```

```{py:method} Peekable.next_if_eq(expected) -> Option[T]

consume the buffered input only if it compares equal to `expected`.
rejection or an equality exception retains the input.
```

```{py:method} Peekable.peekable() -> Peekable[T]

return this existing Peekable, without another wrapper or buffer.
```

## inherited operations

{py:meth}`Iter.map`, {py:meth}`Iter.take`, {py:meth}`Iter.collect`, and the
other inherited operations read through the same buffer. Python length hints
include a buffered input and report zero after cached exhaustion.

## example

```{doctest}
>>> from kamokamo import Iter, Nothing, Some
>>> values = Iter([None, 2]).peekable()
>>> first = values.peek()
>>> first
Some(None)
>>> values.peek() is first
True
>>> values.next() is first
True
>>> next(values)
2
>>> values.peek()
Nothing
```

see [retaining a delimiter](../how-to/lookahead.md) for a parsing example.
