chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getTabTitle") {
        sendResponse({ title: document.title });
    }
    
    if (message.action === "copyToClipboard") {
        copyToClipboard(message.text);
    }
});

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log('Title copied to clipboard');
    } catch (err) {
        console.error('Failed to copy title: ', err);
    }
}
