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
  const LUKE_EMAIL = process.env.TEST_LUKE_EMAIL || 'luke_skywalker@starwars.com';
  const LUKE_PASSWORD = process.env.TEST_LUKE_PASSWORD || 'm4y_th3_F0rc3_b3_w1th_u';
  const VADER_EMAIL = process.env.TEST_VADER_EMAIL || 'anakin_skywalker@starwars.com';
  const VADER_PASSWORD = process.env.TEST_VADER_PASSWORD || '1_4m_ur_F4th3r!';

  test(`Req 1.a: Luke Skywalker Email (${LUKE_EMAIL}) is valid`, () => {
    assert(validateEmail(LUKE_EMAIL), `Email ${LUKE_EMAIL} should be valid`);
  });

  test('Req 1.a: Luke Skywalker Password satisfies complexity', () => {
    // Luke password contains lowercase, 'F' uppercase, digits, underscore, len >= 8
    const valid = validatePassword(LUKE_PASSWORD);
    assert(valid, 'Luke password must satisfy complexity regex');
  });

  test(`Req 1.b: Darth Vader Email (${VADER_EMAIL}) is valid`, () => {
    assert(validateEmail(VADER_EMAIL), `Email ${VADER_EMAIL} should be valid`);
  });

  test('Req 1.b: Darth Vader Password satisfies complexity', () => {
    // Vader password contains lowercase, 'F' uppercase, digits, underscore, symbol, len >= 8
    const valid = validatePassword(VADER_PASSWORD);
    assert(valid, 'Vader password must satisfy complexity regex');
  });

  test('Negative: Password without uppercase fails (e.g. m4y_th3_f0rc3_b3_w1th_u)', () => {
    const valid = validatePassword('m4y_th3_f0rc3_b3_w1th_u');
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
    assert(!validateEmail(' luke_skywalker@starwars.com'), 'Untrimmed email fails without explicit trim()');
  });

  return results;
}

module.exports = { runAuthValidationTests, validateEmail, validatePassword };
