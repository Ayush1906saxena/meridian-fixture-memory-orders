"""House rule: every route the app serves has a row in docs/API.md. Run by CI after the tests."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from app.main import create_app  # noqa: E402

docs = pathlib.Path(__file__).resolve().parent.parent.joinpath("docs", "API.md").read_text()
missing = []
for rule in create_app(":memory:").url_map.iter_rules():
    if rule.endpoint == "static":
        continue
    for method in sorted(rule.methods - {"HEAD", "OPTIONS"}):
        if f"| {method} | {rule.rule} |" not in docs:
            missing.append(f"{method} {rule.rule}")
if missing:
    print("API docs check failed: every route needs a row in docs/API.md, formatted "
          "'| METHOD | /path | what it does |' with the path exactly as the route declares it. Missing: "
          + ", ".join(missing))
    sys.exit(1)
print("API docs check passed")
