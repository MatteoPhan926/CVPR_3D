"""Pure local arithmetic illustration; never imports spaces or calls a service."""
import json
from pathlib import Path

base = Path(__file__).parent / "spaces_0_50_2_source/spaces/zero"
configs = json.loads((base / "configs.json").read_text())
rows = []
for config in configs:
    declared = 120
    factor = config["duration_factor"]
    # Exact non-xlarge arithmetic used in client.py:126-135 and :145-146.
    scheduled = round(declared * factor)
    displayed = declared
    rows.append({
        "hardware_config": config["model"],
        "duration_factor": factor,
        "declared_seconds": declared,
        "scheduled_seconds_if_this_config_selected": scheduled,
        "displayed_requested_seconds": displayed,
        "176_less_than_scheduled": 176 < scheduled,
        "180_less_than_scheduled": 180 < scheduled,
    })
result = {
    "kind": "local arithmetic illustration, not scheduler or account verification",
    "rows": rows,
    "remote_gpu_config_known": False,
    "remote_comparison_rule_known": False,
    "backend_rounding_known": False,
}
print(json.dumps(result, indent=2))
