How it works
============

This feature sounds like it should be a simple matter of moving a
:rst:dir:`toctree`. The complication is that Sphinx does not keep one tree for
the whole build. It has:

* a **document tree** (or *doctree*) for the content of each source file;
* a separate **navigation tree** in ``env.tocs`` for sidebars and numbering;
  and
* for single-file output, a later pass that copies the included documents into
  one combined document.

To keep those views consistent, the extension has to meet the same
``toctree`` more than once during a build.

The starting point
------------------

Imagine this source:

.. code-block:: rst

   Guide
   =====

   First steps
   -----------

   Introductory text.

   .. toctree::
      :level-up: 1

      installation

   More text about first steps.

Without ``:level-up:``, Sphinx treats **Installation** as a child of **First
steps**, because that section contains the directive:

.. code-block:: text

   Guide
   └── First steps
       └── Installation

The requested value of ``1`` means "climb out of one containing section."
The desired navigation hierarchy is therefore:

.. code-block:: text

   Guide
   ├── First steps
   └── Installation

Only the hierarchy changes. In regular multi-page HTML, the visible list of
links still appears between the introductory text and the text that follows
the directive. This distinction drives the rest of the implementation.

Stage 1: teaching the parser the new option
-------------------------------------------

When Sphinx starts, :gitref:`setup()
<sphinx_toctree_level_up/__init__.py::setup>` first checks whether the
installed Sphinx already supports ``:level-up:``. If it does, the backport
steps aside and asks the user to remove it. Otherwise, the extension replaces
the registered ``toctree`` directive with a small :rst:dir:`toctree` subclass
and registers the new :rst:dir:`toc-level-up` directive.

The subclassed :rst:dir:`toctree` lets Sphinx do its normal parsing, then
records the effective value as ``toctree['level-up']`` on the resulting node.
An explicit ``:level-up:`` option wins over the per-document default set by
:rst:dir:`toc-level-up`.

No content moves at this stage, the node is only carrying an instruction for
later build stages. This is important because moving source content while it is
being parsed would also move nearby paragraphs and would change where the
HTML link list is rendered.

Stage 2: adjusting Sphinx's navigation copy
-------------------------------------------

After parsing a document, Sphinx's built-in ``TocTreeCollector`` makes a
smaller TOC representation and stores it in ``env.tocs``. That is the copy
used to assemble global navigation and section numbering. At this point,
Sphinx has followed its normal rule, so **Installation** is still nested below
**First steps**.

The extension waits until that collector is finished. Its ``doctree-read``
handler runs at priority ``600``, after the collector's priority ``500``, and
calls :gitref:`promote_env_toc() <sphinx_toctree_level_up/_promote.py::promote_env_toc>`.
The handler finds the marked ``toctree`` in the navigation copy and bubbles it up by the
requested number of section ancestors.

For the example, the navigation copy changes from:

.. code-block:: text

   Guide
   └── First steps
       └── toctree(installation, level-up=1)

to:

.. code-block:: text

   Guide
   ├── First steps
   └── toctree(installation, level-up=1)

The original document tree is deliberately untouched. Regular HTML can now
read the promoted hierarchy for its sidebar while resolving the original
node in place for the page's visible list.

.. note:: The detailed bubbling rules, including requests that exceed the available
   ancestors and :rst:dir:`only` handling, are covered in :doc:`toc-promotion`.

Stage 3: handling builders that combine documents
-------------------------------------------------

The previous stage is enough for regular multi-page HTML, but not for builders
that produce one combined document. ``singlehtml``, ``latex``, ``texinfo``,
and ``man`` replace a ``toctree`` node with the full content of every document
it includes. Sphinx calls this process *inlining*.

If the extension changed only ``env.tocs``, a PDF could show **Installation**
as a sibling in its table of contents while still rendering its heading and
body inside **First steps**, which would make the navigation and the actual
document structure disagree.

Those builders call ``inline_all_toctrees()`` directly and provide no event
between inlining and placement that this backport can hook. The extension
therefore replaces that function in Sphinx and in the builder modules that
already imported it. Its version performs normal recursive inlining, then
:gitref:`replace_toctree_with_inlined()
<sphinx_toctree_level_up/_inline.py::replace_toctree_with_inlined>` moves the
included document after the requested ancestor section.

In the example, all of **First steps** stays together, including the text
after the directive. The combined result is conceptually:

.. code-block:: text

   Guide
   ├── First steps
   │   ├── Introductory text.
   │   └── More text about first steps.
   └── Installation

This placement gives **Installation** the heading level promised by the
promoted navigation. See :doc:`single-file` for the builder-specific path.

The complete journey
--------------------

The same small ``level-up`` marker coordinates the build:

1. Parsing records the request but preserves the source layout.
2. The ``doctree-read`` handler promotes the navigation copy used by sidebars
   and numbering.
3. Regular HTML leaves the in-page list where the author wrote it.
4. Single-file builders move the inlined document content so its real heading
   structure matches the promoted TOC.

The central idea behind that split is that promotion changes a document's
place in the documentation hierarchy without pretending that the directive
was written somewhere else in its source page.
