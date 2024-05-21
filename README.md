<p align="center">
  <picture>
    <img alt="K-Scale Open Source Robotics" src="https://media.kscale.dev/kscale-open-source-header.png" style="max-width: 100%;">
  </picture>
</p>

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/kscalelabs/gym-ksuite/main/LICENSE)
[![Discord](https://img.shields.io/discord/1224056091017478166)](https://discord.gg/k5mSvCkYQh)
[![Wiki](https://img.shields.io/badge/wiki-humanoids-black)](https://humanoids.wiki)
[![python](https://img.shields.io/badge/-Python_3.10-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)

</div>
<h1 align="center">
    <p>K-Scale Discord Bot</p>
</h1>

This is the source code for the K-Scale Labs Discord bot.

## Installation

To develop this bot, you can use [uv](https://astral.sh/blog/uv):

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
pip install -e '.[dev]'  # Installs the package with developer dependencies
```

Run the main bot locally using:

```bash
make serve-local
```

## Functionality

- [ ] Automatically scrapes Arxiv for new papers and posts them to the `#arxiv` channel
