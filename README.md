# Image to PDF (Android APK)

A tiny offline Android app that turns a set of photos from your gallery into a
single PDF. Built with Capacitor, so the whole UI is one self-contained HTML
page in `www/`. No network access needed, no external PDF library.

## Build the APK

The APK is built in the cloud by GitHub Actions — no Android SDK needed locally.

1. Push to `main` (or run the **Build APK** workflow from the Actions tab).
2. Open the workflow run and download the `image-to-pdf-apk` artifact.
3. Unzip it and install `app-debug.apk` on your phone (allow "install unknown apps").

## Build locally

```bash
npm install
npx cap add android
python3 scripts/patch-manifest.py
npx cap sync android
cd android && ./gradlew assembleDebug
```

Output: `android/app/build/outputs/apk/debug/app-debug.apk`

## How it works

There is no PDF library. `www/index.html` writes the PDF itself:

- Each page is a PDF page object plus an image XObject using the `DCTDecode`
  filter, which stores JPEG bytes as-is.
- At **Original quality** the app reads the JPEG headers (dimensions, colour
  components, EXIF orientation) and, when the file is a plain baseline or
  progressive JPEG that needs no rotation, embeds the original bytes without
  re-encoding. Nothing is decoded into memory at all.
- Any other format, or a JPEG that needs re-scaling or rotating, goes through a
  canvas and is re-encoded at the chosen quality.
- The PDF is assembled as a list of Blobs and saved by slicing it into 1.5 MB
  pieces (`writeFile`, then `appendFile`). The piece size is a multiple of 3
  bytes so every base64 piece decodes back to exactly the right bytes.

## Features

- Pick many images at once; reorder, reverse, remove
- A4, Letter, or fit-to-image page sizes
- Quality: Original / High (2400 px) / Medium (1800 px) / Small
- Live status, and unreadable files are skipped instead of aborting the run

## Large batches

The list decodes thumbnails one at a time through a queue at 120 px, so picking
hundreds of photos does not decode them all at once. `scripts/patch-manifest.py`
adds `android:largeHeap="true"` during the CI build.

For 300+ photos prefer **High** or **Medium** quality: at Original quality the
PDF keeps every original JPEG, so a 300-photo batch can easily exceed 1 GB and
the share step may fail. The app warns when a large batch is left on Original.
