# sphinx-toctree-level-up

[![PyPI version](https://img.shields.io/pypi/v/sphinx-toctree-level-up.svg)](https://pypi.org/project/sphinx-toctree-level-up/)
![Parallel safe](https://img.shields.io/badge/parallel%20safe-true-brightgreen)
[![CI](https://github.com/jdillard/sphinx-toctree-level-up/actions/workflows/ci.yml/badge.svg)](https://github.com/jdillard/sphinx-toctree-level-up/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/sphinx-toctree-level-up/badge/?version=latest)](https://sphinx-toctree-level-up.readthedocs.io/en/latest/)

A [Sphinx](http://sphinx-doc.org/) extension that promotes pages listed in a toctree so they sit higher in the TOC hierarchy than the section that contains the directive. It serves as a stop gap for the toctree `:level-up:` option, until [sphinx-doc/sphinx#8287](https://github.com/sphinx-doc/sphinx/issues/8287) lands in a release.

> [!NOTE]
> **Status: beta.** The origin of this project was largely created with the assistance of AI, so use it with appropriate caution. I use it myself and plan to maintain and support it, but its behavior may still change as it matures. Pull requests gladly accepted.

## Documentation

The docs are built as **singlehtml** so you can see how `:level-up:` affects the heiarchy.

- https://sphinx-toctree-level-up.readthedocs.io/

The same site is also published with no `:level-up:`, so you can compare:

- https://sphinx-toctree-level-up.readthedocs.io/en/latest/without-level-up/
