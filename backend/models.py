from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BBox(BaseModel):
    x: float
    y: float
    w: float
    h: float
    page: int = 0

    def union(self, other):
        return BBox(
            x=min(self.x, other.x),
            y=min(self.y, other.y),
            w=max(self.x + self.w, other.x + other.w) - min(self.x, other.x),
            h=max(self.y + self.h, other.y + other.h) - min(self.y, other.y),
            page=self.page
        )


class Token(BaseModel):
    text: str
    bbox: BBox
    conf: float


class PageImage(BaseModel):
    index: int
    path: str
    width: int
    height: int


class SignalScore(BaseModel):
    name: str
    score: float
    weight: float
    reason: str


class FieldConfidence(BaseModel):
    raw: float
    signals: list[SignalScore] = Field(default_factory=list)


class FieldSource(str, Enum):
    VLM = "vlm"
    OCR = "ocr"


class ExtractedField(BaseModel):
    name: str
    value: Optional[str] = None
    bbox: Optional[BBox] = None
    source: FieldSource = FieldSource.VLM
    confidence: Optional[FieldConfidence] = None


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    unit_price: Optional[str] = None
    amount: Optional[str] = None


class RoutingAction(str, Enum):
    AUTO_APPROVE = "auto_approve"
    REVIEW = "review"
    REJECT = "reject"


class RoutingDecision(BaseModel):
    action: RoutingAction
    doc_score: float
    reasons: list[str] = []


class ExtractionResult(BaseModel):
    doc_id: str
    pages: list[PageImage] = []
    fields: list[ExtractedField] = []
    tokens: list[Token] = []
    line_items: list[LineItem] = []

    def field(self, name):
        return next(
            (
                f
                for f in self.fields
                if f.name == name
            ),
            None
        )