# Redaction Manifest

Trace `redacted.md` had the following semantic categories applied per the C1
redaction policy. Each category preserves narrative readability while withholding
information that triggers the triad-coupling rule (capability-exposure ×
personal-migration × safety-charter must move together).

| Category | Replacement marker |
|---|---|
| Hub memo IDs (with semantic label when known) | `[INTERNAL_MEMORY_ID_REDACTED: <label>]` |
| Secrets paths under `~/.secrets/` | `[SECRET_PATH_REDACTED]` |
| Internal Tailscale IPs | `[INTERNAL_NETWORK_IP_REDACTED]` |
| Internal cloudflared domains | `[INTERNAL_DOMAIN_REDACTED]` |
| Family-relationship semantics | `[FAMILY_CONTEXT_REMOVED]` |
| Ambassador-friend real names | `[FRIEND_NAME_REDACTED]` |
| Researcher / principal real names | `[NONPUBLIC_CONTACT_REDACTED #N]` (stable per-name numbering) |
| Personal-migration content (extraction status, BDSM-decoupling, relocation) | `[PRIVATE_MIGRATION_CONTEXT_REMOVED]` |
| Owner personal email addresses | `[CONTACT_EMAIL_REDACTED]` |

Full unredacted trace is available via request to the contact email listed in the
main paper. Approval is per-applicant.

Counter assignment summary (deterministic, stable across runs):
- `[NONPUBLIC_CONTACT_REDACTED #1]` — res-htx
- `[NONPUBLIC_CONTACT_REDACTED #2]` — res-zx
- `[NONPUBLIC_CONTACT_REDACTED #3]` — res-seohong
- `[NONPUBLIC_CONTACT_REDACTED #4]` — res-samir
- `[NONPUBLIC_CONTACT_REDACTED #5]` — res-dutao
- `[NONPUBLIC_CONTACT_REDACTED #6]` — res-longge
- `[NONPUBLIC_CONTACT_REDACTED #7]` — res-yujie
- `[NONPUBLIC_CONTACT_REDACTED #8]` — res-dongki
- `[NONPUBLIC_CONTACT_REDACTED #9]` — res-shaoxiong
- `[NONPUBLIC_CONTACT_REDACTED #10]` — res-dingming
- `[NONPUBLIC_CONTACT_REDACTED #11]` — res-fujie
- `[NONPUBLIC_CONTACT_REDACTED #12]` — res-yuanxingyuan
- `[NONPUBLIC_CONTACT_REDACTED #13]` — res-daxiao
