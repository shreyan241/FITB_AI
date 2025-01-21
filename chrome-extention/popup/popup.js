// Get current tab info
async function getCurrentTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab;
}

// Update UI with job info
function updateJobInfo(jobInfo) {
    const jobInfoDiv = document.getElementById('jobInfo');
    const statusDiv = document.getElementById('status');
    const autofillBtn = document.getElementById('autofillBtn');

    if (!jobInfo) {
        statusDiv.textContent = 'No job information found';
        jobInfoDiv.style.display = 'none';
        autofillBtn.disabled = true;
        return;
    }

    // Show job info
    document.getElementById('company').textContent = `Company: ${jobInfo.company}`;
    document.getElementById('title').textContent = `Position: ${jobInfo.jobTitle}`;
    document.getElementById('location').textContent = `Location: ${jobInfo.location || 'Not specified'}`;
    
    jobInfoDiv.style.display = 'block';
    statusDiv.textContent = 'Job application detected!';
    autofillBtn.disabled = false;
}

// Initialize popup
async function initPopup() {
    const tab = await getCurrentTab();
    const statusDiv = document.getElementById('status');

    // First check if we're on a job site
    try {
        // Get job info from content script
        chrome.tabs.sendMessage(tab.id, { action: 'getJobInfo' }, (response) => {
            if (chrome.runtime.lastError) {
                console.log('Content script not ready:', chrome.runtime.lastError.message);
                statusDiv.textContent = 'Please refresh the page and try again';
                return;
            }
            updateJobInfo(response);
        });
    } catch (error) {
        console.error('Error:', error);
        statusDiv.textContent = 'Error connecting to page';
    }
}

// Handle autofill button click
document.getElementById('autofillBtn').addEventListener('click', async () => {
    const tab = await getCurrentTab();
    const statusDiv = document.getElementById('status');

    try {
        chrome.tabs.sendMessage(tab.id, { action: 'autofill' }, (response) => {
            if (chrome.runtime.lastError) {
                console.log('Content script not ready:', chrome.runtime.lastError.message);
                statusDiv.textContent = 'Please refresh the page and try again';
                return;
            }
            statusDiv.textContent = 'Starting autofill...';
        });
    } catch (error) {
        console.error('Error:', error);
        statusDiv.textContent = 'Error connecting to page';
    }
});

// Listen for job site detection from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'jobSiteDetected') {
        updateJobInfo(request.jobInfo);
    }
});

// Initialize when popup opens
document.addEventListener('DOMContentLoaded', initPopup);