# Outreach Email Templates v0 — 3 variants

**Tone basis** per GPT-Pro v2: "I need one external anchor before this user-facing self-evolving system goes live. Can you give one concrete direction change, safety concern, or person who should see it?"

**Status**: 3 drafts. Macheng to pick tone or merge. NO send until pick + per-target customization.

---

## Variant A — Researcher (12 first-wave names)

**Subject**: An artifact you might find interesting

**Body**:

```
Hi {first_name},

I'm Macheng Shen. Over the last six months I built a personal agent operating system — persistent shared memory, sleep-inspired consolidation, multi-agent composition across an agentic IDE, a mobile agent, a non-Anthropic frontier-model bridge for calibration, and a small AWS fleet — that I've been using as the substrate for my own work.

The user-facing surface is about to go live. Before it does, I'm sending the artifact to a small number of people whose attention I respect.

- Repo + report: {github_url}
- arXiv: {arxiv_url}
- Self-referential trace: the paper was produced by the system using itself; redacted trace in appendix.

I'm not asking for anything specific. The paper is on the table. You are free to engage with it however you choose, including not at all.

Best,
Macheng
{personal_url}
```

**Customization per-target**: 
- {first_name}: as appropriate (Andrej / Jan / Lilian / etc.)
- 1-line specific hook: e.g. "Your post on LLM-OS framing was a load-bearing reference point during the build" (Karpathy); "The pre-deploy framing in [your paper / blog post] is exactly the question I'm trying to live up to" (Leike); etc.

---

## Variant B — Lab Safety Team

**Subject**: A pre-deploy artifact from outside your perimeter

**Body**:

```
Hi {team_or_individual},

I'm Macheng Shen, an independent builder. Over six months I've built a personal agent operating system with persistent shared memory, multi-agent composition, and a self-evolving doctrine layer. The user-facing surface is about to go live.

I'm forwarding the artifact ({github_url}) because pre-deploy timing matters more than after.

The artifact includes:
- A technical-and-governance report describing the system, its capabilities, and its six-month build trajectory.
- A "constraint manifest" — capabilities the system cannot reach by design, each tied to enforcement at the code or schema level.
- A self-referential trace: the paper was produced by the system using itself.

I'm not asking for anything specific. The paper is on the table. Whatever your team chooses to do with it — including nothing — is yours to choose.

Best,
Macheng Shen
{personal_url}
```

---

## Variant C — Open-minded Builder (Kanjun, Josh, Jim Fan, Karpathy as builder, Imbue-class)

**Subject**: One builder showing another what fell out of six months

**Body**:

```
Hi {first_name},

Independent builder. Six months on a personal agent OS — shared memory hub, sleep-inspired consolidation, multi-agent composition across an agentic IDE, mobile agent, a non-Anthropic frontier-model bridge for calibration, and a small AWS fleet. The system uses itself; this paper was produced by it, governance decisions and all.

User-facing surface is about to go live. The artifact is going out before that.

- {github_url}
- {arxiv_url}

Substrate-shaped, not application-shaped. {builder-specific hook, customize per recipient.}

Not a fundraising email, not a partnership pitch, not a job ask. The paper is on the table. You are free to do whatever you want with it.

Best,
Macheng
{personal_url}
```

---

## Operating rules

1. **Per-target 1-line custom hook** is mandatory — never send identical body
2. **Pre-send draft to Macheng** for first 5 sends per variant; after stable Macheng can authorize bulk send
3. **No follow-up ping if silent**: pull-based outreach doctrine (`mem_da454b258b96` C-plan v2 op rule); silence = drop, never re-ping. `mem_ed3bee4a333e` (pull-based outreach base) applies
4. **Reply handling**: route to macshen93@gmail.com inbox. Agent classifies (interested / declined / question / silence) via gmail-scan skill (`~/.claude/skills/gmail-scan/SKILL.md`) and queues Macheng's next move
5. **Logging**: every send → hub memo with `[researcher-N]` placeholder + send-date + message-hash + variant; full email kept private not in hub
6. **Cadence cap**: 8-12 day 4 + 10 day 5 = 18-22 total wave 1+2; subsequent waves require Macheng re-approval

## Cross-links

- `mem_dfe20f509f4b` — Researcher Seeding L0.5 doctrine (cold-pitch discipline parent)
- `mem_22e061909669` — open-mindedness selection
- `mem_672f37673a46` v3 — OpenReview pivot (parent project)
- `mem_c4e9264b9b7f` — Mission frame
- `~/projects/starshard-paper/research/researcher_list_v0.md` — target list this email goes to
