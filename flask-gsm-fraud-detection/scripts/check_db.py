"""Simple DB health-check script for the GSM fraud project.

Usage:
  python scripts/check_db.py        # prints summary
  python scripts/check_db.py <file>  # prints the upload record for <file>
"""
import sys
import json
import os
from typing import Optional

# When a script is executed directly (python scripts/check_db.py), Python
# sets sys.path[0] to the scripts/ directory, which prevents imports of
# sibling modules (like `database`) from the project root. Add the
# project root to sys.path so the script can import project modules
# regardless of how it's executed.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database import DB_PATH, init_db, list_uploads, get_upload_by_file


def main(target_file: Optional[str] = None, limit: int = 10):
    print('DB path:', DB_PATH)
    print('DB file exists:', os.path.exists(DB_PATH))
    # ensure schema exists
    init_db()
    uploads = list_uploads(limit)
    print(f'Total uploads returned (limit {limit}):', len(uploads))
    if uploads:
        print('\nLatest uploads:')
        for u in uploads:
            print(f"- {u['results_file']} | total={u['total']} frauds={u['predicted_frauds']} avg_prob={u.get('avg_prob')}")

    if target_file:
        print(f"\nLooking up file: {target_file}")
        r = get_upload_by_file(target_file)
        if not r:
            print('No record found for', target_file)
            return 2
        print('Record found:')
        print(json.dumps(r, indent=2))
    return 0


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(main(arg))
