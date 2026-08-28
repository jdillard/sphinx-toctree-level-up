Single-file builders
====================

HTML resolves :rst:dir:`toctree` directives in place.
LaTeX, ``singlehtml``, Texinfo, and man call
:gitref:`inline_all_toctrees() <sphinx_toctree_level_up/_inline.py::inline_all_toctrees>`,
which pastes
included documents **where the toctree sits**.
Without a patch, ``page1`` would still nest under "My header" in the PDF even after TOC promotion.

The extension replaces that function. After inlining,
:gitref:`replace_toctree_with_inlined() <sphinx_toctree_level_up/_inline.py::replace_toctree_with_inlined>`:

* Walks up the number of containing sections requested by
  :rst:dir:`:level-up: <toctree:level-up>`.
* Removes the empty toctree wrapper.
* Inserts the inlined documents **after** that ancestor section (as siblings).
* Re-wraps ``only`` nodes so builder tags still apply.

That is why a ``singlehtml`` build of this site shows promoted page titles at the same heading level as **This page is the example** and **Later sibling**, instead of nesting them as subsections.
