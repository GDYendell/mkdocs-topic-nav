# setup.py

from setuptools import setup

setup(
    name="mkdocs-topic-nav",
    version="0.1",
    description="Custom MkDocs plugin for context-aware navigation of different topics",
    packages=["mkdocs_topic_nav"],
    package_dir={"": "src"},
    install_requires=["mkdocs"],
    entry_points={
        "mkdocs.plugins": [
            "topic-nav = mkdocs_topic_nav.plugin:TopicNavPlugin",
        ]
    },
)
