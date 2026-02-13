# Contributing

Thanks for your interest in contributing! 🎉

---

## How to Contribute

### Report a Bug
1. Check [existing issues](../../issues) first.
2. Open a new issue and include:
   - Python version and OS
   - The command you ran
   - Expected vs actual output
   - Full error traceback

### Suggest a Feature
Open an issue describing:
- The problem it solves
- How you'd want to call it

### Submit a Pull Request

```bash
# 1. Fork and clone
git clone https://github.com/your-username/healthcare-data-pipeline.git
cd healthcare-data-pipeline

# 2. Create a branch
git checkout -b fix/your-fix-name

# 3. Make changes, then test
python scripts/generate_dataset.py
python scripts/clean_data.py
python scripts/health_report.py

# 4. Commit using conventional commits
git commit -m "fix: handle empty blood_pressure values"

# 5. Push and open a PR
git push origin fix/your-fix-name
```

---

## Commit Message Format

```
feat:     new feature
fix:      bug fix
docs:     documentation change
refactor: code change with no feature or fix
```

---

## Code Style

- Follow PEP 8
- Add a docstring to every function
- Keep functions short and single-purpose
