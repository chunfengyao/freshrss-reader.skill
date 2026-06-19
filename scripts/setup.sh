#!/usr/bin/env bash

_venv="${HOME}/workspace/.venv_freshrss-reader"
mkdir -p "${_venv}"
uv venv "${_venv}" --clear

uv pip install --python "${_venv}"/bin/python requests

