from sqlalchemy.orm import declarative_base
from app.db.session import Base  # noqa: F401
from app.db import models  # IMPORTANT: imports models so SQLAlchemy registers them
from app.db.models import Leader  # noqa: F401
