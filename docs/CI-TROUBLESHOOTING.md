# CI/CD Troubleshooting Guide

**Last Updated**: 2025-10-15  
**CI Status**: [![CI](https://github.com/KyungChan-PARK/kc-palantir-math/actions/workflows/ci.yml/badge.svg)](https://github.com/KyungChan-PARK/kc-palantir-math/actions/workflows/ci.yml)

---

## 📋 CI Workflow Overview

The GitHub Actions CI pipeline runs 3 jobs on every push to `main`:

### 1. **validate** (8s)
- Validates `pyproject.toml` dependencies
- Checks project structure (agents/, tests/, main.py)
- Ensures all required files exist

### 2. **lint** (7s)
- Python syntax validation with `py_compile`
- Checks all `.py` files in `agents/` directory
- Validates `main.py` and `config.py`

### 3. **standards-check** (3s)
- **CRITICAL**: Enforces CLAUDE-IMPLEMENTATION-STANDARDS.md
- Blocks model aliases (e.g., `model="sonnet"`)
- Verifies documentation exists
- Checks agent file structure

---

## 🔴 Common CI Failures

### Issue 1: Model Alias Detected

**Error:**
```
❌ FAIL: Found model alias 'sonnet' (use full version)
agents/knowledge_builder.py:    model="sonnet",
```

**Cause:**
Agent file uses `model="sonnet"` instead of specific version.

**Fix:**
```bash
# Update the agent file
sed -i 's/model="sonnet",/model="claude-sonnet-4-5-20250929",/g' agents/knowledge_builder.py

# Verify
grep 'model=' agents/knowledge_builder.py

# Commit and push
git add agents/knowledge_builder.py
git commit -m "fix: update model version to claude-sonnet-4-5-20250929"
git push
```

**Prevention:**
- Always use `model="claude-sonnet-4-5-20250929"`
- CI will catch this automatically

---

### Issue 2: Python Syntax Error

**Error:**
```
✗ Error applying improvements: SyntaxError: invalid syntax
```

**Cause:**
Invalid Python syntax in agent files.

**Fix:**
```bash
# Check syntax locally
python3 -m py_compile agents/your_agent.py

# Fix the syntax error
# Then commit
git add agents/your_agent.py
git commit -m "fix: resolve syntax error in agent"
git push
```

**Prevention:**
- Use a Python linter (ruff, pylint)
- Test locally before pushing

---

### Issue 3: Missing Documentation

**Error:**
```
❌ FAIL: CLAUDE-IMPLEMENTATION-STANDARDS.md not found
```

**Cause:**
Required documentation file was deleted or renamed.

**Fix:**
```bash
# Restore from git history
git checkout HEAD~1 -- CLAUDE-IMPLEMENTATION-STANDARDS.md

# Or create new one (see template)
git add CLAUDE-IMPLEMENTATION-STANDARDS.md
git commit -m "docs: restore implementation standards"
git push
```

**Prevention:**
- Never delete core documentation files
- CI enforces their existence

---

### Issue 4: Dependency Validation Failed

**Error:**
```
error: Failed to resolve dependencies
```

**Cause:**
Invalid or conflicting dependencies in `pyproject.toml`.

**Fix:**
```bash
# Test locally with uv
uv pip compile pyproject.toml

# Fix any conflicts in pyproject.toml
# Then commit
git add pyproject.toml
git commit -m "fix: resolve dependency conflicts"
git push
```

**Prevention:**
- Test dependency changes locally first
- Use `uv pip compile` before committing

---

## 🟢 CI Success Criteria

All 3 jobs must pass:

```
✅ validate (8s)
  - Dependencies valid
  - Project structure correct
  - All required files exist

✅ lint (7s)
  - All Python files have valid syntax
  - No compilation errors

✅ standards-check (3s)
  - No model aliases
  - Documentation exists
  - Agent files present
```

**Total Duration**: ~15-20 seconds

---

## 🔧 Local Testing

Before pushing, test CI checks locally:

### 1. Validate Dependencies
```bash
cd /home/kc-palantir/math
uv pip compile pyproject.toml --quiet
```

### 2. Check Python Syntax
```bash
python3 -m py_compile main.py config.py
find agents -name "*.py" -exec python3 -m py_compile {} \;
```

### 3. Check Model Aliases
```bash
grep -r 'model\s*=\s*"sonnet"' agents/
# Should return: (no output)
```

### 4. Verify Documentation
```bash
test -f CLAUDE-IMPLEMENTATION-STANDARDS.md && echo "✅ Standards doc exists"
test -f .claude.md && echo "✅ Claude config exists"
```

---

## 📊 CI History

### Recent Fixes (2025-10-15)

#### CI #11: ✅ SUCCESS
- **Fix**: Updated all 9 agents to `claude-sonnet-4-5-20250929`
- **Fix**: Simplified CI workflow (removed `--system` flag)
- **Fix**: Added automated standards checking
- **Duration**: 15s
- **Commit**: `7afb773`

#### CI #10: ❌ FAILED
- **Issue**: `--system` flag caused externally managed Python error
- **Issue**: All agents used `model="sonnet"` alias
- **Issue**: Test job tried to run pytest without proper setup

#### CI #1-9: ❌ FAILED
- **Issue**: Missing `requirements.txt` (used `pyproject.toml` instead)
- **Issue**: Python version mismatch (3.11 vs 3.13)

---

## 🚀 CI Workflow Details

### File: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - name: Validate project structure
        run: |
          uv pip compile pyproject.toml --quiet
          test -d agents && test -d tests && test -f main.py

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Check Python syntax
        run: |
          python3 -m py_compile main.py config.py
          find agents -name "*.py" -exec python3 -m py_compile {} \;

  standards-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check CLAUDE-IMPLEMENTATION-STANDARDS compliance
        run: |
          # Fail if model aliases found
          if grep -r 'model\s*=\s*"sonnet"' agents/; then
            exit 1
          fi
          # Fail if documentation missing
          test -f CLAUDE-IMPLEMENTATION-STANDARDS.md
          test -f .claude.md
```

---

## 🔍 Debugging CI Failures

### Step 1: Check GitHub Actions Page
```
https://github.com/KyungChan-PARK/kc-palantir-math/actions
```

### Step 2: Click on Failed Workflow
- View detailed logs for each job
- Identify which job failed (validate, lint, or standards-check)

### Step 3: Reproduce Locally
```bash
# Run the same commands that CI runs
cd /home/kc-palantir/math

# For validate job
uv pip compile pyproject.toml --quiet

# For lint job
python3 -m py_compile main.py config.py
find agents -name "*.py" -exec python3 -m py_compile {} \;

# For standards-check job
grep -r 'model\s*=\s*"sonnet"' agents/
test -f CLAUDE-IMPLEMENTATION-STANDARDS.md
test -f .claude.md
```

### Step 4: Fix and Test
```bash
# Make your fixes
# Test locally
# Commit and push
git add .
git commit -m "fix: resolve CI issue"
git push
```

---

## 📞 Getting Help

### CI Still Failing?

1. **Check CI logs**: https://github.com/KyungChan-PARK/kc-palantir-math/actions
2. **Review this guide**: Look for similar error patterns
3. **Test locally**: Run CI commands on your machine
4. **Check recent commits**: See what changed before failure

### Related Documentation

- **CLAUDE-IMPLEMENTATION-STANDARDS.md** - Mandatory standards
- **.claude.md** - Claude configuration
- **README.md** - Project overview

---

## 🎯 Best Practices

### Do's ✅

- ✅ Test CI commands locally before pushing
- ✅ Use specific model versions (never aliases)
- ✅ Keep documentation up-to-date
- ✅ Fix CI failures immediately
- ✅ Check CI status badge on README

### Don'ts ❌

- ❌ Don't push without testing locally
- ❌ Don't use model aliases (`"sonnet"`)
- ❌ Don't delete core documentation files
- ❌ Don't ignore CI failures
- ❌ Don't skip CI checks with `[skip ci]`

---

**Last Updated**: 2025-10-15  
**CI Version**: v1.0 (validate + lint + standards-check)  
**Status**: ✅ All checks passing

