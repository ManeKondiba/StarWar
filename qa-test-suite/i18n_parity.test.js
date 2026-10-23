/**
 * Test Suite: Localization & Internationalization (I18n / L10n) Parity
 * Compares en.json and id.json to verify complete key parity,
 * parameter matching (e.g. {{count}}), and detects missing/empty translations.
 */

const fs = require('fs');
const path = require('path');

function getKeysRecursively(obj, prefix = '') {
  let keys = [];
  for (const k of Object.keys(obj)) {
    const fullKey = prefix ? `${prefix}.${k}` : k;
    if (typeof obj[k] === 'object' && obj[k] !== null && !Array.isArray(obj[k])) {
      keys = keys.concat(getKeysRecursively(obj[k], fullKey));
    } else {
      keys.push({ key: fullKey, value: obj[k] });
    }
  }
  return keys;
}

function runI18nParityTests() {
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

  const enPath = path.join(__dirname, '../StarWarsApp-main/src/constants/en.json');
  const idPath = path.join(__dirname, '../StarWarsApp-main/src/constants/id.json');

  const enContent = JSON.parse(fs.readFileSync(enPath, 'utf8'));
  const idContent = JSON.parse(fs.readFileSync(idPath, 'utf8'));

  const enKeys = getKeysRecursively(enContent);
  const idKeys = getKeysRecursively(idContent);

  const enKeySet = new Set(enKeys.map((k) => k.key));
  const idKeySet = new Set(idKeys.map((k) => k.key));

  test('Req 13: en.json and id.json files exist and are valid JSON', () => {
    assert(enContent && typeof enContent === 'object', 'en.json must be valid');
    assert(idContent && typeof idContent === 'object', 'id.json must be valid');
  });

  test('Req 13: All keys in en.json exist in id.json (Zero missing Indonesian translations)', () => {
    const missingInId = [];
    for (const key of enKeySet) {
      if (!idKeySet.has(key)) {
        missingInId.push(key);
      }
    }
    assert(
      missingInId.length === 0,
      `Missing keys in id.json: ${missingInId.join(', ')}`
    );
  });

  test('Req 13: All keys in id.json exist in en.json (Zero missing English translations)', () => {
    const missingInEn = [];
    for (const key of idKeySet) {
      if (!enKeySet.has(key)) {
        missingInEn.push(key);
      }
    }
    assert(
      missingInEn.length === 0,
      `Missing keys in en.json: ${missingInEn.join(', ')}`
    );
  });

  test('Req 13: No empty translation strings in en.json', () => {
    const emptyEn = enKeys.filter((k) => typeof k.value === 'string' && k.value.trim() === '');
    assert(emptyEn.length === 0, `Empty strings found in en.json: ${emptyEn.map((e) => e.key).join(', ')}`);
  });

  test('Req 13: No empty translation strings in id.json', () => {
    const emptyId = idKeys.filter((k) => typeof k.value === 'string' && k.value.trim() === '');
    assert(emptyId.length === 0, `Empty strings found in id.json: ${emptyId.map((e) => e.key).join(', ')}`);
  });

  test('Req 13: Dynamic interpolation variables match between en.json and id.json', () => {
    const regex = /\{\{([^}]+)\}\}/g;
    const mismatches = [];

    const enMap = new Map(enKeys.map((k) => [k.key, k.value]));
    const idMap = new Map(idKeys.map((k) => [k.key, k.value]));

    for (const [key, enVal] of enMap.entries()) {
      const idVal = idMap.get(key);
      if (typeof enVal === 'string' && typeof idVal === 'string') {
        const enVars = (enVal.match(regex) || []).sort();
        const idVars = (idVal.match(regex) || []).sort();
        if (enVars.join(',') !== idVars.join(',')) {
          mismatches.push(`${key} (EN: ${enVars} vs ID: ${idVars})`);
        }
      }
    }
    assert(mismatches.length === 0, `Interpolation variable mismatch in: ${mismatches.join('; ')}`);
  });

  return results;
}

module.exports = { runI18nParityTests };
