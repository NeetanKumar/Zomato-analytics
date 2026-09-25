# Zomato Order Analytics (browser extension)

Same analytics as the Python scripts in the repo root, but as a Chrome
extension: click it while logged into zomato.com in your normal browser,
and it shows your spend, top restaurants, and monthly trends right in the
popup. Everything runs in your own browser using your own already-logged-in
session — nothing is sent anywhere else.

This isn't published to the Chrome Web Store (an extension built around an
undocumented internal endpoint of another company is unlikely to survive
store review), so you load it locally instead.

## Install (Chrome / Brave / Edge)

1. Go to `chrome://extensions`
2. Turn on **Developer mode** (top right)
3. Click **Load unpacked**
4. Select this `extension/` folder

## Use

1. Log into [zomato.com](https://www.zomato.com) normally, in the same
   browser
2. Click the extension icon
3. Click **Analyze my orders**

## Notes

- Relies on Zomato's internal order-history endpoint, same as the Python
  scripts — may break if Zomato changes it.
- Nothing is stored: each click re-fetches fresh from Zomato and computes
  everything in memory in the popup.
