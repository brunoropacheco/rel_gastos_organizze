---
project_name: 'rel_gastos_organizze'
user_name: 'Bruno'
date: '2026-06-04'
sections_completed: ['technology_stack', 'language_rules', 'critical_rules', 'usage_guidelines']
status: 'complete'
rule_count: 15
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Python:** 3.x
- **Data Manipulation:**
    - `pandas` (v2.2.3)
    - `numpy` (v2.2.4)
- **APIs & Integration:**
    - `google-api-python-client` (v2.194.0) - Google Drive v3, Google Sheets v4
    - `requests` (v2.32.3) - Organizze REST v2
    - `smtplib` (Native) - Email reporting
- **Utilities:**
    - `python-dateutil` (v2.9.0.post0)
    - `httpx` (v0.28.1)
    - `PyYAML` (v6.0.3)
- **Environment Management:**
    - `os.environ` for credentials and tokens.

## Critical Implementation Rules

### Language-Specific Rules (Python)

- **Naming Conventions:** Use `snake_case` for functions and variables. The project uses a hybrid naming scheme (English and Portuguese); maintain consistency with existing names in the same module.
- **Documentation:** **Mandatory** docstrings in Portuguese for all functions, detailing arguments and return values.
- **Data Formatting:** Use `f-strings` for string interpolation.
- **Character Normalization:** Always normalize strings (lowercase, remove accents, replace spaces/hyphens with underscores) before using them for categorization or comparison.

### Critical Don't-Miss Rules & Anti-Patterns

- **Credential Security:** NEVER hardcode tokens or passwords. Use `os.environ.get()` for `TOKEN_ORGANIZZE`, `PASSWORD_GMAIL`, and `GOOGLE_DRIVE_CREDENTIALS`.
- **Manual Installment Management:** Be aware that the Organizze API does not automatically move future installments. Logic affecting installments must document that manual movement in the Organizze app is required.
- **Data Filtering:**
    - Always filter out `deb._autom._de_fatura` from descriptions.
    - Ignore transactions marked with "ignorar" in the notes field (case-insensitive).
- **Fallback Logic:** If Google Sheets authentication or data retrieval fails, the system **must** use the hardcoded default limits dictionary.
- **Duplicate Handling:** When merging transaction data, remove duplicates based on `description`, `date`, and `amount_cents`, keeping the most recent entry.

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code.
- Follow ALL rules exactly as documented.
- When in doubt, prefer the more restrictive option.
- Update this file if new patterns emerge.

**For Humans:**

- Keep this file lean and focused on agent needs.
- Update when technology stack changes.
- Review quarterly for outdated rules.
- Remove rules that become obvious over time.