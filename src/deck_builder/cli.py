from pathlib import Path
from typing import Annotated

import typer

from deck_builder.builders.titles_digest import (
    DEFAULT_ATTRIBUTION_TEXT,
    DEFAULT_SUPTITLE_TEXT,
    DEFAULT_TITLE_TEXT,
    TitlesDigest,
)

app = typer.Typer(add_completion=False, pretty_exceptions_enable=False)


@app.command()
def main(
    input_file: Annotated[
        Path,
        typer.Argument(
            exists=True, dir_okay=False, readable=True, help="Входной Excel-файл."
        ),
    ],
    output_file: Annotated[
        Path,
        typer.Argument(dir_okay=False, help="Выходной PPTX-файл."),
    ],
    title: Annotated[
        str, typer.Option(help="Заголовок презентации.")
    ] = DEFAULT_TITLE_TEXT,
    suptitle: Annotated[
        str, typer.Option(help="Подзаголовок презентации.")
    ] = DEFAULT_SUPTITLE_TEXT,
    attribution: Annotated[
        str, typer.Option(help="Подпись на титульном слайде.")
    ] = DEFAULT_ATTRIBUTION_TEXT,
) -> None:
    """Создать дайджест книг из Excel и сохранить в PowerPoint."""
    if output_file.suffix.lower() != ".pptx":
        output_file = output_file.with_suffix(".pptx")
    if output_file.resolve() == input_file.resolve():
        raise typer.BadParameter("Выходной файл должен отличаться от входного.")

    try:
        digest = TitlesDigest.from_excel(str(input_file))
        if digest.df is None:
            typer.echo(
                "Ошибка: проверьте обязательные столбцы и типы данных Excel.", err=True
            )
            raise typer.Exit(code=1)
        digest.build(
            title_text=title,
            suptitle_text=suptitle,
            attribution_text=attribution,
        ).to_pptx(output_file)
    except typer.Exit:
        raise
    except Exception as exc:
        # CLI boundary: report reader, image and export errors without a traceback.
        typer.echo(f"Ошибка создания презентации: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Сохранено: {output_file}")


if __name__ == "__main__":
    app()
