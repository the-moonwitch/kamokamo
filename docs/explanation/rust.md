# Rust vocabulary in Python

kamokamo takes its names and callback order from Rust's
[Option](https://doc.rust-lang.org/std/option/enum.Option.html),
[Result](https://doc.rust-lang.org/std/result/enum.Result.html), and
[Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html).
those familiar operations compose with Python's own values and iteration.

## values and ownership

Python references replace Rust borrowing. the wrappers are immutable, but
their payloads can still be mutable. an input resource remains the caller's
responsibility.

Rust enum variants become Python classes: {py:class}`~kamokamo.Some`,
{py:class}`~kamokamo.Ok`, and {py:class}`~kamokamo.Err`.
{py:data}`~kamokamo.Nothing` names absence while preserving Python's None
as a possible payload. the [value explanation](values.md) describes their
Python protocols.

## spelling and behavior

| Rust idiom | kamokamo spelling |
| --- | --- |
| `None` variant | {py:data}`~kamokamo.Nothing` |
| `is_some()` | {py:attr}`~kamokamo.Option.is_some` |
| `is_ok()` | {py:attr}`~kamokamo.Result.is_ok` |
| `and(...)` | {py:meth}`~kamokamo.Option.and_` or {py:meth}`~kamokamo.Result.and_` |
| `or(...)` | {py:meth}`~kamokamo.Option.or_` or {py:meth}`~kamokamo.Result.or_` |
| iterator `collect()` | {py:meth}`~kamokamo.Iter.collect`, returning a list |

`and_` and `or_` avoid Python keyword conflicts. state predicates are boolean
attributes. unwrap failures raise Python {py:exc}`ValueError` exceptions.
mutating wrapper operations, unchecked access, and type-directed defaults
are outside this API.

## fallible iteration

{py:meth}`~kamokamo.Iter.try_fold` and
{py:meth}`~kamokamo.Iter.try_for_each` use Result-returning callbacks.
{py:meth}`~kamokamo.Iter.collect_result` and
{py:meth}`~kamokamo.Iter.collect_option` collect payloads while stopping at
an error or absence. Python has no equivalent of Rust's `?` syntax here;
compose with {py:meth}`~kamokamo.Result.and_then` or handle a variant explicitly.

Rust leaves calls after map_while's first None unspecified. kamokamo's
{py:meth}`~kamokamo.Iter.map_while` stays exhausted permanently.
wrapper iteration creates a fresh zero-or-one iterator; Iter pipelines share
one cursor. see [iteration](iteration.md) for the stopping and aliasing rules.
