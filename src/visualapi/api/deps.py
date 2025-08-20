"""API Dependencies"""

from typing import Annotated

from auth.api import authorize as authorize
from db import visual
from fastapi import Depends
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(visual.get_db)]
