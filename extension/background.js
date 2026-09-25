// Clicking the toolbar icon opens the analytics page as a normal tab
// (instead of a popup) so that clicking elsewhere, switching windows, etc.
// never interrupts an in-progress fetch -- a popup's JS context is
// destroyed the instant it loses focus, a tab's isn't.
chrome.action.onClicked.addListener(() => {
  chrome.tabs.create({ url: chrome.runtime.getURL("results.html") });
});
