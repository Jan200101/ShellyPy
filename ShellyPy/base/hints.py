from dataclasses import dataclass
from typing import Annotated, Literal

@dataclass
class ValueRange:
    def __hash__(self):
        return hash(self.min) + hash(self.max)

    min: float
    max: float

byte = Annotated[int, ValueRange(0, 255)]
percent = Annotated[int, ValueRange(0, 100)]
temperaur = Annotated[int, ValueRange(3000, 6500)]
transition = Annotated[int, ValueRange(0, 5000)]

rgbw_mode = Literal["color", "white"]
