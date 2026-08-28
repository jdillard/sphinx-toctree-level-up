How it works
============

.. note:: This section is intended for extension maintainers and Sphinx contributors.
   It explains both the behavior intended for Sphinx core and the extension-specific integration required by this backport.

Sphinx nests a :rst:dir:`toctree` under whichever section contains it.
:rst:dir:`:level-up: <toctree:level-up>` promotes those listed pages up the
tree without moving the visible in-page list.

It does this by:

1. :gitref:`setup() <sphinx_toctree_level_up/__init__.py::setup>` **overrides**
   :rst:dir:`toctree` and adds :rst:dir:`toc-level-up`.
2. **Hooks** ``doctree-read`` at priority 600, after Sphinx's own TOC
   collector (500).
3. **Monkeypatches**
   :gitref:`inline_all_toctrees() <sphinx_toctree_level_up/_inline.py::inline_all_toctrees>`,
   which single-file builders call with no event hook.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Surface
     - What happens
   * - Parse
     - Record :rst:dir:`:level-up: <toctree:level-up>` on the toctree node
   * - HTML in-page list
     - Unchanged location
   * - Sidebar / ``env.tocs`` / numbering
     - Nodes re-parented after collection
   * - ``latex``, ``singlehtml``, ``texinfo``, ``man``
     - Included docs inserted after the ancestor section

Parse-time handling
-------------------

Nothing is re-parented at parse time. Directives only stamp
``toctree['level-up'] = N`` on the node for later passes.

:gitref:`TocTree <sphinx_toctree_level_up/__init__.py::TocTree>` subclasses
Sphinx's builtin toctree. After ``super().run()``, it writes the effective
value onto every ``addnodes.toctree`` node.

:gitref:`TocLevelUp <sphinx_toctree_level_up/__init__.py::TocLevelUp>` stores
the per-document default on ``env.current_document`` (or ``env.temp_data`` on
older Sphinx), similar to ``highlight``.
