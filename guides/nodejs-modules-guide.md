# Node.js Module Systems Guide for ARM64

## Environment Requirements

- Windows 11 ARM64 (Version 10.0.26100)
- Node.js v22.14.0 (ARM64)
- npm v11.1.0
- pnpm v9.15.3
- PowerShell Core 7.4.6

## Module Types Overview

### ES Modules (ESM)

Modern JavaScript module system, recommended for ARM64 development.

```javascript
// Importing
import express from 'express';
import { function1, function2 } from 'package';
import * as allExports from 'package';

// Exporting
export default express;
export const myFunction = () => {};
export { function1, function2 };

// Verify ARM64
console.log(`Running on ${process.arch}`);  // should show 'arm64'
```

### CommonJS (CJS)

Traditional Node.js module system, some modules may require x64 emulation.

```javascript
// Importing
const express = require('express');
const { function1, function2 } = require('package');

// Exporting
module.exports = express;
exports.myFunction = () => {};
module.exports = { function1, function2 };

// Verify ARM64
console.log(`Running on ${process.arch}`);  // should show 'arm64'
```

## ARM64 Considerations

### Native Modules

1. Check module compatibility:

   ```powershell
   # List native dependencies
   npm list | Where-Object { $_ -match "node-gyp" }
   
   # Check specific module
   npm view module-name cpu
   ```

2. Handle binary modules:

   ```javascript
   // Graceful fallback for incompatible modules
   try {
       const nativeModule = require('native-module');
   } catch (error) {
       console.warn('Native module not available on ARM64, using fallback');
       const fallbackModule = require('./fallbacks/native-module');
   }
   ```

3. Use ARM64-specific builds:

   ```json
   {
     "dependencies": {
       "module-name": "npm:@arm64/module-name"
     }
   }
   ```

### Performance Optimization

1. Memory management:

   ```javascript
   // Configure heap limits for ARM64
   const v8 = require('v8');
   v8.setFlagsFromString('--max-old-space-size=8192');
   
   // Monitor memory usage
   const used = process.memoryUsage();
   console.log(`Memory usage: ${Math.round(used.heapUsed / 1024 / 1024)}MB`);
   ```

2. Worker threads:

   ```javascript
   // Optimize for ARM64 cores
   import { Worker, isMainThread, parentPort } from 'worker_threads';
   
   if (isMainThread) {
     const worker = new Worker(__filename);
     worker.on('message', (msg) => console.log(msg));
   } else {
     // Worker code optimized for ARM64
     parentPort.postMessage('Worker running on ARM64');
   }
   ```

## Module Systems in Modern Development

### Next.js 14 Integration (ARM64 Native)

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable ARM64 optimizations
  experimental: {
    optimizePackageImports: true,
    serverActions: true,
  },
  
  // Configure module resolution
  webpack: (config, { isServer }) => {
    // Handle native modules
    config.resolve.alias = {
      ...config.resolve.alias,
      // Add ARM64-specific aliases
    };
    return config;
  }
};

export default nextConfig;
```

### Package Management

```json
{
  "name": "your-project",
  "version": "1.0.0",
  "type": "module",
  "engines": {
    "node": ">=22.14.0",
    "npm": ">=11.1.0"
  },
  "scripts": {
    "verify-arch": "node -p \"process.arch === 'arm64' ? 'ARM64 ✅' : 'Not ARM64 ❌'\"",
    "check-natives": "npm list | grep -i 'node-gyp'",
    "postinstall": "node scripts/verify-arm64-modules.js"
  }
}
```

### Module Verification Script

```javascript
// scripts/verify-arm64-modules.js
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs/promises';

const require = createRequire(import.meta.url);
const __dirname = dirname(fileURLToPath(import.meta.url));

async function verifyModules() {
    const pkgPath = join(__dirname, '../package.json');
    const pkg = JSON.parse(await fs.readFile(pkgPath, 'utf8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    
    console.log('Checking module compatibility with ARM64...\n');
    
    for (const [name, version] of Object.entries(deps)) {
        try {
            const moduleInfo = require(`${name}/package.json`);
            const hasARM64 = moduleInfo.cpu?.includes('arm64');
            const isNative = moduleInfo.gypfile;
            
            console.log(`${name}@${version}`);
            console.log(`  Native Module: ${isNative ? 'Yes' : 'No'}`);
            console.log(`  ARM64 Support: ${hasARM64 ? '✅' : '❌'}`);
            
            if (isNative && !hasARM64) {
                console.warn(`  ⚠️ Warning: Native module without ARM64 support`);
            }
        } catch (error) {
            console.error(`  Error checking ${name}: ${error.message}`);
        }
    }
}

verifyModules().catch(console.error);
```

### Development Tools Integration

1. VS Code settings:

   ```json
   {
     "typescript.tsdk": "node_modules/typescript/lib",
     "npm.packageManager": "pnpm",
     "javascript.preferences.importModuleSpecifier": "relative",
     "javascript.updateImportsOnFileMove.enabled": "always"
   }
   ```

2. ESLint configuration:

   ```javascript
   // .eslintrc.js
   module.exports = {
     extends: ['next/core-web-vitals'],
     rules: {
       'import/extensions': ['error', 'ignorePackages', {
         js: 'never',
         jsx: 'never',
         ts: 'never',
         tsx: 'never'
       }]
     }
   };
   ```

## Common Issues and Solutions

### 1. Native Module Compatibility

```javascript
// Check and handle native modules
async function loadNativeModule(moduleName) {
    try {
        // Try loading native version
        const module = await import(moduleName);
        return module;
    } catch (error) {
        console.warn(`Native module ${moduleName} failed to load on ARM64`);
        // Load pure JS fallback
        return await import(`${moduleName}-fallback`);
    }
}
```

### 2. Performance Monitoring

```javascript
// Monitor ARM64 performance
import { performance, PerformanceObserver } from 'perf_hooks';

const obs = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    entries.forEach((entry) => {
        console.log(`${entry.name}: ${entry.duration}ms`);
    });
});
obs.observe({ entryTypes: ['measure'] });

// Measure operations
performance.mark('start');
// ... your code ...
performance.mark('end');
performance.measure('Operation', 'start', 'end');
```

### 3. Memory Management

```javascript
// Monitor memory usage on ARM64
function monitorMemory() {
    const used = process.memoryUsage();
    console.log({
        rss: `${Math.round(used.rss / 1024 / 1024)}MB`,
        heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)}MB`,
        heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)}MB`,
        external: `${Math.round(used.external / 1024 / 1024)}MB`
    });
}

// Monitor every 5 minutes
setInterval(monitorMemory, 300000);
```

## Verification and Testing

```powershell
# PowerShell verification script
function Test-NodeEnvironment {
    $tests = @(
        @{
            Name = "Node.js Version"
            Test = { (node -v) -eq "v22.14.0" }
        },
        @{
            Name = "Architecture"
            Test = { (node -p "process.arch") -eq "arm64" }
        },
        @{
            Name = "npm Version"
            Test = { (npm -v) -eq "11.1.0" }
        },
        @{
            Name = "pnpm Version"
            Test = { (pnpm -v) -eq "9.15.3" }
        }
    )
    
    foreach ($test in $tests) {
        Write-Host "Testing $($test.Name)... " -NoNewline
        if (& $test.Test) {
            Write-Host "PASSED" -ForegroundColor Green
        } else {
            Write-Host "FAILED" -ForegroundColor Red
        }
    }
}

# Run verification
Test-NodeEnvironment
```

## Additional Resources

- [Node.js ARM64 Documentation](https://nodejs.org/docs/)
- [Next.js ARM64 Guide](https://nextjs.org/docs)
- [Native Module Guide](https://nodejs.org/api/n-api.html)
- [Performance Tuning](https://nodejs.org/docs/latest/api/perf_hooks.html)

Last Updated: February 12, 2024
