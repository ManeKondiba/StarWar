# StarWars Mobile App - QA Test Assessment & Engineering Deliverables

[![Node.js QA Suite](https://img.shields.io/badge/QA%20Suite-32%20Tests%20Passing-brightgreen)]()
[![Test Cases](https://img.shields.io/badge/Test%20Cases-60%20Executed-blue)]()
[![Defects Logged](https://img.shields.io/badge/Defects-26%20Documented-red)]()
[![Traceability](https://img.shields.io/badge/RTM-100%25%201%3A1%20Traceability-success)]()
[![Release Status](https://img.shields.io/badge/Release%20Status-NOT%20READY%20(Fixes%20Required)-orange)]()

Comprehensive Quality Assurance evaluation of the **StarWars Mobile Application** (React Native & StarWars API) conducted in accordance with the official **Junior QA Engineer Coding Assignment**.

---

## 📌 Critical Repository Notice
> **IMPORTANT FOR REVIEWERS:**  
> This repository contains **QA deliverables, test documentation, test matrices, defect logs with evidence, and helper automation scripts**.  
> The original mobile application source code provided by the company is hosted in the official company repository:  
> 🔗 **Original Application Repository:** [https://github.com/worlderteam/StarWarsApp](https://github.com/worlderteam/StarWarsApp)  
> *Do not assume this QA repository is the application source code.*

---

## 📋 Master QA Deliverables & Documentation Index

| Deliverable | In-Browser Markdown | Raw Excel Workbook / Asset | Description |
| :--- | :---: | :---: | :--- |
| **Comprehensive QA Test Report** | **[📖 QA_TEST_REPORT.md](QA_TEST_REPORT.md)** | — | Complete 18-section technical audit report: Strategy, RTM, Usability Heuristics, Resource Performance Profiling, OWASP Security Audit, Usability Study Plan, and Regression Strategy. |
| **QA Test Cases (60 Scenarios)** | **[🔍 View Online (TEST_CASES.md)](TEST_CASES.md)** | **[📥 Download .xlsx](StarWars_QA_Test_Cases.xlsx?raw=true)** | 60 test cases covering Functional, Boundary, Compatibility, and Security domains with 100% RTM traceability. |
| **QA Defect Report (26 Bugs)** | **[🐞 View Online (BUG_REPORT.md)](BUG_REPORT.md)** | **[📥 Download .xlsx](StarWars_QA_Bug_Report.xlsx?raw=true)** | 26 documented defects (1:1 mapping with 26 failed test cases) with severity, reproduction steps, code evidence, and developer fixes. |
| **Device Compatibility Matrix** | **[📱 TEST_ENVIRONMENT.md](TEST_ENVIRONMENT.md)** | — | Detailed matrix across physical Android phones (Pixel 7, Galaxy S21), AVD emulators (API 26–34), and iOS archives. |
| **Evidence Repository & Index** | **[📁 EVIDENCE_INDEX.md](EVIDENCE_INDEX.md)** | **[📂 Evidence/](Evidence/)** | Catalog of genuine runtime visual screenshots, MMKV storage dumps, code citations, and test transcripts (`EV-AND-001`, etc.). |
| **Automated Suite & CI/CD** | **[⚙️ AUTOMATION_AND_CICD.md](AUTOMATION_AND_CICD.md)** | **[`qa-test-suite/`](qa-test-suite/)** | Zero-dependency Node.js test harness verifying validation logic, negative input boundaries, i18n translation parity, and OWASP security configurations. |
| **Action Plan & Gap Roadmap** | **[🗺️ ACTION_PLAN.md](ACTION_PLAN.md)** | — | Transparent audit of environmental constraints and prioritized developer remediation sequence. |
| **Traceability Audit Engine** | **[`audit_traceability.py`](audit_traceability.py)** | — | Python verification engine guaranteeing 100% bidirectional 1:1 traceability between test cases and defects. |

---

## 🎯 Requirements Coverage (Functionalities 1 – 13)

| Req # | Functionality Description | Evaluation Status | Core Findings | Linked Defect IDs |
| :---: | :--- | :---: | :--- | :--- |
| **1** | Register new users & passwords | **DEFECT** | Regex validates credentials, but denying location locks user email permanently (**DEF-01**). Chevrons on inputs (**DEF-02**). Missing input bounds (**DEF-03**, **DEF-04**). | `DEF-01`, `DEF-02`, `DEF-03`, `DEF-04` |
| **2** | Camera or image library photo upload | **DEFECT** | Photo gallery upload missing (**DEF-05**). Camera permission false-negative bug (**DEF-06**). Uncompressed Base64 bloat (**DEF-07**). | `DEF-05`, `DEF-06`, `DEF-07`, `DEF-25` |
| **3** | Login with registered email & password | **DEFECT** | Mandatory GPS blocks login if denied (**DEF-08**). Login needlessly re-evaluates creation password regex (**DEF-09**). | `DEF-08`, `DEF-09`, `DEF-19` |
| **4** | SWAPI character particulars (height, mass, etc.) | **PASS / UI** | Particulars render accurately from SWAPI role object. Minor landscape column spacing flaw (**DEF-10**). | `DEF-10` |
| **5** | Create group & bidirectional invitations | **PASS** | Luke invites Vader & Vader invites Luke both succeed in local MMKV storage. | None |
| **6** | In-app notifications of invitations | **PASS (Local)** | Local banner notification triggers and focuses "Unjoined Group" tab upon login. | None |
| **7** | Joining invited groups | **DEFECT** | Join button disappears when switching app language to Indonesian (`ID`) (**DEF-11**). | `DEF-11` |
| **8** | Group profile joined users & GPS map | **DEFECT** | `<MapView>` commented out in code due to missing API billing account (**DEF-12**). Only raw coordinate text shown. | `DEF-12` |
| **9** | Starship specs via SWAPI | **DEFECT (Search)** | Starship particulars display, but search fails on static mirror without client filtering (**DEF-13**). Pagination missing (**DEF-14**). | `DEF-13`, `DEF-14` |
| **10** | Adobe XD design specifications adherence | **DEFECT (UI Mismatch)** | Audited against official [Adobe XD Design](https://xd.adobe.com/view/766eb608-0d2b-4f6d-baab-6256bf1ce52e-233d/screen/058244c1-e23f-4d8f-9209-d89b44d82bbf). Key deviations: right-aligned inputs with chevrons (**DEF-02**), missing gallery (**DEF-05**), commented MapView (**DEF-12**), and 200px empty state padding (**DEF-17**). | `DEF-02`, `DEF-05`, `DEF-10`, `DEF-12`, `DEF-17` |
| **11** | Reasonable authentication & security | **CRITICAL DEFECT** | Plaintext password in MMKV (**DEF-20**). Exposed Google API key (**DEF-21**). Insecure release signing with debug key (**DEF-23**). | `DEF-20` to `DEF-26` |
| **12** | Orientation & device compatibility (Phone/Tablet) | **DEFECT** | Frozen window metrics distort pie charts on rotation (**DEF-15**). Missing ScrollView causes screen lock (**DEF-16**). | `DEF-15` to `DEF-19` |
| **13** | Internationalization (I18n) and Localization (L10n) | **PARTIAL** | Dictionaries have 100% key parity, but UI button rendering breaks under Indonesian locale (**DEF-11**). | `DEF-11` |

---

## 🛠️ Upstream Application Build & Execution Instructions

To run the original mobile application from [worlderteam/StarWarsApp](https://github.com/worlderteam/StarWarsApp):

### 1. Prerequisites
- **Node.js**: `>= 18.0.0`
- **Yarn**: `v1.22+` or `v3.6.4`
- **Java Development Kit (JDK)**: OpenJDK 17 (LTS)
- **Android Studio**: Android SDK Build-Tools 34.0.0, Android API Levels 26–34
- **macOS & Xcode** *(for iOS only)*: Xcode 15+, CocoaPods (`gem install cocoapods`)

### 2. Clone & Dependency Installation
```bash
git clone https://github.com/worlderteam/StarWarsApp.git
cd StarWarsApp
yarn install
```

### 3. Running on Android
Ensure an Android emulator is running or a physical device is connected with USB Debugging enabled:
```bash
# Start Metro bundler in a separate terminal:
yarn start

# Build and deploy debug APK to connected device/emulator:
yarn android
```

### 4. Running on iOS (macOS Required)
```bash
cd ios
pod install
cd ..
yarn ios
```

---

## 🧪 How to Run QA Helper Scripts & Audits

All helper scripts in this repository are standalone and run with standard runtimes:

### 1. Run Master Automated QA Suite
```bash
node qa-test-suite/runner.js
```
*Executes all 32 automated checks across auth regexes, boundary matrices, i18n dictionary parity, OWASP security configs, and live SWAPI contracts in ~1.7 seconds.*

### 2. Run 100% Bidirectional Traceability Audit
```bash
python audit_traceability.py
```
*Verifies that every single failed test case in `StarWars_QA_Test_Cases.xlsx` maps 1-to-1 to an active defect in `StarWars_QA_Bug_Report.xlsx` with zero orphaned entries.*

### 3. Regenerate Spreadsheet Workbooks (Optional)
If modifications are made to the source datasets:
```bash
# Regenerate Test Cases Excel & CSV:
python generate_sheets.py

# Regenerate Bug Report Excel & CSV:
python generate_bug_report_sheets.py
```

---

## 📊 Opening and Navigating Excel Spreadsheets

1. **`StarWars_QA_Test_Cases.xlsx`**:
   - **Sheet 1 (`Dashboard & Summary`):** High-level execution metrics, category distribution, and pass rate charts.
   - **Sheet 2 (`All Test Cases`):** Complete 60-row test matrix with filters enabled on `Status` (PASS/FAIL), `Module`, `Severity`, and `Linked Defect`.
2. **`StarWars_QA_Bug_Report.xlsx`**:
   - **Sheet 1 (`Bug Metrics & Summary`):** Severity distribution (Blocker, High, Medium, Low) and category risk breakdown.
   - **Sheet 2 (`Defect Log with Evidence`):** Master defect log featuring `Associated Test Case ID`, concrete code citations, reproduction steps, root cause analysis, and developer remedies.

---

## ⚠️ Known Limitations & Remaining Work

In accordance with strict QA transparency:
1. **Adobe XD Design Specification Audit:** Evaluated against the official design artboards ([Assignment - frontend - starwars](https://xd.adobe.com/view/766eb608-0d2b-4f6d-baab-6256bf1ce52e-233d/screen/058244c1-e23f-4d8f-9209-d89b44d82bbf)). Discrepancies regarding text alignment, chevrons, gallery picker, map view, and empty state padding were identified, audited, and logged under `DEF-02`, `DEF-05`, `DEF-10`, `DEF-12`, and `DEF-17`.
2. **macOS / Native iOS Hardware:** Testing was conducted on a Windows 11 host. While static security and configuration audits were completed on the iOS project files (`Info.plist`, ATS, bridge calls), native on-device iOS execution remains **"Pending Physical Lab Validation"**.
3. **Interactive MapView:** The `<MapView>` component is commented out in source code (`/* Paid Account API Key needed */`) due to missing Google Cloud billing.

---

## ⚖️ Final Release Verdict

### ❌ NOT READY FOR PRODUCTION RELEASE
The application currently contains **2 Blocker/Critical defects** (plaintext password storage in MMKV, camera permission launch bug) and **10 High-severity defects** (mandatory GPS login blocker, vanishing Indonesian join button, distorted landscape metrics).  
Following the prioritized remediation sequence in [`ACTION_PLAN.md`](ACTION_PLAN.md) will elevate the application to **Release Candidate (RC)** quality.
