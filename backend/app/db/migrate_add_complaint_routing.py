from sqlalchemy import text
from app.db.session import engine


def add_column(sql: str):
    try:
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
    except Exception as e:
        # If column already exists, sqlite throws error; ignore
        print("Skip:", e)


def main():
    add_column("ALTER TABLE complaints ADD COLUMN ward VARCHAR(120)")
    add_column("ALTER TABLE complaints ADD COLUMN routing_level VARCHAR(20)")
    add_column("ALTER TABLE complaints ADD COLUMN target_office VARCHAR(120)")
    print("✅ Complaint routing migration done")


if __name__ == "__main__":
    main()
