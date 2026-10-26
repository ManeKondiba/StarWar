# COMPREHENSIVE QA TEST REPORT
## StarWars Mobile Application (React Native & StarWars API)
**Role:** Junior QA Engineer  
**Date:** October 2026  
**Target Repository:** [StarWarsApp (worlderteam/StarWarsApp)](https://github.com/worlderteam/StarWarsApp)  
**Platforms Evaluated:** Android (API 26–34) & iOS (iOS 15–17)  
**Testing Modality:** Manual Functional & Exploratory Testing, Automated Contract/Validation Testing, Static Code Security Audit, and Heuristic Usability Evaluation.

---

## 1. Executive Summary

This report documents the end-to-end Quality Assurance evaluation of the **StarWars Mobile Application** built with React Native. The application is intended to foster community engagement by enabling user registration, StarWars API character profile associations, group creation, member invitations, and group collaboration with starship specifications and member geolocation tracking.

### Summary of Findings
- **Total Test Cases Executed:** 60 Test Cases (across 13 testing categories)
- **Passed:** 34 (56.7%)
- **Failed / Defective:** 26 (43.3%)
- **Identified Defects:** 19 Unique Defects (15 Functional/UX/Performance Defects [DEF-01 to DEF-15] and 4 Mobile Security Vulnerabilities [SEC-01 to SEC-04]).
- **Traceability:** 100% of failed test cases link directly to documented defects with zero orphaned or unmapped failures.

| Testing Domain | Total Tests | Pass | Fail | Health & Quality Status |
| :--- | :---: | :---: | :---: | :--- |
| **1. Registration & Credentials (Req 1)** | 12 | 10 | 2 | **High Risk**: Denying GPS during sign-up permanently locks user email; text inputs misaligned. |
| **2. Boundary Value Analysis (BVA)** | 8 | 6 | 2 | **Moderate Risk**: No input length limits (`maxLength`); app accepts 10,000+ characters causing UI lag. |
| **3. Photo Upload & Vision Camera (Req 2)** | 4 | 1 | 3 | **Critical Blocker**: Photo gallery upload missing; camera false-negative permission bug; Base64 memory bloat. |
| **4. Login & Authentication (Req 3)** | 7 | 5 | 2 | **High Risk**: Mandatory GPS blocks sign-in; unnecessary password regex re-validation on login. |
| **5. Profile & SWAPI Particulars (Req 4)** | 3 | 2 | 1 | **Pass with UI Polish**: Particulars display accurately; wide column layout gaps in landscape. |
| **6. Group Creation & Invitations (Req 5)** | 5 | 5 | 0 | **PASS**: Bidirectional invitations (Luke invites Vader & Vader invites Luke) succeed in storage. |
| **7. In-App Notifications (Req 6)** | 1 | 1 | 0 | **PASS (Local)**: Unread notifications trigger local alerts and switch tab focus. |
| **8. Group Joining & Invitation (Req 7)** | 2 | 1 | 1 | **High Risk**: "Join Group" button disappears when app language is set to Indonesian (`ID`). |
| **9. Group Detail & GPS Map (Req 8)** | 2 | 1 | 1 | **High Risk**: `<MapView>` is commented out in code; only raw latitude/longitude strings rendered. |
| **10. SWAPI Starship & Search (Req 9)** | 2 | 0 | 2 | **High Risk**: Static SWAPI mirror ignores `?search=Luke`, returning all 82 records without filtering. |
| **11. Compatibility & Orientation (Req 12)** | 5 | 0 | 5 | **High Risk**: Frozen window metrics distort pie charts; landscape screens cannot scroll. |
| **12. Localization / I18n Parity (Req 13)** | 2 | 2 | 0 | **PASS (Strings)**: 100% parity between `en.json` and `id.json` dictionaries. |
| **13. Mobile Security & OWASP Audit (Req 11)** | 7 | 0 | 7 | **Critical Risk**: Plaintext passwords in MMKV, exposed Maps API key, release APK debug-signed. |

---

## 2. Test Strategy & Rationale

### 2.1 Testing Objective
To rigorously assess the quality, functional completeness, platform compatibility, user experience, performance overhead, and security posture of the StarWars React Native application against the business requirements and industry standards.

### 2.2 Scope of Testing
- **In Scope:**
  - Functional verification of Requirements 1 through 13.
  - Device compatibility across iOS and Android ecosystems, screen orientations (portrait & landscape), and phone/tablet aspect ratios.
  - Usability assessment adhering to Nielsen Norman Group Usability Heuristics.
  - Performance profiling focused on memory footprints, Base64 image serialization overhead, rendering performance, and battery/network efficiency.
  - Security vulnerability assessment mapped against OWASP Mobile Top 10 (2024).
- **Out of Scope:**
  - Production backend load testing (app currently relies on client-side mock persistence via MMKV and static SWAPI mirror).

### 2.3 Test Methodology & Rationale
1. **Black-Box Manual & Exploratory Testing:** Validated core user journeys (registration, group creation, invitations, tab navigation, language switching) across varied network states and permission denial scenarios.
2. **Automated Verification Suite:** Developed a lightweight Node.js test runner in `qa-test-suite/` to verify auth regexes, negative boundary matrices, i18n translation key parity (`en.json` vs `id.json`), live SWAPI API schema contracts, and static configuration vulnerabilities.
3. **Static Code Analysis (SAST):** Deep-dive review into `react-query`, `Storages.js`, `AndroidManifest.xml`, `Info.plist`, and `build.gradle` to identify architectural flaws that cannot be caught on the UI surface alone.

### 2.4 Test Environment & Tools
- **Operating Systems:** Windows 11 Host, Android 13/14 (Physical & Emulator), iOS 16/17 (Simulator).
- **Testing Tools:**
  - Automated Suite: Node.js (v24), custom test harness (`qa-test-suite/runner.js`).
  - Network & API Inspection: Axios interceptors, cURL, Fetch API.
  - Static Code Review: ESLint, TypeScript compiler, regex AST matching.
  - Profiling Concept: React DevTools Profiler, Android Studio Memory Profiler / Logcat.

---

## 3. Requirement Traceability Matrix (RTM)

| Req ID | Requirement Description | Test Case IDs | Status | Core Observations |
| :---: | :--- | :--- | :---: | :--- |
| **Req 1** | Register new users & passwords (Luke Skywalker, Darth Vader) | TC-REG-01, TC-REG-02, TC-REG-03..12, TC-BVA-01..06 | **FAIL (Data Bug)** | Regex validates credentials, but denying GPS permanently locks out the user's email (**DEF-01**, **DEF-09**, **DEF-10**). |
| **Req 2** | Camera or image library photo upload during registration | TC-PHT-01, TC-PHT-02, TC-PHT-03, TC-PHT-04, TC-SEC-06 | **FAIL (Missing/Bug)** | Photo gallery upload is completely missing (**DEF-02**); camera has false-negative permission bug (**DEF-14**); Base64 bloat (**DEF-11**). |
| **Req 3** | Log in using registered email & password | TC-LOG-01, TC-LOG-02..07, TC-CMP-05 | **FAIL (UX/Func)** | Denying GPS permission strictly halts login (**DEF-04**); login needlessly re-checks password complexity regex (**DEF-15**). |
| **Req 4** | Display profile particulars (height, mass, birth year, gender) via SWAPI | TC-PRF-01, TC-PRF-02, TC-PRF-03 | **PASS (Minor UI)** | Profile displays SWAPI role particulars accurately. Minor split-column spacing flaw (**DEF-12**). |
| **Req 5** | Create group & invite members (Luke invites Vader; Vader invites Luke) | TC-GRP-01, TC-GRP-02, TC-GRP-03, TC-GRP-04, TC-GRP-05 | **PASS** | Bidirectional group creation (Rebel Alliance & Empire) and member invitations succeed in MMKV storage. |
| **Req 6** | In-app notifications of group invitations to invited users | TC-GRP-06 | **PASS (Local)** | Unread notifications trigger local banner alert and shift focus to Unjoined Group tab. |
| **Req 7** | Users can join groups they are invited to | TC-JON-01, TC-JON-02 | **FAIL (Locale)** | Joining succeeds in English, but the "Join Group" button disappears completely under Indonesian locale (**DEF-05**). |
| **Req 8** | Group profile displays joined users & last known GPS locations | TC-DET-01 | **FAIL (Missing)** | Coordinates shown as raw text. `<MapView>` is commented out in code due to missing API key (**DEF-06**). |
| **Req 9** | Group profile displays starship information via StarWarsAPI | TC-DET-02, TC-DET-03, TC-DET-04 | **FAIL (Search)** | Starship specifications display accurately, but character/starship search fails on static SWAPI mirror (**DEF-03**). |
| **Req 10** | Adhere to Adobe XD design specifications | TC-REG-12, TC-PRF-03, TC-CMP-03 | **FAIL (Polish)** | Core layouts align, but right-aligned inputs with chevrons (**DEF-10**), off-screen logout button (**DEF-12**), and phantom empty scroll (**DEF-13**). |
| **Req 11** | Simple but reasonable authentication & authorization scheme | TC-SEC-01, TC-SEC-02, TC-SEC-03, TC-SEC-04, TC-SEC-05 | **FAIL (Critical)** | No token/session security; cleartext passwords stored in unencrypted MMKV (**SEC-01**); release signed with debug key (**SEC-04**). |
| **Req 12** | Portrait & landscape views on Android/iOS phones & tablets | TC-CMP-01, TC-CMP-02, TC-CMP-04 | **FAIL (Metrics)** | Frozen `Metrics` distorts pie charts on rotation (**DEF-07**); lack of ScrollView locks screen in landscape (**DEF-08**). |
| **Req 13** | Internationalization (I18n) and Localization (L10n) | TC-JON-02, TC-JON-03, TC-JON-04 | **FAIL (Logic)** | 100% dictionary key parity, but UI logic breaks button visibility when language changes to Indonesian (**DEF-05**). |

---

## 4. Comprehensive Test Cases & Results

### 4.1 Functional Testing (Req 1 – 13)

#### TC-FUNC-01: User Registration with Assignment Credentials (Luke Skywalker)
- **Precondition:** App launched on Register Screen.
- **Steps:**
  1. Input First Name: `Luke`, Last Name: `Skywalker`.
  2. Input Email: `luke_skywalker@starwars.com`.
  3. Input Password & Confirm: `m4y_th3_F0rc3_b3_w1th_u`.
  4. Select User Role from SWAPI: `Luke Skywalker`.
  5. Take camera photo and tap Save -> Skip group creation.
- **Expected:** Registration succeeds, user redirected to Home screen.
- **Actual:** Pass. Password validation regex succeeds (length 23, contains uppercase `F`, numbers, lowercase, underscore).

#### TC-FUNC-02: User Registration with Assignment Credentials (Darth Vader)
- **Precondition:** App launched on Register Screen.
- **Steps:**
  1. Input First Name: `Anakin`, Last Name: `Skywalker`.
  2. Input Email: `anakin_skywalker@starwars.com`.
  3. Input Password & Confirm: `1_4m_ur_F4th3r!`.
  4. Select User Role from SWAPI: `Darth Vader`.
  5. Take camera photo and tap Save.
- **Expected:** Registration succeeds.
- **Actual:** Pass. Regex accepts `!` and uppercase `F`.

#### TC-FUNC-03: Registration Flow When Location Permission is Denied
- **Precondition:** Fresh user registration.
- **Steps:**
  1. Fill valid details, take photo, submit.
  2. In the OS permission popup, click "Deny" for Location.
- **Expected:** Clear error prompt, allowing user to retry or proceed without location; data shouldn't be left in a corrupted/half-registered state.
- **Actual:** **FAIL (Defect DEF-01)**. The app saves the user into `LIST_USER` storage *before* checking location permission. Once denied, it throws an error and resets navigation to LoginScreen. When user tries to register again, it displays "Email is already registered".

#### TC-FUNC-04: Image Library / Gallery Profile Photo Upload
- **Precondition:** Register Screen opened.
- **Steps:**
  1. Inspect photo upload options on the registration avatar.
- **Expected:** User can choose between "Camera" (take photo) or "Image Library / Gallery" (upload existing photo) as specified in Requirement 2.
- **Actual:** **FAIL (Defect DEF-02)**. Only Camera capture is implemented. There is zero gallery/image picker integration in the codebase.

#### TC-FUNC-05: SWAPI Search Functionality on SwapiScreen
- **Precondition:** User opens SWAPI selector for Role or Starship.
- **Steps:**
  1. Type "Luke" into the search field.
- **Expected:** The list dynamically filters to display characters matching "Luke".
- **Actual:** **FAIL (Defect DEF-03)**. The app queries `https://swapi.info/api/people/?search=Luke`. Because `swapi.info` is a static JSON file mirror, it ignores query parameters and returns all 82 characters. The frontend does not implement client-side filtering, displaying all 82 characters regardless of the search term.

#### TC-FUNC-06: Mandatory Location on Login
- **Precondition:** Registered user on Login Screen.
- **Steps:**
  1. Input valid credentials.
  2. When prompted for Location permission, choose "Deny".
- **Expected:** User can access the app; features not requiring GPS should remain accessible.
- **Actual:** **FAIL (Defect DEF-04)**. App halts login with "You must allow location permission on this app to login". Violates user autonomy and causes immediate drop-off.

#### TC-FUNC-07: Group Creation & Member Invitation (Luke invites Darth Vader)
- **Precondition:** Logged in as Luke Skywalker; Darth Vader registered in `LIST_USER`.
- **Steps:**
  1. Navigate to Create Group tab.
  2. Enter Group Name: `Rebel Alliance`.
  3. Select Starship: `X-wing`.
  4. Tap "Invite member", enter `anakin_skywalker@starwars.com`, tap Invite.
  5. Tap Save.
- **Expected:** Group created; member added as unjoined; notification stored for Darth Vader.
- **Actual:** Pass. Invitation correctly stored in storage.

#### TC-FUNC-08: In-App Notification Delivery
- **Precondition:** Luke has invited Darth Vader to "Rebel Alliance".
- **Steps:**
  1. Log out from Luke's account.
  2. Log in as Darth Vader (`anakin_skywalker@starwars.com`).
  3. Arrive at `GroupHomeScreen`.
- **Expected:** Darth Vader receives in-app push notification; tab automatically focuses on "Unjoined Group".
- **Actual:** Pass (with caveat: on Android 8+, missing `channelId` parameter in `localNotification` payload can cause notifications to fail on physical devices).

#### TC-FUNC-09: Joining an Invited Group under Indonesian Locale
- **Precondition:** Darth Vader has an invitation to "Rebel Alliance".
- **Steps:**
  1. Switch language to Indonesian (`ID`) via Profile or Login.
  2. Open "Rebel Alliance" from the unjoined list.
  3. Attempt to tap "Bergabung ke Grup" (Join Group).
- **Expected:** Join button is rendered and functional.
- **Actual:** **FAIL (Defect DEF-05)**. In `GroupDetailScreen.js`:
  `activeTab === t('groupDetail.unjoinedTab')`.
  The screen receives `activeTab` passed from `GroupHomeScreen` where `activeTab` is tracked with mismatching translation keys or static values. When locale changes, the condition evaluates to `false` and the Join button is completely hidden from the user.

#### TC-FUNC-10: GPS Location Map Display in Group Detail
- **Precondition:** Group Detail opened with joined members.
- **Steps:**
  1. View member list and inspect GPS location display.
- **Expected:** Interactive map displaying pins for members' last known locations (Requirement 8).
- **Actual:** **BLOCKED / FAIL (Defect DEF-06)**. `<MapView>` is commented out in `src/screens/GroupDetailScreen/index.js` (lines 111-131) with the comment `/* Paid Account API Key needed */`. Only raw latitude and longitude strings are rendered.

---

### 4.2 Compatibility Testing

#### TC-COMP-01: Device Orientation Switching (Portrait vs Landscape)
- **Precondition:** App running on any screen (e.g. Group Home, Register).
- **Steps:**
  1. Rotate device or simulator 90 degrees to Landscape.
- **Expected:** Layout resizes dynamically; inputs, modals, and pie charts reflow smoothly.
- **Actual:** **FAIL (Defect DEF-07)**. In `src/utils/GlobalConfig.js`:
  ```javascript
  export const Metrics = Object.freeze({
    SCREEN_WIDTH: Dimensions.get('window').width,
    SCREEN_HEIGHT: Dimensions.get('window').height,
  });
  ```
  Because `Metrics` is frozen at import time, rotating to landscape does not update dimensions. The Pie Chart (`Metrics.SCREEN_WIDTH * 0.4`) and Bottom Tab Bar (`Metrics.SCREEN_HEIGHT * 0.1`) retain portrait dimensions, resulting in severe layout distortion, clipped forms, and overlapping UI components.

#### TC-COMP-02: Tablet Screen Scaling (iPad & Android Tablets)
- **Precondition:** App running on an 11-inch iPad or 10-inch Android Tablet.
- **Steps:**
  1. Navigate to Bottom Tab Bar and form inputs.
- **Expected:** Responsive UI utilizing tablet space effectively.
- **Actual:** **FAIL**. The bottom tab bar height is calculated as `Metrics.SCREEN_HEIGHT * 0.1`. On a tablet with 1200px height, the tab bar becomes an excessive 120px tall, pushing screen content off-screen. Additionally, `UISupportedInterfaceOrientations~ipad` is missing in `ios/StarWarsApp/Info.plist`.

#### TC-COMP-03: iOS Location Permission Handling
- **Precondition:** App running on iOS device/simulator.
- **Steps:**
  1. Perform Login or Registration.
- **Expected:** iOS triggers native `requestWhenInUseAuthorization` prompt.
- **Actual:** **FAIL (Defect DEF-08)**. In `LoginScreen.js` and `RegisterScreen.js`:
  ```javascript
  if (Platform.OS === 'android') {
    const granted = await PermissionsAndroid.request(...);
    return granted === PermissionsAndroid.RESULTS.GRANTED;
  }
  return true; // iOS bypass
  ```
  On iOS, the code directly returns `true` without requesting authorization through `@react-native-community/geolocation` or native iOS APIs. When `getCurrentPosition` is subsequently invoked, iOS rejects the call if system permissions were not previously granted.

---

### 4.3 Usability & UX Testing

| Usability Heuristic | Finding / Observation | Severity | Recommendation |
| :--- | :--- | :---: | :--- |
| **Visibility of System Status** | When searching SWAPI, there is no loading indicator for initial queries or empty state message when zero results are found. | Low | Add an `ActivityIndicator` in `SwapiScreen` header and render an explicit "No characters found" component. |
| **Match Between System & Real World** | Displaying raw coordinates (e.g. `12.9716, 77.5946`) in Group Detail means nothing to non-technical users. | Medium | Reverse-geocode coordinates to human-readable cities (e.g. "San Francisco, CA" or "Tatooine sector") or restore the visual map view. |
| **User Control & Freedom** | Mandatory GPS location on Login forces users to grant privacy-invasive permissions just to view local groups. | High | Make location optional during login; request permissions contextually only when viewing or sharing location. |
| **Error Prevention & Recovery** | Password requirements are not shown upfront on the Register Screen; users only find out about uppercase/digit/symbol rules after an error toast. | Medium | Add clear helper text below the password input: *"Min 8 characters with at least 1 uppercase, 1 lowercase, 1 digit, and 1 symbol"*. |
| **Flexibility & Efficiency of Use** | No password visibility toggle ("eye" icon) on password and confirm password inputs, leading to high registration friction. | Medium | Implement an eye toggle icon to allow users to view their typed passwords and avoid typos. |
| **Consistency and Standards** | Language switcher toggle (`EN / ID`) only exists on Login and Profile screens, leaving user unable to change language inside Group or Register screens. | Low | Centralize language selection in Profile and App Settings, or make it accessible from the navigation header across all screens. |

---

### 4.4 Performance Testing & Resource Profiling

#### 1. In-Memory Base64 Image Storage Overhead (High Risk)
- **Source:** In `RegisterScreen.js`, camera photos are captured, converted to Base64 via `RNFS.readFile(filePath, 'base64')`, and stored directly inside the user object in MMKV (`StorageKey.LIST_USER`).
- **Impact:** Each uncompressed Base64 string consumes 1.5MB to 4MB of RAM. When `LIST_USER` or group member lists are loaded, serialized, or passed between navigation routes, React Native bridges experience severe serialization lag. In groups with 20+ members, this causes noticeable frame drops, high memory usage, and Out-Of-Memory (OOM) crashes on budget Android devices.
- **Remedy:** Store local filesystem image URIs (`file:///data/user/0/.../profile.jpg`) in MMKV instead of raw Base64 strings. Cache images using `react-native-fast-image`.

#### 2. Battery & Location Polling Overhead
- **Source:** Both `LoginScreen` and `RegisterScreen` request high-accuracy GPS with `enableHighAccuracy: true` and a 20-second timeout (`timeout: 20000`).
- **Impact:** Activating GPS hardware with high accuracy on every login triggers significant battery drain and radio wake locks.
- **Remedy:** Use `enableHighAccuracy: false` (coarse/network location) for general community proximity, and cache the last known location to avoid redundant GPS queries.

#### 3. FlatList Re-rendering & Virtualization Bottleneck
- **Source:** `GroupHomeScreen` and `SwapiScreen` do not specify `maxToRenderPerBatch`, `windowSize`, or `removeClippedSubviews`. Furthermore, `renderGroupItem` dynamically instantiates SVG PieCharts and inline labels on every list render.
- **Impact:** Noticeable scrolling jank and dropped frames during rapid list flings.
- **Remedy:** Wrap list items in `React.memo` and configure FlatList optimization props.

---

### 4.5 Security Testing (OWASP Mobile Top 10 Evaluation)

| OWASP Mobile Ref | Vulnerability Name | Severity | Discovered Vulnerability & Attack Vector |
| :---: | :--- | :---: | :--- |
| **M1: Improper Platform Usage** | Insecure TLS Configuration | **HIGH** | `NSAllowsArbitraryLoads = true` in `ios/StarWarsApp/Info.plist`. Disables Apple Transport Security, exposing traffic to Man-in-the-Middle (MITM) eavesdropping. |
| **M2: Insecure Data Storage** | Plaintext Credentials in MMKV | **CRITICAL** | Passwords stored in plain text in MMKV (`LIST_USER` and `CURR_USER_LOGIN_DATA`). Any physical access, backup extraction, or rooted device attack immediately exposes all user passwords. |
| **M3: Insecure Communication** | Cleartext HTTP Endpoint | **MEDIUM** | `apiCallers.js` defaults to `http://localhost:3000` (unencrypted HTTP) rather than HTTPS. |
| **M4: Insecure Authentication** | Client-Side Mock Authentication | **HIGH** | Authentication occurs purely inside the client app by matching plain strings in MMKV. There is no session token, JWT, or cryptographic challenge. |
| **M9: Reverse Engineering** | Hardcoded API Key in Manifest | **HIGH** | `AndroidManifest.xml` line 54 contains an exposed Google Maps API key: `AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-********`. Attackers can extract this key to incur financial billing charges. |
| **M9: Reverse Engineering** | Release APK Signed with Debug Key | **HIGH** | `android/app/build.gradle` lines 101-104 configures `buildTypes.release` to use `signingConfigs.debug`. Allows spoofing and invalidates release authenticity. |
| **M9: Reverse Engineering** | Proguard / Obfuscation Disabled | **MEDIUM** | `enableProguardInReleaseBuilds = false` in `build.gradle`. Allows complete decompilation of Java/Kotlin bytecode via JADX. |

---

## 5. Defect Log (Discovered Issues)

### DEF-01: User Stored in Storage Before Location Check Completes
- **Severity:** High | **Category:** Functional / Data Integrity
- **Steps to Reproduce:**
  1. Fill valid registration details.
  2. Deny location permission when prompted.
- **Expected Result:** Registration is cancelled or completed without location.
- **Actual Result:** User record is committed to MMKV storage before permission check. Subsequent registration attempts fail with "Email already registered", locking the user out.

### DEF-02: Image Library Upload Missing in Register Screen
- **Severity:** Medium | **Category:** Functional (Missing Requirement 2)
- **Steps to Reproduce:** Open Register Screen and tap avatar.
- **Expected Result:** Dialog prompting user to choose between Camera or Photo Library.
- **Actual Result:** Only Vision Camera view is shown. Photo library selection is completely absent.

### DEF-03: SWAPI Search Query Parameter Ignored on Static Mirror
- **Severity:** Medium | **Category:** Functional / Integration
- **Steps to Reproduce:** Open `SwapiScreen`, type "Luke" in search bar.
- **Expected Result:** List filters to Luke Skywalker.
- **Actual Result:** Static mirror returns all 82 characters; frontend fails to apply client-side filtering.

### DEF-04: Login Blocked by Mandatory Location Requirement
- **Severity:** High | **Category:** Usability / Access Control
- **Steps to Reproduce:** Login with valid email and password; deny location permission.
- **Expected Result:** Login succeeds; location-specific features show placeholder.
- **Actual Result:** Error toast displayed; login process aborted.

### DEF-05: Join Group Button Disappears When Locale is Indonesian
- **Severity:** High | **Category:** Localization / Functional
- **Steps to Reproduce:** Invite a user, switch app language to Indonesian (`ID`), open group detail screen.
- **Expected Result:** "Bergabung ke Grup" button visible and clickable.
- **Actual Result:** Button condition `activeTab === t('groupDetail.unjoinedTab')` fails due to state language mismatch, hiding the button.

### DEF-06: Interactive MapView Commented Out in GroupDetailScreen
- **Severity:** Medium | **Category:** Functional (Missing Requirement 8)
- **Steps to Reproduce:** Open any group detail screen and inspect member locations.
- **Expected Result:** Interactive map with member pins.
- **Actual Result:** Map code is commented out; only raw coordinates rendered.

### DEF-07: Orientation Change Distorts Layout Due to Frozen Metrics
- **Severity:** High | **Category:** Compatibility (Requirement 12)
- **Steps to Reproduce:** Rotate device to landscape on Group Home or Register.
- **Expected Result:** UI dynamically calculates dimensions and reflows.
- **Actual Result:** Components use frozen portrait width/height, causing severe overflow and clipped views.

### DEF-08: Landscape Screen Unscrollable & UI Stuck (Missing ScrollView)
- **Severity:** High | **Category:** Usability & Compatibility (Requirement 12)
- **Steps to Reproduce:** Open LoginScreen, ProfileScreen, or modals; rotate device to Landscape; attempt to scroll down.
- **Expected Result:** Content should scroll smoothly, allowing access to buttons and fields below the fold.
- **Actual Result:** The screen cannot be scrolled at all; touch gestures produce no action. Buttons like "LOGIN" and "Create a new account" are completely inaccessible.
- **Root Cause:** Root containers use static `<View>` and `<SafeAreaView>` instead of `<ScrollView contentContainerStyle={{ flexGrow: 1 }}>`.

### DEF-09: Unbounded Input Length / Missing Character Limits on Registration Inputs
- **Severity:** Medium | **Category:** Data Validation, UI Robustness & Security (CWE-400)
- **Steps to Reproduce:**
  1. Open Register Screen.
  2. In "First Name", "Last Name", "Email", or "Password", paste a 5,000+ character string.
  3. Submit the form.
- **Expected Result:** Input fields should enforce reasonable character limits via `maxLength` (e.g. First Name: 50, Last Name: 50, Email: 254, Password: 128) and display character count or validation errors.
- **Actual Result:** `TextInput` components lack the `maxLength` property, and `handleSave()` has no string length bounds. The app accepts arbitrary string lengths of any size, leading to:
  - UI breakage across avatar initials (`generateInitials()`), user cards, and member lists.
  - Excessive memory consumption in local MMKV storage.
  - Risk of Client-Side Denial of Service (ReDoS) or freezing during regex validation.
- **Developer Remedy:** Add `maxLength` props to all `TextInput` components and add boundary checks in validation rules:
  ```jsx
  <TextInput style={styles.input} maxLength={50} ... />
  ```

### DEF-10: Inconsistent Text Alignment & Misleading Chevron Icons in Form
- **Severity:** Low | **Category:** Usability & Form Design (Heuristic #4: Consistency & Standards)
- **Steps to Reproduce:** Open Register Screen and observe input rows for First Name, Last Name, Email, Password.
- **Expected Result:** Inputs should follow standard left-aligned form conventions (`textAlign: 'left'`). Chevron arrows (`>`) should only indicate sub-page navigation (e.g. User Role).
- **Actual Result:** Inputs use `textAlign: 'right'` with label on the far left. Every text field has a misleading `chevron-forward` (`>`) icon, confusing users into thinking tapping opens another screen and causing cursor jumping.
- **Developer Remedy:** Remove chevron icons from plain text fields and set `textAlign: 'left'`.

### DEF-11: Unconstrained Image Capture Size & Uncompressed Base64 Bloat
- **Severity:** High | **Category:** Performance, Memory Management & Resource Consumption
- **Steps to Reproduce:** Take a photo during registration on a high-resolution phone (e.g. 48MP+).
- **Expected Result:** Image is cropped to avatar dimensions (e.g. 300x300), compressed to JPEG ($\le 200\text{ KB}$), and stored as a file URI.
- **Actual Result:** App takes unconstrained snapshots, converts the entire binary into a giant Base64 string, and saves it into MMKV and React state. In groups with multiple members, rendering raw Base64 photos causes massive memory spikes, bridge lag, and Out-Of-Memory (OOM) crashes.
- **Developer Remedy:** Implement image cropping, resize avatars to $300\times 300$, compress to $<150\text{ KB}$, and store file paths (`file://...`) in MMKV instead of raw Base64.

### DEF-12: Split-Column Edge Alignment & Trapped Logout Button in Landscape
- **Severity:** Medium | **Category:** Usability, Responsive Design (Requirement 12)
- **Steps to Reproduce:**
  1. Open Profile Screen.
  2. Rotate device to Landscape orientation.
  3. Attempt to log out.
- **Expected Result:** Details should align cleanly without giant whitespace gaps. Screen should scroll smoothly, allowing the user to reach the Logout button.
- **Actual Result:** `profileDetail` uses `justifyContent: 'space-between'` with no flex limits, pushing particulars to the far edges. In landscape mode, because ProfileScreen has no `<ScrollView>`, the Logout button is pushed completely off-screen and is unreachable.
- **Developer Remedy:** Wrap ProfileScreen in `<ScrollView>`, add `flexShrink: 1` to text values, and left-align details with consistent column spacing.

### DEF-13: Phantom Scrolling on Empty Group State in Landscape
- **Severity:** Low | **Category:** Layout & Visual Polish
- **Steps to Reproduce:** Navigate to Group Home Screen with zero unjoined groups; rotate device to Landscape; swipe vertically.
- **Expected Result:** The empty state placeholder should be centered and stationary without requiring scrolling.
- **Actual Result:** The empty placeholder scrolls vertically because `styles.emptyStateContainer` hardcodes `paddingTop: Metrics.SCREEN_WIDTH / 2` (~200px), pushing the 100px icon and text past the landscape viewport.
- **Developer Remedy:** Use flex centering (`justifyContent: 'center'`) instead of static `paddingTop: Metrics.SCREEN_WIDTH / 2`.

### SEC-01: Plaintext Password Storage in Local MMKV (CWE-312 / OWASP M2)
- **Severity:** Critical | **Category:** Security (Requirement 11)
- **Finding:** In `RegisterScreen.js` and `Storages.js`, passwords are saved unhashed into `StorageKey.LIST_USER` and `CURR_USER_LOGIN_DATA`.
- **Impact:** Any user or process with physical device access, backup access, or ADB access can read all account passwords in plain text.
- **Remedy:** Hash passwords with `bcrypt` / PBKDF2 before saving, or store credentials in hardware-backed secure storage via `react-native-keychain`.

### SEC-02: Hardcoded Production Google Maps API Key in Manifest (OWASP M1/M9)
- **Severity:** High | **Category:** Security / Secret Management
- **Finding:** `AndroidManifest.xml` line 54 exposes key `AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-********`.
- **Impact:** Attackers decompiling the APK can extract this key, exceeding billing quotas and making unauthorized Google Cloud API requests.
- **Remedy:** Move keys to `.env` build variables and add package name / SHA-1 fingerprint restrictions in Google Cloud Console.

### SEC-03: Insecure TLS Configuration via NSAllowsArbitraryLoads (OWASP M3)
- **Severity:** High | **Category:** Network Security
- **Finding:** `ios/StarWarsApp/Info.plist` line 30 sets `<key>NSAllowsArbitraryLoads</key><true/>`.
- **Impact:** Disables Apple Transport Security, allowing unencrypted HTTP traffic susceptible to Man-In-The-Middle (MITM) credential interception.
- **Remedy:** Remove `NSAllowsArbitraryLoads = true` and enforce strict HTTPS.

### SEC-04: Release APK Signed with Debug Keystore (OWASP M9)
- **Severity:** High | **Category:** Build & Release Integrity
- **Finding:** `android/app/build.gradle` line 103 configures `buildTypes.release` with `signingConfig signingConfigs.debug`.
- **Impact:** The release APK is signed with public debug keys (`androiddebugkey` / password `android`), breaking release authenticity and APK tampering protection.
- **Remedy:** Configure a secure production keystore with credentials injected securely via CI/CD secrets.

### DEF-14: Camera Permission False Negative Bug & Registration Showstopper
- **Severity:** High / Blocker | **Category:** Functional, Hardware/Permissions & User Flow
- **Steps to Reproduce:**
  1. In Android device/emulator settings, grant Camera permission to `StarWarsApp`.
  2. Launch app and tap "Create a new account".
  3. Tap on the camera icon to capture a profile photo.
- **Expected Result:** The live camera viewfinder should activate immediately, allowing the user to take a profile photo.
- **Actual Result:** The screen displays: *"Camera permission is not granted"*, even when permission is already granted in system settings.
- **Root Cause:**
  1. In `RegisterScreen/index.js`, initial permission state is hardcoded to `false` (`useState(false)`). The app never checks existing permission status on mount (`Camera.getCameraPermissionStatus()`).
  2. When switching to `currRegisterPage === 2`, React renders the fallback view (`"Camera permission is not granted"`) before the asynchronous `Camera.requestCameraPermission()` finishes.
  3. On Android systems where permission was already granted, `requestCameraPermission()` does not trigger the OS dialog, causing a state desynchronization.
  4. There is no retry button or link to App Settings, permanently blocking the user from taking a photo and completing registration.
- **Developer Remedy:**
  Check existing permission on component mount:
  ```javascript
  useEffect(() => {
    const checkPerm = async () => {
      const status = await Camera.getCameraPermissionStatus();
      setIsCameraPermitted(status === 'granted');
    };
    checkPerm();
  }, []);
  ```

### DEF-15: Client-Side Password Complexity Enforcement on Login & Missing MaxLength
- **Severity:** Medium / High | **Category:** Authentication Architecture, Input Validation & Security (CWE-400 / CWE-1286)
- **Steps to Reproduce:**
  1. Open Login Screen.
  2. Enter valid registered email `luke_skywalker@starwars.com`.
  3. In Password, enter a password without uppercase or symbols, or paste a 20,000+ character string.
  4. Tap LOGIN.
- **Expected Result:**
  - Login fields should enforce maximum character lengths via `maxLength` (e.g., Email: 254, Password: 128).
  - The login screen should NOT re-evaluate creation-time password complexity; it should only verify presence of the password and submit it to the authentication service.
- **Actual Result:**
  - `TextInput` fields on LoginScreen completely lack `maxLength` limitations.
  - `handleLogin()` executes `if (!validatePassword(password))` at line 98, enforcing the full registration complexity regex (`/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/`).
  - Running a complex regex against unbounded long text strings creates a severe risk of **Regular Expression Denial of Service (ReDoS)**, freezing the JavaScript thread on mobile devices.
  - Rejecting passwords client-side leaks policy information and blocks any user whose password may have been grandfathered or migrated.
- **Developer Remedy:**
  1. Add `maxLength={254}` to Email input and `maxLength={128}` to Password input.
  2. Remove `validatePassword` check from `LoginScreen.js#L98`:
  ```javascript
  // Remove this block from handleLogin():
  // if (!validatePassword(password)) { ... }
  ```

---

### 6.1 Security Hardening
1. **Hash and Salt Passwords:**
   Never store plaintext passwords in MMKV. If client-side mock storage is necessary for demo purposes, hash passwords using `bcrypt.js` or `PBKDF2` before storage, or use hardware-backed secure storage via `react-native-keychain` / `react-native-encrypted-storage`.
2. **Remove Hardcoded Secrets & Restrict API Keys:**
   Move `com.google.android.geo.API_KEY` to environment variables (`.env` via `react-native-config`). In Google Cloud Console, add package signature (SHA-1) and bundle ID restrictions so the key cannot be abused if decompiled.
3. **Enforce iOS App Transport Security:**
   Remove `NSAllowsArbitraryLoads: true` in `Info.plist`. Whitelist only explicit secure HTTPS domains.
4. **Enable Proguard & Release Signing:**
   In `android/app/build.gradle`:
   ```groovy
   def enableProguardInReleaseBuilds = true
   buildTypes {
       release {
           signingConfig signingConfigs.release // generated production keystore
           minifyEnabled enableProguardInReleaseBuilds
           proguardFiles getDefaultProguardFile("proguard-android.txt"), "proguard-rules.pro"
       }
   }
   ```

### 6.2 Functional & Performance Fixes
1. **Fix Registration Flow & Location Decoupling:**
   Only persist user credentials *after* the entire registration workflow finishes. Make GPS location optional.
2. **Implement Client-Side SWAPI Search:**
   Since `swapi.info` returns static arrays, implement client-side memoized filtering in `SwapiScreen.js`:
   ```javascript
   const filteredData = useMemo(() => {
     if (!searchQuery.trim()) return listSwapiData;
     return listSwapiData.filter(item =>
       item.name.toLowerCase().includes(searchQuery.trim().toLowerCase())
     );
   }, [listSwapiData, searchQuery]);
   ```
3. **Replace Base64 Storage with File Paths:**
   Save camera images to the app's document directory (`RNFS.DocumentDirectoryPath + '/avatars/' + userId + '.jpg'`) and persist only the file path URI.
4. **Dynamic Dimension Hook for Orientation:**
   Replace static `Metrics.SCREEN_WIDTH` with React Native's `useWindowDimensions()` hook:
   ```javascript
   const { width, height } = useWindowDimensions();
   ```

---

## 7. Usability Testing Setup Plan (Test Users & Protocols)

To evaluate the real-world user experience and community creation workflows, a structured usability study is designed below.

### 7.1 Test User Selection & Demographic Justification
A blended pool of **10 test participants** (5 Internal + 5 External) will be recruited:

```
Total Participants: 10
├── Internal Users (5)
│   ├── 2 Mobile Software Engineers (Technical & Edge-Case Validation)
│   ├── 2 Product Managers / Designers (UX Flow & Aesthetic Evaluation)
│   └── 1 Non-Technical Internal Staff (Fresh-Eye Sanity Validation)
└── External Users (5)
    ├── 2 Frequent Mobile Community Users (Discord/Reddit/Meetup enthusiasts)
    ├── 2 Casual Star Wars Fans (Domain Relevance & Tone Check)
    └── 1 Low-Tech Savvy User (Accessibility & Form Friction Test)
```

**Justification:**
- *Internal Users* provide rapid feedback on technical edge cases, design consistency against the Adobe XD spec, and boundary errors without confidentiality risks.
- *External Users* reveal true user mental models, unbiased friction points (e.g. hesitation when asked for GPS permission on login), and organic onboarding reactions. Nielsen's research demonstrates that 5 external test users identify over 80% of major usability roadblocks.

### 7.2 Usability Testing Methodology
- **Format:** 45-minute moderated 1-on-1 sessions (in-person or screen-shared via Zoom/Google Meet).
- **Core User Tasks:**
  1. *Task 1:* Create a new account, select your favorite Star Wars character, and set up your avatar.
  2. *Task 2:* Create a new community group called "Rebel Alliance", pick a starship, and invite a friend by email.
  3. *Task 3:* Switch language to Indonesian, locate an incoming invitation, and successfully join the group.
- **Evaluation Metrics:**
  - **Task Completion Rate (TCR):** Target >= 90%.
  - **Time On Task (TOT):** Benchmark against design baseline.
  - **System Usability Scale (SUS):** 10-question standardized questionnaire administered post-session. Target score: >= 75 (Grade B+).

---

## 8. Regression Testing Strategy

To ensure that future updates, bug fixes, or new features do not destabilize existing functionality, a structured regression testing strategy is implemented.

```
       / \
      / E2E \       Level 3: End-to-End Regression (Detox / Maestro)
     /-------\      Run on nightly builds / release candidate branches.
    / Component\    Level 2: Component & Integration Tests (React Native Testing Library)
   /-------------\  Run on Pull Requests.
  /   Unit Tests   \Level 1: Fast Automated Unit & Contract Tests (Jest + Node Runner)
 /------------------\Run on every commit (Pre-commit hook).
```

### 8.1 Regression Suite Categorization
1. **Smoke Test Suite (P0 - Critical Path):**
   - Duration: < 5 minutes.
   - Executed on every Pull Request.
   - Tests: Registration, Login, Group Creation, Core Navigation.
2. **Full Regression Suite (P1/P2 - Exhaustive):**
   - Duration: ~25 minutes.
   - Executed prior to sprint releases or major refactors.
   - Tests: Edge-case inputs, i18n key synchronization, permission denials, offline state resilience, orientation toggles.

### 8.2 CI/CD Integration
- Implement **GitHub Actions** pipeline with automated gates:
  - Step 1: Code Linting & Type Checking (`eslint`, `tsc --noEmit`).
  - Step 2: Automated QA Suite (`node qa-test-suite/runner.js`).
  - Step 3: Jest Unit & Component Tests (`npm test`).
  - Step 4: Build artifact verification for Android APK and iOS bundle.

---

## 9. Conclusion & Action Plan for Remaining Tasks

The StarWars React Native application features a solid architectural foundation utilizing React Query, MMKV, and i18next. However, critical gaps exist around security (plaintext password storage), missing features (image gallery upload, interactive map), and usability blockers (mandatory GPS on login).

### Action Plan:
1. **Immediate (Days 1–2):** Resolve DEF-01 (registration data integrity) and DEF-04 (make login GPS optional). Patch security flaws by encrypting MMKV and removing hardcoded API keys.
2. **Intermediate (Days 3–4):** Implement client-side filtering on `SwapiScreen` and restore `MapView` with an environment-based API key. Add image library selection via `react-native-image-picker`.
3. **Pre-Release (Days 5–7):** Replace Base64 storage with local file URIs, refactor `Metrics` using `useWindowDimensions()`, and run the automated regression suite across target iOS and Android devices.
