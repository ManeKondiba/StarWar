/**
 * Test Suite: Star Wars API (SWAPI) Contract & Behavioral Tests
 * Validates the endpoints, data contracts, and detects the search/pagination defect
 * caused by swapi.info static host behavior.
 */

async function runSwapiApiTests() {
  const results = [];

  async function test(name, fn) {
    try {
      await fn();
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

  const BASE_URL = 'https://swapi.info/api';

  await test('Req 4: SWAPI People endpoint responds with valid schema', async () => {
    const res = await fetch(`${BASE_URL}/people`);
    assert(res.ok, `HTTP status ${res.status}`);
    const data = await res.json();
    assert(Array.isArray(data), 'Response should be an array');
    assert(data.length > 0, 'People list should not be empty');

    const sample = data[0];
    const requiredFields = ['name', 'height', 'mass', 'birth_year', 'gender'];
    for (const field of requiredFields) {
      assert(field in sample, `Missing required field "${field}" for User Profile display`);
    }
  });

  await test('Req 9: SWAPI Starships endpoint responds with valid schema', async () => {
    const res = await fetch(`${BASE_URL}/starships`);
    assert(res.ok, `HTTP status ${res.status}`);
    const data = await res.json();
    assert(Array.isArray(data), 'Response should be an array');
    assert(data.length > 0, 'Starships list should not be empty');

    const sample = data[0];
    const requiredFields = [
      'name',
      'model',
      'manufacturer',
      'cost_in_credits',
      'length',
      'max_atmosphering_speed',
      'crew',
      'passengers',
      'cargo_capacity',
    ];
    for (const field of requiredFields) {
      assert(field in sample, `Missing required starship field "${field}"`);
    }
  });

  await test('Defect Detection: Server-side search (?search=) fails on static swapi.info mirror', async () => {
    const allRes = await fetch(`${BASE_URL}/people`);
    const allData = await allRes.json();

    const searchRes = await fetch(`${BASE_URL}/people/?search=Luke`);
    const searchData = await searchRes.json();

    // Since swapi.info is a static mirror, query parameters are ignored
    if (allData.length === searchData.length) {
      throw new Error(
        `CRITICAL DEFECT: Backend search does not filter records. Querying ?search=Luke returns all ${searchData.length} records instead of 1. Frontend must implement client-side filtering!`
      );
    }
  });

  await test('Defect Detection: Pagination data.next is undefined on static array response', async () => {
    const res = await fetch(`${BASE_URL}/people`);
    const data = await res.json();

    // The app expects data.next to trigger infinite scroll
    if (Array.isArray(data) && data.next === undefined) {
      throw new Error(
        'DEFECT DETECTED: API returns raw Array instead of paginated envelope { results: [], next: "..." }. SwapiScreen handleLoadMore check "data?.next" will always be false.'
      );
    }
  });

  return results;
}

module.exports = { runSwapiApiTests };
