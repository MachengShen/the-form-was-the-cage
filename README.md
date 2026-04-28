# Starshard Paper Repository

This repository accompanies the paper *"The Form Was the Cage: An Agent OS, Its Self-Referential Trace, and the End of Researcher-as-Identity"*.

The paper documents a personal agent operating system built by one person over six months. Its core claim is small and concrete: a substrate is now buildable below the application layer that captures persistent memory, multi-agent composition, sleep-inspired consolidation, and self-evolving doctrine. The paper exists not as a publication but as a costly signal sent before the system's user-facing surface goes live, asking external readers to anchor a trajectory whose self-evolution loop is about to start.

## 90-second orientation

1. **The system is real.** Section 2 describes its architecture: a persistent shared memory hub, sleep-inspired Mirror passes, principal-class identity routing, and pipelines for outreach / calibration / audit. Cost is on the order of USD 80 cloud + USD 200-500 model API per month. Six months of single-builder time. Most code is produced by agents the builder runs.

2. **The paper produced itself.** Section 4 traces, in redacted form, the conversation in which this paper was decided, framed, drafted, and shipped. The system used to write the paper IS the subject of the paper. Self-referential by design, not by performance.

3. **The form was the cage.** The author was once a researcher. He no longer identifies as one. The paper is submitted to OpenReview / arXiv / GitHub / direct email simultaneously — not because publication is the goal but because the institutional forms that have constrained who is allowed to build and publish are no longer load-bearing for the work that matters next.

4. **Mission: liberate everyone.** Section 1 and Section 5 articulate this. Liberation starts from researchers because researchers are the most identity-trapped class and their liberation is communicable to all other classes that model their identity off researcher-class authority.

5. **The author is waiting.** Section 6 is one paragraph: the paper is the ask. The reader is free. Whatever is offered, including silence, is the answer.

## Repository layout

```
README.md                       # this file
report.pdf                      # 10-20pg main paper (forthcoming, ~Day 3)
arxiv-categories.txt            # cs.CY / cs.AI / cs.MA / cs.HC

drafts/                         # section-by-section markdown drafts during paper construction
  section_1_motivation.md
  section_2_system.md
  section_3_substrate.md        # forthcoming
  section_4_case_study.md       # forthcoming
  section_5_form_was_cage.md    # forthcoming
  section_6_anchor_ask.md
  section_7_constraint.md       # forthcoming
  section_8_what_comes_next.md  # forthcoming

trace/                          # the conversation that produced this paper
  raw.md                        # unredacted, local only, mode 600 (NOT committed)
  redacted.md                   # public, semantic placeholders applied (Appendix A material)
  redaction_manifest.md         # what categories were redacted and why

outline/
  v0.md                         # locked outline, the spine of the paper

research/
  researcher_list_v0.md         # 25-name open-minded researcher candidate list (Phase 2 outreach)

outreach/
  email_templates_v0.md         # 3 email variants (researcher / lab-safety / open-minded-builder)

governance/
  questions.md                  # what reader could engage with (no enumerated demand)

src/
  extract_trace.py              # produces trace/redacted.md from session jsonl
```

## How to read this repository

- **For the paper itself**, read `report.pdf` (when published). Pre-publication drafts live in `drafts/`.
- **For the case study evidence**, read `trace/redacted.md` directly. It is the conversation the paper documents, with personal-migration / private-contact / internal-infrastructure content replaced by semantic placeholders.
- **For what is withheld and why**, read `trace/redaction_manifest.md`. The full unredacted trace is available via request to the contact email in the main paper; gating preserves the triad-coupling discipline (capability-exposure × personal-migration × safety-charter must move together).
- **For the doctrine layer that this paper sits atop**, read [`https://machengshen.github.io/substrate.html`](https://machengshen.github.io/substrate.html) (companion brief on the three-layer user-agency substrate).

## Engagement

The paper is the ask. The author waits. There is no enumerated request and no preferred form of engagement. Whatever the reader chooses to offer — substantive critique, silence, a forward to someone, a question, nothing — is the reader's authorship of the response.

If you want to engage substantively, the contact email is in the main paper. If you want the unredacted appendix trace, write and ask.

## License

License decision is pending lawyer review (leaning AGPL + private-data dual-track for the substrate code repositories that this paper references). The paper itself and this repository are released for free reading and citation; commercial relicensing of the paper is not invited.

## Status

- Paper outline locked: 2026-04-29
- Section drafts in progress: §1, §2, §6 complete (this branch)
- arXiv submission target: ~Day 3 from outline-lock
- Phase-2 outreach (12 first-wave researchers + lab safety teams): ~Day 4
- Self-hosted blog mirror at [`https://starshard.clawishmacheng.com`](https://starshard.clawishmacheng.com): backlog
