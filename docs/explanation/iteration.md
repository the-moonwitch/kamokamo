# lazy pipelines and shared cursors

{py:class}`~kamokamo.Iter` wraps one Python iterator. each adapter creates a
view over its remaining inputs. adapters run as values are requested, and
all aliases share progress through the same source.

## one cursor, several views

```{doctest}
>>> from kamokamo import Iter, Nothing, Some
>>> source = Iter(range(6))
>>> doubled = source.map(lambda value: value * 2)
>>> doubled.take(2).collect()
[0, 2]
>>> source.next()
Some(2)
>>> doubled.collect()
[6, 8, 10]
>>> source.collect()
[]
```

consuming the derived pipeline advanced the source. reading from the source
then changed what the derived pipeline would see next. keeping a second
reference does not make the data replayable.

Iter is an iterable: Python iteration returns raw inputs from its underlying
cursor. {py:meth}`~kamokamo.Iter.next` deliberately wraps an input in Some.
ordinary `for` loops and {py:meth}`~kamokamo.Iter.collect` do not create an
Option for every input.

## order changes how much input is read

`take(10).filter_map(parse)` examines at most ten inputs.
`filter_map(parse).take(10)` seeks ten present outputs and may examine more.
this distinction matters for large streams, expensive callbacks, and
unbounded sources.

{py:meth}`~kamokamo.Iter.filter_map` skips Nothing and continues.
{py:meth}`~kamokamo.Iter.map_while` ends at the first Nothing. both yield a
present None as a real item.

## stopping and the remaining source

short-circuiting consumers leave later inputs available. the item that caused
the stop has already been read:

```{doctest}
>>> from kamokamo import Err, Ok
>>> results = Iter([Ok(1), Err("bad"), Ok(3)])
>>> results.collect_result()
Err('bad')
>>> results.collect_result()
Ok([3])
```

some stopping rules differ:

| operation | stopping input | later inputs |
| --- | --- | --- |
| {py:meth}`~kamokamo.Iter.take_while` | rejected item is consumed | remain unread |
| {py:meth}`~kamokamo.Iter.map_while` | input producing Nothing is consumed | remain unread |
| {py:meth}`~kamokamo.Iter.scan` | input producing Nothing is consumed | remain unread |
| {py:meth}`~kamokamo.Peekable.next_if` | rejected item stays buffered | remain unread |

map_while and scan stay exhausted after their stopping point. Peekable caches
exhaustion too. Iter otherwise follows the behavior of its underlying
iterator; it does not promise to make an arbitrary Python source permanently
exhausted.

{py:meth}`~kamokamo.Iter.zip` uses Python's zip rules. if the right iterator
ends first, one extra left input may have been read to discover that fact.

## lookahead has an owner

{py:meth}`~kamokamo.Peekable.peek` may advance the upstream source, but it
retains the item in the Peekable buffer. subsequent reads through that wrapper
see the buffered item. an upstream alias skips the buffer, which is why
[delimiter parsing](../how-to/lookahead.md) continues through the Peekable.

## resource ownership

the caller owns files, generators, and other input resources. Iter does not
close them when a consumer finishes or stops early. consume file-backed
pipelines inside the file's context manager:

```python
from kamokamo import Iter

with open("settings.txt", encoding="utf-8") as source:
    first_line = Iter(source).next()
```

[reading configuration sections](../configuration.md) gives a runnable
example that keeps the stream open across consecutive reads.

## allocation and performance

lazy adapters retain cursors rather than intermediate collections.
{py:meth}`~kamokamo.Iter.collect` and {py:meth}`~kamokamo.Iter.partition`
retain their output lists. use {py:meth}`~kamokamo.Option.map_or` or
{py:meth}`~kamokamo.Result.map_or` for a terminal mapped value when another
wrapper is unnecessary.

a direct loop can be faster when it avoids wrappers or intermediate output.
measure the whole workload, including parsing and collection; the
[development guide](../development.md#measure-a-workload) gives the commands.
