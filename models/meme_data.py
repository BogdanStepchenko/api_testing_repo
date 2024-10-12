from pydantic import BaseModel


class MemeJson(BaseModel):
    id: int
    info: dict
    tags: list
    text: str
    updated_by: str
    url: str
