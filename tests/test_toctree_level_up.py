"""Test toctree ``:level-up:`` promotion (#8287)."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

import pytest
from docutils import nodes

from sphinx import addnodes
from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx.testing.util import assert_node

from sphinx_toctree_level_up._promote import promote_env_toc

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


def _strip_warnings(text: str) -> str:
    try:
        from sphinx._cli.util.errors import strip_escape_sequences
    except ImportError:
        from sphinx.util.console import strip_colors as strip_escape_sequences
    return strip_escape_sequences(text)


def _toc_children(item: nodes.list_item) -> list[tuple[str, object]]:
    """Return ``('section', title)`` / ``('toctree', includefiles)`` pairs."""
    if len(item) < 2 or not isinstance(item[1], nodes.bullet_list):
        return []
    result: list[tuple[str, object]] = []
    for child in item[1]:
        if isinstance(child, addnodes.toctree):
            result.append(('toctree', list(child['includefiles'])))
        elif isinstance(child, nodes.list_item):
            result.append(('section', child[0].astext()))
        elif isinstance(child, addnodes.only):
            for nested in child:
                if isinstance(nested, addnodes.toctree):
                    result.append(('only-toctree', list(nested['includefiles'])))
    return result


@pytest.mark.sphinx('xml', testroot='toctree-level-up')
@pytest.mark.test_params(shared_result='test_toctree_level_up')
def test_level_up_env_tocs(app: SphinxTestApp) -> None:
    app.build()

    title_item = app.env.tocs['index'][0]
    assert isinstance(title_item, nodes.list_item)
    children = _toc_children(title_item)
    assert children == [
        ('toctree', ['defaults', 'over']),
        ('section', 'Intro header'),
        ('toctree', ['page1']),
        ('section', 'Later sibling'),
        ('section', 'Level two'),
        ('toctree', ['page2']),
        ('section', 'Hidden section'),
        ('toctree', ['hidden']),
        ('section', 'Numbered section'),
        ('toctree', ['numbered']),
    ]

    assert isinstance(title_item[1], nodes.bullet_list)
    level_two = title_item[1][4]
    assert isinstance(level_two, nodes.list_item)
    assert _toc_children(level_two) == [('section', 'Nested')]


@pytest.mark.sphinx('xml', testroot='toctree-level-up')
@pytest.mark.test_params(shared_result='test_toctree_level_up')
def test_toc_level_up_directive_and_override(app: SphinxTestApp) -> None:
    app.build()

    title_item = app.env.tocs['defaults'][0]
    assert isinstance(title_item, nodes.list_item)
    children = _toc_children(title_item)
    assert children == [
        ('section', 'Section A'),
        ('toctree', ['default']),
        ('section', 'Section B'),
    ]

    assert isinstance(title_item[1], nodes.bullet_list)
    section_b = title_item[1][2]
    assert isinstance(section_b, nodes.list_item)
    assert isinstance(section_b[1], nodes.bullet_list)
    subsection = section_b[1][0]
    assert isinstance(subsection, nodes.list_item)
    assert _toc_children(subsection) == [('toctree', ['override'])]


@pytest.mark.sphinx('xml', testroot='toctree-level-up')
@pytest.mark.test_params(shared_result='test_toctree_level_up')
def test_level_up_over_promotion_warns(app: SphinxTestApp) -> None:
    app.build()

    # Promoted to a sibling of the document title, then stopped with a warning.
    toc = app.env.tocs['over']
    assert isinstance(toc[0], nodes.list_item)
    assert toc[0][0].astext() == 'Over'
    assert _toc_children(toc[0]) == [('section', 'Deep')]
    assert_node(toc[1], addnodes.toctree, includefiles=['over-child'])

    warnings = _strip_warnings(app.warning.getvalue())
    assert 'toctree :level-up: 5 exceeds the number of containing sections' in warnings


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_level_up_html_global_toc(app: SphinxTestApp) -> None:
    app.build()
    kwargs = {
        'collapse': False,
        'includehidden': True,
    }
    if 'tags' in inspect.signature(global_toctree_for_doc).parameters:
        kwargs['tags'] = app.tags
    toctree = global_toctree_for_doc(
        app.env,
        'index',
        app.builder,
        **kwargs,
    )
    assert toctree is not None
    # Hidden include of defaults/over, then promoted siblings of local sections.
    titles = [
        entry[0].astext()
        for entry in toctree.findall(nodes.list_item)
        if entry[0].astext()
        in {'Defaults', 'Over', 'Page 1', 'Page 2', 'Hidden page', 'Numbered page'}
    ]
    assert titles == [
        'Defaults',
        'Over',
        'Page 1',
        'Page 2',
        'Hidden page',
        'Numbered page',
    ]


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_level_up_html_in_page_order(app: SphinxTestApp) -> None:
    app.build()
    content = (app.outdir / 'index.html').read_text(encoding='utf8')
    before = content.index('Paragraph before toctree')
    after = content.index('Paragraph after toctree')
    # The visible list stays where the directive was written.
    page1 = content.index('main-toctree')
    later = content.index('Later sibling content')
    assert before < page1 < after < later


@pytest.mark.sphinx('latex', testroot='toctree-level-up')
def test_toctree_level_up_section_nesting(app: SphinxTestApp) -> None:
    app.build(force_all=True)
    tex_files = list(app.outdir.glob('*.tex'))
    assert tex_files
    result = tex_files[0].read_text(encoding='utf8')
    intro = result.index('\\chapter{Intro header}')
    page1 = result.index('\\chapter{Page 1}')
    later = result.index('\\chapter{Later sibling}')
    page2 = result.index('\\chapter{Page 2}')
    assert intro < page1 < later < page2
    assert '\\section{Page 1}' not in result
    assert '\\section{Page 2}' not in result
    assert '\\section{Hidden page}' not in result
    assert '\\chapter{Hidden page}' in result
    # Content after the toctree stays in the original section.
    assert result.index('Paragraph after toctree') < page1
    # toc-level-up default promotes default.rst; :level-up: 0 keeps override nested.
    assert '\\section{Default page}' in result
    assert '\\subsubsection{Override page}' in result


@pytest.mark.sphinx('singlehtml', testroot='toctree-level-up')
def test_toctree_level_up_singlehtml_section_nesting(app: SphinxTestApp) -> None:
    app.build(force_all=True)
    result = (app.outdir / 'index.html').read_text(encoding='utf8')
    intro = result.index('<h2>Intro header')
    page1 = result.index('<h2>Page 1')
    later = result.index('<h2>Later sibling')
    page2 = result.index('<h2>Page 2')
    assert intro < page1 < later < page2
    assert '<h3>Page 1' not in result
    assert '<h3>Page 2' not in result


@pytest.mark.sphinx('texinfo', testroot='toctree-level-up')
def test_toctree_level_up_texinfo_section_nesting(app: SphinxTestApp) -> None:
    app.build(force_all=True)
    texinfo_files = list(app.outdir.glob('*.texi'))
    assert texinfo_files
    result = texinfo_files[0].read_text(encoding='utf8')
    intro = result.index('@chapter Intro header')
    page1 = result.index('@chapter Page 1')
    later = result.index('@chapter Later sibling')
    page2 = result.index('@chapter Page 2')
    assert intro < page1 < later < page2
    assert '@section Page 1' not in result
    assert '@section Page 2' not in result


@pytest.mark.sphinx('man', testroot='toctree-level-up')
def test_toctree_level_up_man_section_nesting(app: SphinxTestApp) -> None:
    app.build(force_all=True)
    man_files = list(app.outdir.glob('*.[1-9]'))
    assert man_files
    result = man_files[0].read_text(encoding='utf8')
    intro = result.index('.SH INTRO HEADER')
    page1 = result.index('.SH PAGE 1')
    later = result.index('.SH LATER SIBLING')
    page2 = result.index('.SH PAGE 2')
    assert intro < page1 < later < page2
    assert '.SS Page 1' not in result
    assert '.SS Page 2' not in result


@pytest.mark.sphinx('latex', testroot='only-level-up')
def test_level_up_only_wrapper_excludes_latex(app: SphinxTestApp) -> None:
    app.build(force_all=True)
    tex_files = list(app.outdir.glob('*.tex'))
    assert tex_files
    result = tex_files[0].read_text(encoding='utf8')
    assert 'Child body.' not in result


@pytest.mark.sphinx('singlehtml', testroot='only-level-up')
def test_level_up_only_wrapper_includes_singlehtml(app: SphinxTestApp) -> None:
    app.build(force_all=True)
    result = (app.outdir / 'index.html').read_text(encoding='utf8')
    assert 'Child body.' in result


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_setup_native_support_warning(app: SphinxTestApp) -> None:
    from sphinx.directives.other import TocTree as BuiltinTocTree

    warnings = _strip_warnings(app.warning.getvalue())
    native = 'level-up' in BuiltinTocTree.option_spec
    needed = 'sphinx_toctree_level_up is no longer needed' in warnings
    assert needed is native


@pytest.mark.sphinx('xml', testroot='only-level-up')
def test_level_up_preserves_only_wrapper(app: SphinxTestApp) -> None:
    app.build()
    title_item = app.env.tocs['index'][0]
    assert isinstance(title_item, nodes.list_item)
    assert _toc_children(title_item) == [
        ('section', 'Section'),
        ('only-toctree', ['child']),
    ]


def test_promote_preserves_only_wrapper() -> None:
    toctree = addnodes.toctree()
    toctree['level-up'] = 1
    toctree['includefiles'] = ['page1']
    toctree['entries'] = [(None, 'page1')]
    only = addnodes.only(expr='html')
    only.source = 'index.rst'
    only.line = 4
    only.append(toctree)

    title = nodes.list_item('', nodes.paragraph('', 'Title'))
    section = nodes.list_item('', nodes.paragraph('', 'Section'))
    section.append(nodes.bullet_list('', only))
    title.append(nodes.bullet_list('', section))
    toc = nodes.bullet_list('', title)

    promote_env_toc(toc)

    children = list(title[1])
    assert isinstance(children[0], nodes.list_item)
    assert children[0][0].astext() == 'Section'
    assert isinstance(children[1], addnodes.only)
    assert children[1]['expr'] == 'html'
    assert isinstance(children[1][0], addnodes.toctree)
    assert list(children[1][0]['includefiles']) == ['page1']
