import subprocess
from dotenv import load_dotenv

load_dotenv()


def run_spider():
    try:
        subprocess.run(
            [
                "scrapy", "crawl", "autoria",
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_spider()
