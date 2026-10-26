import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import csv

wb = openpyxl.Workbook()

# Define color schemes
HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=16, bold=True, color="1F4E78")
SUBTITLE_FONT = Font(name="Calibri", size=11, italic=True, color="595959")
SECTION_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
SECTION_FONT = Font(name="Calibri", size=11, bold=True, color="1F4E78")

PASS_FILL = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
PASS_FONT = Font(name="Calibri", size=10, bold=True, color="375623")
FAIL_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
FAIL_FONT = Font(name="Calibri", size=10, bold=True, color="C65911")
BLOCK_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
BLOCK_FONT = Font(name="Calibri", size=10, bold=True, color="806000")

THIN_BORDER = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

# ----------------------------------------------------
# SHEET 1: EXECUTIVE DASHBOARD & SUMMARY
# ----------------------------------------------------
ws_dash = wb.active
ws_dash.title = "Dashboard & Summary"
ws_dash.views.sheetView[0].showGridLines = True

ws_dash["A1"] = "STARWARS MOBILE APPLICATION - QA TEST SUITE & EXECUTION DASHBOARD"
ws_dash["A1"].font = TITLE_FONT
ws_dash["A2"] = "Role: Junior QA Engineer | Project: StarWarsApp (React Native) | Date: October 2026"
ws_dash["A2"].font = SUBTITLE_FONT

headers_summary = ["Metric / Domain", "Total Cases", "Passed", "Failed", "Blocked", "Pass Rate (%)"]
row_idx = 4
for col_idx, h in enumerate(headers_summary, start=1):
    cell = ws_dash.cell(row=row_idx, column=col_idx, value=h)
    cell.fill = HEADER_FILL
    cell.font = HEADER_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center")

summary_data = [
    ["1. Functional Testing (Reqs 1-13)", 24, 15, 6, 3, "=ROUND(C5/B5*100, 1)"],
    ["2. Boundary Value Analysis (BVA)", 8, 7, 1, 0, "=ROUND(C6/B6*100, 1)"],
    ["3. Compatibility & Orientation Testing", 6, 2, 4, 0, "=ROUND(C7/B7*100, 1)"],
    ["4. Usability & UX Design Testing", 6, 2, 4, 0, "=ROUND(C8/B8*100, 1)"],
    ["5. Performance & Resource Testing", 4, 1, 3, 0, "=ROUND(C9/B9*100, 1)"],
    ["6. Security Testing (OWASP Mobile)", 7, 1, 6, 0, "=ROUND(C10/B10*100, 1)"],
    ["TOTAL EXECUTION SUMMARY", "=SUM(B5:B10)", "=SUM(C5:C10)", "=SUM(D5:D10)", "=SUM(E5:E10)", "=ROUND(C11/B11*100, 1)"]
]

for r in summary_data:
    row_idx += 1
    for c_idx, val in enumerate(r, start=1):
        cell = ws_dash.cell(row=row_idx, column=c_idx, value=val)
        cell.border = THIN_BORDER
        if row_idx == 11:
            cell.font = Font(name="Calibri", size=11, bold=True)
            cell.fill = SECTION_FILL
        if c_idx >= 2:
            cell.alignment = Alignment(horizontal="center")

# Key Insights Box
ws_dash["A14"] = "CRITICAL FINDINGS & DEFECT SUMMARY"
ws_dash["A14"].font = SECTION_FONT
insights = [
    ["Defect ID", "Severity", "Impacted Requirement", "Summary Description"],
    ["SEC-01", "Critical", "Req 11 (Auth Scheme)", "Plaintext Password Storage in MMKV (CWE-312 / OWASP M2)"],
    ["DEF-14", "Blocker", "Req 2 (Photo Upload)", "Camera permission false negative displays 'permission not granted' even when allowed"],
    ["DEF-01", "High", "Req 1 (Registration)", "Premature storage save locks out user email permanently when location is denied"],
    ["DEF-04", "High", "Req 3 (Login)", "Mandatory GPS requirement blocks user from logging into the community app"],
    ["DEF-05", "High", "Req 7 & 13 (Join & I18n)", "'Join Group' button completely disappears when app language is set to Indonesian"],
    ["DEF-08", "High", "Req 12 (Orientation)", "Landscape mode screen cannot scroll; touch gestures stuck and buttons unreachable"],
    ["DEF-11", "High", "Req 2 & Task 4 (Perf)", "Uncompressed raw Base64 photo storage in MMKV causes memory bloat and OOM crashes"],
    ["DEF-09", "Medium", "Req 1 (Validation)", "Unbounded input length / missing maxLength on Registration and Login text fields"],
    ["DEF-06", "Medium", "Req 8 (GPS Map)", "Interactive MapView is commented out in code (only raw coordinates shown)"],
    ["DEF-03", "Medium", "Req 4 & 9 (SWAPI)", "SWAPI search query is ignored on static host; app lacks client-side filtering"],
    ["DEF-15", "Medium", "Req 3 (Login Architecture)", "Creation-time password complexity regex incorrectly executed on Login screen"]
]

r_start = 15
for r in insights:
    for c_idx, val in enumerate(r, start=1):
        cell = ws_dash.cell(row=r_start, column=c_idx, value=val)
        cell.border = THIN_BORDER
        if r_start == 15:
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = Alignment(horizontal="center")
        else:
            if c_idx == 1:
                cell.font = Font(name="Calibri", bold=True)
            if c_idx == 2:
                cell.alignment = Alignment(horizontal="center")
                if val == "Critical" or val == "Blocker":
                    cell.fill = FAIL_FILL
                    cell.font = FAIL_FONT
                elif val == "High":
                    cell.fill = BLOCK_FILL
                    cell.font = BLOCK_FONT
    r_start += 1


# ----------------------------------------------------
# SHEET 2: ALL TEST CASES (MASTER EXCEL SHEET)
# ----------------------------------------------------
ws_cases = wb.create_sheet(title="All Test Cases")
ws_cases.views.sheetView[0].showGridLines = True

headers_cases = [
    "Test Case ID",
    "Module / Feature",
    "Req Ref",
    "Test Type",
    "Test Scenario / Description",
    "Preconditions",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Actual Result",
    "Status",
    "Severity",
    "Linked Defect"
]

for col_idx, h in enumerate(headers_cases, start=1):
    cell = ws_cases.cell(row=1, column=col_idx, value=h)
    cell.fill = HEADER_FILL
    cell.font = HEADER_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

test_cases_data = [
    # 1. Registration - Positive
    [
        "TC-REG-01", "Registration", "Req 1.a", "Positive",
        "Verify successful user registration using Luke Skywalker credentials",
        "Fresh app launch on Register Screen",
        "1. Enter First Name, Last Name\n2. Enter Email & Password\n3. Select SWAPI role 'Luke Skywalker'\n4. Capture camera photo\n5. Tap Save -> Skip group creation",
        "First: Luke, Last: Skywalker\nEmail: [User1_Email]\nPwd: [Assignment Password Standard]",
        "Registration succeeds with success toast; user navigated to Home screen; user saved in storage",
        "User registered successfully; credentials saved in MMKV",
        "PASS", "High", ""
    ],
    [
        "TC-REG-02", "Registration", "Req 1.b", "Positive",
        "Verify successful user registration using Darth Vader credentials",
        "Register Screen opened",
        "1. Enter First Name, Last Name\n2. Enter Email & Password\n3. Select SWAPI role 'Darth Vader'\n4. Capture photo\n5. Tap Save",
        "First: Anakin, Last: Skywalker\nEmail: [User2_Email]\nPwd: [Assignment Password Standard]",
        "Registration succeeds; complexity regex accepts special character '!' and uppercase 'F'",
        "User registered successfully",
        "PASS", "High", ""
    ],
    # 2. Registration - Negative & Validation
    [
        "TC-REG-03", "Registration", "Req 1", "Negative",
        "Verify registration rejection when all fields are empty",
        "Register Screen opened",
        "1. Leave all input fields blank\n2. Tap Save button",
        "Empty form",
        "Registration blocked; error toast: 'All fields must be filled out'",
        "Error toast displayed; registration blocked",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-04", "Registration", "Req 1", "Negative",
        "Verify registration rejection when Password and Confirm Password do not match",
        "Register Screen opened",
        "1. Fill valid names and email\n2. Enter Password\n3. Enter different Confirm Password\n4. Tap Save",
        "Password: [Valid Assignment Password]\nConfirm: [Mismatched Confirmation Password]",
        "Registration blocked; error toast: 'Passwords do not match'",
        "Error toast displayed: 'Passwords do not match'",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-05", "Registration", "Req 1", "Negative",
        "Verify password rejection when uppercase letter is missing",
        "Register Screen opened",
        "1. Fill valid form\n2. Enter password with only lowercase, numbers, and symbols\n3. Tap Save",
        "Password: [Sample with all lowercase 'f' - missing uppercase]",
        "Registration rejected; toast displays password complexity policy requirement",
        "Rejected by regex validation",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-06", "Registration", "Req 1", "Negative",
        "Verify password rejection when numbers/digits are missing",
        "Register Screen opened",
        "1. Enter password with letters and symbols but no numbers\n2. Tap Save",
        "Password: May_the_Force_be_with_u!",
        "Registration rejected; error toast displayed",
        "Rejected by regex validation",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-07", "Registration", "Req 1", "Negative",
        "Verify password rejection when special character/underscore is missing",
        "Register Screen opened",
        "1. Enter password without special characters or underscores\n2. Tap Save",
        "Password: m4yth3F0rc3b3w1thu",
        "Registration rejected; error toast displayed",
        "Rejected by regex validation",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-08", "Registration", "Req 1", "Negative",
        "Verify email validation rejects invalid format missing '@' symbol",
        "Register Screen opened",
        "1. Enter email without '@'\n2. Fill remaining valid fields\n3. Tap Save",
        "Email: luke.starwars.com",
        "Registration blocked; error toast: 'Invalid email format'",
        "Error toast displayed: 'Invalid email format'",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-09", "Registration", "Req 1", "Negative",
        "Verify email validation rejects invalid format missing domain/TLD",
        "Register Screen opened",
        "1. Enter email with '@' but missing domain extension\n2. Tap Save",
        "Email: luke@starwars",
        "Registration blocked; error toast displayed",
        "Error toast displayed: 'Invalid email format'",
        "PASS", "Medium", ""
    ],
    [
        "TC-REG-10", "Registration", "Req 1", "Edge",
        "Verify duplicate email registration rejection",
        "User [User1_Email] already registered",
        "1. Open Register Screen\n2. Attempt to register again with same email\n3. Tap Save",
        "Email: [User1_Email]",
        "Registration blocked; toast: 'Email is already registered'",
        "Toast displays: 'Email is already registered'",
        "PASS", "High", ""
    ],
    [
        "TC-REG-11", "Registration", "Req 1", "Edge",
        "Verify registration flow behavior when location permission is denied by user",
        "Fresh registration form filled",
        "1. Fill valid details & photo\n2. Tap Save -> Skip\n3. When Android Location dialog appears, tap 'Don't allow' (Deny)",
        "Valid user details",
        "App handles denial gracefully without corrupting local database state",
        "User is committed to MMKV before permission resolves; denial redirects to login; retrying registration locks email permanently",
        "FAIL", "High", "DEF-01"
    ],
    [
        "TC-REG-12", "Registration", "Req 1 / Task 3", "Usability / UI",
        "Verify registration form text alignment and icon behavior",
        "Register Screen opened",
        "1. Enter text in First Name, Last Name, Email, and Password\n2. Observe text alignment and right-hand icons",
        "Sample text input",
        "Text is aligned to left (textAlign: 'left'); regular typing inputs do not have navigation chevron (>) icons",
        "Inputs force textAlign: 'right' with label on far left, and every row displays a misleading '>' chevron arrow",
        "FAIL", "Low", "DEF-10"
    ],

    # 3. Boundary Value Analysis (BVA)
    [
        "TC-BVA-01", "Input Boundary", "Req 1", "Boundary",
        "Verify password length boundary at Min - 1 (7 characters)",
        "Register Screen opened",
        "1. Enter 7-character password satisfying complexity rules\n2. Tap Save",
        "Password: Ab1!xyz (Length 7)",
        "Password rejected for being below 8-character minimum",
        "Rejected by regex `.{8,}$`",
        "PASS", "Medium", ""
    ],
    [
        "TC-BVA-02", "Input Boundary", "Req 1", "Boundary",
        "Verify password length boundary at exact Minimum (8 characters)",
        "Register Screen opened",
        "1. Enter exact 8-character password satisfying complexity\n2. Tap Save",
        "Password: Ab1!xyzw (Length 8)",
        "Password accepted by validation",
        "Accepted by regex",
        "PASS", "Medium", ""
    ],
    [
        "TC-BVA-03", "Input Boundary", "Req 1", "Boundary",
        "Verify password length boundary at Min + 1 (9 characters)",
        "Register Screen opened",
        "1. Enter 9-character password satisfying complexity\n2. Tap Save",
        "Password: Ab1!xyzwa (Length 9)",
        "Password accepted by validation",
        "Accepted by regex",
        "PASS", "Medium", ""
    ],
    [
        "TC-BVA-04", "Input Boundary", "Req 1", "Boundary",
        "Verify maximum email length boundary (254 characters RFC standard)",
        "Register Screen opened",
        "1. Enter 254-character valid email\n2. Submit registration",
        "Email: 240 'a's + '@starwars.com' (Length 254)",
        "Email accepted and processed correctly",
        "Accepted by regex",
        "PASS", "Low", ""
    ],
    [
        "TC-BVA-05", "Input Boundary", "Req 1", "Boundary / Security",
        "Verify upper boundary enforcement on text inputs (Missing maxLength)",
        "Register Screen opened",
        "1. Paste 10,000+ characters into First Name, Last Name, and Email\n2. Tap Save",
        "String of 10,000 'A's",
        "Form input should be constrained by maxLength (e.g. 50 chars for name, 254 for email)",
        "Inputs lack maxLength prop; accepts 10,000+ chars, causing UI layout explosion and storage bloat",
        "FAIL", "Medium", "DEF-09"
    ],
    [
        "TC-BVA-06", "Input Boundary", "Req 1", "Boundary / Security",
        "Verify password regex upper bound constraint (ReDoS risk)",
        "Register Screen opened",
        "1. Paste 10,000 characters into password\n2. Submit form",
        "Password: 'A1!' + 9,997 'a's",
        "Password regex should have upper bound (e.g. `.{8,128}$`) to prevent ReDoS",
        "Regex `.{8,}$` has no upper bound; evaluates unbounded strings, risking CPU freeze",
        "FAIL", "Medium", "DEF-09"
    ],
    [
        "TC-BVA-07", "Input Boundary", "Req 1", "Edge",
        "Verify email whitespace boundary handling (Leading & Trailing spaces)",
        "Register Screen opened",
        "1. Enter valid email with spaces at start and end\n2. Submit registration",
        "Email: '  [Sample_Email_With_Spaces]  '",
        "Input should be sanitized with .trim() before validation",
        "Email trimmed properly in formData handling",
        "PASS", "Low", ""
    ],
    [
        "TC-BVA-08", "Input Boundary", "Req 1", "Edge",
        "Verify password handling with whitespace-only input",
        "Register Screen opened",
        "1. Enter 10 spaces into password\n2. Submit form",
        "Password: '          '",
        "Rejected as empty / missing complexity",
        "Rejected by `.trim()` and regex",
        "PASS", "Medium", ""
    ],

    # 4. Photo Upload (Req 2)
    [
        "TC-PHT-01", "Photo Upload", "Req 2", "Positive",
        "Verify profile photo capture using device camera",
        "Camera permission granted; Register Screen page 2",
        "1. Tap avatar camera icon\n2. View live viewfinder\n3. Tap 'Capture Photo'",
        "Live camera feed",
        "Photo captured; preview displayed on avatar; photo converted for storage",
        "Photo captured and displayed",
        "PASS", "High", ""
    ],
    [
        "TC-PHT-02", "Photo Upload", "Req 2", "Functional / Missing",
        "Verify user ability to select profile photo from Image Library / Gallery",
        "Register Screen opened",
        "1. Tap avatar to upload photo\n2. Look for option to choose from Photo Library / Gallery",
        "Device photo gallery",
        "User should have option to choose between Camera or Image Library as per Requirement 2",
        "Image Library selection is completely missing; only camera capture exists",
        "FAIL", "Medium", "DEF-02"
    ],
    [
        "TC-PHT-03", "Photo Upload", "Req 2", "Functional / Blocker",
        "Verify camera viewfinder behavior when Camera permission is pre-granted",
        "Camera permission set to 'Allow' in Android Settings",
        "1. Open Register Screen\n2. Tap camera icon to capture photo",
        "Pre-granted OS permission",
        "Camera viewfinder opens immediately",
        "Screen falsely displays 'Camera permission is not granted'; user blocked from taking photo and registering",
        "FAIL", "Blocker", "DEF-14"
    ],
    [
        "TC-PHT-04", "Photo Upload", "Req 2", "Performance / Resource",
        "Verify image capture file size limitation and storage encoding",
        "Camera captured photo on high-resolution sensor",
        "1. Capture photo\n2. Inspect storage payload in MMKV",
        "Camera snapshot",
        "Image should be cropped/compressed (<200KB) and stored as local file URI",
        "No size limits; entire photo converted to massive raw Base64 string in MMKV, causing memory bloat",
        "FAIL", "High", "DEF-11"
    ],

    # 5. Login & Authentication (Req 3 & 11)
    [
        "TC-LOG-01", "Login", "Req 3", "Positive",
        "Verify successful login with registered Luke Skywalker credentials",
        "User registered; Login Screen opened; GPS enabled",
        "1. Enter email: [User1_Email]\n2. Enter registered password\n3. Tap LOGIN",
        "User credentials",
        "Toast displays 'Login Success'; user navigated to BottomTabBar",
        "Login succeeds; user logged in",
        "PASS", "High", ""
    ],
    [
        "TC-LOG-02", "Login", "Req 3", "Positive",
        "Verify successful login with registered secondary credentials",
        "User registered; Login Screen opened; GPS enabled",
        "1. Enter email: [User2_Email]\n2. Enter registered password\n3. Tap LOGIN",
        "User credentials",
        "Login succeeds; user navigated to BottomTabBar",
        "Login succeeds",
        "PASS", "High", ""
    ],
    [
        "TC-LOG-03", "Login", "Req 3", "Negative",
        "Verify login rejection with incorrect password",
        "User registered; Login Screen opened",
        "1. Enter valid email\n2. Enter incorrect password\n3. Tap LOGIN",
        "Email: [User1_Email]\nPwd: [MismatchedPassword]",
        "Login rejected; toast: 'Invalid email or password'",
        "Login rejected; error toast shown",
        "PASS", "High", ""
    ],
    [
        "TC-LOG-04", "Login", "Req 3", "Negative",
        "Verify login rejection with unregistered email",
        "Login Screen opened",
        "1. Enter non-existent email\n2. Enter password\n3. Tap LOGIN",
        "Email: [UnregisteredEmail]\nPwd: [SamplePassword]",
        "Login rejected; toast: 'Invalid email or password'",
        "Login rejected; error toast shown",
        "PASS", "High", ""
    ],
    [
        "TC-LOG-05", "Login", "Req 3", "Negative / Usability",
        "Verify login behavior when user declines Location Permission",
        "User registered; Login Screen opened",
        "1. Enter valid credentials\n2. Tap 'Don't allow' on Location prompt\n3. Tap LOGIN",
        "Valid credentials",
        "Login should succeed; app should function with location-dependent features degraded",
        "User is strictly blocked from logging in; toast: 'You must allow location permission to login'",
        "FAIL", "High", "DEF-04"
    ],
    [
        "TC-LOG-06", "Login", "Req 3", "Edge",
        "Verify email case-insensitivity on Login",
        "User registered with lowercase email",
        "1. Enter email in uppercase: [USER1_UPPERCASE_EMAIL]\n2. Enter valid password\n3. Tap LOGIN",
        "Uppercase email",
        "Login succeeds due to .toLowerCase() normalization",
        "Login succeeds",
        "PASS", "Medium", ""
    ],
    [
        "TC-LOG-07", "Login", "Req 3 / 11", "Architecture / Flaw",
        "Verify client-side password complexity enforcement on Login screen",
        "Login Screen opened",
        "1. Enter registered email\n2. Enter password without uppercase or symbols\n3. Tap LOGIN",
        "Password: simplepassword",
        "Login screen should NOT check creation-time complexity regex; should only verify with backend",
        "`handleLogin()` re-executes validatePassword regex, rejecting passwords client-side and risking ReDoS",
        "FAIL", "Medium", "DEF-15"
    ],

    # 6. Profile & SWAPI Particulars (Req 4)
    [
        "TC-PRF-01", "Profile", "Req 4", "Positive",
        "Verify profile displays user photo and SWAPI particulars",
        "Logged in as Luke Skywalker; Profile tab selected",
        "1. Navigate to Profile screen\n2. Verify displayed fields",
        "Luke Skywalker profile",
        "Displays photo, email, role (Luke Skywalker), height (172), mass (77), birth year (19BBY), gender (male)",
        "All particulars displayed from roleDetail",
        "PASS", "High", ""
    ],
    [
        "TC-PRF-02", "Profile", "Req 4", "Positive",
        "Verify logout functionality clears session",
        "Logged in on Profile Screen",
        "1. Tap Logout button\n2. Confirm logout in alert dialog",
        "User session",
        "Session removed from MMKV; user redirected to Login Screen",
        "User logged out; redirected to Login",
        "PASS", "Medium", ""
    ],
    [
        "TC-PRF-03", "Profile", "Req 4", "Usability / Layout",
        "Verify profile details alignment and spacing",
        "Profile Screen opened",
        "1. Inspect label and value layout across particulars",
        "Profile particulars",
        "Clean, consistent column layout",
        "Uses justifyContent: 'space-between', pushing labels to far left and values to far right with giant gap",
        "FAIL", "Low", "DEF-12"
    ],

    # 7. Group Creation & Invitations (Req 5 & 6)
    [
        "TC-GRP-01", "Group Creation", "Req 5.a", "Positive",
        "Verify Luke Skywalker creates group 'Rebel Alliance' and invites Darth Vader",
        "Logged in as Luke; Create Group tab selected",
        "1. Enter Group Name: 'Rebel Alliance'\n2. Select starship 'X-wing'\n3. Invite [User2_Email]\n4. Tap Save",
        "Group: Rebel Alliance\nStarship: X-wing\nInvite: [User2_Email]",
        "Group saved in MMKV; invitation stored in Darth Vader's notifications",
        "Group created; invitation added to Vader's record",
        "PASS", "High", ""
    ],
    [
        "TC-GRP-02", "Group Creation", "Req 5.b", "Positive",
        "Verify Darth Vader creates group 'Empire' and invites Luke Skywalker",
        "Logged in as Darth Vader; Create Group tab selected",
        "1. Enter Group Name: 'Empire'\n2. Select starship 'Star Destroyer'\n3. Invite [User1_Email]\n4. Tap Save",
        "Group: Empire\nStarship: Star Destroyer\nInvite: [User1_Email]",
        "Group created; invitation stored in Luke's notifications",
        "Group created; invitation stored successfully",
        "PASS", "High", ""
    ],
    [
        "TC-GRP-03", "Group Creation", "Req 5", "Negative",
        "Verify group creation rejection when Group Name is empty",
        "Create Group Screen opened",
        "1. Leave group name blank\n2. Select starship\n3. Tap Save",
        "Empty group name",
        "Creation blocked; error toast: 'Group name is required.'",
        "Error toast displayed; creation blocked",
        "PASS", "Medium", ""
    ],
    [
        "TC-GRP-04", "Group Creation", "Req 5", "Negative",
        "Verify group creation rejection when Starship is not selected",
        "Create Group Screen opened",
        "1. Enter group name\n2. Leave starship unselected\n3. Tap Save",
        "Name: Test Group; Starship: empty",
        "Creation blocked; toast: 'Select group starship'",
        "Error toast displayed; creation blocked",
        "PASS", "Medium", ""
    ],
    [
        "TC-GRP-05", "Group Creation", "Req 5", "Edge",
        "Verify invitation rejection for non-registered email address",
        "Create Group Screen opened",
        "1. Tap Invite member\n2. Enter non-existent email\n3. Tap Invite",
        "Email: [Unregistered_Email]",
        "Invitation rejected; error toast: 'No users found in the system'",
        "Error toast displayed: 'No users found in the system'",
        "PASS", "Medium", ""
    ],
    [
        "TC-GRP-06", "Notifications", "Req 6", "Positive",
        "Verify in-app push notification delivery for invited user",
        "Luke invited Darth Vader to Rebel Alliance",
        "1. Log in as Darth Vader\n2. Arrive at Group Home Screen",
        "Vader session",
        "In-app push notification displayed: 'You have been invited to Rebel Alliance'; tab switches to Unjoined",
        "Notification triggered and tab switches to Unjoined",
        "PASS", "High", ""
    ],

    # 8. Joining Groups (Req 7)
    [
        "TC-JON-01", "Joining Groups", "Req 7", "Positive",
        "Verify user can join an invited group under English locale",
        "Darth Vader invited to Rebel Alliance; English locale",
        "1. Open Unjoined Group tab\n2. Select 'Rebel Alliance'\n3. Tap 'Join Group' button",
        "English locale",
        "User joined; group moves from Unjoined to Joined tab; member status updated",
        "User joined successfully; group appears in Joined tab",
        "PASS", "High", ""
    ],
    [
        "TC-JON-02", "Joining Groups", "Req 7 / 13", "Edge / Localization",
        "Verify 'Join Group' button visibility and functionality under Indonesian locale",
        "Darth Vader invited to group; language set to Indonesian (ID)",
        "1. Switch language to ID\n2. Open 'Grup Belum Bergabung'\n3. Open group details screen",
        "Indonesian locale",
        "'Bergabung ke Grup' (Join Group) button should be displayed and functional",
        "Join button completely disappears because code checks activeTab === 'Unjoined Group' which fails in ID",
        "FAIL", "High", "DEF-05"
    ],

    # 9. Group Details & GPS Map (Req 8 & 9)
    [
        "TC-DET-01", "Group Details", "Req 8", "Functional / Missing",
        "Verify interactive map displays joined members' last known GPS locations",
        "Group Detail Screen opened with joined members",
        "1. Inspect member location section on Group Detail screen",
        "Joined members with GPS coordinates",
        "Interactive MapView renders pins for member coordinates as per Requirement 8",
        "MapView is commented out in code (/* Paid Account API Key needed */); only raw text numbers shown",
        "FAIL", "Medium", "DEF-06"
    ],
    [
        "TC-DET-02", "Group Details", "Req 9", "Positive",
        "Verify group profile displays starship details from StarWarsAPI",
        "Group Detail Screen opened",
        "1. Inspect Starship Details section",
        "Starship: Millennium Falcon / X-wing",
        "Displays name, model, manufacturer, cost, length, speed, crew, passengers, cargo capacity",
        "All starship details rendered accurately",
        "PASS", "High", ""
    ],
    [
        "TC-DET-03", "SWAPI Integration", "Req 4 & 9", "Functional / Integration",
        "Verify SWAPI search bar filters characters and starships by query",
        "SwapiScreen opened for Character Role or Starship selection",
        "1. Type 'Luke' or 'Falcon' into search bar",
        "Search: 'Luke'",
        "List dynamically filters to show only matching characters/starships",
        "Static mirror ignores ?search=; frontend lacks client-side filtering; all 82 items remain visible",
        "FAIL", "Medium", "DEF-03"
    ],
    [
        "TC-DET-04", "SWAPI Integration", "Req 9", "Edge / Pagination",
        "Verify infinite scroll pagination on SWAPI list",
        "SwapiScreen opened",
        "1. Scroll to the bottom of the list to trigger load more",
        "SWAPI data list",
        "Next page of results fetched and appended",
        "data.next is undefined on static array; pagination check fails and never loads more",
        "FAIL", "Low", "DEF-03"
    ],

    # 10. Compatibility & Responsive Design (Req 12)
    [
        "TC-CMP-01", "Compatibility", "Req 12", "Compatibility",
        "Verify screen layout reflow when rotating device to Landscape orientation",
        "Group Home Screen opened",
        "1. Rotate device or emulator 90 degrees to Landscape",
        "Landscape orientation",
        "Layout dynamically adapts; PieChart and cards reflow proportionally",
        "Metrics frozen statically at boot; PieChart and tab bar retain portrait dimensions, distorting UI",
        "FAIL", "High", "DEF-07"
    ],
    [
        "TC-CMP-02", "Compatibility", "Req 12", "Compatibility / Blocker",
        "Verify screen scrollability in Landscape orientation (Missing ScrollView)",
        "Login Screen or Profile Screen opened",
        "1. Rotate to Landscape\n2. Attempt to scroll down with finger/mouse",
        "Landscape orientation",
        "Content should scroll smoothly to reveal buttons below the viewport",
        "Page is frozen/stuck; touch gestures produce no scrolling; Login and Logout buttons unreachable",
        "FAIL", "High", "DEF-08"
    ],
    [
        "TC-CMP-03", "Compatibility", "Req 12", "Usability / Layout",
        "Verify empty group state display in Landscape orientation",
        "Zero groups in list; Landscape orientation",
        "1. View empty group screen in Landscape\n2. Observe vertical positioning and scrolling",
        "Empty state",
        "Empty placeholder centered cleanly without requiring scrolling",
        "Empty state container hardcodes paddingTop: SCREEN_WIDTH/2 (200px), causing phantom scrolling on empty list",
        "FAIL", "Low", "DEF-13"
    ],
    [
        "TC-CMP-04", "Compatibility", "Req 12", "Compatibility",
        "Verify tablet aspect ratio scaling (iPad & Android Tablets)",
        "App installed on tablet (11-inch screen)",
        "1. Inspect bottom tab bar height and input row proportions",
        "Tablet resolution (e.g. 1200x1920)",
        "Tab bar has proportional, standard height (56-64px)",
        "Tab bar height uses SCREEN_HEIGHT * 0.1, making it an excessive 120-140px tall",
        "FAIL", "Medium", "DEF-07"
    ],
    [
        "TC-CMP-05", "Compatibility", "Req 12", "Compatibility",
        "Verify iOS location authorization prompt handling",
        "App running on iOS simulator/device",
        "1. Open Login Screen\n2. Trigger login",
        "iOS platform",
        "Triggers native iOS CoreLocation permission prompt",
        "Code has `if (Platform.OS === 'android')` check and returns true blindly for iOS without requesting authorization",
        "FAIL", "Medium", "DEF-04"
    ],

    # 11. Localization (Req 13)
    [
        "TC-I18N-01", "Localization", "Req 13", "Positive",
        "Verify dynamic language switching between English (EN) and Indonesian (ID)",
        "Login Screen or Profile Screen opened",
        "1. Tap EN/ID toggle button\n2. Observe UI text updates",
        "Language toggle",
        "All labels update dynamically to selected language",
        "Labels update accurately between English and Indonesian",
        "PASS", "Medium", ""
    ],
    [
        "TC-I18N-02", "Localization", "Req 13", "Positive",
        "Verify translation key parity between en.json and id.json",
        "Automated i18n parity test runner",
        "1. Run i18n_parity.test.js",
        "en.json & id.json",
        "100% key parity with matching interpolation variables (e.g. {{count}})",
        "All 65 translation keys match with zero missing keys and matching variables",
        "PASS", "Medium", ""
    ],

    # 12. Security & OWASP Mobile Top 10 (Req 11)
    [
        "TC-SEC-01", "Security", "Req 11", "Security / OWASP M2",
        "Verify user password storage encryption in local MMKV database (CWE-312)",
        "User registered in app",
        "1. Inspect /data/data/com.starwarsapp/files/mmkv/mmkv.default",
        "MMKV storage file",
        "Passwords must be hashed with bcrypt/Argon2 or stored in Android KeyStore",
        "Password stored in 100% clear text without encryption or hashing in MMKV storage",
        "FAIL", "Critical", "SEC-01"
    ],
    [
        "TC-SEC-02", "Security", "Req 11", "Security / OWASP M1/M9",
        "Verify Google Maps API key protection against reverse engineering",
        "Compiled Android APK",
        "1. Inspect AndroidManifest.xml inside APK",
        "AndroidManifest.xml",
        "Production API keys should not be hardcoded in plaintext manifest files",
        "Production key AIzaSyDwBmG2L0YadPd3JE-Wku5Bdd-******** is hardcoded and exposed",
        "FAIL", "High", "SEC-02"
    ],
    [
        "TC-SEC-03", "Security", "Req 11", "Security / OWASP M3",
        "Verify iOS App Transport Security (ATS) TLS enforcement",
        "ios/StarWarsApp/Info.plist",
        "1. Inspect NSAppTransportSecurity configuration",
        "Info.plist",
        "NSAllowsArbitraryLoads should be false; strict HTTPS enforced",
        "NSAllowsArbitraryLoads is set to true, allowing unencrypted HTTP traffic",
        "FAIL", "High", "SEC-03"
    ],
    [
        "TC-SEC-04", "Security", "Req 11", "Security / OWASP M9",
        "Verify Release APK build signing certificate configuration",
        "android/app/build.gradle",
        "1. Inspect buildTypes.release signing configuration",
        "build.gradle",
        "Release build must be signed with a secure, private production keystore",
        "buildTypes.release is configured to sign with debug.keystore (insecure default debug key)",
        "FAIL", "High", "SEC-04"
    ],
    [
        "TC-SEC-05", "Security", "Req 11", "Security / OWASP M9",
        "Verify code minification and Proguard obfuscation in Release builds",
        "android/app/build.gradle",
        "1. Inspect enableProguardInReleaseBuilds setting",
        "build.gradle",
        "Proguard / R8 obfuscation enabled in release builds to prevent reverse engineering",
        "enableProguardInReleaseBuilds is set to false; bytecode is completely unobfuscated",
        "FAIL", "Medium", "SEC-04"
    ],
    [
        "TC-SEC-06", "Security", "Req 11", "Security / OWASP M1",
        "Verify iOS Photo Library permission description in Info.plist",
        "ios/StarWarsApp/Info.plist",
        "1. Search for NSPhotoLibraryUsageDescription key",
        "Info.plist",
        "Permission description must exist to prevent iOS runtime crash on photo library access",
        "NSPhotoLibraryUsageDescription key is missing; opening gallery crashes iOS app",
        "FAIL", "High", "DEF-02"
    ],
    [
        "TC-SEC-07", "Security", "Req 11", "Security / OWASP M3",
        "Verify backend API protocol security (HTTP vs HTTPS)",
        "src/react-query/utils/apiCallers.js",
        "1. Inspect API_HOST configuration",
        "apiCallers.js",
        "API endpoints must use secure HTTPS protocol",
        "API_HOST is hardcoded to unencrypted 'http://localhost:3000'",
        "FAIL", "Medium", "SEC-03"
    ]
]

row_num = 2
for tc in test_cases_data:
    for c_idx, val in enumerate(tc, start=1):
        cell = ws_cases.cell(row=row_num, column=c_idx, value=val)
        cell.border = THIN_BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        
        # Center align short columns
        if c_idx in [1, 3, 4, 11, 12, 13]:
            cell.alignment = Alignment(horizontal="center", vertical="top")
        
        # Status coloring
        if c_idx == 11:
            if val == "PASS":
                cell.fill = PASS_FILL
                cell.font = PASS_FONT
            elif val == "FAIL":
                cell.fill = FAIL_FILL
                cell.font = FAIL_FONT
            elif val == "BLOCKED":
                cell.fill = BLOCK_FILL
                cell.font = BLOCK_FONT
        
        # Severity coloring
        if c_idx == 12:
            if val in ["Critical", "Blocker"]:
                cell.font = Font(name="Calibri", bold=True, color="C00000")
            elif val == "High":
                cell.font = Font(name="Calibri", bold=True, color="ED7D31")

    row_num += 1

# Auto-fit column widths for cases sheet
col_widths = {
    1: 15, # ID
    2: 18, # Module
    3: 12, # Req
    4: 15, # Type
    5: 35, # Scenario
    6: 25, # Preconditions
    7: 35, # Steps
    8: 30, # Data
    9: 35, # Expected
    10: 35, # Actual
    11: 12, # Status
    12: 14, # Severity
    13: 15  # Defect
}
for col_idx, width in col_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_cases.column_dimensions[col_letter].width = width

# Dashboard column widths
dash_widths = {1: 32, 2: 15, 3: 12, 4: 12, 5: 12, 6: 18}
for col_idx, width in dash_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_dash.column_dimensions[col_letter].width = width

# Save Excel file
excel_path = "C:/Users/HP/Desktop/StarWar/StarWars_QA_Test_Cases.xlsx"
try:
    wb.save(excel_path)
    print("Excel generated successfully:", excel_path)
except PermissionError:
    print("Notice: StarWars_QA_Test_Cases.xlsx is currently open in Excel. Please close it if you want to overwrite the file.")

# Also generate CSV version
csv_path = "C:/Users/HP/Desktop/StarWar/StarWars_QA_Test_Cases.csv"
try:
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers_cases)
        writer.writerows(test_cases_data)
    print("CSV generated successfully:", csv_path)
except PermissionError:
    print("Notice: StarWars_QA_Test_Cases.csv is currently open in Excel. Please close it if you want to overwrite the CSV as well.")
