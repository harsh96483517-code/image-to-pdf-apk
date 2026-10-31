"""Capacitor regenerates the Android manifest on every `cap add android`.
Big batches (hundreds of photos) need a larger heap than the default, so this
script is run by CI right after the platform is added."""
import io
import sys

PATH = "android/app/src/main/AndroidManifest.xml"

try:
    src = io.open(PATH, encoding="utf-8").read()
except FileNotFoundError:
    sys.exit("AndroidManifest.xml not found - run `npx cap add android` first")

if "android:largeHeap" in src:
    print("largeHeap already set")
else:
    if "<application" not in src:
        sys.exit("<application> tag not found in manifest")
    src = src.replace("<application", '<application android:largeHeap="true"', 1)
    io.open(PATH, "w", encoding="utf-8").write(src)
    print("patched android:largeHeap=true")
