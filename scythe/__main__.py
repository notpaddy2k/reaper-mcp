"""Entry point for ``python -m scythe``."""

from scythe.server import mcp


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
