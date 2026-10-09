# Two-minute demo script

**0:00–0:12 — Opening**
“Meet PatchPilot, a review-first coding agent. It helps turn a bug report into a proposed fix and test plan, while keeping code execution in the developer’s hands.”

**0:12–0:30 — Problem and setup**
Show the app and sidebar. “PatchPilot uses NVIDIA Nemotron through Nebius Token Factory. I’ve configured the model and supplied the API key as a secret.” Do not reveal the key.

**0:30–0:50 — Input**
Choose “Python: broken lookup.” Show the invalid `=` in the conditional. Set the request to “Fix the syntax bug and suggest a test for finding a user by ID.”

**0:50–1:05 — Run**
Click “Analyze, patch & test.” Show the loading state. Narrate: “The task and code go to the configured Nemotron model; the app asks for structured findings, replacement code, and test suggestions.”

**1:05–1:35 — Review the result**
Show findings and patch. Point out the corrected comparison `==`. Open Tests and Diff. “These are suggestions to inspect—not evidence that tests were run.”

**1:35–1:50 — Safety**
Show the safety note and download button. “PatchPilot never executes generated code. I review the patch and run it in a sandbox separately.”

**1:50–2:00 — Close**
“PatchPilot: review first, ship with confidence. Built with NVIDIA Nemotron and Nebius Token Factory.” Show repository and live demo links if available.

## Recording checklist
Use an actual running app and valid API key. Capture the real model response; avoid fake test-pass indicators and hide credentials. Keep YouTube/Vimeo video public or unlisted and under two minutes.
