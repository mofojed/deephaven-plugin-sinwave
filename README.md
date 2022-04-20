# Deephaven Plugin for Sin Waves

The Deephaven example Plugin for demonstrating Sin Waves.

## Build

To create your build / development environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools
pip install build deephaven-plugin
```

To build:

```sh
python -m build --wheel
```

produces the wheel into `dist/`.

To install in docker container (update `0.0.1.dev1` to correct version, see `dist/` folder for full name):

```sh
docker cp dist/deephaven_plugin_sinwave-0.0.1.dev1-py3-none-any.whl docker_server_1:/tmp && docker exec docker_server_1 pip install --force-reinstall /tmp/deephaven_plugin_sinwave-0.0.1.dev1-py3-none-any.whl
```

## Examples

You can create `count` number of Sin waves attached to one Figure, all of size `size`. Defaults are `count=1`, `size=100`:
```python
from deephaven.plugin.sinwave import SinWave
s = SinWave(count=1, size=100)
```