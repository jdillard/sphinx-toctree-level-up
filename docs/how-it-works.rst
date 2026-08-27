How it works
============

Sphinx nests a ``toctree`` under whichever section contains it. ``:level-up:``
promotes those listed pages up the tree without moving the visible in-page
list.

On ``setup()``, the extension checks whether Sphinx already has native
``:level-up:``. If so, it warns you to remove the extension and does nothing
else. Otherwise it:

1. **Overrides** the ``toctree`` directive and adds ``toc-level-up``.
2. **Hooks** ``doctree-read`` at priority 600, after Sphinx's own TOC
   collector (500).
3. **Monkeypatches** ``inline_all_toctrees``, which single-file builders call
   with no event hook.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Surface
     - What happens
   * - Parse
     - Record ``level-up`` on the toctree node
   * - HTML in-page list
     - Unchanged location
   * - Sidebar / ``env.tocs`` / numbering
     - Nodes re-parented after collection
   * - LaTeX, ``singlehtml``, Texinfo, man
     - Included docs inserted after the ancestor section
