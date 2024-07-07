from typing import List, Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = "x"
    banana: str = "y"


class Concert(BaseModel):
    foo: Foo
    bars: List[Bar]


a = Spam(foo=Foo(count=1), bars=[Bar()])

print(a)
