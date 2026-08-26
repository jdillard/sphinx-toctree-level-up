"""Monkeypatch ``inline_all_toctrees`` so single-file builders honor ``:level-up:``.

LaTeX, singlehtml, texinfo, and man call ``sphinx.util.nodes.inline_all_toctrees``
with no event hook. This wraps that function with the core
``_replace_toctree_with_inlined`` behavior from sphinx-doc/sphinx#8287.
HTML still resolves toctrees in place; only inlined builders change structure.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes

from sphinx import addnodes
from sphinx.locale import __
from sphinx.util import logging

if TYPE_CHECKING:
    from collections.abc import Callable

    from docutils.nodes import Element, Node

    from sphinx.builders import Builder

logger = logging.getLogger('sphinx.util.nodes')

_patched = False
_INLINED_ONLY_WRAPPER = 'toctree-level-up-inlined'


def patch_inline_all_toctrees() -> None:
    """Replace ``inline_all_toctrees`` on Sphinx and already-imported builders."""
    global _patched
    if _patched:
        return
    _patched = True

    import sphinx.builders.latex as latex_builder
    import sphinx.builders.manpage as manpage_builder
    import sphinx.builders.singlehtml as singlehtml_builder
    import sphinx.builders.texinfo as texinfo_builder
    import sphinx.util.nodes as nodes_mod

    for module in (
        nodes_mod,
        latex_builder,
        manpage_builder,
        singlehtml_builder,
        texinfo_builder,
    ):
        module.inline_all_toctrees = inline_all_toctrees


def inline_all_toctrees(
    builder: Builder,
    docnameset: set[str],
    docname: str,
    tree: nodes.document,
    colorfunc: Callable[[str], str],
    traversed: list[str],
    indent: str = '',
) -> nodes.document:
    """Inline all toctrees in *tree*, honoring ``:level-up:``."""
    tree = tree.deepcopy()
    for toctreenode in list(tree.findall(addnodes.toctree)):
        newnodes: list[Element] = []
        includefiles = map(str, toctreenode['includefiles'])
        indent += ' '
        for includefile in includefiles:
            if includefile not in traversed:
                try:
                    traversed.append(includefile)
                    logger.info(indent + colorfunc(includefile))  # NoQA: G003
                    subtree = inline_all_toctrees(
                        builder,
                        docnameset,
                        includefile,
                        builder.env.get_doctree(includefile),
                        colorfunc,
                        traversed,
                        indent,
                    )
                    docnameset.add(includefile)
                except Exception:
                    logger.warning(
                        __('toctree contains ref to nonexisting file %r'),
                        includefile,
                        location=docname,
                        type='toc',
                        subtype='not_readable',
                    )
                else:
                    sof = addnodes.start_of_file(docname=includefile)
                    sof.children = subtree.children
                    for sectionnode in sof.findall(nodes.section):
                        if 'docname' not in sectionnode:
                            sectionnode['docname'] = includefile
                    newnodes.append(sof)
        replace_toctree_with_inlined(toctreenode, newnodes)
    return tree


def _containing_section(node: Node) -> nodes.section | None:
    parent = node.parent
    while parent is not None:
        if isinstance(parent, nodes.section):
            return parent
        parent = parent.parent
    return None


def _only_ancestors_until(node: Node, ancestor: Node) -> list[addnodes.only]:
    """Return ``only`` ancestors crossed when moving *node* to *ancestor*."""
    result: list[addnodes.only] = []
    parent = node.parent
    while parent is not None and parent is not ancestor:
        if isinstance(parent, addnodes.only):
            result.append(parent)
        parent = parent.parent
    return result


def _wrap_in_only_nodes(
    newnodes: list[Element], only_nodes: list[addnodes.only]
) -> list[Element]:
    """Recreate escaped ``only`` wrappers around inlined documents."""
    wrapped = newnodes
    for original in only_nodes:
        replacement = addnodes.only(expr=original['expr'])
        replacement.source = original.source
        replacement.line = original.line
        replacement[_INLINED_ONLY_WRAPPER] = True
        replacement.extend(wrapped)
        wrapped = [replacement]
    return wrapped


def _is_inlined_document(node: Node) -> bool:
    """Return whether *node* was inserted by a promoted inlined toctree."""
    return isinstance(node, addnodes.start_of_file) or (
        isinstance(node, addnodes.only) and node.get(_INLINED_ONLY_WRAPPER, False)
    )


def replace_toctree_with_inlined(
    toctreenode: addnodes.toctree, newnodes: list[Element]
) -> None:
    """Replace a toctree with inlined documents, honoring ``:level-up:``.

    Single-file builders insert the included documents after the ancestor
    section so PDF/section nesting matches the promoted TOC. The original
    in-page toctree location is not used for HTML (resolved separately).
    """
    parent = toctreenode.parent
    if parent is None:
        return

    level_up = toctreenode.get('level-up', 0)
    if not level_up:
        parent.replace(toctreenode, newnodes)
        return

    target_section: nodes.section | None = None
    current: Node = toctreenode
    for _ in range(level_up):
        section = _containing_section(current)
        if section is None or section.parent is None:
            break
        target_section = section
        current = section

    escaped_only_nodes: list[addnodes.only] = []
    if target_section is not None and target_section.parent is not None:
        escaped_only_nodes = _only_ancestors_until(
            toctreenode, target_section.parent
        )

    toc_index = parent.index(toctreenode)
    wrapper_parent = parent.parent
    wrapper_index = wrapper_parent.index(parent) if wrapper_parent is not None else 0
    parent.remove(toctreenode)
    removed_wrapper = False
    if (
        isinstance(parent, nodes.compound)
        and 'toctree-wrapper' in parent.get('classes', ())
        and len(parent) == 0
        and wrapper_parent is not None
    ):
        wrapper_parent.remove(parent)
        removed_wrapper = True

    if not newnodes:
        return

    if target_section is not None and target_section.parent is not None:
        insert_parent = target_section.parent
        idx = insert_parent.index(target_section) + 1
        while idx < len(insert_parent) and _is_inlined_document(insert_parent[idx]):
            idx += 1
        moved_nodes = _wrap_in_only_nodes(newnodes, escaped_only_nodes)
        for offset, newnode in enumerate(moved_nodes):
            insert_parent.insert(idx + offset, newnode)
        return

    if removed_wrapper and wrapper_parent is not None:
        for offset, newnode in enumerate(newnodes):
            wrapper_parent.insert(wrapper_index + offset, newnode)
    else:
        for offset, newnode in enumerate(newnodes):
            parent.insert(toc_index + offset, newnode)
