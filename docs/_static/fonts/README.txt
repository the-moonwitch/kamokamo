# vendored fonts

- `xkcd-script.woff` is the unmodified xkcd Script webfont from
  [ipython/xkcd-font](https://github.com/ipython/xkcd-font/tree/d6a83979937c7c36475926009c1eb471e6d62b9d),
  revision `d6a83979937c7c36475926009c1eb471e6d62b9d`, at
  `xkcd-script/font/xkcd-script.woff`. it derives from Randall Munroe's
  handwriting. `xkcd-LICENSE.txt` contains its CC BY-NC 3.0 license.
- `kamokamo-yusei-magic.woff2` is a subset of
  `fonts/ttf/YuseiMagic-Regular.ttf` from
  [Yusei Magic](https://github.com/tanukifont/YuseiMagic/tree/d622b0ea84059a411a1344bd2f948d9e0df92a1b),
  revision `d622b0ea84059a411a1344bd2f948d9e0df92a1b`. the Yusei Magic
  Project Authors' copyright notice and SIL OFL 1.1 are in `YuseiMagic-OFL.txt`.
  FontTools 4.66.1 retained the Japanese characters used in the docs:
  `か` (U+304B), `も` (U+3082), and `鴨` (U+9D28), with their layout features
  and license metadata. the subset was renamed "Kamokamo Japanese" and
  compressed as WOFF2. its timestamp was retained from the original.

when adding Japanese text, regenerate the subset with the new characters
and update the `unicode-range` in `duck.css`. fonts are static assets;
building or reading the docs does not require FontTools or a font service.
