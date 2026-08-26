"""Backport of Sphinx toctree ``:level-up:`` (sphinx-doc/sphinx#8287).

When the installed Sphinx already provides this feature, ``setup()`` emits a
warning and does not register handlers, so the native implementation is not
applied twice.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives.other import TocTree as BuiltinTocTree
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from sphinx_toctree_level_up._inline import patch_inline_all_toctrees
from sphinx_toctree_level_up._promote import promote_env_toc

if TYPE_CHECKING:
    from typing import ClassVar

    from docutils.nodes import Node

    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec

__version__ = '0.1.1'
__all__ = ['TocLevelUp', 'TocTree', 'setup']

EXTENSION_NAME = 'sphinx_toctree_level_up'
logger = logging.getLogger(__name__)

# Mapping key stored on ``env.current_document`` / ``env.temp_data``.
# Writes go to ``_CurrentDocument._extension_data``; we do not add a slot.
_TOC_LEVEL_UP_KEY = 'toc_level_up'


def _has_native_level_up() -> bool:
    """Return True if builtin ``toctree`` already accepts ``:level-up:``."""
    return 'level-up' in BuiltinTocTree.option_spec


def _get_toc_level_up(env: BuildEnvironment) -> int:
    """Return the per-document default ``:level-up:`` (0 if unset)."""
    current = getattr(env, 'current_document', None)
    if current is not None:
        try:
            value = current.get(_TOC_LEVEL_UP_KEY, 0)
        except (AttributeError, TypeError):
            value = 0
        if value is None:
            return 0
        return int(value)
    temp_data = getattr(env, 'temp_data', None)
    if temp_data is not None:
        return int(temp_data.get(_TOC_LEVEL_UP_KEY, 0) or 0)
    return 0


def _set_toc_level_up(env: BuildEnvironment, level: int) -> None:
    """Store the per-document default without adding a ``_CurrentDocument`` slot."""
    current = getattr(env, 'current_document', None)
    if current is not None:
        current[_TOC_LEVEL_UP_KEY] = level
        return
    env.temp_data[_TOC_LEVEL_UP_KEY] = level


class TocTree(BuiltinTocTree):
    """Builtin ``toctree`` plus ``:level-up:``."""

    option_spec = {
        **BuiltinTocTree.option_spec,
        'level-up': directives.nonnegative_int,
    }

    def run(self) -> list[Node]:
        result = super().run()
        level_up = self.options.get('level-up', _get_toc_level_up(self.env))
        for node in result:
            if isinstance(node, nodes.Element):
                for toctree in node.findall(addnodes.toctree):
                    toctree['level-up'] = level_up
        return result


class TocLevelUp(SphinxDirective):
    """Set the default ``toctree`` ``:level-up:`` for this document."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {}

    def run(self) -> list[Node]:
        try:
            level = directives.nonnegative_int(self.arguments[0])
        except (TypeError, ValueError) as exc:
            msg = 'invalid toc-level-up argument'
            raise self.error(msg) from exc
        _set_toc_level_up(self.env, level)
        return []


def _on_doctree_read(app: Sphinx, doctree: nodes.document) -> None:
    """Re-parent toctree copies in ``env.tocs`` after the builtin collector."""
    env = app.env
    docname = env.docname
    toc = env.tocs.get(docname)
    if toc is None:
        return
    promote_env_toc(toc)


def setup(app: Sphinx) -> ExtensionMetadata:
    if _has_native_level_up():
        logger.warning(
            '%s is no longer needed; Sphinx already provides toctree :level-up:.\n'
            'Remove this extension from conf.py.',
            EXTENSION_NAME,
            type='toc',
            subtype='level_up',
        )
        return {
            'version': __version__,
            'parallel_read_safe': True,
            'parallel_write_safe': True,
        }

    app.add_directive('toctree', TocTree, override=True)
    app.add_directive('toc-level-up', TocLevelUp)
    # Builtin TocTreeCollector uses the default priority (500). Run after it.
    app.connect('doctree-read', _on_doctree_read, priority=600)
    patch_inline_all_toctrees()

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
