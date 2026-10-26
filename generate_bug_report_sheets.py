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
    "Description",
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
        "User Passwords Saved in Plain Text Without Encryption",
        "When a user registers or logs into the app, their password is saved in local phone storage as completely unencrypted plain text. Any person or malicious app with physical or ADB file access can read all stored passwords without needing any decryption keys.",
        "Req 11",
        "Security",
        "Critical",
        "P1",
        "Open",
        "Android (API 26-37) & iOS",
        "1. Register a new user (e.g. luke_skywalker@starwars.com)\n2. Open Android Studio -> Device File Explorer\n3. Go to /data/data/com.starwarsapp/files/mmkv/mmkv.default\n4. Open the file in a text editor",
        "Passwords should be securely encrypted (hashed with bcrypt or stored in Android Keystore / iOS Keychain) so no one can read them.",
        "The password is saved in 100% readable plain text directly in the phone's storage.",
        "LIVE STORAGE PROOF:\nInside 'mmkv.default' file:\nCURR_USER_LOGIN_DATA: { email: 'luke_skywalker@starwars.com', password: '[RAW_PLAINTEXT_PASSWORD]' }\nAnyone with USB debugging can view everyone's password in plain text.",
        "The registration code directly writes the user's password string into MMKV without hashing or encrypting it first.",
        "Use 'react-native-keychain' for secure hardware storage, or hash the password using bcrypt before saving it."
    ],

    # 2. DEF-14
    [
        "DEF-14",
        "Camera Screen Shows 'Permission Not Granted' Even When Allowed (Blocks Registration)",
        "Even after a user grants camera permissions in the Android system settings, opening the camera inside the app immediately displays a black screen with an error saying 'Camera permission is not granted'. This prevents the user from taking a profile photo and completely blocks account registration.",
        "Req 2 & 1",
        "Functional",
        "Blocker",
        "P1",
        "Open",
        "Android 13/14/17 (Emulator & Physical Devices)",
        "1. In phone Settings -> Apps -> StarWarsApp, grant Camera permission\n2. Open the app and tap 'Create a new account'\n3. Tap the camera avatar to take a profile picture",
        "The camera should open smoothly and show the viewfinder so the user can take a photo.",
        "The screen turns black and shows a red error: 'Camera permission is not granted'. The user cannot take a photo and cannot complete registration.",
        "SCREEN PROOF:\nPhone displays 'Camera permission is not granted' despite Camera permission being set to 'Allowed' in Android system settings.",
        "The camera screen sets its initial permission status to 'false' (useState(false)) and does not check the existing permission status when the screen first loads.",
        "Check existing camera permission when the screen opens using Camera.getCameraPermissionStatus() inside a useEffect hook."
    ],

    # 3. DEF-01
    [
        "DEF-01",
        "Denying Location During Registration Permanently Locks Out the User's Email",
        "During account registration, the application saves the user's account details into storage before the location permission dialog is answered. If the user taps 'Deny' on location, the registration aborts, but their email is permanently saved, blocking them from ever registering again with that email.",
        "Req 1",
        "Functional",
        "High",
        "P1",
        "Open",
        "Android & iOS",
        "1. Fill out the registration form and take a photo\n2. Tap Save -> Skip group creation\n3. When the phone asks for Location permission, tap 'Don't allow' (Deny)",
        "If location is denied, the registration should be cancelled cleanly without saving corrupted data.",
        "The app saves the user's email into storage BEFORE checking location. Denying location throws an error and returns to login. Trying to register again shows: 'Email is already registered', permanently locking the user out.",
        "CODE PROOF:\nIn RegisterScreen/index.js lines 91-95:\nThe app calls Storage.setItem(LIST_USER) to save the user BEFORE it waits for the location permission prompt to finish.",
        "The app saves the user into the database before confirming whether all required permissions were granted.",
        "Only save the user to storage after all permissions and steps have completed successfully."
    ],

    # 4. DEF-04
    [
        "DEF-04",
        "App Blocks User from Logging In if Location (GPS) Permission is Denied",
        "The login screen strictly requires active GPS location access before allowing a user to sign in. If a user has GPS disabled or denies location permission, the app refuses to log them in, preventing legitimate users from accessing their account.",
        "Req 3",
        "Usability / Auth",
        "High",
        "P1",
        "Open",
        "Android & iOS",
        "1. Enter correct registered email and password on Login screen\n2. Turn off GPS or tap 'Don't allow' on the location prompt\n3. Tap LOGIN button",
        "The user should be logged into the app. Location should only be requested when opening map features.",
        "Login is strictly blocked. An error toast says: 'You must allow location permission on this app to login'.",
        "TOAST ERROR PROOF:\nToast alert appears: 'You must allow location permission on this app to login'. User is stuck on the login screen.",
        "The login function is wrapped inside the location request, forcing GPS access just to view the home screen.",
        "Separate login from location. Let the user log in first, and only ask for GPS when they open group maps."
    ],

    # 5. DEF-08
    [
        "DEF-08",
        "Screen Gets Stuck and Cannot Scroll When Phone is in Landscape Mode",
        "When the phone is rotated into landscape mode on the login or profile screen, the interface cannot be scrolled vertically. Essential action buttons like 'LOGIN' and 'Register' get pushed below the visible screen area and cannot be reached by the user.",
        "Req 12",
        "Compatibility",
        "High",
        "P2",
        "Open",
        "Android & iOS (Landscape / Tablet)",
        "1. Open Login screen or Profile screen\n2. Rotate the phone sideways to Landscape mode\n3. Try to swipe up or down with your finger",
        "The screen should scroll smoothly so the user can reach buttons below the bottom of the screen.",
        "The screen is frozen and cannot scroll. The LOGIN button and Register link are pushed off-screen and cannot be clicked.",
        "TEST PROOF:\nIn landscape mode (height ~360px), input boxes fill the whole screen. The LOGIN button is invisible below the fold and touch swiping does nothing.",
        "The screens use static <View> containers instead of a scrollable <ScrollView> container.",
        "Wrap the screen contents in a <ScrollView contentContainerStyle={{ flexGrow: 1 }}>."
    ],

    # 6. DEF-05
    [
        "DEF-05",
        "'Join Group' Button Disappears When Language is Switched to Indonesian",
        "When the application language is switched to Indonesian, the 'Join Group' button completely disappears from the group details screen. This prevents Indonesian-speaking users from joining any community groups.",
        "Req 7 & 13",
        "Functional / Localization",
        "High",
        "P2",
        "Open",
        "Android & iOS",
        "1. Switch the app language to Indonesian (ID)\n2. Navigate to 'Grup Belum Bergabung' (Unjoined Groups)\n3. Tap on any group to view group details",
        "A 'Bergabung ke Grup' (Join Group) button should be visible at the bottom so the user can join the group.",
        "The 'Join Group' button completely disappears from the screen in Indonesian.",
        "CODE PROOF:\nIn GroupDetailScreen/index.js line 133:\nThe code checks `activeTab === t('groupDetail.unjoinedTab')`. In Indonesian, activeTab remains English 'Unjoined Group', but t() is translated to Indonesian, causing the check to fail.",
        "The app compares translated user-interface text to decide whether to show a button, instead of using a standard language-independent status code.",
        "Use a language-independent code like 'UNJOINED' instead of comparing translated screen text."
    ],

    # 7. DEF-11
    [
        "DEF-11",
        "App Runs Slow and Crashes Because Profile Photos Are Stored as Giant Text",
        "Profile pictures captured by the camera are saved into local storage as enormous uncompressed Base64 text strings containing over 150,000 characters per user. As more users join groups, this causes severe memory lag and crashes the app with Out-Of-Memory errors.",
        "Req 2 & Task 4",
        "Performance / Memory",
        "High",
        "P2",
        "Open",
        "Android & iOS",
        "1. Take a photo using the camera\n2. Complete registration\n3. Inspect the saved user data in phone storage",
        "Profile photos should be compressed (<150 KB) and saved as a file link (e.g. file:///avatar.jpg).",
        "The full raw photo is converted into a giant text string (150,000+ characters) and saved directly in memory. Loading multiple group members causes the app to lag and crash with Out-Of-Memory errors.",
        "STORAGE PROOF:\nIn 'mmkv.default': \"photo\": \"/9j/4AAQSkZJRgABAQ...\" (over 150,000 characters for a single user!).",
        "The camera screen reads the full uncompressed image into a Base64 text string instead of saving a compressed image file.",
        "Compress the photo to a small 300x300 JPEG and save the file path URI, never raw Base64 text."
    ],

    # 8. DEF-07
    [
        "DEF-07",
        "Rotating Phone Between Portrait and Landscape Distorts Layout and Pie Chart",
        "Screen dimensions are measured and permanently frozen only once when the app launches. When the user rotates their device between portrait and landscape, the screen measurements do not update, causing the layout, pie charts, and navigation bars to distort and overflow.",
        "Req 12",
        "Compatibility",
        "High",
        "P2",
        "Open",
        "Android & iOS",
        "1. Open Group Home screen with active groups\n2. Rotate the phone sideways to Landscape mode",
        "The layout and Pie Chart should resize cleanly to fit the wider screen.",
        "The bottom menu becomes gigantic (~120px tall) and the Pie Chart stays stretched to portrait size (400px wide), overflowing and cutting off screen content.",
        "CODE PROOF:\nIn Metrics.js line 16:\nScreen width and height are frozen once when the app starts using Object.freeze(). They never update when the phone rotates.",
        "Screen dimensions are calculated only once at app startup and frozen, so rotation values are never updated.",
        "Use React Native's dynamic `useWindowDimensions()` hook instead of frozen static numbers."
    ],

    # 9. SEC-02
    [
        "SEC-02",
        "Secret Google Maps API Key is Hardcoded and Exposed in App Code",
        "The production Google Maps API key is hardcoded directly in the public Android manifest file. Because there are no restrictions on the key, anyone can decompile the APK, steal the API key, and incur unauthorized billing charges.",
        "Req 11",
        "Security",
        "High",
        "P2",
        "Open",
        "Android",
        "1. Open the Android project configuration file (AndroidManifest.xml)\n2. Search for 'com.google.android.geo.API_KEY'",
        "Secret API keys should be hidden inside secure environment files (.env) and protected by Google Cloud restrictions.",
        "The live production Google Maps API key is written directly in the open code: AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-********.",
        "CODE PROOF:\nIn AndroidManifest.xml line 54:\n<meta-data android:name=\"com.google.android.geo.API_KEY\" android:value=\"AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-********\"/>",
        "The developer pasted the production API key directly into the public manifest file instead of using secure environment variables.",
        "Move the API key into a .env file and add app package and fingerprint restrictions in Google Cloud Console."
    ],

    # 10. SEC-03
    [
        "SEC-03",
        "Insecure HTTP Connections Allowed on iOS Devices (ATS Disabled)",
        "The iOS configuration file has Apple Transport Security disabled (NSAllowsArbitraryLoads is set to true). This allows the application to communicate over insecure, unencrypted HTTP connections, exposing user data to eavesdropping on public Wi-Fi networks.",
        "Req 11",
        "Security",
        "High",
        "P2",
        "Open",
        "iOS",
        "1. Open the iOS configuration file (ios/StarWarsApp/Info.plist)\n2. Search for NSAppTransportSecurity",
        "The app should enforce secure encrypted HTTPS connections for all network traffic (NSAllowsArbitraryLoads = false).",
        "Security settings have NSAllowsArbitraryLoads set to 'true', allowing unencrypted HTTP traffic that hackers can intercept on public Wi-Fi.",
        "CODE PROOF:\nIn Info.plist lines 28-32:\n<key>NSAllowsArbitraryLoads</key>\n<true/>",
        "Apple's App Transport Security (ATS) was completely turned off in the project configuration.",
        "Set NSAllowsArbitraryLoads to false and only use secure HTTPS endpoints."
    ],

    # 11. SEC-04
    [
        "SEC-04",
        "Release App is Signed with an Insecure Test Key Instead of a Production Key",
        "The production release build of the Android app is configured to be signed with the public debug keystore instead of an official secure production key. This compromises the authenticity and integrity of the published app.",
        "Req 11",
        "Security / Build",
        "High",
        "P2",
        "Open",
        "Android",
        "1. Open android/app/build.gradle\n2. Inspect the release build configuration (buildTypes.release)",
        "Production release builds must be signed with a private, password-protected production key.",
        "The release build is configured to sign with 'debug.keystore' (the default public test key with password 'android').",
        "CODE PROOF:\nIn android/app/build.gradle lines 100-104:\nbuildTypes {\n  release {\n    signingConfig signingConfigs.debug\n  }\n}",
        "The build file was accidentally left pointing to the debug keystore for production releases.",
        "Create a dedicated release keystore and keep the signing credentials secure in build environment variables."
    ],

    # 12. DEF-02
    [
        "DEF-02",
        "Cannot Pick Profile Photos from Phone Gallery (Only Camera Available)",
        "Requirement 2 specifies that users should be able to upload profile pictures from either the camera or the photo library. However, the app only opens the camera and provides no option to pick existing photos from the device gallery.",
        "Req 2",
        "Functional",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. Open the Registration screen\n2. Tap the avatar icon to add a profile photo",
        "As required by Requirement 2, the user should be given a choice to either 'Take Photo' with camera OR 'Choose from Gallery'.",
        "The app immediately forces open the camera. There is no button or option to choose an existing picture from the phone gallery.",
        "CODE PROOF:\nIn RegisterScreen/index.js lines 270-275:\nTapping the avatar directly switches to the camera page without offering a gallery picker.",
        "The developers only built the camera feature and forgot to build the photo library picker.",
        "Add an option dialog (ActionSheet) asking the user: 'Take Photo' or 'Choose from Gallery', using react-native-image-picker."
    ],

    # 13. DEF-03
    [
        "DEF-03",
        "Character Search Does Not Filter Results (Always Shows All 82 People)",
        "The search input on character and starship selection screens fails to filter results. Because the public SWAPI mirror is a static file host that ignores URL search queries, typing any name continues to display all 82 items in the list.",
        "Req 4 & 9",
        "Functional",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. Open the character or starship selection screen\n2. Type 'Luke' into the search bar",
        "The list should instantly filter to show only characters named 'Luke'.",
        "The search bar does nothing. The screen continues to show all 82 Star Wars characters in the list.",
        "TEST PROOF:\nSearching 'Luke' sends a request to https://swapi.info/api/people/?search=Luke. The server ignores the search query and returns all 82 items. The app does not filter them on the phone.",
        "The backend server is a static file server that ignores search parameters, and the app code does not filter the list on the client side.",
        "Add client-side filtering in JavaScript so the phone filters the list when the user types in the search bar."
    ],

    # 14. DEF-06
    [
        "DEF-06",
        "Interactive Map is Disabled and Blank in Group Details Screen",
        "Requirement 8 states that group details should display an interactive map showing where members are located. In the current app, the map view component has been completely commented out in the code, showing only raw GPS numbers instead of a real map.",
        "Req 8",
        "Functional",
        "Medium",
        "P3",
        "Open",
        "Android & iOS",
        "1. Open a Group Detail screen with members\n2. Tap on a member to view their location",
        "An interactive Google Map should display showing a pin for where the member is located.",
        "The map is completely missing and blank. Only plain numbers (latitude and longitude) are displayed.",
        "CODE PROOF:\nIn GroupDetailScreen/index.js lines 111-125:\nThe entire <MapView> code is commented out with a developer note: 'Paid Account API Key needed'.",
        "The developer commented out the MapView component because they did not have a Google Maps billing account.",
        "Uncomment the MapView component and provide a valid Google Maps API key."
    ],

    # 15. DEF-09
    [
        "DEF-09",
        "No Character Limits on Inputs (Users Can Paste Unlimited 10,000+ Letters)",
        "Input boxes on the registration and login forms lack character limits (maxLength). Users can paste tens of thousands of characters into name, email, or password fields, causing layout distortion and excessive database bloat.",
        "Req 1 & 3",
        "Validation / UX",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. In the First Name, Last Name, Email, or Password boxes, paste 10,000+ letters\n2. Tap Save or Login",
        "Input boxes should stop accepting text after a reasonable limit (e.g. 50 characters for names, 128 for passwords).",
        "The input boxes have no character limit. They accept huge amounts of text, breaking the layout and crashing storage.",
        "CODE PROOF:\nIn RegisterScreen/index.js and LoginScreen/index.js:\nNone of the <TextInput> components have a 'maxLength' property set.",
        "Developers forgot to add the 'maxLength' limit property to the text input fields.",
        "Add `maxLength={50}` for names, `maxLength={254}` for email, and `maxLength={128}` for password inputs."
    ],

    # 16. DEF-15
    [
        "DEF-15",
        "Login Screen Unnecessarily Re-Checks Password Complexity Rules on Sign-In",
        "The login button re-evaluates complex password creation rules (requiring uppercase, lowercase, numbers, and symbols) during sign-in. A login screen should only check whether credentials match the account, not re-validate creation rules on existing passwords.",
        "Req 3",
        "Auth / Architecture",
        "Medium",
        "P2",
        "Open",
        "Android & iOS",
        "1. Open the Login screen\n2. Enter registered email and password\n3. Tap LOGIN",
        "The login screen should only check if the password matches the account. It should not re-run password creation complexity rules.",
        "The login screen runs the complex password regex rule every time a user logs in. If long passwords are typed, it can freeze older phones.",
        "CODE PROOF:\nIn LoginScreen/index.js lines 98-101:\nThe login button runs `validatePassword(password)` before sending the login request.",
        "Password complexity rules are meant for account registration, not for logging into an existing account.",
        "Remove the password complexity regex check from the Login screen and only check if the password field is not empty."
    ],

    # 17. DEF-10
    [
        "DEF-10",
        "Text Inputs Are Aligned to the Right with Confusing Arrow Icons",
        "Text input fields on the registration screen force all typed text to be aligned to the right side, and each input row displays a right-arrow navigation icon. This misleads users into thinking the inputs are clickable menu items.",
        "Req 10 / Task 3",
        "Usability / UI",
        "Low",
        "P3",
        "Open",
        "Android & iOS",
        "1. Open the Register screen\n2. Type into First Name, Email, or Password",
        "Text should be aligned to the left, and simple text boxes should not have clickable arrow (chevron) icons.",
        "Text typed in boxes is pushed all the way to the right side, and every single box has a misleading '>' arrow icon as if it was a menu button.",
        "CODE PROOF:\nIn RegisterScreen/styles.js:\n`textAlign: 'right'` is forced on all inputs, and every row includes `<Ionicons name=\"chevron-forward\" />`.",
        "Inconsistent form styling that confuses users by putting navigation arrows on regular typing fields.",
        "Change text alignment to `textAlign: 'left'` and remove the chevron arrow icons from simple input fields."
    ],

    # 18. DEF-12
    [
        "DEF-12",
        "Logout Button Cut Off at Screen Edge in Landscape Mode on Profile Screen",
        "On the profile screen in landscape orientation, labels and user details are pushed to extreme opposite edges of the screen, and the Logout button gets cut off at the bottom with no way for the user to scroll down to click it.",
        "Req 4 & 12",
        "Usability / UI",
        "Medium",
        "P3",
        "Open",
        "Android & iOS",
        "1. Open Profile screen\n2. Rotate phone to Landscape mode\n3. Try to tap Logout",
        "Profile info should fit neatly on screen, and the Logout button should be easy to reach.",
        "Text labels are pushed to the extreme edges of the screen, and the Logout button gets cut off at the bottom with no way to scroll.",
        "CODE PROOF:\nIn ProfileScreen/styles.js:\n`justifyContent: 'space-between'` pushes text apart, and the screen has no `<ScrollView>`.",
        "Missing scroll container and unconstrained spacing on landscape displays.",
        "Add a ScrollView and keep profile labels aligned neatly together."
    ],

    # 19. DEF-13
    [
        "DEF-13",
        "Empty Group Screen Has Too Much Blank Space and Unnecessary Scrolling",
        "When a user has no joined groups, viewing the empty state in landscape mode shows unnecessary scrollbars and vertical dragging because a fixed 200px top padding pushes the empty state icon past the bottom of the screen.",
        "Req 10 & 12",
        "UI Polish",
        "Low",
        "P3",
        "Open",
        "Android & iOS (Landscape)",
        "1. Open Group Home screen when you have no groups\n2. Rotate phone to Landscape\n3. Swipe the screen up and down",
        "The empty state message ('No groups yet') should sit nicely centered without needing to scroll.",
        "The empty icon and message scroll up and down because there is a giant invisible 200px blank space added at the top.",
        "CODE PROOF:\nIn GroupHomeScreen/styles.js line 77:\n`paddingTop: Metrics.SCREEN_WIDTH / 2` (adds 200px of forced top padding, exceeding screen height in landscape).",
        "Using a fixed screen width calculation for top padding creates oversized blank spaces on landscape screens.",
        "Use simple flex centering (`justifyContent: 'center'`) instead of fixed pixel top padding."
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
        if c_idx in [1, 2, 5, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal="center", vertical="top")
        
        # Severity coloring
        if c_idx == 7:
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
    4: 42,  # Description
    5: 12,  # Req
    6: 18,  # Category
    7: 14,  # Severity
    8: 10,  # Priority
    9: 12,  # Status
    10: 22, # Environment
    11: 35, # Steps
    12: 30, # Expected
    13: 35, # Actual
    14: 45, # Evidence
    15: 35, # Root Cause
    16: 40  # Fix
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
