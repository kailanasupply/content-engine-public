# /switch-brand
# Change the active brand and confirm the switch.
# Prevents silent errors from generating content for the wrong brand.
#
# Usage: /switch-brand [brand-name]
# Example: /switch-brand sayso
# Example: /switch-brand brian

---

## Step 1: Validate the brand name

Read `config/settings.yaml` to get all registered brands.

If the requested brand name is not in the brands list:
→ Report: "⚠ Brand '[name]' is not registered. Available brands: [list all registered brands]"
→ Stop

---

## Step 2: Check brand context completeness

Before switching, check if the target brand's context is complete:

Required files for full operation:
- `brand/[brand]/voice-personal.md` (if voice_profiles includes personal)
- `brand/[brand]/voice-company.md` (if voice_profiles includes company)
- `brand/[brand]/pillars.md`
- `brand/[brand]/personas.yaml`
- `brand/[brand]/messaging.md`
- `brand/[brand]/examples/personal/` (at least 1 file, if personal voice)
- `brand/[brand]/examples/company/` (at least 1 file, if company voice)

If required files have only placeholder content (contain "[" brackets from template):
→ Warn: "⚠ Brand '[name]' context is incomplete. Sections not yet filled: [list]"
→ Ask: "Switch anyway? Generation will produce generic output until brand context is completed. (yes / no)"
→ If no → don't switch

---

## Step 3: Execute the switch

Update `config/settings.yaml`:
- Change `active_client` to the requested brand name

---

## Step 4: Load and display brand summary

Load the new brand's context and display a summary:

```
✅ Switched to: [Brand Display Name]

Active channels:
  ✅ [channel 1]
  ✅ [channel 2]
  🚫 [blocked channel] — [reason]

Voice profiles available:
  [personal ✅ / ⚠ incomplete]
  [company ✅ / ⚠ incomplete]

Examples loaded:
  Personal: [n] examples
  Company: [n] examples

Cadence rules:
  [Format]: [frequency]
  [Format]: [frequency]
  🚫 [blocked format]: blocked

Brand context status: [Complete / ⚠ Incomplete — run /new-brand [brand] to finish setup]

Ready to generate. Run /morning-scan or /generate-campaign [file] to continue.
```

---

## Step 5: If switching to SaySo — display restrictions banner

If the new active brand is `sayso`, always display:

```
⚠️  SAYSO ACTIVE — CHANNEL RESTRICTIONS IN EFFECT

Active: X (Twitter) + Company LinkedIn ONLY
Blocked: Personal LinkedIn | Newsletter | Blog | Email sequences | Sales assets

All generation this session will only produce X posts and Company LinkedIn posts.
If you need newsletter or personal LinkedIn content, switch to a different brand first.
```

---

## Multi-brand morning scan note

The morning scan processes all active brands in sequence.
`/switch-brand` sets the focus for manual commands (generate-campaign, review-drafts, etc.).
The morning scan ignores `active_client` and uses `brands:` from settings.yaml directly.
