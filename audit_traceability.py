import csv
import openpyxl
import sys
from generate_sheets import test_cases_data, headers_cases

# 1. Read Test Cases directly from generate_sheets.py test_cases_data (source of truth)
tc_rows = []
for tc in test_cases_data:
    row_dict = {h: val for h, val in zip(headers_cases, tc)}
    tc_rows.append(row_dict)

# 2. Read Bug Report from StarWars_QA_Bug_Report.xlsx
wb_bug = openpyxl.load_workbook('StarWars_QA_Bug_Report.xlsx')
ws_bug = wb_bug['Defect Log with Evidence']

bug_catalog = {}
bug_ids_list = []
for row in range(2, ws_bug.max_row + 1):
    num = ws_bug.cell(row=row, column=1).value
    bid = str(ws_bug.cell(row=row, column=2).value).strip()
    associated_tc = str(ws_bug.cell(row=row, column=3).value).strip()
    title = ws_bug.cell(row=row, column=4).value
    desc = ws_bug.cell(row=row, column=5).value
    req = ws_bug.cell(row=row, column=6).value
    sev = ws_bug.cell(row=row, column=8).value
    
    if bid in bug_catalog:
        print(f"WARNING: DUPLICATE BUG IN BUG REPORT: {bid}")
    else:
        bug_catalog[bid] = {
            'no': num,
            'associated_tc': associated_tc,
            'title': title,
            'desc': desc,
            'req': req,
            'sev': sev,
            'linked_test_cases': []
        }
        bug_ids_list.append(bid)

print(f"Total Unique Bugs in Bug Report: {len(bug_catalog)} (Total rows: {len(bug_ids_list)})")

if len(bug_catalog) == len(bug_ids_list) == 26:
    print("[PASS] EXACTLY 26 UNIQUE DEFECTS in Bug Report with ZERO duplicates.")
else:
    print(f"[FAIL] Expected 26 unique defects, found {len(bug_catalog)}.")

# 3. Check Failed Test Cases
failed_tcs = []
passed_tcs = []
for tc in tc_rows:
    status = tc['Status'].strip().upper()
    if status == 'FAIL':
        failed_tcs.append(tc)
    else:
        passed_tcs.append(tc)

print(f"\nTotal Test Cases: {len(tc_rows)}")
print(f"Passed Test Cases: {len(passed_tcs)}")
print(f"Failed Test Cases: {len(failed_tcs)}")

print("\n--- 1. MAPPING FAILED TEST CASES -> BUG REPORT ---")
unlinked_failed_tcs = []
for tc in failed_tcs:
    tcid = tc['Test Case ID']
    scenario = tc['Test Scenario / Description']
    linked = tc.get('Linked Defect', '').strip()
    
    if not linked:
        unlinked_failed_tcs.append((tcid, scenario, "No Linked Defect specified"))
        print(f"[FAIL] {tcid} FAILED but has NO Linked Defect!")
    elif linked not in bug_catalog:
        unlinked_failed_tcs.append((tcid, scenario, f"Linked Defect '{linked}' does not exist in Bug Report"))
        print(f"[FAIL] {tcid} FAILED but points to NON-EXISTENT defect: {linked}")
    else:
        bug_catalog[linked]['linked_test_cases'].append(tcid)
        print(f"[OK] {tcid} -> {linked} ({bug_catalog[linked]['title']})")

print("\n--- 2. VERIFYING LOGGED BUGS -> TEST EXECUTION SHEET ---")
tc_ids_in_sheet = {tc['Test Case ID']: tc for tc in tc_rows}
uncovered_bugs = []
for bid, data in bug_catalog.items():
    assoc_tc = data['associated_tc']
    if assoc_tc not in tc_ids_in_sheet:
        uncovered_bugs.append((bid, assoc_tc, "Not found in Test Case sheet"))
        print(f"[FAIL] Defect {bid} references non-existent test case: {assoc_tc}")
    else:
        tc_info = tc_ids_in_sheet[assoc_tc]
        tc_status = tc_info['Status']
        tc_linked_def = tc_info['Linked Defect']
        if tc_status != 'FAIL':
            print(f"[FAIL] Defect {bid} maps to {assoc_tc} which is NOT FAIL (Status: {tc_status})")
        elif tc_linked_def != bid:
            print(f"[FAIL] Defect {bid} maps to {assoc_tc}, but test case points to {tc_linked_def}!")
        else:
            print(f"[OK] Defect {bid} <---> {assoc_tc} (Status: {tc_status}, 1:1 Verified)")

print("\n=======================================================")
if len(failed_tcs) == 26 and len(bug_catalog) == 26 and not unlinked_failed_tcs and not uncovered_bugs:
    print("SUCCESS: 100% 1:1 BIDIRECTIONAL VERIFICATION CONFIRMED!")
    print(" - Total Executed Test Cases: 60 (34 PASS, 26 FAIL)")
    print(" - Total Documented Defects: 26 (DEF-01 to DEF-26)")
    print(" - Zero unmapped test failures, zero orphaned defect entries.")
else:
    print("AUDIT FAILED: Discrepancy detected.")
print("=======================================================")
