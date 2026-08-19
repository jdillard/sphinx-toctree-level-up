"""Directive surface for ``:level-up:`` and ``toc-level-up``."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from docutils import nodes

from sphinx import addnodes
from sphinx.testing import restructuredtext
from sphinx.testing.util import assert_node

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_toctree_level_up_option(app: SphinxTestApp) -> None:
    text = '.. toctree::\n   :level-up: 2\n\n   page1\n'

    app.env.find_files(app.config, app.builder)
    doctree = restructuredtext.parse(app, text, 'index')
    assert_node(doctree, [nodes.document, nodes.compound, addnodes.toctree])
    assert_node(doctree[0][0], addnodes.toctree, level_up=2)


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_toc_level_up_directive_sets_default(app: SphinxTestApp) -> None:
    text = '.. toc-level-up:: 1\n\n.. toctree::\n\n   page1\n'

    app.env.find_files(app.config, app.builder)
    doctree = restructuredtext.parse(app, text, 'index')
    assert_node(doctree, [nodes.document, nodes.compound, addnodes.toctree])
    assert_node(doctree[0][0], addnodes.toctree, level_up=1)
    assert app.env.current_document.get('toc_level_up') == 1


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_explicit_zero_overrides_default(app: SphinxTestApp) -> None:
    text = '.. toc-level-up:: 1\n\n.. toctree::\n   :level-up: 0\n\n   page1\n'

    app.env.find_files(app.config, app.builder)
    doctree = restructuredtext.parse(app, text, 'index')
    assert_node(doctree[0][0], addnodes.toctree, level_up=0)


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_no_target_level_or_level_option(app: SphinxTestApp) -> None:
    from docutils.parsers.rst import directives as rst_directives

    spec = rst_directives._directives['toctree'].option_spec
    assert 'target-level' not in spec
    assert 'level' not in spec
    assert 'level-up' in spec
