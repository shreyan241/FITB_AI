// Entry point for popup script
(async () => {
    try {
        console.log('FITB AI: Loading popup script');
        const src = chrome.runtime.getURL('popup/popup_main.js');
        const popupMain = await import(src);
        
        // Initialize when popup opens
        document.addEventListener('DOMContentLoaded', () => {
            popupMain.init();
        });
    } catch (error) {
        console.error('FITB AI: Error loading popup script:', error);
    }
})();