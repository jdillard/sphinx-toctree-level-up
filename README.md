# sphinx-toctree-level-up

[![PyPI version](https://img.shields.io/pypi/v/sphinx-toctree-level-up.svg)](https://pypi.org/project/sphinx-toctree-level-up/)
![Parallel safe](https://img.shields.io/badge/parallel%20safe-true-brightgreen)
[![CI](https://github.com/jdillard/sphinx-toctree-level-up/actions/workflows/ci.yml/badge.svg)](https://github.com/jdillard/sphinx-toctree-level-up/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/sphinx-toctree-level-up/badge/?version=latest)](https://sphinx-toctree-level-up.readthedocs.io/en/latest/)

Standalone Sphinx extension that backports toctree `:level-up:` from [sphinx-doc/sphinx#8287](https://github.com/sphinx-doc/sphinx/issues/8287).

Use the same markup on your current Sphinx; delete the extension after you upgrade to a release that includes the native implementation.

> [!NOTE]
> **Status: beta.** This project was largely vibe-coded, so use it with appropriate caution. I use it myself and plan to maintain and support it, but its behavior may still change as it matures.

## Documentation

The docs are built as **singlehtml** so you can see `:level-up:` change heading structure, not only the sidebar TOC. The same site also publishes a nested copy with no `:level-up:`:

- With `:level-up:`: https://sphinx-toctree-level-up.readthedocs.io/
- Without: https://sphinx-toctree-level-up.readthedocs.io/en/latest/without-level-up/

```bash
pip install -e ".[docs]"
sphinx-build -b singlehtml docs docs/_build/singlehtml
LEVEL_UP_DEMO=0 sphinx-build -b singlehtml docs docs/_build/singlehtml/without-level-up
mv docs/_build/singlehtml/without-level-up/index-without.html docs/_build/singlehtml/without-level-up/index.html
```

## Install

```bash
pip install sphinx-toctree-level-up
```

In `conf.py`:

```python
extensions = [
    'sphinx_toctree_level_up',
]
```

## Usage

`:level-up: N` is relative: promote *N* section levels from the section that contains the toctree. The visible HTML in-page list stays where the directive is written. Only the TOC hierarchy (sidebar / `env.tocs` / section numbering) and single-file builders (LaTeX, singlehtml, texinfo, man) change structure.

Promote listed pages to siblings of the current section:

```rst
My title
========

My header
---------

.. toctree::
   :level-up: 1

   page1
```

This produces a TOC hierarchy of:

```text
My title
├── My header
└── page1
```

rather than nesting `page1` under `My header`.

Set a per-document default for later `toctree` directives (like `highlight`). An explicit `:level-up:` on a toctree overrides it, including `:level-up: 0` to opt out:

```rst
.. toc-level-up:: 1

My header
---------

.. toctree::

   page1
```

Requesting more levels than there are ancestor sections emits a warning (`type='toc'`, `subtype='level_up'`) and promotes as far as possible.

This extension does **not** add `:target-level:` or `:level:`.

## Remove after upgrading Sphinx

This extension is meant as a stop gap. When Sphinx provides native `:level-up:`, this extension does not register its directives, so the feature is not applied twice. At startup it warns:

```text
sphinx_toctree_level_up is no longer needed; Sphinx already provides toctree :level-up:.
Remove this extension from conf.py.
```

Then delete `'sphinx_toctree_level_up'` from `extensions` and uninstall the package.
