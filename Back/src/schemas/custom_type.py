from typing import Annotated
from datetime import datetime
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
time = Annotated[TIMESTAMP, mapped_column(TIMESTAMP, default=datetime.utcnow)]
email = Annotated[str, mapped_column(unique=True, index=True, nullable=False)]
