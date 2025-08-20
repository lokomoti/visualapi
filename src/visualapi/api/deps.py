"""API Dependencies"""
from typing import Annotated
from auth.api import authorize as authorize
from fastapi import Depends
from sqlmodel import Session
from db import visual


SessionDep = Annotated[Session, Depends(visual.get_db)]


