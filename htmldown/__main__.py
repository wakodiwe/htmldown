import argparse
import sys
from htmldown import fetch_to_file, fetch_and_convert


def main():
    parser = argparse.ArgumentParser(
        description="Fetch HTML from URL and convert to Markdown"
    )
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument(
        "-d", "--dir", default=".", help="Output directory (default: current)"
    )
    parser.add_argument(
        "-p", "--print", action="store_true", help="Print to stdout instead of saving"
    )

    args = parser.parse_args()

    try:
        if args.print:
            markdown = fetch_and_convert(args.url)
            print(markdown)
        elif args.output:
            fetch_and_convert(args.url, args.output)
            print(f"Saved to: {args.output}")
        else:
            output_path = fetch_to_file(args.url, args.dir)
            print(f"Saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
