sphinx-toctree-level-up
=======================

Standalone Sphinx extension that backports toctree ``:level-up:`` from
`sphinx-doc/sphinx#8287 <https://github.com/sphinx-doc/sphinx/issues/8287>`_.

This site is built as **single-page HTML** on purpose. This copy of the site
does **not** use ``:level-up:``, so listed pages stay nested under the section
that contains the toctree.

.. note::

   This build has no ``:level-up:``. Compare with the
   `same docs with promotion <../index.html>`__.

This page is the example
------------------------

The toctree below sits under this section and has no ``:level-up:``.

The listed pages nest *under* this section (``<h3>`` in ``singlehtml``).
:ref:`later-sibling-without` stays a sibling of this section (``<h2>``).

.. toctree::
   :maxdepth: 2

   usage
   how-it-works
   directives
   toc-promotion
   single-file

.. _later-sibling-without:

Later sibling
-------------

This section is a sibling of **This page is the example**, not a child of it.
In this ``singlehtml`` build, the toctree pages should appear as subsections
of **This page is the example**, at a deeper heading level than this section.
