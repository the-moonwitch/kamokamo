# develop and check kamokamo

work from a checkout with mise installed. the library requires Python 3.14+
and has no runtime dependencies.

## prepare the environment

```sh
mise trust
mise install
mise run setup
```

mise pins uv. uv installs Python and the locked development dependencies.
the default dev group includes test tools; CI's compatibility jobs install
only the test group.

## check a change

```sh
mise run format
mise run check
mise run test
```

Ruff formats at 79 columns. the checks run Ruff, BasedPyright, mypy, and
upstream Pyright. `pyrightconfig.json` also configures Pylance in the editor;
CI checks its analysis compatibility with upstream Pyright.

write public use sites and their types before changing the implementation.
preserve meaningful None payloads, lazy callbacks, shared cursors, and
short-circuit remainders. use focused examples and independent Hypothesis
oracles to check behavior. coverage locates gaps and has no enforced threshold.

run `mise run fuzz` for the 5000-example Hypothesis profile.
CI tests Python 3.14 on Linux, macOS, and Windows and checks lint, typing,
documentation, and distribution builds.

personal `.zed/`, `.vscode/`, and `AGENTS.md` stay local, ignored, and excluded
from distributions. experimental scripts and raw profiles also stay local.

## build the docs

```sh
mise run docs
```

open `build/docs/index.html`. the task renders the HTML and runs Sphinx
doctests; warnings, unresolved object references, and failed examples cause
the command to fail.

the pages follow [Diátaxis](https://diataxis.fr/): a guided tutorial,
task-focused how-to guides, an API reference, and explanations of the model.
keep a page focused on one of those reader needs.

use MyST roles such as `{py:type}` and `{py:meth}` for API objects. define
public entries with Sphinx's Python-domain directives so they appear in
the object index and inventory. use `{doctest}`, `{testcode}`, and
`{testoutput}` for runnable examples. Python standard-library references
are resolved through intersphinx. the configuration example uses
`{literalinclude}` to keep its displayed implementation tied to the source.

[Read the Docs](https://kamokamo.readthedocs.io/en/latest/) builds from
`.readthedocs.yaml` with Python 3.14 and the uv docs group. hosted builds
treat warnings as errors too. `latest` follows the repository's default
branch, currently `codex/scaffold`.

the docs' visual style follows [snecs](https://snecs.slavfox.space/), with
Alabaster, serif body text, and self-hosted
[xkcd Script](https://github.com/ipython/xkcd-font) headings. the font derives
from Randall Munroe's handwriting and is bundled unchanged with its
{download}`CC BY-NC 3.0 license <_static/fonts/xkcd-LICENSE.txt>`.
Japanese text uses a three-glyph WOFF2 subset of
[Yusei Magic](https://github.com/tanukifont/YuseiMagic), renamed
"Kamokamo Japanese", with its
{download}`Open Font License <_static/fonts/YuseiMagic-OFL.txt>`.
{download}`font sources and subset details <_static/fonts/README.txt>`
record the upstream revisions and included characters.

## measure a workload

use the tools directly:

```sh
mise run bench -- --fast -s 'from kamokamo import Some' 'Some(42).map(str)'
mise run profile -- path/to/workload.py
```

before timing a comparison, verify equal outputs, callback counts, error
behavior, and remaining source inputs. compare with a strong direct Python
loop. separate wrapper costs from traversal, parsing, and collection; try
empty, small, and larger workloads when setup costs could change the result.

run timing experiments sequentially, without competing tests or profiles.
record the interpreter version, JIT state, sample count, and variation.
profile separately to identify work behind a timing difference. distinguish
opcode samples and allocation peaks from elapsed time.

## build distributions

```sh
mise run build
```

the wheel contains the library and its `py.typed` marker. the source
distribution also contains the documentation and `examples` package.
