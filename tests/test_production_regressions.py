"""Desired contracts violated by the supplied production source.

Strict xfails keep the normal suite useful. Run --runxfail to expose failures.
No production modules are changed by these tests.
"""

import inspect
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from deck_builder.configs.base import PresentationAssets
from deck_builder.core import images


@pytest.mark.parametrize(
    "module", ["deck_builder.core.slides", "deck_builder.builders.titles_digest"]
)
def test_public_module_import(module):
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        cwd=root,
        env={**os.environ, "PYTHONPATH": str(root / "src")},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_title_text_api(isolated_slides, deck, config):
    isolated_slides.add_title_slide(
        deck,
        config=config,
        title_text="Title",
        suptitle_text="Sub",
        attribution_text="By",
        logo_path=config.assets.logo,
    )


def test_book_accent_api(isolated_slides, monkeypatch, deck, config, book):
    monkeypatch.setattr(images, "download_cover_from_cdn", Mock(return_value=None))
    isolated_slides.add_bookinfo_slide(deck, config=config, book=book)


def test_title_width(isolated_slides, monkeypatch, deck, config):
    text = Mock()
    monkeypatch.setattr(isolated_slides, "add_safe_textbox", text)
    isolated_slides.add_title_slide(
        deck,
        config=config,
        title_text="T",
        suptitle_text="S",
        attribution_text="A",
        logo_path=config.assets.logo,
    )
    assert (
        text.call_args_list[0].kwargs["width"]
        == config.slide_size.width - config.margins.left - config.margins.right
    )


@pytest.mark.parametrize("name", ["logo", "icon"])
def test_default_assets_from_project_root(monkeypatch, name):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    assert getattr(PresentationAssets(), name).is_file()


def test_book_cover_contract(isolated_slides, monkeypatch, deck, config, book):
    textbox = Mock()
    textbox.return_value.text_frame.paragraphs = []
    monkeypatch.setattr(isolated_slides, "add_safe_textbox", textbox)
    monkeypatch.setattr(isolated_slides, "add_accent_text_box", Mock())
    cover = Mock()
    monkeypatch.setattr(isolated_slides, "add_cover_with_backdrop", cover)
    isolated_slides.add_bookinfo_slide(deck, config=config, book=book)
    kwargs = cover.call_args.kwargs
    assert kwargs.get("item_code") == book.item_code
    inspect.signature(images.add_cover_with_backdrop).bind(**kwargs)


def test_real_builder_build(builder, deck, config, frame, monkeypatch, tmp_path):
    from pptx import Presentation

    monkeypatch.setattr(images, "download_cover_from_cdn", Mock(return_value=None))
    digest = builder.TitlesDigest(config, deck, frame)
    digest.build(title_text="Title", suptitle_text="Sub", attribution_text="By")
    digest.to_pptx(tmp_path / "digest.pptx")
    assert len(Presentation(tmp_path / "digest.pptx").slides) == 2
