sphinx-toctree-level-up
=======================

Standalone Sphinx extension that backports toctree ``:level-up:`` from
`sphinx-doc/sphinx#8287 <https://github.com/sphinx-doc/sphinx/issues/8287>`_.

This site is built as **single-page HTML** on purpose. Single-file builders
(``singlehtml``, LaTeX, Texinfo, man) are where ``:level-up:`` changes
document structure, not only the sidebar TOC.

.. note::

   This build uses ``:level-up: 1``. Compare with the
   `same docs without promotion <without-level-up/index.html>`__.

This page is the example
------------------------

The toctree below sits under this section and uses ``:level-up: 1``.

Without the extension, the listed pages would nest *under* this section
(``<h3>`` in ``singlehtml``). With it, they are promoted to **siblings** of
this section (``<h2>``), matching :ref:`later-sibling` below.

.. toctree::
   :maxdepth: 2
   :level-up: 1

   usage
   how-it-works
   directives
   toc-promotion
   single-file

.. _later-sibling:

Later sibling
-------------

This section is a sibling of **This page is the example**, not a child of it.
In this ``singlehtml`` build, each promoted page title should appear at the
same heading level as this section.
