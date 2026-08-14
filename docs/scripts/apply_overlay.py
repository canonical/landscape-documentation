#!/usr/bin/env python3
"""Apply docs/_static/openapi-overlay.yaml to docs/_static/openapi.yaml.

Produces docs/_static/openapi-with-examples.yaml, the merged spec that
docs/reference/api/debarchive.md points Scalar at. That output file is
generated and gitignored; it is never committed.

Run automatically by:
  * the Read the Docs `pre_build` job (see .readthedocs.yaml)
  * `make html` / `make run` from the repository root (see the root Makefile)

See https://documentation.ubuntu.com/landscape-internal/en/latest/design-docs/openapi-examples-overlay/
for the full design behind this script, including why overlay targets MUST be
literal JSONPaths and why a target that matches nothing MUST fail the build
rather than silently doing nothing.
"""

import sys
from pathlib import Path

import yaml
from jsonpath_ng.ext import parse as parse_jsonpath
from oas_patch import apply_overlay as apply_overlay_actions
from oas_patch import load_file, save_file
from oas_patch import validate as validate_overlay_doc

STATIC_DIR = Path(__file__).resolve().parent.parent / "_static"
BASE_SPEC = STATIC_DIR / "openapi.yaml"
OVERLAY = STATIC_DIR / "openapi-overlay.yaml"
OUTPUT = STATIC_DIR / "openapi-with-examples.yaml"

# oas-patch corrupted unrelated parts of the document when tested against a
# wildcard-and-filter target (see "Targets MUST be literal" in
# openapi-examples-overlay.md), so targets using either are rejected outright.
DISALLOWED_TARGET_SUBSTRINGS = ("*", "[?")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def reject_non_literal_targets(actions: list) -> None:
    for action in actions:
        target = action.get("target", "")
        if any(substring in target for substring in DISALLOWED_TARGET_SUBSTRINGS):
            fail(
                f"overlay target {target!r} in {OVERLAY.name} uses a wildcard or "
                "filter expression ('*' or '[?'). Targets MUST be full literal "
                "JSONPaths. See 'Targets MUST be literal' in "
                "openapi-examples-overlay.md."
            )


def validate_overlay_schema(overlay_doc: dict) -> None:
    report_yaml = validate_overlay_doc(overlay_doc, "yaml")
    report = yaml.safe_load(report_yaml) or {}
    if report.get("status") != "success":
        print(report_yaml, file=sys.stderr)
        fail(f"{OVERLAY.name} failed Overlay schema validation.")


def check_targets_match(actions: list, base_spec: dict) -> None:
    """Fail if any overlay target matches nothing in the base spec.

    oas-patch silently no-ops when a target matches nothing, which would let a
    proto rename or removal delete examples without the build noticing. See
    '"Overlay target matched nothing"' in openapi-examples-overlay.md.
    """
    for action in actions:
        target = action["target"]
        try:
            matches = parse_jsonpath(target).find(base_spec)
        except Exception as exc:  # noqa: BLE001 - surface any JSONPath parse error
            fail(f"overlay target {target!r} in {OVERLAY.name} is invalid: {exc}")
        if not matches:
            fail(
                f"overlay target matched nothing in {BASE_SPEC.name}: {target!r}. "
                "The path or operation this example documents was probably "
                f"renamed or removed upstream. Update the target in "
                f"{OVERLAY.name} to match, in the same PR."
            )


def main() -> None:
    if not BASE_SPEC.exists():
        fail(f"{BASE_SPEC} not found.")
    if not OVERLAY.exists():
        fail(f"{OVERLAY} not found.")

    try:
        overlay_doc = load_file(str(OVERLAY))
        base_spec = load_file(str(BASE_SPEC))
    except (FileNotFoundError, ValueError) as exc:
        fail(str(exc))

    actions = overlay_doc.get("actions", [])
    if not actions:
        fail(f"{OVERLAY.name} defines no overlay actions.")

    reject_non_literal_targets(actions)
    validate_overlay_schema(overlay_doc)
    check_targets_match(actions, base_spec)

    merged_spec = apply_overlay_actions(base_spec, overlay_doc)
    save_file(merged_spec, str(OUTPUT))
    print(f"Applied {OVERLAY.name} to {BASE_SPEC.name} -> {OUTPUT.name}")


if __name__ == "__main__":
    main()
