# sphinx-toctree-level-up

[![PyPI version](https://img.shields.io/pypi/v/sphinx-toctree-level-up.svg)](https://pypi.org/project/sphinx-toctree-level-up/)
![Parallel safe](https://img.shields.io/badge/parallel%20safe-true-brightgreen)
[![CI](https://github.com/jdillard/sphinx-toctree-level-up/actions/workflows/ci.yml/badge.svg)](https://github.com/jdillard/sphinx-toctree-level-up/actions/workflows/ci.yml)

Standalone Sphinx extension that backports toctree `:level-up:` from [sphinx-doc/sphinx#8287](https://github.com/sphinx-doc/sphinx/issues/8287).

Use the same markup on your current Sphinx; delete the extension after you upgrade to a release that includes the native implementation.

> [!NOTE]
> **Status: beta.** This project was largely vibe-coded, so use it with appropriate caution. I use it myself and plan to maintain and support it, but its behavior may still change as it matures.

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
