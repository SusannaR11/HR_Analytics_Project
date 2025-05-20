import json
from pathlib import Path

# test for model materialization for debugging
manifest_path = Path("target/manifest.json")

if not manifest_path.exists():
    print("❌ manifest.json saknas. Kör `dbt build` först.")
    exit(1)

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print("📦 dbt-modeller och deras materialized-typ:\n")

for node_id, node in manifest["nodes"].items():
    if node_id.startswith("model."):
        name = node["name"]
        resource_type = node["resource_type"]
        materialized = node["config"].get("materialized", "(okänd)")
        path = node["path"]

        print(f"🧱 {name.ljust(30)}  →  {materialized.ljust(10)}  ({path})")
# source gpt