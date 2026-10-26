/**
 * Test Suite: Missing Required Inputs & Negative Boundary Matrix
 * Verifies character subset rejections and empty/whitespace handling for password validation.
 */

const { validatePassword } = require('./auth_validation.test');

const missingInputTests = [
  { scenario: 'Empty String', input: '', expected: false, reason: 'Zero characters' },
  { scenario: 'Whitespace Only', input: '        ', expected: false, reason: 'No alphanumeric or special characters' },
  { scenario: 'Missing Lowercase ([a-z])', input: 'LUKE123!FORCE', expected: false, reason: 'Only uppercase, numbers, and symbol' },
  { scenario: 'Missing Uppercase ([A-Z])', input: 'luke123!force', expected: false, reason: 'Only lowercase, numbers, and symbol' },
  { scenario: 'Missing Number ([0-9])', input: 'Luke_Skywalker!', expected: false, reason: 'Only letters and symbol' },
  { scenario: 'Missing Symbol/Underscore ([\\W_])', input: 'LukeSkywalker123', expected: false, reason: 'Only letters and numbers' },
  { scenario: 'Only Numbers', input: '12345678', expected: false, reason: 'Missing lowercase, uppercase, symbol' },
  { scenario: 'Only Lowercase', input: 'abcdefgh', expected: false, reason: 'Missing uppercase, number, symbol' },
  { scenario: 'Only Uppercase', input: 'ABCDEFGH', expected: false, reason: 'Missing lowercase, number, symbol' },
  { scenario: 'Only Special Characters', input: '!@#$%^&*()', expected: false, reason: 'Missing lowercase, uppercase, number' },
  { scenario: 'Valid (All Required Present)', input: 'm4y_th3_F0rc3_b3_w1th_u', expected: true, reason: 'Contains [a-z], [A-Z], [0-9], and [_]' }
];

function runMissingInputsTests() {
  const results = [];
  missingInputTests.forEach(t => {
    try {
      const result = validatePassword(t.input);
      if (result !== t.expected) {
        throw new Error(`Expected ${t.expected} but received ${result} (${t.reason})`);
      }
      results.push({
        name: `Input Matrix: ${t.scenario} -> Rejected: ${!result} (${t.reason})`,
        status: 'PASS'
      });
    } catch (err) {
      results.push({
        name: `Input Matrix: ${t.scenario}`,
        status: 'FAIL',
        error: err.message
      });
    }
  });
  return results;
}

if (require.main === module) {
  console.log('--- MISSING REQUIRED INPUTS TEST MATRIX ---');
  const results = runMissingInputsTests();
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✔ PASS' : '✖ FAIL';
    console.log(`${icon} | ${r.name}`);
  });
}

module.exports = {
  runMissingInputsTests,
  missingInputTests
};
