/**
 * Test Suite: Security Static Analysis & Configuration Audit
 * Evaluates the codebase against OWASP Mobile Top 10 guidelines:
 * - M1: Improper Platform Usage
 * - M2: Insecure Data Storage
 * - M3: Insecure Communication
 * - M4: Insecure Authentication
 * - M9: Reverse Engineering & Code Tampering
 */

const fs = require('fs');
const path = require('path');

function runSecurityAuditTests() {
  const results = [];

  function audit(name, severity, fn) {
    try {
      const issue = fn();
      if (issue) {
        results.push({
          name,
          status: 'VULNERABILITY_FOUND',
          severity,
          details: issue,
        });
      } else {
        results.push({
          name,
          status: 'SECURE',
          severity: 'NONE',
          details: 'No vulnerability detected',
        });
      }
    } catch (err) {
      results.push({
        name,
        status: 'ERROR',
        severity: 'HIGH',
        details: err.message,
      });
    }
  }

  const projectRoot = path.join(__dirname, '../StarWarsApp-main');

  // 1. Insecure Data Storage: Plaintext password saved to MMKV
  audit('OWASP M2: Plaintext Password Stored in Local MMKV Storage', 'CRITICAL', () => {
    const registerScreen = fs.readFileSync(path.join(projectRoot, 'src/screens/RegisterScreen/index.js'), 'utf8');
    const apiServices = fs.readFileSync(path.join(projectRoot, 'src/react-query/states/apiServices.js'), 'utf8');
    
    const hasPlaintextSave = registerScreen.includes('StorageKey.CURR_USER_LOGIN_DATA, { email: data.email, password: data.password }') ||
                             apiServices.includes('password: params?.password');

    if (hasPlaintextSave) {
      return 'Passwords are stored unhashed (plaintext) in client-side MMKV storage via StorageKey.CURR_USER_LOGIN_DATA and LIST_USER. Violates CWE-312.';
    }
    return null;
  });

  // 2. Hardcoded Secrets: Google Maps API key in AndroidManifest.xml
  audit('OWASP M1/M9: Hardcoded Google Maps API Key in AndroidManifest.xml', 'HIGH', () => {
    const manifest = fs.readFileSync(path.join(projectRoot, 'android/app/src/main/AndroidManifest.xml'), 'utf8');
    const apiKeyMatch = manifest.match(/android:name="com.google.android.geo.API_KEY"\s+android:value="([^"]+)"/);
    if (apiKeyMatch && apiKeyMatch[1]) {
      const maskedKey = apiKeyMatch[1].substring(0, 24) + '********';
      return `Exposed production API key detected in AndroidManifest.xml: "${maskedKey}". Anyone decompiling the APK can extract and abuse this key.`;
    }
    return null;
  });

  // 3. Insecure Communication: Plaintext HTTP allowed on iOS & Android
  audit('OWASP M3: iOS App Transport Security (NSAllowsArbitraryLoads = true)', 'HIGH', () => {
    const plist = fs.readFileSync(path.join(projectRoot, 'ios/StarWarsApp/Info.plist'), 'utf8');
    if (plist.includes('<key>NSAllowsArbitraryLoads</key>') && plist.includes('<true/>')) {
      return 'NSAllowsArbitraryLoads is set to true in Info.plist. This disables iOS TLS enforcement, allowing unencrypted HTTP traffic susceptible to MITM attacks.';
    }
    return null;
  });

  // 4. Insecure Communication: Cleartext HTTP localhost endpoint in apiCallers.js
  audit('OWASP M3: Cleartext HTTP Backend URL Configured', 'MEDIUM', () => {
    const apiCaller = fs.readFileSync(path.join(projectRoot, 'src/react-query/utils/apiCallers.js'), 'utf8');
    if (apiCaller.includes("API_HOST = 'http://localhost:3000'")) {
      return "Default API_HOST is configured using unencrypted 'http://localhost:3000' instead of secure HTTPS.";
    }
    return null;
  });

  // 5. Code Tampering / Reverse Engineering: Release APK signed with Debug Keystore
  audit('OWASP M9: Release Build Uses Debug Keystore Signing', 'HIGH', () => {
    const buildGradle = fs.readFileSync(path.join(projectRoot, 'android/app/build.gradle'), 'utf8');
    if (buildGradle.includes('release {') && buildGradle.includes('signingConfig signingConfigs.debug')) {
      return 'android/app/build.gradle configures buildTypes.release to sign with debug.keystore. Compromises application authenticity and APK integrity.';
    }
    return null;
  });

  // 6. Code Tampering: Proguard / Code Obfuscation Disabled
  audit('OWASP M9: Code Minification & Proguard Obfuscation Disabled in Release', 'MEDIUM', () => {
    const buildGradle = fs.readFileSync(path.join(projectRoot, 'android/app/build.gradle'), 'utf8');
    if (buildGradle.includes('def enableProguardInReleaseBuilds = false')) {
      return 'enableProguardInReleaseBuilds is set to false. Release APK will contain unobfuscated Java/Kotlin bytecode easily reverse-engineered via JADX.';
    }
    return null;
  });

  // 7. Missing Permission Description in iOS Info.plist
  audit('OWASP M1: Missing NSPhotoLibraryUsageDescription in iOS Info.plist', 'HIGH', () => {
    const plist = fs.readFileSync(path.join(projectRoot, 'ios/StarWarsApp/Info.plist'), 'utf8');
    if (!plist.includes('<key>NSPhotoLibraryUsageDescription</key>')) {
      return 'NSPhotoLibraryUsageDescription is missing in Info.plist. Attempting to open device photo gallery on iOS will immediately crash the application.';
    }
    return null;
  });

  return results;
}

module.exports = { runSecurityAuditTests };
