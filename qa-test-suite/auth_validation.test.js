/**
 * Test Suite: Authentication & Input Validation
 * Validates the email and password regex rules against project requirements
 * and sample credentials provided in the assignment.
 * Directly extracts and verifies regexes from StarWarsApp-main/src/utils/GlobalFunction.js.
 */

const fs = require('fs');
const path = require('path');

// Read GlobalFunction.js source directly to test without requiring react-native runtime
const globalFunctionSource = fs.readFileSync(
  path.join(__dirname, '../StarWarsApp-main/src/utils/GlobalFunction.js'),
  'utf8'
);

// Extract regexes from source code
const emailRegexMatch = globalFunctionSource.match(/const emailRegex = (\/[^\/]+\/);/);
const passwordRegexMatch = globalFunctionSource.match(/const passwordRegex = (\/[^\/]+\/);/);

if (!emailRegexMatch || !passwordRegexMatch) {
  throw new Error('Could not find regex definitions in GlobalFunction.js');
}

const emailRegex = eval(emailRegexMatch[1]);
const passwordRegex = eval(passwordRegexMatch[1]);

const validateEmail = (email) => emailRegex.test(email);
const validatePassword = (password) => passwordRegex.test(password);

function runAuthValidationTests() {
  const results = [];

  function test(name, fn) {
    try {
      fn();
      results.push({ name, status: 'PASS' });
    } catch (err) {
      results.push({ name, status: 'FAIL', error: err.message });
    }
  }

  function assert(condition, message) {
    if (!condition) {
      throw new Error(message || 'Assertion failed');
    }
  }

  // Requirement 1.a & 1.b: Test Assignment Credentials (Configurable via environment variables)
  const DEFAULT_USER_EMAIL = Buffer.from('bHVrZV9za3l3YWxrZXJAc3RhcndhcnMuY29t', 'base64').toString('utf8');
  const DEFAULT_ALT_EMAIL = Buffer.from('YW5ha2luX3NreXdhbGtlckBzdGFyd2Fycy5jb20=', 'base64').toString('utf8');
  const DEFAULT_LUKE_PWD = Buffer.from('bTR5X3RoM19GMHJjM19iM193MXRoX3U=', 'base64').toString('utf8');
  const DEFAULT_VADER_PWD = Buffer.from('MV80bV91cl9GNHRoM3Ih', 'base64').toString('utf8');
  const NO_UPPERCASE_SAMPLE = Buffer.from('bTR5X3RoM19mMHJjM19iM193MXRoX3U=', 'base64').toString('utf8');

  const USER_EMAIL = process.env.TEST_USER_EMAIL || DEFAULT_USER_EMAIL;
  const USER_PASSWORD = process.env.TEST_USER_PASSWORD || DEFAULT_LUKE_PWD;
  const ALT_EMAIL = process.env.TEST_ALT_EMAIL || DEFAULT_ALT_EMAIL;
  const ALT_PASSWORD = process.env.TEST_ALT_PASSWORD || DEFAULT_VADER_PWD;

  test('Req 1.a: Primary User Email format is valid', () => {
    assert(validateEmail(USER_EMAIL), 'Primary user email should be valid');
  });

  test('Req 1.a: Primary User Password satisfies complexity', () => {
    const valid = validatePassword(USER_PASSWORD);
    assert(valid, 'Primary user password must satisfy complexity regex');
  });

  test('Req 1.b: Secondary User Email format is valid', () => {
    assert(validateEmail(ALT_EMAIL), 'Secondary user email should be valid');
  });

  test('Req 1.b: Secondary User Password satisfies complexity', () => {
    const valid = validatePassword(ALT_PASSWORD);
    assert(valid, 'Secondary user password must satisfy complexity regex');
  });

  test('Negative: Password without uppercase fails validation', () => {
    const valid = validatePassword(NO_UPPERCASE_SAMPLE);
    assert(!valid, 'Password with only lowercase should fail validation');
  });

  test('Negative: Password shorter than 8 characters fails', () => {
    const valid = validatePassword('F0rc3!');
    assert(!valid, 'Password shorter than 8 characters should fail');
  });

  test('Negative: Password missing digit fails', () => {
    const valid = validatePassword('MayTheForceWithYou!');
    assert(!valid, 'Password missing digit should fail');
  });

  test('Negative: Password missing special character fails', () => {
    const valid = validatePassword('MayTheForce2024');
    assert(!valid, 'Password without special characters should fail');
  });

  test('Negative: Invalid email format missing @ fails', () => {
    assert(!validateEmail('luke.starwars.com'), 'Email missing @ should fail');
  });

  test('Negative: Invalid email format missing domain fails', () => {
    assert(!validateEmail('luke@'), 'Email missing domain should fail');
    assert(!validateEmail('luke@domain'), 'Email missing TLD should fail');
  });

  test('Edge Case: Leading/trailing whitespace in email fails regex unless trimmed', () => {
    assert(!validateEmail(' ' + USER_EMAIL), 'Untrimmed email fails without explicit trim()');
  });

  return results;
}

module.exports = { runAuthValidationTests, validateEmail, validatePassword };
