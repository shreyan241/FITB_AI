// Listen for tab URL changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && isJobSite(changeInfo.url)) {
        console.log('Detected job site:', changeInfo.url);
        const jobInfo = parseJobInfo(changeInfo.url);
        if (jobInfo) {
            // Notify popup if it's open
            chrome.runtime.sendMessage({
                action: 'jobSiteDetected',
                jobInfo: jobInfo
            });
        }
    }
});

// Listen for messages
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'isJobSite') {
        const url = sender.tab.url;
        sendResponse({ isJobSite: isJobSite(url) });
    }
});
