sphinx-toctree-level-up
=======================

Standalone Sphinx extension that backports toctree ``:level-up:`` from
`sphinx-doc/sphinx#8287 <https://github.com/sphinx-doc/sphinx/issues/8287>`_.

A `Sphinx <http://sphinx-doc.org/>`_ extension that promotes pages listed in a
toctree so they sit higher in the TOC hierarchy than the section that contains
the directive. It serves as a stop gap for the toctree `:level-up:` option,
until `sphinx-doc/sphinx#8287 <https://github.com/sphinx-doc/sphinx/issues/8287>`_
lands in a release.

This site is built as **single-page HTML** on purpose. Single-file builders
(``singlehtml``, LaTeX, Texinfo, man) are where ``:level-up:`` changes
document structure, not only the sidebar TOC.

.. note::

   This build uses ``:level-up: 1``. Compare with the
   `same docs without promotion <without-level-up/index.html>`__.

The docs are the example
------------------------

The toctree below sits under this section and uses ``:level-up: 1``.

Without the extension, the listed pages would nest *under* this section
(``<h3>`` in ``singlehtml``). With it, they are promoted to **siblings** of
this section (``<h2>``), matching :ref:`later-sibling` below.

The TOC hierarchy is:

.. code-block:: text

   sphinx-toctree-level-up
   ├── This page is the example
   ├── Usage
   ├── How it works
   ├── Directives
   ├── TOC promotion
   ├── Single-file builders
   └── Later sibling

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
