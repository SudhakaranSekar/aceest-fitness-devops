# ============================================================
#   ACEest Fitness - Git Version Setup Script
#   Run this from INSIDE your aceest_flask folder
#   Usage: powershell -ExecutionPolicy Bypass -File setup_git_versions.ps1
# ============================================================

# ── CHANGE THIS TO YOUR GITHUB USERNAME ──────────────────────
$GITHUB_USERNAME = "sudhakaran sekar"
# ─────────────────────────────────────────────────────────────

$REPO_NAME = "aceest-fitness-devops"
$REMOTE_URL = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   ACEest Fitness - Git Versioning Setup   " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── STEP 1: Check all version files exist ───────────────────
Write-Host "Checking version files in versions folder..." -ForegroundColor Yellow

$versionFiles = @(
    "versions\Aceestver-1.0.py",
    "versions\Aceestver-1.1.py",
    "versions\Aceestver1.1.2.py",
    "versions\Aceestver2.0.1.py",
    "versions\Aceestver-2.1.2.py",
    "versions\Aceestver-2.2.1.py",
    "versions\Aceestver-2.2.4.py",
    "versions\Aceestver-3.0.1.py",
    "versions\Aceestver-3.1.2.py",
    "versions\Aceestver-3.2.4.py"
)

$allFound = $true
foreach ($f in $versionFiles) {
    if (-Not (Test-Path $f)) {
        Write-Host "  MISSING: $f" -ForegroundColor Red
        $allFound = $false
    } else {
        Write-Host "  FOUND: $f" -ForegroundColor Green
    }
}

if (-Not $allFound) {
    Write-Host ""
    Write-Host "ERROR: Some version files are missing in the versions folder!" -ForegroundColor Red
    Write-Host "Make sure all .py files from the ZIP are inside the versions folder." -ForegroundColor Red
    exit 1
}

Write-Host "All version files found!" -ForegroundColor Green

# ── STEP 2: Initialize Git ───────────────────────────────────
Write-Host ""
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init
git remote add origin $REMOTE_URL

# ── Helper: write CHANGELOG entry ───────────────────────────
function Add-Changelog($version, $notes) {
    $entry = "`n## $version`n$notes`n"
    Add-Content -Path "CHANGELOG.md" -Value $entry
}

# ── STEP 3: v1.0 ────────────────────────────────────────────
Write-Host "Committing v1.0..." -ForegroundColor Yellow
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v1.0 - Initial Release`n- Basic client registration`n- SQLite database`n- Simple login system"
Set-Content "CHANGELOG.md" "# ACEest Fitness Changelog"
Add-Changelog "v1.0" "- Initial release`n- Basic client registration`n- SQLite database setup`n- Simple login system"
git add versions\Aceestver-1.0.py README.md CHANGELOG.md
git commit -m "v1.0 - Initial ACEest Fitness app with basic client management"
git tag -a v1.0 -m "Version 1.0 - Initial Release"
Write-Host "  v1.0 done" -ForegroundColor Green

# ── STEP 4: v1.1 ────────────────────────────────────────────
Write-Host "Committing v1.1..." -ForegroundColor Yellow
Add-Changelog "v1.1" "- Added workout session tracking`n- Improved login system`n- UI enhancements"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v1.1 - Workout Tracking`n- Workout session tracking added`n- Improved login"
git add versions\Aceestver-1.1.py README.md CHANGELOG.md
git commit -m "v1.1 - Added workout tracking and session management"
git tag -a v1.1 -m "Version 1.1 - Workout Tracking"
Write-Host "  v1.1 done" -ForegroundColor Green

# ── STEP 5: v1.1.2 ──────────────────────────────────────────
Write-Host "Committing v1.1.2..." -ForegroundColor Yellow
Add-Changelog "v1.1.2" "- Fixed login session bugs`n- UI improvements`n- Stability updates"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v1.1.2 - Bug Fixes`n- Login session bug fixes`n- UI improvements"
git add "versions\Aceestver1.1.2.py" README.md CHANGELOG.md
git commit -m "v1.1.2 - Bug fixes and UI improvements"
git tag -a v1.1.2 -m "Version 1.1.2 - Bug Fixes"
Write-Host "  v1.1.2 done" -ForegroundColor Green

# ── STEP 6: v2.0.1 ──────────────────────────────────────────
Write-Host "Committing v2.0.1..." -ForegroundColor Yellow
Add-Changelog "v2.0.1" "- Added full nutrition planning module`n- Diet recommendations by goal`n- Calorie tracking per client`n- New database tables for nutrition"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v2.0.1 - Nutrition Module`n- Full nutrition planning`n- Calorie tracking"
git add "versions\Aceestver2.0.1.py" README.md CHANGELOG.md
git commit -m "v2.0.1 - Major update: Added nutrition planning and diet module"
git tag -a v2.0.1 -m "Version 2.0.1 - Nutrition Module"
Write-Host "  v2.0.1 done" -ForegroundColor Green

# ── STEP 7: v2.1.2 ──────────────────────────────────────────
Write-Host "Committing v2.1.2..." -ForegroundColor Yellow
Add-Changelog "v2.1.2" "- Added weekly adherence tracking`n- Progress reports per client`n- Client goal setting"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v2.1.2 - Progress Tracking`n- Weekly adherence tracking`n- Progress reports"
git add "versions\Aceestver-2.1.2.py" README.md CHANGELOG.md
git commit -m "v2.1.2 - Added progress tracking and adherence metrics"
git tag -a v2.1.2 -m "Version 2.1.2 - Progress Tracking"
Write-Host "  v2.1.2 done" -ForegroundColor Green

# ── STEP 8: v2.2.1 ──────────────────────────────────────────
Write-Host "Committing v2.2.1..." -ForegroundColor Yellow
Add-Changelog "v2.2.1" "- Added body measurement tracking`n- Weight history logging`n- Waist and body fat tracking"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v2.2.1 - Body Metrics`n- Body measurement tracking`n- Weight history"
git add "versions\Aceestver-2.2.1.py" README.md CHANGELOG.md
git commit -m "v2.2.1 - Added body metrics and measurement tracking"
git tag -a v2.2.1 -m "Version 2.2.1 - Body Metrics"
Write-Host "  v2.2.1 done" -ForegroundColor Green

# ── STEP 9: v2.2.4 ──────────────────────────────────────────
Write-Host "Committing v2.2.4..." -ForegroundColor Yellow
Add-Changelog "v2.2.4" "- Database query optimizations`n- Faster data loading`n- Minor bug fixes"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v2.2.4 - Performance`n- Database optimizations`n- Bug fixes"
git add "versions\Aceestver-2.2.4.py" README.md CHANGELOG.md
git commit -m "v2.2.4 - Performance improvements and database optimizations"
git tag -a v2.2.4 -m "Version 2.2.4 - Performance Improvements"
Write-Host "  v2.2.4 done" -ForegroundColor Green

# ── STEP 10: v3.0.1 ─────────────────────────────────────────
Write-Host "Committing v3.0.1..." -ForegroundColor Yellow
Add-Changelog "v3.0.1" "- Full dashboard with charts`n- Data visualizations using matplotlib`n- Admin panel improvements`n- Multi-role user support"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v3.0.1 - Full Dashboard`n- Charts and visualizations`n- Admin panel"
git add "versions\Aceestver-3.0.1.py" README.md CHANGELOG.md
git commit -m "v3.0.1 - Major release: Full dashboard with charts and visualizations"
git tag -a v3.0.1 -m "Version 3.0.1 - Full Dashboard"
Write-Host "  v3.0.1 done" -ForegroundColor Green

# ── STEP 11: v3.1.2 ─────────────────────────────────────────
Write-Host "Committing v3.1.2..." -ForegroundColor Yellow
Add-Changelog "v3.1.2" "- Membership tracking added`n- Renewal date management`n- Payment status tracking"
Set-Content "README.md" "# ACEest Fitness & Gym`n`n## Version: v3.1.2 - Membership`n- Membership tracking`n- Renewal management"
git add "versions\Aceestver-3.1.2.py" README.md CHANGELOG.md
git commit -m "v3.1.2 - Added membership management and billing module"
git tag -a v3.1.2 -m "Version 3.1.2 - Membership Management"
Write-Host "  v3.1.2 done" -ForegroundColor Green

# ── STEP 12: v3.2.4 - FINAL FLASK VERSION ───────────────────
Write-Host "Committing v3.2.4 - Final Flask Version..." -ForegroundColor Yellow
Add-Changelog "v3.2.4" "- MAJOR: Converted Tkinter to Flask web app`n- REST API endpoints`n- Kubernetes /health endpoint`n- 18 Pytest unit tests`n- Dockerfile added`n- Jenkinsfile for CI/CD`n- SonarQube integration`n- Kubernetes 5 deployment strategies"

Set-Content "README.md" @"
# ACEest Fitness & Gym - v3.2.4 (Final)

## CI/CD Pipeline - DevOps Assignment (CSIZG514/SEZG514)

### Architecture
- **App**: Flask Web Application (Python)
- **Testing**: Pytest (18 test cases)
- **CI**: Jenkins Pipeline
- **Code Quality**: SonarQube
- **Containerization**: Docker
- **Registry**: Docker Hub
- **Orchestration**: Kubernetes (Minikube)

### Deployment Strategies
1. Rolling Update
2. Blue-Green Deployment
3. Canary Release
4. A/B Testing
5. Shadow Deployment

### How to Run
``````bash
pip install -r requirements.txt
python app.py
``````
Open: http://localhost:5000
Login: admin / admin

### Run Tests
``````bash
pytest test_app.py -v
``````

### Docker
``````bash
docker build -t aceest-fitness:v3.2.4 .
docker run -p 5000:5000 aceest-fitness:v3.2.4
``````
"@

git add .
git commit -m "v3.2.4 - Final Flask web app with complete CI/CD pipeline"
git tag -a v3.2.4 -m "Version 3.2.4 - Final Flask CI/CD Release"
Write-Host "  v3.2.4 done" -ForegroundColor Green

# ── STEP 13: Create branches ─────────────────────────────────
Write-Host ""
Write-Host "Creating branches..." -ForegroundColor Yellow
git checkout -b develop
git push origin develop
git checkout -b "feature/flask-conversion"
git push origin "feature/flask-conversion"
git checkout main
Write-Host "  Branches: main, develop, feature/flask-conversion" -ForegroundColor Green

# ── STEP 14: Push everything ─────────────────────────────────
Write-Host ""
Write-Host "Pushing to GitHub (enter your Personal Access Token when asked)..." -ForegroundColor Yellow
git push -u origin main
git push origin --tags

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ALL DONE!" -ForegroundColor Green
Write-Host ""
Write-Host "  Your GitHub repo:" -ForegroundColor White
Write-Host "  https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Pushed:" -ForegroundColor White
Write-Host "  10 real version commits" -ForegroundColor Green
Write-Host "  10 annotated tags (v1.0 to v3.2.4)" -ForegroundColor Green
Write-Host "  3 branches (main, develop, feature/flask-conversion)" -ForegroundColor Green
Write-Host "  README.md + CHANGELOG.md" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
