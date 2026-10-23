# StarWars App - Automated QA Test Suite

This directory contains the automated QA test suite created for the **Junior QA Engineer Coding Assignment (StarWars App)**.

## Overview
The suite provides automated test coverage for:
1. **Authentication & Credential Validation**: Verifies assignment test accounts (Luke Skywalker, Darth Vader), regex patterns, boundary cases, and edge cases.
2. **I18n & L10n Localization Parity**: Verifies 100% key and parameter parity between English (`en.json`) and Indonesian (`id.json`).
3. **OWASP Mobile Security & Configuration Audit**: Scans Android & iOS manifests, build configurations, and storage mechanisms for OWASP Mobile Top 10 vulnerabilities (CWE-312 plaintext storage, hardcoded secrets, insecure ATS, release signing).
4. **SWAPI Integration & Contract Testing**: Verifies live Star Wars API schemas (`/people`, `/starships`) and uncovers defects with static mirror query filtering and pagination.

---

## Prerequisites
- **Node.js**: v18.0.0 or higher (no external npm dependencies required; uses standard Node.js libraries).

---

## How to Run the Tests

### 1. Run the Entire QA Test Suite (Master Runner)
From the repository root or within this directory:
```bash
node qa-test-suite/runner.js
```
Or if inside the `qa-test-suite` folder:
```bash
cd qa-test-suite
node runner.js
```

### 2. Run Individual Test Modules
You can also run specific test categories individually:

- **Authentication & Validation Test**:
  ```bash
  npm run test:auth
  # or
  node -e "const { runAuthValidationTests } = require('./auth_validation.test'); console.log(runAuthValidationTests());"
  ```

- **Localization (I18n) Parity Test**:
  ```bash
  npm run test:i18n
  # or
  node -e "const { runI18nParityTests } = require('./i18n_parity.test'); console.log(runI18nParityTests());"
  ```

- **Security & Config Audit**:
  ```bash
  npm run test:security
  # or
  node -e "const { runSecurityAuditTests } = require('./security_audit.test'); console.log(runSecurityAuditTests());"
  ```

- **Live SWAPI Contract & Defect Verification**:
  ```bash
  npm run test:swapi
  # or
  node -e "const { runSwapiApiTests } = require('./swapi_api.test'); runSwapiApiTests().then(console.log);"
  ```

---

## Test Suite Architecture
```
qa-test-suite/
├── auth_validation.test.js     # Validates Luke & Vader credentials, password complexity, email regex
├── i18n_parity.test.js         # Validates en.json and id.json key sync and {{count}} variables
├── security_audit.test.js      # Static analysis for OWASP Mobile Top 10 flaws
├── swapi_api.test.js           # SWAPI contract validation and static mirror defect detection
├── runner.js                   # Master CLI runner with colored status output & execution metrics
├── package.json                # Project manifest and test scripts
└── README.md                   # Instructions and documentation
```
