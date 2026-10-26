# StarWars Mobile App - QA Test Assessment & Engineering Deliverables

[![Node.js QA Suite](https://img.shields.io/badge/QA%20Suite-32%20Tests%20Passing-brightgreen)]()
[![Test Cases](https://img.shields.io/badge/Test%20Cases-60%20Executed-blue)]()
[![Defects Logged](https://img.shields.io/badge/Defects-19%20Documented-red)]()
[![Traceability](https://img.shields.io/badge/RTM-100%25%20Traceability-success)]()

Comprehensive Quality Assurance evaluation of the **StarWars Mobile Application** (React Native & StarWars API) conducted in accordance with the official **Junior QA Engineer Coding Assignment**.

---

## 📋 Executive Overview & Deliverables

| Deliverable | In-Browser View | Raw Excel Workbook | Description |
| :--- | :---: | :---: | :--- |
| **QA Test Report** | **[📖 QA_TEST_REPORT.md](QA_TEST_REPORT.md)** | — | Complete technical audit report: Strategy, RTM, Usability Heuristics, Resource Performance Profiling, OWASP Security Audit, Usability Study Plan, and Regression Strategy. |
| **QA Test Cases (60 Scenarios)** | **[🔍 View Online (TEST_CASES.md)](TEST_CASES.md)** | **[📥 Download .xlsx](StarWars_QA_Test_Cases.xlsx?raw=true)** | 60 test cases covering Functional, Boundary, Compatibility, and Security domains with 100% RTM traceability. |
| **QA Defect Report (19 Bugs)** | **[🐞 View Online (BUG_REPORT.md)](BUG_REPORT.md)** | **[📥 Download .xlsx](StarWars_QA_Bug_Report.xlsx?raw=true)** | 19 unique defects (15 Functional/UX/Performance + 4 Security Vulnerabilities) with severity, reproduction steps, code evidence, and developer fixes. |
| **Automated QA Suite** | **[`qa-test-suite/`](qa-test-suite/)** | — | Lightweight Node.js test harness verifying validation logic, negative input boundaries, i18n translation parity, and OWASP security configurations. |
| **Traceability Audit Engine** | **[`audit_traceability.py`](audit_traceability.py)** | — | Zero-dependency verification engine guaranteeing 100% bidirectional traceability between test cases and defects. |

---

## 🎯 Requirements Coverage (Functionalities 1 – 13)

| Req # | Functionality Description | Evaluation Status | Core Findings |
| :---: | :--- | :---: | :--- |
| **1** | Register new users & passwords | **DEFECT** | Regex validates credentials, but denying location locks user email permanently (**DEF-01**). Missing input bounds (**DEF-09**). |
| **2** | Camera or image library photo upload | **DEFECT** | Photo gallery upload is completely missing (**DEF-02**). Camera permission false-negative bug (**DEF-14**). |
| **3** | Login with registered email & password | **DEFECT** | Mandatory GPS blocks login if denied (**DEF-04**). Login needlessly re-evaluates creation password regex (**DEF-15**). |
| **4** | SWAPI character particulars (height, mass, etc.) | **PASS** | Particulars render accurately from SWAPI role object. (Minor landscape column spacing flaw **DEF-12**). |
| **5** | Create group & bidirectional invitations | **PASS** | Luke invites Vader & Vader invites Luke both succeed in local storage. |
| **6** | In-app notifications of invitations | **PASS (Local)** | Local banner notification triggers and focuses "Unjoined Group" tab upon login. |
| **7** | Joining invited groups | **DEFECT** | Join button disappears when switching app language to Indonesian (`ID`) (**DEF-05**). |
| **8** | Group profile joined users & GPS map | **DEFECT** | `<MapView>` is commented out in code due to missing API key (**DEF-06**). Only raw coordinate text shown. |
| **9** | Starship specs via SWAPI | **DEFECT (Search)** | Starship particulars display, but search fails on static mirror without client filtering (**DEF-03**). |
| **10** | Adobe XD design specifications adherence | **PARTIAL** | General layouts align, but right-aligned inputs with chevrons (**DEF-10**) and phantom empty scroll (**DEF-13**). |
| **11** | Reasonable authentication & security | **CRITICAL DEFECT** | Plaintext password storage in MMKV (**SEC-01**). Insecure release signing with debug key (**SEC-04**). |
| **12** | Orientation & device compatibility (Phone/Tablet) | **DEFECT** | Frozen window metrics distort pie charts on rotation (**DEF-07**). Missing ScrollView causes screen lock (**DEF-08**). |
| **13** | Internationalization (I18n) and Localization (L10n) | **PARTIAL** | Dictionaries have 100% key parity, but UI button rendering breaks under Indonesian locale (**DEF-05**). |

---

## 🔬 Testing Modalities (Task Description Coverage)

1. **Functional Testing:** Verified all 13 core business requirements, registration workflows, group lifecycles, and invitation states.
2. **Compatibility Testing:** Evaluated portrait vs. landscape responsiveness, tablet viewport scaling, and iOS/Android permission divergences.
3. **Usability (UX) Testing:** Conducted heuristic evaluation based on Nielsen Norman Group Heuristics (visibility of system status, user control, error prevention, consistency).
4. **Performance Testing:** Profiled Base64 in-memory image serialization overhead, high-accuracy GPS battery polling, and FlatList rendering jank.
5. **Security Testing:** Mapped application attack surface against OWASP Mobile Top 10 (2024) (CWE-312 plaintext storage, hardcoded secrets, ATS transport security, release keystore signing).

---

## 🚀 How to Run the Automated Test Suite

### Prerequisites
* **Node.js**: v18.0.0 or higher (no external npm dependencies required; uses standard Node.js libraries).
* **Python**: v3.8 or higher (optional, for running Excel traceability audits).

### 1. Run Master Automated QA Suite
From the repository root:
```bash
node qa-test-suite/runner.js
```
*Executes all 32 tests in ~1.3 seconds across:*
* Authentication & credential complexity validation
* Negative boundary & missing input matrix
* I18n translation key parity (`en.json` vs `id.json`)
* OWASP Mobile Top 10 static security audit
* Live StarWars API (SWAPI) contract & pagination checks

### 2. Run Individual Test Modules
```bash
# Authentication & Regex Validation
node -e "const { runAuthValidationTests } = require('./qa-test-suite/auth_validation.test'); console.log(runAuthValidationTests());"

# Negative Input Boundary Matrix
node qa-test-suite/missing_inputs_test.js

# Translation Dictionary Parity
node -e "const { runI18nParityTests } = require('./qa-test-suite/i18n_parity.test'); console.log(runI18nParityTests());"

# OWASP Security Configuration Audit
node -e "const { runSecurityAuditTests } = require('./qa-test-suite/security_audit.test'); console.log(runSecurityAuditTests());"

# Live SWAPI Contract Tests
node -e "const { runSwapiApiTests } = require('./qa-test-suite/swapi_api.test'); runSwapiApiTests().then(console.log);"
```

### 3. Verify 100% Test Case & Defect Traceability
To verify that every test case in `StarWars_QA_Test_Cases.xlsx` maps 1-to-1 with `StarWars_QA_Bug_Report.xlsx`:
```bash
python audit_traceability.py
```
*Outputs: 60 Test Cases, 19 Unique Defects, 100% Traceability, 0 duplicates.*

---

## 📌 Optional Deliverables Included in Report

* **Section 7 of QA Test Report:** Detailed Usability Testing Setup Plan (10 participants: 5 internal + 5 external, task scenarios, TCR, TOT, and SUS evaluation metrics).
* **Section 8 of QA Test Report:** 3-Tier Regression Testing Strategy (Detox E2E, React Native Testing Library component tests, Unit/Contract tests in CI/CD pipeline).
* **Section 9 of QA Test Report:** Action plan for developer bug remediation.
