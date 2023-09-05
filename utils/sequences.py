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
def main():
    try:
        print(random_sequence(str(sys.argv[1])))
    except:
        return 1

if __name__ == "__main__":
    sys.exit(main())
