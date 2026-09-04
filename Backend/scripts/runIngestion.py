from app.ingestion.pipeline import run_pipeline

from app.ingestion.scrapers.BuiltInScraper import BuiltInScraper
from app.ingestion.parsers.BuiltInParser import BuiltInParser

from app.ingestion.scrapers.WellfoundScraper import WellfoundScraper
from app.ingestion.parsers.WellfoundParser import WellfoundParser


def main():

    run_pipeline(
        BuiltInScraper(),
        BuiltInParser(),
        "Built In"
    )

    run_pipeline(
        WellfoundScraper(),
        WellfoundParser(),
        "Wellfound"
    )


if __name__ == "__main__":
    main()