from database import SessionLocal


def get_db():
    """Return data connection for given request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
