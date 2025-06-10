import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def dump_db():
    os.makedirs("dumps", exist_ok=True)

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_file = f"dumps/dump_{timestamp}.sql"

    os.environ["PGPASSWORD"] = db_pass

    try:
        subprocess.run(
            [
                "pg_dump",
                "-h", db_host,
                "-p", db_port,
                "-U", db_user,
                "-F", "p",
                "-f", dump_file,
                db_name
            ],
            check=True
        )
        print(f"Dump saved: {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during dump process: {e}")


if __name__ == "__main__":
    dump_db()
