sphinx-toctree-level-up
=======================

A `Sphinx <http://sphinx-doc.org/>`_ extension that promotes pages listed in a
:rst:dir:`toctree` so they sit higher in the TOC hierarchy than the section
that contains the directive. It serves as a stop gap for the
:rst:dir:`:level-up: <toctree:level-up>` option, until
`sphinx-doc/sphinx#8287 <https://github.com/sphinx-doc/sphinx/issues/8287>`_
lands in a release.

This site is built as **single-page HTML** on purpose. This copy of the site
does **not** use ``:level-up:``, so listed pages stay nested under the section
that contains the :rst:dir:`toctree`.

.. note::

   This build has no ``:level-up:``. Compare with the
   `same docs with promotion <../index.html>`__.

This page is the example
------------------------

The :rst:dir:`toctree` below sits under this section and has no ``:level-up:``.

The listed pages nest *under* this section (``<h3>`` in ``singlehtml``).
:ref:`later-sibling-without` stays a sibling of this section (``<h2>``).

The TOC hierarchy is:

.. code-block:: text

   sphinx-toctree-level-up
   ├── This page is the example
   │   ├── Usage
   │   ├── How it works
   │   ├── Directives
   │   ├── TOC promotion
   │   └── Single-file builders
   └── Later sibling

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
