from dataclasses import dataclass
from typing import ClassVar, TypedDict

from polars import Int16, Int64, Schema, Utf8


class BaseSchema:
    dtypes: ClassVar[Schema]


# Обязательные столбцы из выгрузки для дайджеста новинок
class TitlesDigestSchema(BaseSchema):
    dtypes: ClassVar[Schema] = Schema(
        {
            "Код ном-ры": Utf8,
            "ISBN": Utf8,
            "Наименование на обложку": Utf8,
            "Авторы на обложку": Utf8,
            "Аннотация": Utf8,
            "Пять причин купить": Utf8,
            "Серия": Utf8,
            "Формат": Utf8,
            "Продукция.Тип переплета": Utf8,
            "Кол-во стр": Int16,
            "Красочность блока текста": Utf8,
            "Тираж": Int64,
            "Продукция.Возрастное ограничение": Utf8,
        }
    )


BookRow = TypedDict(
    "BookRow",
    {
        "Код ном-ры": str,
        "ISBN": str,
        "Наименование на обложку": str,
        "Авторы на обложку": str,
        "Аннотация": str,
        "Пять причин купить": str,
        "Серия": str,
        "Формат": str,
        "Продукция.Тип переплета": str,
        "Кол-во стр": int,
        "Красочность блока текста": str,
        "Тираж": int,
        "Продукция.Возрастное ограничение": str,
    },
)


@dataclass
class BookInfo:
    item_code: str
    isbn: str
    title: str
    authors: str
    annotation: str
    reasons: str
    series: str
    book_format: str
    binding: str
    pages: int
    colority: str
    print_run: int
    age_limit: str
