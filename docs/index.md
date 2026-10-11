# kamokamo · 鴨かも

```{image} _static/kamokamo-logo.png
:width: 600
:align: center
:class: kamokamo-logo
:alt: two yellow ducks beside the blue and yellow 鴨かも wordmark
```

## maybe a value. definitely a duck.

kamokamo brings Rust's Option, Result, and iterator vocabulary to Python.
it requires Python 3.14+ and has no runtime dependencies.

{py:type}`~kamokamo.Option` holds a value or represents absence.
{py:type}`~kamokamo.Result` holds a successful value or an expected error.
{py:class}`~kamokamo.Iter` builds lazy pipelines, and
{py:class}`~kamokamo.Peekable` adds one item of lookahead.

## find your way

- [tutorials](tutorials.md): build a small program, step by step.
- [how-to guides](how-to.md): handle missing values, errors, and streams.
- [API reference](reference.md): look up a type, signature, or behavior.
- [explanation](explanation.md): understand the choices behind the API.

## a duck, perhaps

鴨 (*kamo*) means "duck"; かも expresses "maybe." 鴨かも brings them together:
Python's duck typing meets Maybe types. sometimes there is
{py:class}`~kamokamo.Some`. sometimes there is {py:data}`~kamokamo.Nothing`.

```{toctree}
:hidden:
:maxdepth: 2

tutorials
how-to
reference
explanation
```
