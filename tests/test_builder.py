from pathlib import Path
from unittest.mock import Mock

import pytest

from deck_builder.configs.schemas import TitlesDigestSchema


def test_from_excel(builder, monkeypatch, frame, deck):
    reader = Mock(return_value=frame)
    monkeypatch.setattr(builder, "load_from_excel", reader)
    monkeypatch.setattr(builder, "Presentation", Mock(return_value=deck))
    result = builder.TitlesDigest.from_excel(Path("input.xlsx"))
    reader.assert_called_once_with(file_path="input.xlsx", schema=TitlesDigestSchema)
    assert result.df is frame and result.deck is deck
    assert result.config is builder.TITLES_DIGEST_CONFIG


@pytest.mark.parametrize("kind", ["none", "empty", "rows"])
def test_build(builder, monkeypatch, config, deck, frame, book, kind):
    title = Mock()
    detail = Mock()
    monkeypatch.setattr(builder, "add_title_slide", title)
    monkeypatch.setattr(builder, "add_bookinfo_slide", detail)
    df = (
        None
        if kind == "none"
        else frame.head(0)
        if kind == "empty"
        else frame.vstack(frame)
    )
    digest = builder.TitlesDigest(config, deck, df)
    assert (
        digest.build(title_text="Title", suptitle_text="Sub", attribution_text="By")
        is digest
    )
    assert (deck.slide_width, deck.slide_height) == (
        config.slide_size.width,
        config.slide_size.height,
    )
    title.assert_called_once_with(
        logo_path=config.assets.logo,
        presentation=deck,
        config=config,
        title_text="Title",
        suptitle_text="Sub",
        attribution_text="By",
    )
    assert detail.call_count == (2 if kind == "rows" else 0)
    for call in detail.call_args_list:
        assert call.kwargs == dict(presentation=deck, config=config, book=book)


def test_export_delegates(builder, monkeypatch, config, deck):
    export = Mock()
    monkeypatch.setattr(builder, "to_pptx", export)
    assert builder.TitlesDigest(config, deck, None).to_pptx("out.pptx") is None
    export.assert_called_once_with(deck, "out.pptx")


def test_loader_failure_propagates(builder, monkeypatch):
    monkeypatch.setattr(
        builder, "load_from_excel", Mock(side_effect=OSError("bad file"))
    )
    with pytest.raises(OSError, match="bad file"):
        builder.TitlesDigest.from_excel("bad.xlsx")


def test_invalid_excel_retained_as_none(builder, monkeypatch):
    monkeypatch.setattr(builder, "load_from_excel", Mock(return_value=None))
    assert builder.TitlesDigest.from_excel("bad.xlsx").df is None


def test_main(capsys):
    from deck_builder import main

    assert main() is None
    assert capsys.readouterr().out == "Hello from deck-builder!\n"
