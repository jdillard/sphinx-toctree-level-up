"""Sphinx configuration for sphinx-toctree-level-up.

This site is meant to be built with the ``singlehtml`` builder so the
``toctree`` ``:level-up:`` option is visible in heading structure, not only
in the sidebar TOC.

Set ``LEVEL_UP_DEMO=0`` to build the comparison tree (no ``:level-up:``).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sphinx_toctree_level_up import __version__

project = 'sphinx-toctree-level-up'
copyright = '2026, Jared Dillard'
author = 'Jared Dillard'
release = __version__

# Default build uses :level-up:. ``LEVEL_UP_DEMO=0`` is the nested comparison.
# Leading underscore so Sphinx does not treat this as a config value.
_level_up_demo = os.environ.get('LEVEL_UP_DEMO', '1').lower() not in {
    '0',
    'false',
    'off',
    'no',
}

root_doc = 'index' if _level_up_demo else 'index-without'
# Sphinx 7 still reads master_doc in some paths.
master_doc = root_doc
# singlehtml names the page after root_doc, so the without build writes
# index-without.html, then CI deploys it as index.html.

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx_toctree_level_up',
    'sphinx_gitref',
    'sphinx_rtd_theme',
]

intersphinx_mapping = {
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

gitref_relative_project_root = '..'
gitref_remote_url = 'https://github.com/jdillard/sphinx-toctree-level-up'
gitref_branch = (
    os.environ.get('READTHEDOCS_GIT_COMMIT_HASH')
    or os.environ.get('GITHUB_SHA')
    or 'main'
)
gitref_hashing = False


exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
if _level_up_demo:
    exclude_patterns.append('index-without.rst')
else:
    exclude_patterns.append('index.rst')

html_theme = 'sphinx_rtd_theme'
html_title = (
    'sphinx-toctree-level-up'
    if _level_up_demo
    else 'sphinx-toctree-level-up (without :level-up:)'
)
