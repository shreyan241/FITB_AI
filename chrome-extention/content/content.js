console.log('FITB AI Content Script Loaded');

// Parse job info when page loads
document.addEventListener('DOMContentLoaded', () => {
    const url = window.location.href;
    if (!isJobSite(url)) {
        console.log('Not a supported job site');
        return;
    }

    const jobInfo = parseJobInfo(url);
    if (jobInfo) {
        console.log('Job Information:', jobInfo);
        // Store info for later use
        chrome.storage.local.set({ currentJob: jobInfo }, () => {
            console.log('Job info saved to storage');
        });
    } else {
        console.log('Failed to parse job information');
    }
});

// Listen for messages from popup or background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Content script received message:', request.action);
    
    if (request.action === 'getJobInfo') {
        const jobInfo = parseJobInfo(window.location.href);
        sendResponse(jobInfo);
        return true; // Keep the message channel open for async response
    }
    else if (request.action === 'autofill') {
        console.log('Starting autofill process');
        const jobInfo = parseJobInfo(window.location.href);
        console.log('Current job:', jobInfo);
        sendResponse({ status: 'started' });
        return true;
    }
});