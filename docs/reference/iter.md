# Iter

```{py:currentmodule} kamokamo
```

```{py:class} Iter[T](iterable)

capture one iterator from `iterable`. all derived pipelines share its position.
Iter is a Python iterable; `iter(values)` returns its underlying iterator.
use `next(iter(values))` for a raw item or {py:meth}`Iter.next` for an Option.
```

adapters are lazy: creating one requests no input items and runs no
transformation callbacks. consumers read from the current position.
see [shared cursors](../explanation/iteration.md) for the consequences.

## adapters

```{py:method} Iter.map(function) -> Iter[U]

yield `function(value)` for each input.
```

```{py:method} Iter.filter(predicate) -> Iter[T]

yield inputs for which `predicate(value)` is true.
```

```{py:method} Iter.filter_map(function) -> Iter[U]

call an Option-returning function for each input. yield Some payloads
and skip Nothing. a present None is yielded as a real item.
```

```{py:method} Iter.map_while(function) -> Iter[U]

yield Some payloads until the callback first returns Nothing.
consume that stopping input, leave later inputs unread, and stay exhausted.
```

```{py:method} Iter.flat_map(function) -> Iter[U]

concatenate the iterables returned by `function(value)`.
```

```{py:method} Iter.flatten() -> Iter[U]

concatenate nested iterables from an `Iter[Iterable[U]]`.
```

```{py:method} Iter.take(count) -> Iter[T]

yield at most `count` inputs. count must be a nonnegative index accepted
by {py:func}`itertools.islice`.
```

```{py:method} Iter.skip(count) -> Iter[T]

discard `count` inputs when consumed, then yield the remainder.
count must be a nonnegative index accepted by {py:func}`itertools.islice`.
```

```{py:method} Iter.take_while(predicate) -> Iter[T]

yield the accepted prefix. the first rejected input is consumed.
use {py:meth}`Peekable.next_if` when that item must be retained.
```

```{py:method} Iter.skip_while(predicate) -> Iter[T]

discard the accepted prefix. yield the first rejected input and all
remaining inputs, without testing them again.
```

```{py:method} Iter.scan(initial, function) -> Iter[U]

call `function(state, value)`, which returns `(new_state, Option[output])`.
yield present outputs; Nothing consumes the stopping input and permanently
ends the adapter. the initial state is not yielded.
```

```{py:method} Iter.peekable() -> Peekable[T]

wrap the remaining cursor with one item of lookahead.
```

```{py:method} Iter.chain(other) -> Iter[T | U]

yield the remaining inputs, then the inputs of `other`.
```

```{py:method} Iter.zip(other) -> Iter[tuple[T, U]]

yield pairs until the shorter input ends. Python
{py:func}`zip` can consume an extra left input when the right side ends.
```

```{py:method} Iter.enumerate(start=0) -> Iter[tuple[int, T]]

yield `(index, value)` pairs, starting at the given index.
```

```{py:method} Iter.inspect(function) -> Iter[T]

call `function(value)` as each item is read, then yield that item.
the callback return value is ignored.
```

## consumers

```{py:method} Iter.next() -> Option[T]

consume one input and return Some, or return Nothing on exhaustion.
a raw None becomes Some(None).
```

```{py:method} Iter.collect() -> list[T]

consume all remaining inputs into a list.
```

```{py:method} Iter.partition(predicate) -> tuple[list[T], list[T]]

consume into matching and rejected lists, preserving order within each.
call the predicate once per input. empty input returns two distinct lists.
```

```{py:method} Iter.count() -> int

consume and count all remaining inputs.
```

```{py:method} Iter.last() -> Option[T]

consume the remainder and return its last input as Some.
return Nothing on empty input.
```

```{py:method} Iter.nth(index) -> Option[T]

consume through the zero-based `index` of the remaining inputs.
return the selected input as Some, or Nothing if it does not exist.
the index follows {py:func}`itertools.islice` rules.
```

```{py:method} Iter.fold(initial, function) -> U

consume all inputs with `function(accumulator, value)`, beginning with
`initial`. return initial on empty input.
```

```{py:method} Iter.reduce(function) -> Option[T]

use the first input as the accumulator, then call
`function(accumulator, value)` for later inputs. wrap the result in Some;
return Nothing on empty input.
```

```{py:method} Iter.find(predicate) -> Option[T]

consume through the first accepted input and return it as Some.
return Nothing when there is no match.
```

```{py:method} Iter.position(predicate) -> Option[int]

consume through the first accepted input. return its zero-based index
within the remaining inputs as Some, or Nothing if there is no match.
```

```{py:method} Iter.find_map(function) -> Option[U]

consume until an Option-returning callback first returns Some.
return that existing wrapper; return Nothing when no output is present.
```

```{py:method} Iter.any(predicate) -> bool

stop at the first true predicate result. return False on empty input.
```

```{py:method} Iter.all(predicate) -> bool

stop at the first false predicate result. return True on empty input.
```

```{py:method} Iter.for_each(function) -> None

call the function for every remaining input. its return value is ignored.
```

## fallible consumers

```{py:method} Iter.collect_option() -> Option[list[U]]

collect payloads from an `Iter[Option[U]]`. stop and return Nothing at the
first absence, leaving later inputs unread. empty input returns Some([]).
```

```{py:method} Iter.collect_result() -> Result[list[U], E]

collect successful payloads from an `Iter[Result[U, E]]`.
stop and retain the first Err, leaving later inputs unread.
empty input returns Ok([]).
```

```{py:method} Iter.try_fold(initial, function) -> Result[U, E]

call `function(accumulator, value)`, which returns a Result.
keep accumulating Ok payloads; stop and retain an Err.
empty input returns Ok(initial). later source inputs remain unread.
```

```{py:method} Iter.try_for_each(function) -> Result[None, E]

call a `Result[None, E]` callback for each input. stop and retain an Err,
leaving later inputs unread. completion, including empty input, returns
Ok(None).
```

## exceptions and storage

source and callback exceptions propagate. callbacks inside generator-based
adapters that raise {py:exc}`StopIteration` become {py:exc}`RuntimeError`.
native Python adapters can interpret StopIteration as exhaustion; do not use
it as a callback error signal.

count, last, and position use bounded auxiliary storage. collect and
partition retain their output lists. the caller owns input resources;
see [resource ownership](../explanation/iteration.md#resource-ownership).

## examples

```{doctest}
>>> from kamokamo import Err, Iter, Ok, Some
>>> Iter(range(6)).map(lambda value: value * 2).take(3).collect()
[0, 2, 4]
>>> values = Iter([Ok(1), Err("bad"), Ok(3)])
>>> values.collect_result()
Err('bad')
>>> values.next()
Some(Ok(3))
>>> Iter([]).reduce(lambda left, right: left + right)
Nothing
```
