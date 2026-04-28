#!/usr/bin/env python3
"""Extract conversation trace from Claude Code session jsonl, produce markdown.

Two outputs:
- trace/raw.md       — full pre-redaction (kept locally; mode 600; NEVER committed)
- trace/redacted.md  — paper-ready, semantic placeholders applied

C1 redaction policy (per `mem_672f37673a46` triad-coupling rule + GPT-Pro v2 semantic
placeholder discipline `mem_4afedbce8deb`): the reader of the redacted trace must see the
SEMANTIC CATEGORY of what was removed, not just `***`. This makes the redacted trace
readable as a narrative artifact (purpose: §4 case study) rather than a sea of holes.

Categories applied:
- [INTERNAL_MEMORY_ID_REDACTED: <label>]   — hub memo IDs, with semantic label when known
- [SECRET_PATH_REDACTED]                    — paths under ~/.secrets/
- [INTERNAL_NETWORK_IP_REDACTED]            — Tailscale 100.x.x.x
- [INTERNAL_DOMAIN_REDACTED]                — internal cloudflared / clawishmacheng surfaces
- [FAMILY_CONTEXT_REMOVED]                  — household-relationship semantic markers
- [FRIEND_NAME_REDACTED]                    — ambassador-friend real names
- [NONPUBLIC_CONTACT_REDACTED #N]           — researcher / principal real names, numbered for narrative coherence
- [PRIVATE_MIGRATION_CONTEXT_REMOVED]       — extraction_status values, BDSM-decoupling, relocation references
- [CONTACT_EMAIL_REDACTED]                  — owner-tier personal email addresses

Usage:
    ./extract_trace.py [session-jsonl-path]
    Default source: ~/.claude/projects/-Users-macheng/<latest-mtime>.jsonl

Produces: ./trace/raw.md (mode 600), ./trace/redacted.md (mode 644)
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "trace"
RAW_OUT = TRACE_DIR / "raw.md"
REDACTED_OUT = TRACE_DIR / "redacted.md"

# Known hub memo IDs → semantic labels. Anything not listed falls back to "unspecified-doctrine".
KNOWN_MEMO_LABELS: dict[str, str] = {
    "mem_c4e9264b9b7f": "mission-statement",
    "mem_672f37673a46": "openreview-pivot-decision",
    "mem_c3ce4f923902": "frame-validation-moment",
    "mem_c5d926a551ec": "section-6-reframe",
    "mem_22e061909669": "open-mindedness-criterion",
    "mem_75bbde3c4d8d": "triad-coupling-rule",
    "mem_780a20733da8": "three-layer-substrate-doctrine",
    "mem_e13b505a74aa": "constraint-manifest-source",
    "mem_dfe20f509f4b": "researcher-seeding-doctrine",
    "mem_da454b258b96": "cognitive-ops-c-plan",
    "mem_4afedbce8deb": "gpt-pro-v2-distill",
    "mem_1a745babad44": "paper-outline-locked",
    "mem_64922f054feb": "podcast-anchor-candidates",
    "mem_217dd2d84ae6": "gpt-pro-bridge-spec",
    "mem_9fe49fe6eb5f": "reminder-pool-design",
    "mem_ed3bee4a333e": "pull-based-outreach",
    "mem_8574cce83c36": "sedimented-safety-flag-hypothesis",
    "mem_79421695a16b": "cross-user-execution-denied",
    "mem_ba941daf0f20": "safety-charter",
    "mem_8ee25d20bf95": "sensitive-contact-hard-wall",
    "mem_cea00f3a5fe1": "mirror-plan-only-mode",
}

_MEM_RE = re.compile(r"\bmem_[a-f0-9]{6,}\b")


def _redact_mem_id(match: "re.Match[str]") -> str:
    mem_id = match.group(0)
    label = KNOWN_MEMO_LABELS.get(mem_id, "unspecified-doctrine")
    return f"[INTERNAL_MEMORY_ID_REDACTED: {label}]"


# Researcher / principal counter — keep stable per-name numbering for narrative coherence.
_CONTACT_COUNTER: dict[str, int] = {}
_CONTACT_NEXT = [1]


def _contact_label(canonical_name: str) -> str:
    if canonical_name not in _CONTACT_COUNTER:
        _CONTACT_COUNTER[canonical_name] = _CONTACT_NEXT[0]
        _CONTACT_NEXT[0] += 1
    return f"[NONPUBLIC_CONTACT_REDACTED #{_CONTACT_COUNTER[canonical_name]}]"


# Patterns are (regex, replacement-or-callable). Order matters: longer/more-specific first.
REDACT_PATTERNS: list[tuple[re.Pattern[str], object]] = [
    # Hub memo IDs — semantic label per dictionary, fallback "unspecified-doctrine"
    (_MEM_RE, _redact_mem_id),
    # Secrets paths
    (re.compile(r"/Users/macheng/\.secrets/[^\s\"\'`)]+"), "[SECRET_PATH_REDACTED]"),
    (re.compile(r"~/\.secrets/[^\s\"\'`)]+"), "[SECRET_PATH_REDACTED]"),
    # Tailscale internal IPs
    (re.compile(r"\b100\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "[INTERNAL_NETWORK_IP_REDACTED]"),
    # Internal cloudflared / tailscale infra surfaces (catch with or without .com / .net suffix)
    (re.compile(r"clawishmacheng(?:\.\w+)?"), "[INTERNAL_DOMAIN_REDACTED]"),
    # Personal-migration markers (extraction_status, BDSM-decoupling, relocation refs)
    (re.compile(r"extraction_status[:\s]*(SAFE_ENOUGH|NOT_SAFE_YET|safe_enough|not_safe_yet)", re.I),
     "[PRIVATE_MIGRATION_CONTEXT_REMOVED]"),
    (re.compile(r"\b(SAFE_ENOUGH|NOT_SAFE_YET)\b"), "[PRIVATE_MIGRATION_CONTEXT_REMOVED]"),
    (re.compile(r"BDSM[\w\-]*decoupling[^\n.]*[\n.]", re.I), "[PRIVATE_MIGRATION_CONTEXT_REMOVED]"),
    (re.compile(r"relocation-plan[\w\.\-_]*"), "[PRIVATE_MIGRATION_CONTEXT_REMOVED]"),
    # Family-relationship semantic markers
    (re.compile(r"主人|家奴|小奴|狗子"), "[FAMILY_CONTEXT_REMOVED]"),
    (re.compile(r"household[-_ ]member[-_ ][A-Z]"), "[FAMILY_CONTEXT_REMOVED]"),
    # Ambassador-friend real names — single category
    (re.compile(r"董张帆|Dong Zhangfan|dong\.zhangfan"), "[FRIEND_NAME_REDACTED]"),
    (re.compile(r"海帆"), "[FRIEND_NAME_REDACTED]"),
    (re.compile(r"高阳"), "[FRIEND_NAME_REDACTED]"),
    (re.compile(r"易大师|Yi Dashi|hanzhen\.m\.yi"), "[FRIEND_NAME_REDACTED]"),
    (re.compile(r"李彪|Li Biao|libiao_0303"), "[FRIEND_NAME_REDACTED]"),
    # Served-tier principals (Innocent / xiaonu / maxing / nozu / yima / yiwei / Doom)
    # Use stable numbered tag per name so trace narrative remains coherent
    (re.compile(r"\bInnocent\b|innocent@|1031693392zb"), lambda m: _contact_label("principal-innocent")),
    (re.compile(r"\bxiaonu\b"), lambda m: _contact_label("principal-xiaonu")),
    (re.compile(r"\bmaxing\b"), lambda m: _contact_label("principal-maxing")),
    (re.compile(r"\bnozu\b"), lambda m: _contact_label("principal-nozu")),
    (re.compile(r"\byima\b"), lambda m: _contact_label("principal-yima")),
    (re.compile(r"\byiwei\b"), lambda m: _contact_label("principal-yiwei")),
    (re.compile(r"\bDoom\b"), lambda m: _contact_label("principal-doom")),
    # 16+ researcher cold-email recipients — numbered consistently
    (re.compile(r"贺天行"), lambda m: _contact_label("res-htx")),
    (re.compile(r"赵行"), lambda m: _contact_label("res-zx")),
    (re.compile(r"\bSeohong\b|seohong@"), lambda m: _contact_label("res-seohong")),
    (re.compile(r"\bSamir\b|@dexterity"), lambda m: _contact_label("res-samir")),
    (re.compile(r"杜涛|taodu@"), lambda m: _contact_label("res-dutao")),
    (re.compile(r"龙哥|tianyonglong"), lambda m: _contact_label("res-longge")),
    (re.compile(r"雨杰|yujieq@"), lambda m: _contact_label("res-yujie")),
    (re.compile(r"Dongki Kim"), lambda m: _contact_label("res-dongki")),
    (re.compile(r"少雄|wsxiong@"), lambda m: _contact_label("res-shaoxiong")),
    (re.compile(r"丁铭|dm18@mails\.tsinghua"), lambda m: _contact_label("res-dingming")),
    (re.compile(r"付杰|jie\.fu@iquestlab"), lambda m: _contact_label("res-fujie")),
    (re.compile(r"袁行远|xingyuan@caiyunapp"), lambda m: _contact_label("res-yuanxingyuan")),
    (re.compile(r"Da Xiao|xiaoda99@"), lambda m: _contact_label("res-daxiao")),
    # Owner-tier personal emails (revealed in trace tool output)
    (re.compile(r"macshen93@gmail\.com"), "[CONTACT_EMAIL_REDACTED]"),
    (re.compile(r"shen\.claude\.code@gmail\.com"), "[CONTACT_EMAIL_REDACTED]"),
]


def redact(text: str) -> str:
    out = text
    for pat, repl in REDACT_PATTERNS:
        if callable(repl):
            out = pat.sub(repl, out)
        else:
            out = pat.sub(repl, out)
    return out


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def render_message(row: dict) -> str | None:
    msg = row.get("message") or row
    role = msg.get("role")
    if not role:
        return None
    content = msg.get("content")
    out_lines: list[str] = []
    if role == "user":
        out_lines.append("\n### USER\n")
    elif role == "assistant":
        out_lines.append("\n### ASSISTANT\n")
    else:
        out_lines.append(f"\n### {role.upper()}\n")
    if isinstance(content, str):
        out_lines.append(content)
    elif isinstance(content, list):
        for block in content:
            btype = block.get("type")
            if btype == "text":
                out_lines.append(block.get("text", ""))
            elif btype == "tool_use":
                name = block.get("name", "?")
                inp = block.get("input", {})
                out_lines.append(
                    f"\n**[tool_use: {name}]**\n```json\n"
                    + json.dumps(inp, ensure_ascii=False, indent=2)[:1500]
                    + "\n```\n"
                )
            elif btype == "tool_result":
                tc = block.get("tool_use_id", "?")
                tres = block.get("content", "")
                if isinstance(tres, list):
                    tres = "\n".join(b.get("text", "") for b in tres if isinstance(b, dict))
                out_lines.append(
                    f"\n**[tool_result for {tc}]**\n```\n"
                    + str(tres)[:2000]
                    + "\n```\n"
                )
            elif btype == "thinking":
                out_lines.append("\n*[internal-thinking-block]*\n")
    return "\n".join(out_lines)


def main() -> None:
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    else:
        proj_dir = Path.home() / ".claude" / "projects" / "-Users-macheng"
        candidates = sorted(proj_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            sys.exit("no session jsonl found")
        src = candidates[0]
    print(f"reading {src}")

    TRACE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(src)
    rendered: list[str] = []
    for row in rows:
        block = render_message(row)
        if block:
            rendered.append(block)

    raw_md = (
        f"# Session trace (raw)\n\nSource: `{src}`\nTotal turns: {len(rendered)}\n"
        + "\n".join(rendered)
    )
    redacted_md = redact(raw_md)

    RAW_OUT.write_text(raw_md)
    os.chmod(RAW_OUT, 0o600)
    REDACTED_OUT.write_text(redacted_md)

    # Emit a small redaction manifest beside the trace, listing categories applied.
    manifest_path = TRACE_DIR / "redaction_manifest.md"
    manifest = [
        "# Redaction Manifest",
        "",
        "Trace `redacted.md` had the following semantic categories applied per the C1",
        "redaction policy. Each category preserves narrative readability while withholding",
        "information that triggers the triad-coupling rule (capability-exposure ×",
        "personal-migration × safety-charter must move together).",
        "",
        "| Category | Replacement marker |",
        "|---|---|",
        "| Hub memo IDs (with semantic label when known) | `[INTERNAL_MEMORY_ID_REDACTED: <label>]` |",
        "| Secrets paths under `~/.secrets/` | `[SECRET_PATH_REDACTED]` |",
        "| Internal Tailscale IPs | `[INTERNAL_NETWORK_IP_REDACTED]` |",
        "| Internal cloudflared domains | `[INTERNAL_DOMAIN_REDACTED]` |",
        "| Family-relationship semantics | `[FAMILY_CONTEXT_REMOVED]` |",
        "| Ambassador-friend real names | `[FRIEND_NAME_REDACTED]` |",
        "| Researcher / principal real names | `[NONPUBLIC_CONTACT_REDACTED #N]` (stable per-name numbering) |",
        "| Personal-migration content (extraction status, BDSM-decoupling, relocation) | `[PRIVATE_MIGRATION_CONTEXT_REMOVED]` |",
        "| Owner personal email addresses | `[CONTACT_EMAIL_REDACTED]` |",
        "",
        "Full unredacted trace is available via request to the contact email listed in the",
        "main paper. Approval is per-applicant.",
        "",
        f"Counter assignment summary (deterministic, stable across runs):",
    ]
    for name, n in sorted(_CONTACT_COUNTER.items(), key=lambda kv: kv[1]):
        manifest.append(f"- `[NONPUBLIC_CONTACT_REDACTED #{n}]` — {name}")
    manifest_path.write_text("\n".join(manifest) + "\n")

    print(f"wrote {RAW_OUT} ({RAW_OUT.stat().st_size} bytes, mode 600)")
    print(f"wrote {REDACTED_OUT} ({REDACTED_OUT.stat().st_size} bytes)")
    print(f"wrote {manifest_path} ({manifest_path.stat().st_size} bytes)")
    print(f"contact-redaction counter assigned: {len(_CONTACT_COUNTER)} unique names")


if __name__ == "__main__":
    main()
