from sqlalchemy import text
from app.db.session import engine


def main():
    try:
        with engine.connect() as conn:
            conn.execute(
                text("ALTER TABLE leaders ADD COLUMN image_path TEXT"))
            conn.commit()
        print("✅ Added image_path to leaders")
    except Exception as e:
        print("Skip:", e)


if __name__ == "__main__":
    main()
