# pykv

# pykv

**A lightweight educational Key-Value Store** built in Python.

Features a clean CLI and FastAPI-powered REST API.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-success)

## Features

- In-memory key-value storage with TTL support
- Write-Ahead Log (WAL) for crash recovery
- Beautiful CLI interface (with Rich)
- REST API with Swagger UI
- Easy to extend

## Installation

```bash
git clone https://github.com/DjCodepulse/pykv.git
cd pykv
python -m venv .venv
.venv\Scripts\activate
pip install -e .