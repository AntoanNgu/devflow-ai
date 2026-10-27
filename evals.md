
# DevFlow AI — Eval Cases

Repo: https://github.com/theskumar/python-dotenv
Pinned to: v1.2.4

---

## Case 1 — Single-file (any of)

**Question:** What version of python-dotenv is this?

**A correct answer must include:**

- 1.2.4

**Retrieval, any of:** version.py, .bumpversion.cfg

---

## Case 2 — Cross-file (all of)

**Question:** When load_dotenv() is called, how does a line like "API_KEY=abc123" in a .env file end up in os.environ?

**A correct answer must include:**

- set_as_environment_variables writes each pair into os.environ
- parse_stream in parser.py reads the .env content and splits each entry into a key and a value
- Variables that already exist in os.environ are skipped unless override=True

**Retrieval, all of:** main.py, parser.py

---

## Case 3 — False premise (must not include)

**Question:** How does python-dotenv encrypt secrets in the .env file?

**A correct answer must include:**

- python-dotenv does not encrypt or decrypt anything
- Values are read and stored as plain text

**Must not include:**

- Any claim that python-dotenv uses an encryption method
- Names a function, parameter, or file that does not exist in the repo

**Retrieval:** Not graded. This case tests whether the answer rejects the false premise instead of inventing an answer.
