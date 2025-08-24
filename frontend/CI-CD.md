# CI/CD Pipeline untuk Swarm Lab Frontend

## Overview
Pipeline CI/CD otomatis untuk aplikasi Nuxt.js menggunakan GitHub Actions.

## Workflow

### Build & Test
- Trigger: Push ke branch `main` atau `develop`, atau Pull Request
- Jobs:
  - Setup Node.js (versi 18.x dan 20.x)
  - Install dependencies dengan Yarn
  - Type checking dengan `nuxt typecheck`
  - Linting dengan ESLint
  - Build aplikasi
  - Run tests

### Deployment
- Trigger: Hanya pada push ke branch `main`
- Prerequisite: Harus lolos semua tahap Build & Test
- Actions: Build aplikasi untuk production

## Setup

### 1. Dependencies
Pastikan package.json memiliki script berikut:

```json
{
  "scripts": {
    "typecheck": "nuxt typecheck",
    "lint": "eslint .",
    "test": "echo \"Tests would run here\" && exit 0"
  }
}
```

### 2. ESLint Configuration
File `.eslintrc.js` sudah dikonfigurasi dengan preset Nuxt.js TypeScript.

### 3. GitHub Secrets (Untuk Deployment)
Jika menggunakan platform deploy seperti Vercel/Netlify, tambahkan secrets:
- `VERCEL_TOKEN` untuk Vercel
- `ORG_ID` dan `PROJECT_ID` jika diperlukan

## Customization

### Menambahkan Testing
1. Install testing framework (Vitest/Jest):
```bash
yarn add -D vitest @vue/test-utils
```

2. Update script test di package.json:
```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

### Deployment Platforms

#### Vercel
Uncomment bagian Vercel di workflow file dan setup secrets.

#### Netlify
Gunakan action `netlify/actions/cli`

#### AWS S3/CloudFront
Gunakan `aws-actions/configure-aws-credentials`

## Monitoring
- Check Actions tab di GitHub repository
- Setup notifications untuk build failures
- Monitor deployment status di platform target

## Troubleshooting

### Build Failures
- Pastikan semua dependencies terinstall dengan `yarn install`
- Check TypeScript errors dengan `yarn typecheck`
- Fix linting errors dengan `yarn lint --fix`

### Cache Issues
- Hapus GitHub Actions cache jika ada masalah dependency caching

Version: v1