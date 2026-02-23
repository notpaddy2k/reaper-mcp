"""Entry point for Scythe MCP server.

Works both as ``python -m scythe`` (when pip-installed) and when run
directly by Claude Desktop from an extracted .mcpb extension.
"""

import os
import sys

# When launched from a .mcpb extension, the package isn't pip-installed,
# so we add the parent directory to sys.path so "from scythe.server ..."
# can resolve.
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from scythe.server import mcp  # noqa: E402


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
