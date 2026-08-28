Directives
==========

Nothing is re-parented at parse time.
Directives only stamp ``toctree['level-up'] = N`` on the node for later passes.

toctree
-------

:gitref:`TocTree <sphinx_toctree_level_up/__init__.py::TocTree>` subclasses
Sphinx's builtin toctree, adds ``:level-up:`` as a nonnegative int, then after
``super().run()`` writes that value onto every ``addnodes.toctree`` node.

If the option is omitted, it uses a per-document default from ``.. toc-level-up:: N``. An explicit ``:level-up: 0`` opts that toctree out.

.. rst:directive:: toc-level-up

   :gitref:`TocLevelUp <sphinx_toctree_level_up/__init__.py::TocLevelUp>`
   stores the default on ``env.current_document`` (or ``env.temp_data`` on
   older Sphinx), similar to ``highlight``.
   The value applies to later ``toctree`` directives in the same document until another ``toc-level-up`` replaces it.
