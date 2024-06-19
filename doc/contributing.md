---
title: "Contributing"
---

See the [Scientific Python Developer Guide][spc-dev-intro] for a detailed
description of best practices for developing scientific packages.

[spc-dev-intro]: https://learn.scientific-python.org/development/


## Quick development

The fastest way to start with development is to use nox. If you don't have nox,
you can use `pipx run nox` to run it without installing, or `pipx install nox`.
If you don't have pipx (pip for applications), then you can install with
`pip install pipx` (the only case were installing an application with regular
pip is reasonable). If you use macOS, then pipx and nox are both in brew, use
`brew install pipx nox`.

To use, run `nox`. This will typecheck and test using every installed version of
Python on your system, skipping ones that are not installed. You can also run
specific jobs:

```console
$ nox -s typecheck              # Typecheck only
$ nox -s tests                  # Python tests
$ nox -s build_docs -- --serve  # Build and serve the docs
$ nox -s build_pkg              # Make an SDist and wheel
```

Nox handles everything for you, including setting up an temporary virtual
environment for each run.


## Setting up a development environment manually

You can set up a development environment using the environment manager of your choice.
For example, using `venv`:

```bash
python3 -m venv .venv
source ./.venv/bin/activate
```

Once you've created and activated an environment, install the package in editable mode:

```bash
pip install --editable .[dev]
```


## Automated checks and fixes

You should prepare pre-commit, which will help you by checking that commits pass
required checks and autofixing some issues. To set it up to run automatically on each
commit **(recommended)**:

```bash
pre-commit install # Will install a pre-commit hook into the git repo
```

To check the full repository manually:

```bash
pre-commit run --all-files
```


## Testing

Use pytest to run the unit checks:

```bash
nox -s test
```


## Coverage

Use pytest-cov to generate coverage reports:

```bash
pytest --cov=aross-stations-db
```


## Building docs

You can build the docs using:

```bash
nox -s build_docs
```

You can see a preview with:

```bash
nox -s build_docs -- --serve
```
