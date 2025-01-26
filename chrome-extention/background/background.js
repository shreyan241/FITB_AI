chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url) {
        console.log('urlChanged', changeInfo.url);
        
        // Only try to send message if the page is complete
        if (tab.status === 'complete') {
            chrome.tabs.sendMessage(tabId, {
                action: 'urlChanged',
                url: changeInfo.url
            }).then(response => {
                if (response?.status === 'handled') {
                    console.log('Content script processed URL change');
                }
            }).catch(error => {
                console.log('Could not send message to content script (not loaded yet)');
            });
        }
    }
});