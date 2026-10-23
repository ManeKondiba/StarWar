/**
 * StarWars App - Master QA Test Suite Runner
 * Executes all automated test modules and reports results.
 */

const { runAuthValidationTests } = require('./auth_validation.test');
const { runI18nParityTests } = require('./i18n_parity.test');
const { runSecurityAuditTests } = require('./security_audit.test');
const { runSwapiApiTests } = require('./swapi_api.test');

// ANSI color codes
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const GRAY = '\x1b[90m';

async function main() {
  const startTime = Date.now();
  console.log(`\n${BOLD}${CYAN}====================================================${RESET}`);
  console.log(`${BOLD}${CYAN}  STAR WARS REACT NATIVE APP - QA AUTOMATED SUITE   ${RESET}`);
  console.log(`${BOLD}${CYAN}====================================================${RESET}\n`);

  let totalTests = 0;
  let passedTests = 0;
  let failedTests = 0;
  let vulnerabilitiesFound = 0;

  // 1. Auth Validation Tests
  console.log(`${BOLD}1. Authentication & Input Validation Tests${RESET}`);
  const authResults = runAuthValidationTests();
  for (const r of authResults) {
    totalTests++;
    if (r.status === 'PASS') {
      passedTests++;
      console.log(`  ${GREEN}✔ PASS${RESET}  ${r.name}`);
    } else {
      failedTests++;
      console.log(`  ${RED}✖ FAIL${RESET}  ${r.name} - ${GRAY}${r.error}${RESET}`);
    }
  }

  // 2. I18n Parity Tests
  console.log(`\n${BOLD}2. I18n & L10n Translation Parity Tests (en.json vs id.json)${RESET}`);
  const i18nResults = runI18nParityTests();
  for (const r of i18nResults) {
    totalTests++;
    if (r.status === 'PASS') {
      passedTests++;
      console.log(`  ${GREEN}✔ PASS${RESET}  ${r.name}`);
    } else {
      failedTests++;
      console.log(`  ${RED}✖ FAIL${RESET}  ${r.name} - ${GRAY}${r.error}${RESET}`);
    }
  }

  // 3. Security Audit Tests
  console.log(`\n${BOLD}3. OWASP Mobile Top 10 Security & Config Audit${RESET}`);
  const secResults = runSecurityAuditTests();
  for (const r of secResults) {
    if (r.status === 'VULNERABILITY_FOUND') {
      vulnerabilitiesFound++;
      const color = r.severity === 'CRITICAL' ? RED : r.severity === 'HIGH' ? YELLOW : CYAN;
      console.log(`  ${color}[${r.severity}] VULNERABILITY${RESET}  ${r.name}`);
      console.log(`    ${GRAY}↳ ${r.details}${RESET}`);
    } else if (r.status === 'SECURE') {
      console.log(`  ${GREEN}✔ SECURE${RESET}  ${r.name}`);
    } else {
      console.log(`  ${RED}✖ ERROR${RESET}  ${r.name} - ${r.details}`);
    }
  }

  // 4. SWAPI API Contract & Defect Detection Tests
  console.log(`\n${BOLD}4. Star Wars API (SWAPI) Contract & Integration Tests${RESET}`);
  const swapiResults = await runSwapiApiTests();
  for (const r of swapiResults) {
    totalTests++;
    if (r.status === 'PASS') {
      passedTests++;
      console.log(`  ${GREEN}✔ PASS${RESET}  ${r.name}`);
    } else {
      failedTests++;
      console.log(`  ${RED}✖ DEFECT DETECTED${RESET}  ${r.name}`);
      console.log(`    ${GRAY}↳ ${r.error}${RESET}`);
    }
  }

  const duration = ((Date.now() - startTime) / 1000).toFixed(2);

  console.log(`\n${BOLD}${CYAN}====================================================${RESET}`);
  console.log(`${BOLD}QA TEST EXECUTION SUMMARY${RESET}`);
  console.log(`${BOLD}${CYAN}====================================================${RESET}`);
  console.log(`  Execution Time:          ${duration}s`);
  console.log(`  Total Functional Tests:  ${totalTests}`);
  console.log(`  Passed Tests:            ${GREEN}${passedTests}${RESET}`);
  console.log(`  Failed / Defect Tests:   ${RED}${failedTests}${RESET}`);
  console.log(`  Security Vulnerabilities:${YELLOW}${vulnerabilitiesFound}${RESET}`);
  console.log(`${BOLD}${CYAN}====================================================${RESET}\n`);
}

main().catch((err) => {
  console.error('Fatal error during test execution:', err);
  process.exit(1);
});
