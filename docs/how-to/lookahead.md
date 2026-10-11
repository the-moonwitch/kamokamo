# retain a delimiter while reading a stream

wrap the source in {py:class}`~kamokamo.Peekable` and consume it through that
wrapper. {py:meth}`~kamokamo.Peekable.next_if` leaves a rejected item in the
buffer so the next stage can read it.

```{doctest}
>>> from kamokamo import Iter, Nothing, Some
>>> characters = Iter("12+34").peekable()
>>> characters.next_if(str.isdecimal)
Some('1')
>>> characters.next_if(str.isdecimal)
Some('2')
>>> characters.next_if(str.isdecimal)
Nothing
>>> characters.peek()
Some('+')
```

consume the delimiter explicitly, then read the rest:

```{doctest}
>>> characters.next_if_eq("+")
Some('+')
>>> characters.collect()
['3', '4']
```

repeated {py:meth}`~kamokamo.Peekable.peek` calls observe the same buffered
item. derived adapters also use the buffer. an upstream Iter alias bypasses
it, so use the Peekable for subsequent reads.

use {py:meth}`~kamokamo.Iter.take_while` when discarding the first rejected
item is acceptable. the [cursor explanation](../explanation/iteration.md)
compares the stopping rules.
