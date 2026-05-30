#!/usr/bin/env python3
"""
Utility script to write translated markdown content to a file.
Called with: python3 translate_write.py <output_path>
Reads base64-encoded content from stdin, decodes it, and writes to output_path.
This avoids ALL shell escaping issues since base64 is alphanumeric.
"""
import sys
import base64
import pathlib

def main():
    if len(sys.argv) < 2:
        print("Usage: echo <base64_content> | python3 translate_write.py <output_path>", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[1]
    encoded = sys.stdin.read().strip()

    try:
        content = base64.b64decode(encoded).decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64: {e}", file=sys.stderr)
        sys.exit(1)

    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(output_path).write_text(content, encoding='utf-8')
    print(f"Wrote {len(content)} bytes to {output_path}")

if __name__ == '__main__':
    main()
