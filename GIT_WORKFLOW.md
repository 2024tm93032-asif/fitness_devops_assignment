# ACEest Fitness & Gym Management System - DevOps Pipeline

## Version Control Strategy

### Branching Strategy
- **main**: Production-ready code
- **develop**: Development branch for integration
- **feature/**: Feature branches (feature/user-auth, feature/workout-tracking)
- **release/**: Release preparation branches (release/v1.0.0)
- **hotfix/**: Emergency fixes for production (hotfix/login-bug)

### Commit Message Convention
Format: `<type>(<scope>): <subject>`

Types:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tool changes
- **ci**: CI/CD pipeline changes

Examples:
```
feat(auth): add user registration endpoint
fix(workout): correct calorie calculation
docs(readme): update setup instructions
test(api): add workout endpoint tests
ci(jenkins): configure automated deployment
```

### Git Workflow

1. **Feature Development**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/feature-name
   # Make changes
   git add .
   git commit -m "feat(scope): description"
   git push origin feature/feature-name
   # Create Pull Request to develop
   ```

2. **Release Process**
   ```bash
   git checkout develop
   git checkout -b release/v1.x.x
   # Update version numbers
   git commit -m "chore(release): prepare v1.x.x"
   git checkout main
   git merge release/v1.x.x
   git tag -a v1.x.x -m "Release version 1.x.x"
   git push origin main --tags
   git checkout develop
   git merge release/v1.x.x
   git push origin develop
   ```

3. **Hotfix**
   ```bash
   git checkout main
   git checkout -b hotfix/issue-description
   # Fix the issue
   git commit -m "fix(scope): description"
   git checkout main
   git merge hotfix/issue-description
   git tag -a v1.x.y -m "Hotfix version 1.x.y"
   git push origin main --tags
   git checkout develop
   git merge hotfix/issue-description
   git push origin develop
   ```

### Version Tagging
- Use semantic versioning: MAJOR.MINOR.PATCH
- Tag format: `v1.0.0`, `v1.0.1`, `v1.1.0`
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Setup Instructions

1. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "chore: initial commit"
   ```

2. **Connect to Remote**
   ```bash
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```

3. **Create develop branch**
   ```bash
   git checkout -b develop
   git push -u origin develop
   ```

4. **Protect main and develop branches** (on GitHub)
   - Settings > Branches > Add rule
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

### Pre-commit Hooks (Optional)
Create `.git/hooks/pre-commit`:
```bash
#!/bin/sh
# Run tests before commit
pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```
