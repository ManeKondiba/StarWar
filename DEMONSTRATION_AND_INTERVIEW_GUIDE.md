# LIVE DISCUSSION & DEMONSTRATION GUIDE
## Candidate Presentation & Technical Interview Playbook
**Position:** Junior QA Engineer  
**Project:** StarWars Mobile Community App (React Native)  
**Audience:** Mixed Panel (Engineering Leads, Product Managers, QA Leads, Stakeholders)

---

## 1. Executive Presentation Script (Opening 5–7 Minutes)

### Pitch tailored for Non-Technical Stakeholders (Product, Business)
> *"Hello everyone. Today I'm excited to present my QA evaluation of the StarWars Community Application. Our business goal is to build an engaging, welcoming community app where users can easily register, join groups like the Rebel Alliance, and connect with other fans.
> 
> From a product perspective, the app delivers a fun visual theme and the core community features work well in happy-path testing. However, from a user-experience standpoint, my testing uncovered three critical roadblocks that would cause high user drop-off in production:
> 1. **Login Friction:** Users are currently blocked from logging in unless they allow GPS tracking. Many users will abandon the app here out of privacy concerns.
> 2. **Missing Photo Gallery:** Users can only take a live selfie with the camera; they cannot select an avatar from their photo library.
> 3. **Indonesian Language Bug:** When users switch to Indonesian, the 'Join Group' button vanishes due to a text-matching mismatch.
> 
> Fixing these three issues will immediately protect our user conversion funnel."*

### Pitch tailored for Technical Stakeholders (Tech Lead, Architects)
> *"From an engineering and security perspective, I performed functional testing, static code analysis, and automated contract testing. The app uses modern libraries like React Query and MMKV, but has three major technical risks:
> 1. **Critical Security Flaw (OWASP M2 / CWE-312):** Passwords are stored in plaintext inside client-side MMKV storage. We need salted hashing (bcrypt) or hardware-backed keystore integration.
> 2. **Performance Bottleneck:** Profile photos are converted to raw Base64 strings and persisted directly in MMKV. This consumes 2MB+ per user and causes memory pressure and bridge serialization jank.
> 3. **Static SWAPI Mirror Limitations:** The backend search endpoint ignores `?search=` parameters because `swapi.info` is a static JSON host. We either need client-side memoized filtering or an actual search API.
> 
> To support our QA process, I built a zero-dependency automated test runner that verifies validation regexes, i18n key parity, security configs, and live API schemas in under two seconds."*

---

## 2. Live QA Demonstration Script (Step-by-Step)

### Step 1: Run the Automated Verification Suite
**Action:** Open terminal and run:
```bash
node qa-test-suite/runner.js
```
**Talking Point:**  
*"Before opening the UI, I run our automated suite. In just 1.35 seconds, it executes 21 functional tests, validates 100% key parity between English and Indonesian dictionaries, audits our security configuration against OWASP Mobile standards, and verifies live SWAPI schema contracts."*

### Step 2: Demonstrate the User Registration & Password Validation (Req 1 & 2)
**Action:** Show the Register Screen.
1. Enter Luke Skywalker's credentials: `luke_skywalker@starwars.com` / `m4y_th3_F0rc3_b3_w1th_u`.
2. Demonstrate how the regex enforces uppercase, lowercase, numbers, and special characters.
3. Highlight **DEF-02:** Point out that only the camera is accessible, demonstrating the absence of photo gallery selection.
4. Highlight **DEF-01:** Show that if the user denies GPS permission, the user record is already saved in MMKV, trapping the user in a half-registered state.

### Step 3: Demonstrate Login & The Mandatory GPS Blocker (Req 3)
**Action:** Go to Login Screen.
1. Enter credentials.
2. Tap "Deny" on Location Permission.
3. Show the error toast: *"You must allow location permission on this app to login"*.
4. **Talking Point:** *"As a QA engineer, I advocate for the user. Requiring location to simply authenticate is an anti-pattern. Location should only be requested when viewing location-based features like the group map."*

### Step 4: Demonstrate SWAPI Integration & Search Defect (Req 4 & 9)
**Action:** Open the Character / Starship selection screen (`SwapiScreen`).
1. Type "Luke" or "Falcon" into the search bar.
2. Observe that the list does not filter.
3. **Talking Point:** *"I diagnosed the root cause: the app queries `https://swapi.info/api/people/?search=Luke`, but because swapi.info is a static mirror, it returns all 82 records. As QA, I didn't just log a bug; I provided the exact fix: a client-side filter using `useMemo`."*

### Step 5: Demonstrate Group Creation, Notification & Locale Bug (Req 5, 6, 7 & 13)
**Action:** 
1. Create "Rebel Alliance", invite `anakin_skywalker@starwars.com`.
2. Log in as Darth Vader and show the in-app invitation notification on `GroupHomeScreen`.
3. Switch the language toggle to `ID` (Bahasa Indonesia).
4. Tap the invited group to open `GroupDetailScreen`.
5. Point out **DEF-05:** The "Join Group" button has disappeared because the screen checked for the English string `"Unjoined Group"` instead of using the translated key `t('groupDetail.unjoinedTab')`.

### Step 6: Highlight Security Findings (Req 11)
**Action:** Show the security audit test output.
1. Point to plaintext passwords stored in MMKV.
2. Show hardcoded Google Maps API Key in `AndroidManifest.xml`.
3. Show `NSAllowsArbitraryLoads = true` in `Info.plist`.

---

## 3. QA Knowledge & General Interview Questions (Preparation & Answers)

### Q1: What is the difference between Severity and Priority? How would you classify the defects found in this app?
**Answer:**
- **Severity** refers to the technical impact of the defect on system functionality or security (how bad is the bug?).
- **Priority** refers to the business urgency of fixing the defect (how fast do we need to patch it?).
- *Examples from this app:*
  - **DEF-05 (Join Button Disappears in Indonesian):** High Severity (completely blocks core functionality for Indonesian users) & High Priority (breaks localization requirement).
  - **Plaintext Password in MMKV:** Critical Severity (OWASP M2 security breach) & High Priority (must be resolved before any public beta).
  - **Commented-out MapView (DEF-06):** Medium Severity (fallback text coordinates are shown) & Medium Priority (can be scheduled in next sprint with API key).

### Q2: How do you handle testing mobile apps with poor or fluctuating network connections?
**Answer:**
- I use network link conditioners and proxy tools (like Charles Proxy, Proxyman, or Android Emulator Network settings) to simulate:
  1. **Offline Mode (Airplane Mode):** Verifying graceful degradation, offline caching, and user-friendly error banners.
  2. **3G / Low Bandwidth / High Latency:** Ensuring loaders/skeletons are displayed and API calls don't trigger multiple duplicate requests if the user taps repeatedly.
  3. **Intermittent Connection Drops:** Verifying retry logic and transaction rollback (e.g. registration should not save partial data if a network request fails halfway).

### Q3: How do you deal with "flaky" automated tests?
**Answer:**
- Flaky tests erode trust in CI/CD. When encountering flakiness:
  1. **Identify the root cause:** Most mobile flakiness stems from asynchronous timing, animations, network delays, or uncleaned local state (e.g. MMKV storage persisting between test runs).
  2. **Isolate state:** Ensure each test run initializes with a fresh database/mock storage state (`Storage.removeAllItems()`).
  3. **Use explicit wait conditions:** Avoid arbitrary sleeps (`setTimeout`); wait for UI elements or network state changes using element matchers (e.g., `waitFor(element).toBeVisible()`).
  4. **Quarantine:** If an intermittent test cannot be immediately resolved, quarantine it out of the main blocking CI gate while investigating to keep the deployment pipeline moving.

### Q4: Why is Base64 image storage considered a performance anti-pattern in React Native?
**Answer:**
- Base64 encoding increases file size by roughly **33%** compared to raw binary.
- Storing Base64 strings in React Native means:
  - High RAM consumption when parsing JSON strings across the JavaScript-to-Native bridge.
  - Slower disk I/O when reading large strings from MMKV/AsyncStorage.
  - Image components have to decode the string on the JS thread, leading to dropped frames during list scrolling.
- **Best Practice:** Save the image to the device filesystem (`cacheDirectory` or `documentDirectory`) and reference only the local URI (`file://...`).

### Q5: How would you structure a bug report so developers can fix it without asking clarifying questions?
**Answer:**
- A high-quality bug report must contain:
  1. **Clear, Descriptive Title:** `[Register Screen] User data saved to MMKV before location permission is checked, causing duplicate email lockout on retry`.
  2. **Environment Details:** Device model (e.g. Pixel 7, Android 14), App Build #, Locale (EN/ID).
  3. **Severity & Priority:** High / P1.
  4. **Preconditions:** Fresh install, clean storage.
  5. **Numbered Reproduction Steps:** 1. Open Register, 2. Fill valid form, 3. Tap Save, 4. Tap 'Deny' on OS Location dialog.
  6. **Expected Result vs Actual Result.**
  7. **Visual Evidence:** Screen recording or screenshot highlighting the failure.
  8. **Logs / Stacktrace:** Logcat/Xcode console logs.
  9. **Root Cause Analysis & Suggested Fix:** Link to specific file and line number (e.g. `RegisterScreen.js#L91`).

---

## 4. Summary of Candidate Value Proposition
- **Thoroughness:** Went beyond UI surface testing to examine security configs, architecture, and network contracts.
- **Proactive Engineering:** Provided working automated test scripts and ready-to-merge code remedies for identified defects.
- **User-Centric Mindset:** Balanced technical compliance with user advocacy (privacy, localization parity, form friction).
