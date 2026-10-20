🇧🇷 [Português](SEGURANCA.md) · 🇬🇧 **English**

# Security policy

Crivo is a security tool — flaws in it can give a false sense of protection.

## How to report a vulnerability

**Do not open a public issue** for vulnerabilities. Use **"Report a vulnerability"** (the *Security* tab of this repository, *Private vulnerability reporting*).

Include:
- what happens and the impact (e.g., a pattern that makes the guard allow an installation without approval);
- steps to reproduce, with **harmless** examples;
- the version/commit of Crivo and of the agent used.

## What counts as a vulnerability

- Bypassing the guard (`trava.py`) with a common install command.
- Making the checker or the scan **execute** third-party content.
- Making Crivo send data out (beyond the optional email to the user themselves).
- Instructions in `SKILL.md` that lead the agent to skip the user's approval.

False negatives in the scan (a pattern it doesn't detect) are usually **improvements**, not vulnerabilities — open a regular issue with a harmless example.

## Known limits

See the "Limitations" section of the README. Crivo reduces risk; it does not replace a professional audit.
