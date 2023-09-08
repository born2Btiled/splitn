import sys
from rstr import xeger
from re import error, compile
from loguru import logger

@logger.catch
def random_sequence(pattern: str) -> str:
    try:
        return xeger(compile(pattern))
    except error as e:
        print(f"Non valid regex pattern: {e}")
        return ""

@logger.catch
def main(
    arg: str
) -> None:
    try:
        print(random_sequence(arg))
        sys.exit(0)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1])
