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

console.log('--- MISSING REQUIRED INPUTS TEST MATRIX ---');
missingInputTests.forEach(t => {
  const result = validatePassword(t.input);
  const status = result === t.expected ? '✔ PASS' : '✖ FAIL';
  console.log(`${status} | ${t.scenario.padEnd(35)} -> Rejected: ${!result} (${t.reason})`);
});
