TOC promotion
=============

:doc:`how-it-works` showed the result of that climb: in ``env.tocs``,
**Installation** sits next to **First steps** instead of inside it.

:gitref:`promote_env_toc() <sphinx_toctree_level_up/_promote.py::promote_env_toc>`
walks that tree as a pending-bubble:

* Recurse into nested lists first.
* A toctree with ``level-up > 0`` is not kept at the current level. It is put
  on a pending list with a remaining count.
* After a section's children are finished, remaining ``1`` becomes a
  **sibling** of that section. Remaining ``> 1`` keeps climbing.
* If there are no more ancestor sections, the toctree stays at the top of
  the document's TOC and Sphinx warns (``type='toc'``, ``subtype='level_up'``).
* :rst:dir:`only` nodes are not a section level. The wrapper is kept so
  ``html`` vs ``latex`` filtering still applies, and the remaining count is
  not decremented.

When the builder later pastes included documents into one file, that same
count has to move real headings, not only TOC bullets. That is
:doc:`single-file`.
