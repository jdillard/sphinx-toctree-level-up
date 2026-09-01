sphinx-toctree-level-up
=======================

A `Sphinx <http://sphinx-doc.org/>`_ extension that promotes pages listed in a
:rst:dir:`toctree` so they sit higher in the TOC hierarchy than the section
that contains the directive. It serves as a stop gap for the
:rst:dir:`:level-up: <toctree:level-up>` option, until
`sphinx-doc/sphinx#8287 <https://github.com/sphinx-doc/sphinx/issues/8287>`_
lands in a release.

This site is built as **single-page HTML** on purpose. Single-file builders
(``singlehtml``, ``latex``, ``texinfo``, and ``man``) are where ``:level-up:``
changes document structure, not only the sidebar TOC.

.. note::

   This build uses ``:level-up: 1``. Compare with the
   `same docs without promotion <without-level-up/index.html>`__.

.. _this-page-is-the-example:

This page is the example
------------------------

The :rst:dir:`toctree` below sits under this section and uses
``:level-up: 1``.

With the extension, the listed pages are promoted to **siblings** of this
section (``<h2>``), matching :ref:`later-sibling` below. Without it, they
would nest *under* this section (``<h3>`` in ``singlehtml``), as shown in the
`same docs without promotion <without-level-up/index.html>`__.

So the TOC hierarchy with the extension is:

.. code-block:: text

   sphinx-toctree-level-up
   ├── This page is the example
   ├── Usage
   ├── Directives
   ├── How it works
   ├── TOC promotion
   ├── Single-file builders
   └── Later sibling

.. toctree::
   :maxdepth: 2
   :level-up: 1

   usage
   directives
   how-it-works
   toc-promotion
   single-file

.. _later-sibling:

Later sibling
-------------

This section is a sibling of :ref:`this-page-is-the-example`.
Due to the use of ``:level-up: 1``, each promoted page title should now appear at the same heading level as this section.
