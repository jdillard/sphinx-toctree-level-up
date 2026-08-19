"""Re-parent toctree copies in ``env.tocs`` using the core pending-bubble algorithm.

Builtin ``TocTreeCollector`` already built ``env.tocs`` on ``doctree-read``.
User extensions load after builtins, so this walks the collected TOC and
promotes ``toctree`` nodes the same way ``build_toc`` does in
``sphinx/environment/collectors/toctree.py`` (sphinx-doc/sphinx#8287).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes

from sphinx import addnodes
from sphinx.locale import __
from sphinx.util import logging

if TYPE_CHECKING:
    from docutils.nodes import Element

logger = logging.getLogger(__name__)


def promote_env_toc(toc: nodes.bullet_list) -> None:
    """Move toctree copies in *toc* according to each node's ``level-up``."""
    new_entries, pending = _promote_entries(toc)
    for remaining, toc_item in pending:
        if remaining > 0:
            logger.warning(
                __('toctree :level-up: %s exceeds the number of containing sections'),
                _toctree_level_up(toc_item),
                location=toc_item,
                type='toc',
                subtype='level_up',
            )
        new_entries.append(toc_item)
    toc.clear()
    toc.extend(new_entries)


def _promote_entries(
    container: Element,
) -> tuple[list[Element], list[tuple[int, Element]]]:
    """Apply the pending-bubble algorithm to children of a TOC bullet list or ``only``.

    Returns ``(entries, pending)`` where *pending* items still need *remaining*
    section levels of promotion.
    """
    entries: list[Element] = []
    pending: list[tuple[int, Element]] = []
    for child in list(container.children):
        if isinstance(child, nodes.list_item):
            nested = _nested_bullet_list(child)
            if nested is not None:
                new_children, child_pending = _promote_entries(nested)
                nested.clear()
                if new_children:
                    nested.extend(new_children)
                elif nested.parent is not None:
                    nested.parent.remove(nested)
            else:
                child_pending = []
            entries.append(child)
            for remaining, toc_item in child_pending:
                if remaining == 1:
                    entries.append(toc_item)
                else:
                    pending.append((remaining - 1, toc_item))
        elif isinstance(child, addnodes.only):
            new_children, child_pending = _promote_entries(child)
            child.clear()
            if new_children:
                child.extend(new_children)
                entries.append(child)
            # ``only`` is not a section level; keep builder filtering on
            # promoted toctrees without decrementing ``remaining``.
            for remaining, toc_item in child_pending:
                wrapped = addnodes.only(expr=child['expr'])
                wrapped.source = child.source
                wrapped.line = child.line
                wrapped.append(toc_item)
                pending.append((remaining, wrapped))
        elif isinstance(child, addnodes.toctree):
            level_up = child.get('level-up', 0)
            if level_up:
                pending.append((level_up, child))
            else:
                entries.append(child)
        else:
            entries.append(child)
    return entries, pending


def _nested_bullet_list(item: nodes.list_item) -> nodes.bullet_list | None:
    for child in item.children:
        if isinstance(child, nodes.bullet_list):
            return child
    return None


def _toctree_level_up(node: Element) -> int:
    """Return the ``level-up`` value from *node* or a nested toctree."""
    if isinstance(node, addnodes.toctree):
        return node.get('level-up', 0)
    for toctreenode in node.findall(addnodes.toctree):
        return toctreenode.get('level-up', 0)
    return 0
