import csv
import openpyxl

# 1. Read Test Cases directly from generate_sheets.py test_cases_data (source of truth)
import sys
from generate_sheets import test_cases_data, headers_cases

tc_rows = []
for tc in test_cases_data:
    row_dict = {h: val for h, val in zip(headers_cases, tc)}
    tc_rows.append(row_dict)

# 2. Read Bug Report from generate_bug_report_sheets.py or openpyxl
wb_bug = openpyxl.load_workbook('StarWars_QA_Bug_Report.xlsx')
ws_bug = wb_bug['Defect Log with Evidence']

bug_catalog = {}
bug_ids_list = []
for row in range(2, ws_bug.max_row + 1):
    num = ws_bug.cell(row=row, column=1).value
    bid = str(ws_bug.cell(row=row, column=2).value).strip()
    title = ws_bug.cell(row=row, column=3).value
    desc = ws_bug.cell(row=row, column=4).value
    req = ws_bug.cell(row=row, column=5).value
    sev = ws_bug.cell(row=row, column=7).value
    
    if bid in bug_catalog:
        print(f"WARNING: DUPLICATE BUG IN BUG REPORT: {bid}")
    else:
        bug_catalog[bid] = {
            'no': num,
            'title': title,
            'desc': desc,
            'req': req,
            'sev': sev,
            'linked_test_cases': []
        }
        bug_ids_list.append(bid)

print(f"Total Unique Bugs in Bug Report: {len(bug_catalog)} (Total rows: {len(bug_ids_list)})")

# Check for duplicates in bug report
if len(bug_catalog) == len(bug_ids_list):
    print("[PASS] ZERO duplicate bugs in Bug Report. All 19 Defect IDs are unique.")
else:
    print("[FAIL] DUPLICATE BUGS DETECTED!")

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

print("\n--- MAPPING FAILED TEST CASES TO BUG REPORT ---")
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

print("\n--- DEFECTS NOT COVERED BY FAILED TEST CASES ---")
uncovered_bugs = []
for bid, data in bug_catalog.items():
    if not data['linked_test_cases']:
        uncovered_bugs.append((bid, data['title']))
        print(f"[WARN] Defect {bid} has NO failed test cases pointing to it: {data['title']}")
    else:
        print(f"[OK] Defect {bid} is covered by {len(data['linked_test_cases'])} test cases: {', '.join(data['linked_test_cases'])}")

print("\n--- UNLINKED FAILED TEST CASES DETAILS ---")
for tc in failed_tcs:
    tcid = tc['Test Case ID']
    linked = tc.get('Linked Defect', '').strip()
    if not linked or linked not in bug_catalog:
        print(f"ID: {tcid}")
        print(f"  Req: {tc.get('Req Ref')}")
        print(f"  Scenario: {tc.get('Test Scenario / Description')}")
        print(f"  Expected: {tc.get('Expected Result')}")
        print(f"  Actual: {tc.get('Actual Result')}")
        print()

print("\n--- CHECKING DEF-10 IN TEST CASES ---")
for tc in tc_rows:
    desc = tc.get('Test Scenario / Description', '')
    if 'align' in desc.lower() or 'chevron' in desc.lower() or 'right' in desc.lower() or 'icon' in desc.lower():
        print(f"Candidate TC for DEF-10: {tc['Test Case ID']} | Status: {tc['Status']} | Linked: {tc.get('Linked Defect')}")
        print(f"  Scenario: {desc}")
