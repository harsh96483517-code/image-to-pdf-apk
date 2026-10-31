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

- Pick multiple images from the gallery, including very large batches
- Reorder, reverse, or remove them
- A4 / Letter page sizes, or fit each page to the image
- Quality: Auto / High / Small file
- Live progress bar with cancel
- Share or save the finished PDF via the system share sheet

## Large batches (100-500+ images)

Building a PDF from hundreds of photos is memory-bound, so the app is written
to keep the peak footprint flat instead of growing with the batch:

- Page images are downscaled to a 1240 px long edge (900 px in "Small file"
  mode) before they reach jsPDF. A 48 MP phone photo becomes a few hundred KB
  instead of tens of MB.
- Images are decoded one at a time and every reference is dropped before the
  next one, so only a single bitmap is alive at once.
- List thumbnails are 128 px and decoded lazily as you scroll, not all at once.
- The finished PDF is written to disk in ~400 KB chunks (`writeFile` then
  `appendFile`) rather than as one base64 string of the whole file.
- `android:largeHeap="true"` is added to the manifest by
  `scripts/patch-manifest.py` during the CI build.

Unreadable files are skipped rather than aborting the whole run, and the status
line reports how many were skipped.
