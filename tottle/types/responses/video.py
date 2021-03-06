from typing import Optional

from pydantic import BaseModel

from ..responses.photo import PhotoSize


class Video(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = 0

    width: int
    height: int
    duration: int

    thumb: Optional[PhotoSize] = None
    mime_type: Optional[str] = ""


class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = 0

    length: int
    duration: int
    thumb: Optional[PhotoSize] = None
