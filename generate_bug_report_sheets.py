import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import csv

wb = openpyxl.Workbook()

# Color schemes
HEADER_FILL = PatternFill(start_color="843C0C", end_color="843C0C", fill_type="solid") # Dark Rust/Brown for Bugs
HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=16, bold=True, color="843C0C")
SUBTITLE_FONT = Font(name="Calibri", size=11, italic=True, color="595959")
SECTION_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
SECTION_FONT = Font(name="Calibri", size=11, bold=True, color="843C0C")

CRITICAL_FILL = PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid")
CRITICAL_FONT = Font(name="Calibri", size=10, bold=True, color="C00000")
HIGH_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
HIGH_FONT = Font(name="Calibri", size=10, bold=True, color="B25900")
MED_FILL = PatternFill(start_color="EDEDED", end_color="EDEDED", fill_type="solid")
MED_FONT = Font(name="Calibri", size=10, color="595959")

THIN_BORDER = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

# ----------------------------------------------------
# SHEET 1: DEFECT DASHBOARD
# ----------------------------------------------------
ws_dash = wb.active
ws_dash.title = "Bug Metrics & Summary"
ws_dash.views.sheetView[0].showGridLines = True

ws_dash["A1"] = "STARWARS MOBILE APPLICATION - OFFICIAL QA DEFECT & BUG REPORT"
ws_dash["A1"].font = TITLE_FONT
ws_dash["A2"] = "Format: IEEE 829 / Jira Standard with Code & Storage Evidence | Date: October 2026"
ws_dash["A2"].font = SUBTITLE_FONT

headers_dash = ["Defect Severity Level", "Total Count", "% of Total Bugs", "Recommended Action / Priority"]
for col_idx, h in enumerate(headers_dash, start=1):
    cell = ws_dash.cell(row=4, column=col_idx, value=h)
    cell.fill = HEADER_FILL
    cell.font = HEADER_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center")

severity_summary = [
    ["Critical / Blocker (P1)", 2, "=ROUND(B5/B9*100, 1)", "Immediate hotfix required; blocks release/onboarding"],
    ["High Severity (P1 / P2)", 8, "=ROUND(B6/B9*100, 1)", "Fix in current sprint; breaks core features/security"],
    ["Medium Severity (P2)", 6, "=ROUND(B7/B9*100, 1)", "Fix before production launch; input/data limits"],
    ["Low Severity / Usability (P3)", 3, "=ROUND(B8/B9*100, 1)", "UI polish, alignment, and cosmetic improvements"],
    ["TOTAL DEFECTS LOGGED", "=SUM(B5:B8)", "=ROUND(SUM(C5:C8), 0)", "19 Confirmed Defects & Security Vulnerabilities"]
]

row_idx = 4
for r in severity_summary:
    row_idx += 1
    for c_idx, val in enumerate(r, start=1):
        cell = ws_dash.cell(row=row_idx, column=c_idx, value=val)
        cell.border = THIN_BORDER
        if row_idx == 9:
            cell.font = Font(name="Calibri", size=11, bold=True)
            cell.fill = SECTION_FILL
        if c_idx in [2, 3]:
            cell.alignment = Alignment(horizontal="center")

# Category summary table
ws_dash["A12"] = "DEFECTS GROUPED BY TESTING DOMAIN"
ws_dash["A12"].font = SECTION_FONT
headers_cat = ["Testing Domain", "Defect Count", "Key Impacted Requirements", "Dominant Risk Area"]
for col_idx, h in enumerate(headers_cat, start=1):
    cell = ws_dash.cell(row=13, column=col_idx, value=h)
    cell.fill = HEADER_FILL
    cell.font = HEADER_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center")

cat_summary = [
    ["1. Security Vulnerabilities (OWASP)", 4, "Req 11 (Auth & Encryption)", "Plaintext credentials in MMKV, hardcoded Google API key"],
    ["2. Functional & Permissions", 6, "Req 1, 2, 4, 7, 8, 9", "Camera permission false negative, search failure, vanishing join button"],
    ["3. Compatibility & Responsive Layout", 2, "Req 12 (Orientation & Tablets)", "Unscrollable landscape screen, frozen startup metrics"],
    ["4. Usability & UX Roadblocks", 4, "Req 3, 10, Task 3", "Mandatory GPS login blocker, misleading chevrons, trapped logout"],
    ["5. Performance & Data Boundaries", 3, "Req 1, 2, 3, Task 4", "Uncompressed Base64 photos, missing maxLength, ReDoS risk"]
]

r_cat = 13
for r in cat_summary:
    r_cat += 1
    for c_idx, val in enumerate(r, start=1):
        cell = ws_dash.cell(row=r_cat, column=c_idx, value=val)
        cell.border = THIN_BORDER
        if c_idx == 2:
            cell.alignment = Alignment(horizontal="center")
            cell.font = Font(name="Calibri", bold=True)

# Dash widths
dash_col_widths = {1: 32, 2: 15, 3: 18, 4: 55}
for col_idx, width in dash_col_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_dash.column_dimensions[col_letter].width = width


# ----------------------------------------------------
# SHEET 2: MASTER BUG LOG WITH EVIDENCE
# ----------------------------------------------------
ws_bugs = wb.create_sheet(title="Defect Log with Evidence")
ws_bugs.views.sheetView[0].showGridLines = True

headers_bugs = [
    "No.",
    "Defect ID",
    "Defect Title / Summary",
    "Req Ref",
    "Category",
    "Severity",
    "Priority",
    "Status",
    "Environment / Device",
    "Steps to Reproduce",
    "Expected Result",
    "Actual Result",
    "Concrete Evidence / Proof / Log Reference",
    "Root Cause Analysis",
    "Developer Fix / Actionable Code Remedy"
]

for col_idx, h in enumerate(headers_bugs, start=1):
    cell = ws_bugs.cell(row=1, column=col_idx, value=h)
    cell.fill = HEADER_FILL
    cell.font = HEADER_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

bugs_data = [
    # 1. SEC-01
    [
        "SEC-01",
        "Plaintext Password Storage in Local MMKV (CWE-312 / OWASP M2)",
        "Req 11",
        "Security",
        "Critical",
        "P1",
        "Open",
        "Android (API 26-37) & iOS",
        "1. Register user: luke_skywalker@starwars.com with pwd m4y_th3_F0rc3_b3_w1th_u\n2. Open Android Studio -> Device Explorer\n3. Navigate to /data/data/com.starwarsapp/files/mmkv/mmkv.default\n4. Open file in text editor",
        "Passwords must be salted and cryptographically hashed (bcrypt/Argon2) or stored in hardware Keystore",
        "Passwords are saved unhashed in 100% clear text in client database",
        "LIVE MMKV STORAGE EXTRACT:\n\"LIST_USER\": [{\"email\":\"luke_skywalker@starwars.com\",\"password\":\"m4y_th3_F0rc3_b3_w1th_u\",\"confirmPassword\":\"m4y_th3_F0rc3_b3_w1th_u\"}]\n\"CURR_USER_LOGIN_DATA\": {\"email\":\"luke_skywalker@starwars.com\",\"password\":\"m4y_th3_F0rc3_b3_w1th_u\"}",
        "RegisterScreen.js#L93 and Storages.js#L7 directly serialize raw password strings to MMKV without hashing or encryption",
        "Use react-native-keychain for secure credential storage, or hash password with bcrypt before saving:\nimport bcrypt from 'bcryptjs';\nconst hashed = bcrypt.hashSync(password, 10);"
    ],

    # 2. DEF-14
    [
        "DEF-14",
        "Camera Permission False Negative Bug & Registration Showstopper",
        "Req 2 & 1",
        "Functional",
        "Blocker",
        "P1",
        "Open",
        "Android 13/14/17 (Medium Phone API 37)",
        "1. In Android App Settings, grant Camera permission to StarWarsApp\n2. Open app -> tap 'Create a new account'\n3. Tap camera avatar icon to take profile photo",
        "Live camera viewfinder activates immediately since permission is already granted",
        "Screen displays: 'Camera permission is not granted'; user cannot take photo, blocking registration completely",
        "DEVICE SCREEN EVIDENCE:\nEmulator displays red fallback text: 'Camera permission is not granted' even though Android permission dialog shows 'Allowed'. User is unable to advance.",
        "1. RegisterScreen.js#L30 hardcodes initial state to false (useState(false))\n2. Camera.getCameraPermissionStatus() is never called on mount\n3. React renders error view before async requestCameraPermission() finishes\n4. On newer Android, requestCameraPermission() doesn't fire when pre-granted",
        "Call Camera.getCameraPermissionStatus() in useEffect on mount to initialize real permission state:\nuseEffect(() => {\n  Camera.getCameraPermissionStatus().then(s => setIsCameraPermitted(s === 'granted'));\n}, []);"
    ],

    # 3. DEF-01
    [
        "DEF-01",
        "User Data Committed Before Location Check Completes (Permanent Registration Lockout)",
        "Req 1",
        "Functional / Integrity",
        "High",
        "P1",
        "Open",
        "Android & iOS",
        "1. Fill valid registration form and photo\n2. Tap Save -> Skip\n3. When Android asks for Location, tap 'Don't allow' (Deny)",
        "App handles denial gracefully; user data is not corrupted or prematurely registered",
        "User is committed to MMKV before permission resolves; denial redirects to Login; retrying registration shows 'Email is already registered', locking user out",
        "CODE EVIDENCE:\nRegisterScreen.js#L91-93:\nregisteredUsers.push(data);\nStorage.setItem(StorageKey.LIST_USER, registeredUsers);\n// This happens BEFORE requestLocationPermission() at line 95!",
        "Data persistence is called prior to resolving the asynchronous requestLocationPermission() promise",
        "Move Storage.setItem inside the successful resolution branch of the permission/registration chain; do not persist before checks finish"
    ],

    # 4. DEF-04
    [
        "DEF-04",
        "Mandatory Location Permission Blocks User Login (Hostile Access Gate)",
        "Req 3",
        "Usability / Auth",
        "High",
        "P1",
        "Open",
        "Android & iOS",
        "1. Enter valid email and password on Login Screen\n2. Deny location permission or turn off GPS\n3. Tap LOGIN",
        "User logs in successfully; location-based features degrade gracefully",
        "User is strictly blocked from logging in; error toast: 'You must allow location permission on this app to login'",
        "TOAST EVIDENCE:\nToast alert: 'You must allow location permission on this app to login'. Login flow halts and button shows loading or resets without logging in.",
        "LoginScreen.js#L114-116: fetchLogin() is nested inside requestLocationPermission().then(). Denying permission branches to error toast and aborts login",
        "Decouple GPS location from authentication. Allow login to proceed and request location contextually when opening group maps"
    ],

    # 5. DEF-08
    [
        "DEF-08",
        "Landscape Screen Completely Unscrollable & UI Stuck (Missing ScrollView)",
        "Req 12",
        "Compatibility",
        "High",
        "P2",
        "Open",
        "Android & iOS (Landscape orientation)",
        "1. Open LoginScreen or ProfileScreen\n2. Rotate device to Landscape (Ctrl+Left Arrow)\n3. Attempt to scroll down with finger/mouse",
        "Content scrolls smoothly, allowing access to input fields and buttons below the fold",
        "Screen cannot scroll; touch gestures produce no action; LOGIN button and Register link are cut off and unreachable",
        "LIVE EMULATOR TEST EVIDENCE:\nIn landscape mode (height ~360px), inputs fill the screen; Login button is pushed off-screen. Swiping vertically does nothing because no ScrollView exists.",
        "LoginScreen/index.js and ProfileScreen/index.js wrap content in static <View> and <SafeAreaView> with flex: 1 and no <ScrollView>",
        "Wrap root containers in ScrollView:\n<ScrollView contentContainerStyle={{ flexGrow: 1 }} showsVerticalScrollIndicator={false}>\n  <View style={styles.inputContainer}> ... </View>\n</ScrollView>"
    ],

    # 6. DEF-05
    [
        "DEF-05",
        "'Join Group' Button Disappears in Indonesian Locale",
        "Req 7 & 13",
        "Functional / I18n",
        "High",
        "P2",
        "Open",
        "Android & iOS",
        "1. User invited to group\n2. Switch app language to Indonesian (ID)\n3. Open 'Grup Belum Bergabung' -> open group detail",
        "'Bergabung ke Grup' (Join Group) button is visible and allows user to join",
        "Join Group button completely disappears from the screen",
        "CODE EVIDENCE:\nGroupDetailScreen/index.js#L133:\nactiveTab === t('groupDetail.unjoinedTab')\nIn Indonesian, activeTab is passed as English 'Unjoined Group' from state, while t() evaluates to 'Grup Belum Bergabung'. Condition is false!",
        "Hardcoded UI display string comparison for functional state routing instead of language-agnostic tab enum",
        "Use invariant enum for active tab state:\nconst TAB_KEY = { JOINED: 'JOINED', UNJOINED: 'UNJOINED' };\n{activeTabKey === TAB_KEY.UNJOINED && <JoinButton />}"
    ],

    # 7. DEF-11
    [
        "DEF-11",
        "Unconstrained Image Capture Size & Uncompressed Base64 Memory Bloat",
        "Req 2 & Task 4",
        "Performance / Resource",
        "High",
        "P2",
        "Open",
        "Android & iOS",
        "1. Capture photo on modern camera (e.g. 48MP+ sensor)\n2. Register and create groups\n3. Inspect MMKV storage payload",
        "Photo is cropped (300x300), compressed (<200KB), and stored as a file path URI",
        "Entire raw camera photo converted to massive Base64 string stored in MMKV, causing severe RAM bloat and Out-Of-Memory (OOM) crashes",
        "MMKV STORAGE EVIDENCE:\n\"photo\": \"/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJ...\" (String length: 150,000+ characters for a single user!). In groups with 10 members, FlatList crashes.",
        "RegisterScreen.js#L187 reads raw snapshot with RNFS.readFile(filePath, 'base64') and saves full blob to storage and state",
        "Crop images to avatar square (300x300), compress JPEG (<150KB), and persist only file paths (file:///data/.../avatar.jpg), never raw Base64"
    ],

    # 8. DEF-07
    [
        "DEF-07",
        "Orientation Change Distorts Layout & Pie Chart Due to Frozen Metrics",
        "Req 12",
        "Compatibility",
        "High",
        "P2",
        "Open",
        "Android & iOS (Landscape orientation)",
        "1. Open Group Home Screen with groups\n2. Rotate device to Landscape",
        "UI reflows dynamically; PieChart and cards scale proportionally to screen height/width",
        "Bottom tab bar becomes giant (~120px); PieChart retains portrait width (400px), overflowing the 360px landscape height and distorting layout",
        "CODE EVIDENCE:\nGlobalConfig.js#L15:\nexport const Metrics = Object.freeze({\n  SCREEN_WIDTH: Dimensions.get('window').width,\n  SCREEN_HEIGHT: Dimensions.get('window').height,\n});\nEvaluated once at boot!",
        "Static Object.freeze on Dimensions.get('window') causes metrics to remain stale after orientation changes",
        "Replace static Metrics with React Native's dynamic hook:\nconst { width, height } = useWindowDimensions();"
    ],

    # 9. SEC-02
    [
        "SEC-02",
        "Hardcoded Production Google Maps API Key in AndroidManifest.xml (OWASP M1/M9)",
        "Req 11",
        "Security",
        "High",
        "P2",
        "Open",
        "Android",
        "1. Decompile APK or inspect AndroidManifest.xml\n2. Search for com.google.android.geo.API_KEY",
        "Secrets should be injected via secure build environment variables (.env) with restricted API access",
        "Production API key AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-vwk97mdA is exposed in clear text in manifest",
        "MANIFEST EVIDENCE:\nAndroidManifest.xml line 54-55:\n<meta-data android:name=\"com.google.android.geo.API_KEY\" android:value=\"AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-vwk97mdA\"/>",
        "API key was hardcoded in version control instead of using react-native-config or gradle build properties",
        "Move key to .env file and apply package name and SHA-1 certificate fingerprint restrictions in Google Cloud Console"
    ],

    # 10. SEC-03
    [
        "SEC-03",
        "Insecure iOS TLS Configuration via NSAllowsArbitraryLoads = true (OWASP M3)",
        "Req 11",
        "Security",
        "High",
        "P2",
        "Open",
        "iOS",
        "1. Open ios/StarWarsApp/Info.plist\n2. Inspect NSAppTransportSecurity dictionary",
        "NSAllowsArbitraryLoads must be false; strict HTTPS enforced across network calls",
        "NSAllowsArbitraryLoads is set to true, completely disabling Apple Transport Security TLS enforcement",
        "PLIST EVIDENCE:\nInfo.plist lines 28-32:\n<key>NSAppTransportSecurity</key>\n<dict>\n  <key>NSAllowsArbitraryLoads</key>\n  <true/>\n</dict>",
        "Insecure App Transport Security configuration allows arbitrary plaintext HTTP traffic susceptible to MITM attacks",
        "Set NSAllowsArbitraryLoads to false and enforce strict HTTPS domains"
    ],

    # 11. SEC-04
    [
        "SEC-04",
        "Release APK Configured to Sign with Debug Keystore in build.gradle (OWASP M9)",
        "Req 11",
        "Security / Release",
        "High",
        "P2",
        "Open",
        "Android",
        "1. Open android/app/build.gradle\n2. Inspect buildTypes.release signingConfig",
        "Release APK must be signed with private production keystore with credentials managed in CI secrets",
        "Release build signs with debug.keystore (androiddebugkey / password 'android')",
        "GRADLE EVIDENCE:\nandroid/app/build.gradle lines 100-104:\nbuildTypes {\n  release {\n    signingConfig signingConfigs.debug // CAUTION: Uses debug.keystore!\n  }\n}",
        "Release build type erroneously configured with debug signing configuration, compromising APK authenticity",
        "Create dedicated production keystore and inject keystore password via CI/CD environment variables"
    ],

    # 12. DEF-02
    [
        "DEF-02",
        "Missing Photo Library / Gallery Upload Option (Req 2 Violation)",
        "Req 2",
        "Functional",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. Open Register Screen\n2. Tap avatar camera icon\n3. Look for option to choose from Photo Library / Gallery",
        "User should be able to select photo from either Camera OR Photo Library as specified in Requirement 2",
        "Only Vision Camera opens; photo library option is completely absent from code",
        "CODE EVIDENCE:\nRegisterScreen/index.js lines 270-275:\n<TouchableOpacity onPress={() => setCurrRegisterPage(2)} style={styles.defaultImage}>\nDirectly transitions to page 2 (camera). No image picker dialog or library integration exists.",
        "Developers only implemented Vision Camera snapshot and skipped react-native-image-picker integration",
        "Integrate react-native-image-picker with an ActionSheet allowing user to pick between 'Camera' or 'Photo Library'"
    ],

    # 13. DEF-03
    [
        "DEF-03",
        "SWAPI Search Query Parameter Ignored on Static Mirror",
        "Req 4 & 9",
        "Functional / Integration",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. Open SwapiScreen for role or starship selection\n2. Type 'Luke' or 'Falcon' in search bar",
        "List dynamically filters to show only matching characters/starships",
        "Static mirror ignores ?search=; frontend lacks client-side filter; all 82 items remain visible",
        "API LOG EVIDENCE:\nGET https://swapi.info/api/people/?search=Luke returns all 82 records! SwapiScreen.js directly sets listSwapiData to returned array without filtering.",
        "swapi.info is a static JSON file mirror that does not support server-side query filtering",
        "Implement client-side memoized filtering in SwapiScreen.js:\nconst filtered = list.filter(i => i.name.toLowerCase().includes(query.toLowerCase()));"
    ],

    # 14. DEF-06
    [
        "DEF-06",
        "Interactive MapView Commented Out in GroupDetailScreen (Req 8 Violation)",
        "Req 8",
        "Functional",
        "Medium",
        "P3",
        "Open",
        "Android & iOS",
        "1. Open Group Detail screen with joined members\n2. Inspect member location section",
        "Interactive map displays pins for members' last known GPS locations as per Requirement 8",
        "MapView is commented out; only plain raw coordinate numbers are shown",
        "CODE EVIDENCE:\nGroupDetailScreen/index.js lines 111-131:\n{/* Paid Account API Key needed */}\n{/* {selectedMember && selectedMember.lastLocation && (\n  <MapView style={styles.map} ...>\n)} */}",
        "Developer commented out MapView component due to unconfigured Google Maps billing API key",
        "Restore MapView component and provide configured Google Maps API key via environment variables"
    ],

    # 15. DEF-09
    [
        "DEF-09",
        "Unbounded Input Length / Missing Character Limits on Registration & Login (CWE-400)",
        "Req 1 & 3",
        "Data Validation / Security",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. Paste 10,000+ characters into First Name, Last Name, Email, or Password\n2. Tap Save or Login",
        "Inputs enforce sensible character limits via maxLength (Name: 50, Email: 254, Password: 128)",
        "Inputs lack maxLength prop; accepts unlimited characters, causing UI breakage and storage bloat",
        "CODE EVIDENCE:\nRegisterScreen/index.js line 284-292 and LoginScreen/index.js line 153-166:\n<TextInput style={styles.input} ... />\nNotice: Neither has maxLength property! handleSave() also has no length checks.",
        "Missing maxLength attribute on TextInput components and lack of boundary length checks in validation functions",
        "Add maxLength prop to all inputs: <TextInput maxLength={50} ... /> and check length bounds in handleSave"
    ],

    # 16. DEF-15
    [
        "DEF-15",
        "Client-Side Password Complexity Enforcement on Login & Missing MaxLength",
        "Req 3",
        "Architecture / Security",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. On Login Screen, enter registered email\n2. In Password, paste a 20,000+ character string or enter non-complex password\n3. Tap LOGIN",
        "Login screen should not re-evaluate creation complexity regex; should only check password presence and send to auth service",
        "handleLogin() executes validatePassword() regex client-side, risking ReDoS freeze on long inputs and blocking grandfathered users",
        "CODE EVIDENCE:\nLoginScreen/index.js lines 98-101:\nif (!validatePassword(password)) {\n  toast.current.ShowToastFunction('error', t('common.passwordValidation'));\n  return;\n}",
        "Flawed authentication architecture where registration password creation rules are erroneously re-checked during login",
        "Remove validatePassword check from handleLogin() in LoginScreen.js#L98"
    ],

    # 17. DEF-10
    [
        "DEF-10",
        "Inconsistent Text Right-Alignment & Misleading Chevron Icons in Form",
        "Req 10 / Task 3",
        "Usability / Form Design",
        "Low",
        "P3",
        "Open",
        "Android & iOS",
        "1. Open Register Screen\n2. Type text in First Name, Email, Password",
        "Inputs follow standard left-aligned conventions (textAlign: 'left'); chevrons only on sub-page links",
        "Inputs force textAlign: 'right' with label on far left; every text input has misleading chevron (>) arrow",
        "STYLE EVIDENCE:\nRegisterScreen/styles.js lines 43-48:\ninput: { flex: 2, textAlign: 'right' }\nRegisterScreen/index.js line 293:\n<Ionicons name=\"chevron-forward\" size={20} /> on every input row!",
        "Confusing form styling that misuses navigation chevron icons on simple text inputs and forces right-aligned text",
        "Set textAlign: 'left' on input fields and remove chevron-forward icons from text entry rows"
    ],

    # 18. DEF-12
    [
        "DEF-12",
        "Split-Column Edge Alignment & Trapped Logout Button in Landscape on Profile Screen",
        "Req 4 & 12",
        "Usability / Responsive",
        "Medium",
        "P3",
        "Open",
        "Android & iOS",
        "1. Open Profile Screen\n2. Rotate device to Landscape\n3. Attempt to log out",
        "Particulars align cleanly without giant gap; screen scrolls smoothly to reach Logout button",
        "Particulars forced to far opposite edges; in landscape, Logout button is pushed off-screen with no way to scroll",
        "STYLE EVIDENCE:\nProfileScreen/styles.js lines 18-23:\nprofileDetail: { flexDirection: 'row', justifyContent: 'space-between' }\nProfileScreen/index.js has no <ScrollView> container!",
        "Missing ScrollView wrapper on ProfileScreen combined with unconstrained justifyContent: 'space-between'",
        "Wrap ProfileScreen in ScrollView and use left-aligned detail rows with flexShrink: 1"
    ],

    # 19. DEF-13
    [
        "DEF-13",
        "Phantom Scrolling on Empty Group State in Landscape Due to Hardcoded Padding",
        "Req 10 & 12",
        "Layout Polish",
        "Low",
        "P3",
        "Open",
        "Android & iOS (Landscape orientation)",
        "1. Open Group Home Screen with zero unjoined groups\n2. Rotate to Landscape\n3. Swipe vertically",
        "Empty state placeholder should be centered and stationary without requiring scrolling",
        "Empty state scrolls vertically because paddingTop is hardcoded to 200px, pushing icon past viewport",
        "STYLE EVIDENCE:\nGroupHomeScreen/styles.js line 77:\nemptyStateContainer: { flex: 1, paddingTop: Metrics.SCREEN_WIDTH / 2 (200px) }\nTotal height is ~380px, exceeding the 360px landscape viewport!",
        "Hardcoding paddingTop using screen width creates oversized layout on landscape devices",
        "Use flex centering (justifyContent: 'center') instead of static paddingTop: Metrics.SCREEN_WIDTH / 2"
    ]
]

# Add sequential index (1 to 19) to bugs_data
bugs_data_with_no = [[idx + 1] + bug for idx, bug in enumerate(bugs_data)]

row_idx_bugs = 2
for bug in bugs_data_with_no:
    for c_idx, val in enumerate(bug, start=1):
        cell = ws_bugs.cell(row=row_idx_bugs, column=c_idx, value=val)
        cell.border = THIN_BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        
        # Center align short columns (No, Defect ID, Req, Category, Severity, Priority, Status)
        if c_idx in [1, 2, 4, 5, 6, 7, 8]:
            cell.alignment = Alignment(horizontal="center", vertical="top")
        
        # Severity coloring
        if c_idx == 6:
            if val in ["Critical", "Blocker"]:
                cell.fill = CRITICAL_FILL
                cell.font = CRITICAL_FONT
            elif val == "High":
                cell.fill = HIGH_FILL
                cell.font = HIGH_FONT
            elif val == "Medium":
                cell.fill = MED_FILL
                cell.font = MED_FONT

    row_idx_bugs += 1

# Column widths for Master Bug Log
bug_col_widths = {
    1: 6,   # No.
    2: 14,  # Defect ID
    3: 32,  # Title
    4: 12,  # Req
    5: 18,  # Category
    6: 14,  # Severity
    7: 10,  # Priority
    8: 12,  # Status
    9: 22,  # Environment
    10: 35, # Steps
    11: 30, # Expected
    12: 35, # Actual
    13: 45, # Evidence
    14: 35, # Root Cause
    15: 40  # Fix
}

for col_idx, width in bug_col_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_bugs.column_dimensions[col_letter].width = width

# Set Defect Log with Evidence as the active (default open) sheet
wb.active = ws_bugs

# Save Excel Bug Report
bug_excel_path = "C:/Users/HP/Desktop/StarWar/StarWars_QA_Bug_Report.xlsx"
wb.save(bug_excel_path)
print("Bug Report Excel generated successfully:", bug_excel_path)

# Also save CSV version
bug_csv_path = "C:/Users/HP/Desktop/StarWar/StarWars_QA_Bug_Report.csv"
try:
    with open(bug_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers_bugs)
        writer.writerows(bugs_data_with_no)
    print("Bug Report CSV generated successfully:", bug_csv_path)
except PermissionError:
    print("Notice: StarWars_QA_Bug_Report.csv is currently open in Excel. Please close it if you want to overwrite the CSV as well.")
