# Python Optimization Workshop

Example code for the [Python Optimization Workshop](https://adamj.eu/workshops/python-optimization/).
Follow along with the materials on that page.

## Setup

You need Python 3.12 or later.

```console
$ uv sync

$ source .venv/bin/activate

$ python generate_log.py

$ python analyze.py
```

Or, without uv:

```console
$ python -m venv .venv

$ source .venv/bin/activate

$ python -m pip install profiling-explorer tprof

$ python generate_log.py

$ python analyze.py
```

## Contents

* `analyze.py`: the program to optimize. It reads a web server access log and prints a report.
* `generate_log.py`: generates `access.log` and `bots.txt` for `analyze.py` to read.
* `django/runtests-tprof.patch`: a patch for Django’s `tests/runtests.py` that adds tprof, configured with environment variables.
