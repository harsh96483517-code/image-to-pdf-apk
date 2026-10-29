# Image to PDF (Android APK)

A tiny offline Android app that turns a set of photos from your gallery into a single PDF.

Built with Capacitor, so the whole UI is one self-contained HTML page in `www/`.
jsPDF is bundled locally (`www/vendor/`), so the app works with no internet connection.

## Build the APK

The APK is built in the cloud by GitHub Actions — no Android SDK needed on your machine.

1. Push to `main` (or run the **Build APK** workflow manually from the Actions tab).
2. Open the workflow run and download the `image-to-pdf-apk` artifact.
3. Unzip it and install `app-debug.apk` on your phone (allow "install unknown apps").

## Build locally

```bash
npm install
npm run prepare-web
npx cap add android
npx cap sync android
cd android && ./gradlew assembleDebug
```

Output: `android/app/build/outputs/apk/debug/app-debug.apk`

`npm run prepare-web` copies jsPDF out of `node_modules` into `www/vendor/`, which is gitignored.

## Features

- Pick multiple images from the gallery
- Reorder, reverse, or remove them
- A4 / Letter page sizes, or fit each page to the image
- Share or save the finished PDF via the system share sheet
