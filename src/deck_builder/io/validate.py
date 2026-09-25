from polars import DataFrame
from polars.exceptions import InvalidOperationError

from deck_builder.configs.schemas import BaseSchema


def has_required_columns(
    required_columns: list[str],
    df: DataFrame,
) -> bool:
    present_cols = df.columns
    missing_cols = list(set(required_columns) - set(present_cols))

    if missing_cols:
        print(f"Отсутствуют обязательные столбцы: {missing_cols}")
        return False

    return True


def has_valid_dtypes(
    schema: type[BaseSchema],
    df: DataFrame,
) -> bool:
    wrong_dtypes: list[str] = []

    for column, dtype in schema.dtypes.items():
        try:
            _ = df[column].cast(dtype, strict=True)
        except InvalidOperationError:
            wrong_dtypes.append(f"{column} → {dtype}")

    if wrong_dtypes:
        print("Эти столбцы нельзя привести к нужному типу: " + ", ".join(wrong_dtypes))
        return False

    return True
