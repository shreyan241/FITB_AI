// Entry point for content script
(async () => {
    try {
        console.log('FITB AI: Loading content script');
        const src = chrome.runtime.getURL('content/content_main.js');
        const contentMain = await import(src);
        contentMain.init();
    } catch (error) {
        console.error('FITB AI: Error loading content script:', error);
    }
})();