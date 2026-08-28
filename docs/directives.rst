Directives
==========

.. rst:directive:: toctree

   This extension overrides Sphinx's built-in ``toctree`` directive to add
   the following option. All other options retain their standard behavior.

   .. rst:directive:option:: level-up
      :type: nonnegative integer

      Promote the listed pages by this many section levels, counted from the
      section containing the ``toctree``. A value of ``0`` disables promotion.

      Requesting more levels than there are ancestor sections promotes as far
      as possible and emits a ``[toc.level_up]`` warning.

.. rst:directive:: toc-level-up

   Set the default :rst:dir:`:level-up: <toctree:level-up>` value for later
   :rst:dir:`toctree` directives in the current document.

   The required argument is a nonnegative integer. The default remains in
   effect until another ``toc-level-up`` directive replaces it. An explicit
   :rst:dir:`:level-up: <toctree:level-up>` option takes precedence, including
   ``:level-up: 0`` to opt out.
