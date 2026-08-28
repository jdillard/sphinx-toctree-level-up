TOC promotion
=============

Sphinx's ``TocTreeCollector`` still builds ``env.tocs`` as usual: the
:rst:dir:`toctree` is nested under the current section.
Then a ``doctree-read`` handler runs
:gitref:`promote_env_toc() <sphinx_toctree_level_up/_promote.py::promote_env_toc>`.

That walk is a **pending-bubble** over the TOC bullet list:

* Recurse into nested lists.
* When a toctree has ``level-up > 0``, do not keep it at this level; put it in a pending list with a remaining count.
* After finishing a section's children, pending items with remaining ``1`` become **siblings** of that section; remaining ``> 1`` bubble further up.
* If promotion runs out of ancestor sections, it stops at the top and warns (``type='toc'``, ``subtype='level_up'``).
* ``only`` nodes are not a section level: the wrapper is kept so HTML vs LaTeX filtering still works.

HTML sidebars and numbering then read the promoted ``env.tocs``. The in-page
:rst:dir:`toctree` stays in the original doctree, which is why paragraph-before
/ list / paragraph-after order is unchanged.
