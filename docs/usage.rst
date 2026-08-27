Usage
=====

Install from PyPI and enable the extension in ``conf.py``:

.. code-block:: bash

   pip install sphinx-toctree-level-up

.. code-block:: python

   extensions = [
       'sphinx_toctree_level_up',
   ]

``:level-up: N`` is relative: promote *N* section levels from the section
that contains the toctree. The visible HTML in-page list stays where the
directive is written. Only the TOC hierarchy (sidebar / ``env.tocs`` /
section numbering) and single-file builders (LaTeX, ``singlehtml``, Texinfo,
man) change structure.

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

Set a per-document default for later ``toctree`` directives (like
``highlight``). An explicit ``:level-up:`` on a toctree overrides it,
including ``:level-up: 0`` to opt out:

.. code-block:: rst

   .. toc-level-up:: 1

   My header
   ---------

   .. toctree::

      page1

Requesting more levels than there are ancestor sections emits a warning
(``type='toc'``, ``subtype='level_up'``) and promotes as far as possible.

This extension does **not** add ``:target-level:`` or ``:level:``.

Remove after upgrading Sphinx
-----------------------------

This extension is a stopgap. When Sphinx provides native ``:level-up:``,
the extension does not register its directives, so the feature is not
applied twice. At startup it warns:

.. code-block:: text

   sphinx_toctree_level_up is no longer needed; Sphinx already provides toctree :level-up:.
   Remove this extension from conf.py.

Then delete ``'sphinx_toctree_level_up'`` from ``extensions`` and uninstall
the package.
