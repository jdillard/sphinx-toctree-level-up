Usage
=====

Install from PyPI and enable the extension in **conf.py**:

.. code-block:: bash

   pip install sphinx-toctree-level-up

.. code-block:: python

   extensions = [
       'sphinx_toctree_level_up',
   ]

On the :rst:dir:`toctree` directive, the new
:rst:dir:`:level-up: <toctree:level-up>` option takes a non-negative integer
and represents how many section levels to climb, counted from the section that
contains the directive.
``1`` promotes listed pages to siblings of that section; ``2`` climbs one more level, and so on.

The in-page HTML TOC tree stays where you wrote the directive.
What changes is the TOC hierarchy (sidebar and section numbering) and the
structure in single-file builders (``latex``, ``singlehtml``, ``texinfo``, and
``man``).

Promote listed pages to siblings of the current section:

.. code-block:: rst

   My title
   ========

   My header
   ---------

   .. toctree::
      :level-up: 1

      page1

This produces a TOC hierarchy of:

.. code-block:: text

   My title
   ├── My header
   └── page1

rather than nesting ``page1`` under **My header**.

Use :rst:dir:`toc-level-up` to set a per-document default for later
:rst:dir:`toctree` directives (like :rst:dir:`highlight`).
An explicit :rst:dir:`:level-up: <toctree:level-up>` option overrides it,
including ``:level-up: 0`` to opt out:

.. code-block:: rst

   .. toc-level-up:: 1

   My header
   ---------

   .. toctree::

      page1

Requesting more levels than there are ancestor sections emits a ``[toc.level_up]`` warning and promotes as far as possible.

Remove after upgrading Sphinx
-----------------------------

This extension is meant as a stop gap. When Sphinx provides a native
:rst:dir:`:level-up: <toctree:level-up>` option, this extension will not
register its directives, so the feature is not applied twice.
At startup it will warn to delete ``'sphinx_toctree_level_up'`` from ``extensions`` and uninstall the package.
