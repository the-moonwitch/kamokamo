# kamokamo · 鴨かも

<img src="docs/_static/kamokamo-logo.png" width="600"
     alt="two yellow ducks beside the blue and yellow 鴨かも wordmark">

*maybe a value. definitely a duck.*

Rust-like Option, Result, and iterator idioms for Python 3.14+.
pure Python, precise types, and no runtime dependencies.

鴨 (*kamo*) means "duck"; かも expresses "maybe." the name brings together
Python's duck typing and Maybe types.

## install

```sh
uv add 'kamokamo @ git+https://github.com/the-moonwitch/kamokamo.git'
```

## a small example

```python
from kamokamo import Iter, Nothing, Option, Some


def half_even(value: int) -> Option[int]:
    return Some(value // 2) if value % 2 == 0 else Nothing


assert Some(8).and_then(half_even).map(str) == Some("4")
assert Some(3).and_then(half_even) is Nothing
assert Iter(range(6)).filter_map(half_even).collect() == [0, 1, 2]
```

`Some(value)` and `Nothing` distinguish presence from absence.
`Ok(value)` and `Err(error)` distinguish success from an expected failure.
`Iter` builds lazy pipelines over a shared cursor; `Peekable` adds lookahead.

## documentation

- [tutorials](https://kamokamo.readthedocs.io/en/latest/tutorials.html)
- [how-to guides](https://kamokamo.readthedocs.io/en/latest/how-to.html)
- [API reference](https://kamokamo.readthedocs.io/en/latest/reference.html)
- [explanation](https://kamokamo.readthedocs.io/en/latest/explanation.html)

for development, run `mise run setup`, `mise run check`, `mise run test`, and
`mise run docs`. the [development guide](docs/development.md) covers the
tools, builds, and performance measurements.
