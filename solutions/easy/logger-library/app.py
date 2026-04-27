from models.log_level import LogLevel
from services.logger import Logger


def main() -> None:
    logger = Logger()
    logger.log(LogLevel.INFO, "Application booted")
    logger.log(LogLevel.DEBUG, "Loaded feature flags")
    logger.log(LogLevel.ERROR, "Database connection failed")

    print("INFO", logger.history_for(LogLevel.INFO))
    print("DEBUG", logger.history_for(LogLevel.DEBUG))
    print("ERROR", logger.history_for(LogLevel.ERROR))


if __name__ == "__main__":
    main()