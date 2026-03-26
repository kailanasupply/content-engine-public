# archive/

Processed input files and evergreen content candidates.

## Structure

```
archive/
├── YYYY-MM/                    ← Monthly folders. Files moved here after processing.
│   └── YYYY-MM-DD-[filename]  ← Date-prefixed processed inputs
└── evergreen-candidates/       ← Ideas flagged as evergreen during processing
    └── YYYY-MM-DD-[slug]-[EVERGREEN].md
```

## How files get here

1. After `/process-input` or `/morning-scan` → raw inputs archived to `archive/YYYY-MM/`
2. During archiving, evergreen items get a copy in `archive/evergreen-candidates/`
3. The evergreen miner scans `archive/evergreen-candidates/` for repurpose candidates

## What NOT to put here

Published content goes to `output/[client]/[channel]/`, not archive.
