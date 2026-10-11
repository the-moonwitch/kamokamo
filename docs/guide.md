# your first kamokamo program

we will read an optional setting, validate a port number, and collect a small
pipeline of results. you need Python 3.14+ and uv; no previous experience with
Option or Result is required.

## create a project

run these commands in a directory where you keep your projects:

```sh
uv init --bare --python 3.14 kamokamo-demo
cd kamokamo-demo
uv add 'kamokamo @ git+https://github.com/the-moonwitch/kamokamo.git'
uv run python
```

you now have a Python prompt. enter the examples below at that prompt.

## read a setting

import the types we will use and create a small settings dictionary:

```{doctest}
>>> from kamokamo import Err, Iter, Nothing, Ok, Result, from_optional
>>> settings = {"port": "8080"}
>>> port = from_optional(settings.get("port"))
>>> port
Some('8080')
```

{py:func}`~kamokamo.from_optional` turned the string into a
{py:class}`~kamokamo.Some`. a missing setting becomes
{py:data}`~kamokamo.Nothing`:

```{doctest}
>>> from_optional(settings.get("host"))
Nothing
```

## transform a present value

remove whitespace with {py:meth}`~kamokamo.Option.map`:

```{doctest}
>>> port.map(str.strip)
Some('8080')
>>> Nothing.map(str.strip)
Nothing
```

the first call transformed the string. the second kept the missing value.

## validate the port

write a function that returns {py:class}`~kamokamo.Ok` for a usable port and
{py:class}`~kamokamo.Err` for an invalid one:

```{doctest}
>>> def parse_port(text: str) -> Result[int, str]:
...     try:
...         number = int(text)
...     except ValueError:
...         return Err(f"invalid port: {text!r}")
...     if 1 <= number <= 65535:
...         return Ok(number)
...     return Err("port out of range")
...
>>> parse_port("8080")
Ok(8080)
>>> parse_port("bad")
Err("invalid port: 'bad'")
>>> parse_port("0")
Err('port out of range')
```

convert the setting to a Result with
{py:meth}`~kamokamo.Option.ok_or`, then validate it with
{py:meth}`~kamokamo.Result.and_then`:

```{doctest}
>>> port.ok_or("missing port").and_then(parse_port)
Ok(8080)
>>> Nothing.ok_or("missing port").and_then(parse_port)
Err('missing port')
```

## validate several ports

create an {py:class}`~kamokamo.Iter` from two strings, apply the parser, and
collect the successful values:

```{doctest}
>>> ports = Iter(["8080", "443"]).map(parse_port)
>>> ports.collect_result()
Ok([8080, 443])
```

now include an invalid value:

```{doctest}
>>> ports = Iter(["8080", "bad", "443"]).map(parse_port)
>>> ports.collect_result()
Err("invalid port: 'bad'")
```

{py:meth}`~kamokamo.Iter.collect_result` stopped at the first error.
the final input is still available:

```{doctest}
>>> ports.next()
Some(Ok(443))
```

you have read a missing-or-present setting, validated it, and processed a
sequence with the same parser. exit the Python prompt with `quit()`.

for your own code, continue with [handling missing values](how-to/optional.md)
or [recovering from expected errors](how-to/errors.md). the
[iteration explanation](explanation/iteration.md) covers the shared cursor
used by the last example.
