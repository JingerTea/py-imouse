from typing import List, TypedDict


class ColorParams(TypedDict):
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    first_color: str
    offset_color: str
    similarity: float
    dir: int


class ColorsParams(TypedDict):
    colors: List[ColorParams]
