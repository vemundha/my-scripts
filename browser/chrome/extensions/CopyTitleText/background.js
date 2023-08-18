// This function sets up the context menu item
function setupContextMenu() {
    // First, remove any existing context menu items to avoid duplicates
    chrome.contextMenus.removeAll(function() {
        // Create the new context menu item
        chrome.contextMenus.create({
            id: "copyTabTitle",
            title: "Copy Tab Title",
            contexts: ["page"],
            documentUrlPatterns: ["<all_urls>"]
        });
    });
}

// Set up the context menu item when the browser starts
chrome.runtime.onStartup.addListener(setupContextMenu);

// Also, set up the context menu item when the extension is installed/updated
chrome.runtime.onInstalled.addListener(setupContextMenu);

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === "copyTabTitle") {
        try {
            const response = await chrome.tabs.sendMessage(tab.id, {action: "getTabTitle"});
            const titleText = response.title;
            
            // Send a new message to content script to copy to clipboard
            chrome.tabs.sendMessage(tab.id, {action: "copyToClipboard", text: titleText});
        } catch (error) {
            console.error("Failed to get tab title:", error);
        }
    }
});
