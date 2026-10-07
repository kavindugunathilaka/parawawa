"""Build everything (articles, system pages, comparison pages, hub, sitemap): python tools/build.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_articles  # noqa: E402
import build_systems  # noqa: E402
import build_compare  # noqa: E402

build_articles.main()
build_systems.main()
build_compare.main()
