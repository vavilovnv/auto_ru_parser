"""Main module."""

from src.parser import parse_response
from src.to_csv import save_to_file


def main():
    data = parse_response(input("Please enter a URL to parse: ").strip())
    if not len(data):
        print("No data found")
        return

    save_to_file(data)


if __name__ == "__main__":
    main()
