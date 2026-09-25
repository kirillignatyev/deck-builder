from polars import DataFrame, read_excel

from deck_builder.configs.schemas import BaseSchema
from deck_builder.io.validate import has_required_columns, has_valid_dtypes


def load_from_excel(
    file_path: str,
    schema: type[BaseSchema],
) -> DataFrame | None:
    df = read_excel(file_path)

    if not has_required_columns(
        required_columns=list(schema.dtypes),
        df=df,
    ):
        return None

    if not has_valid_dtypes(
        schema=schema,
        df=df,
    ):
        return None

    return df.cast(schema.dtypes, strict=True)
