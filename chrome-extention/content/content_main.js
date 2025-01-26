import { PAGE_TYPES } from '../autofill/sites/base.js';
import { Lever } from '../autofill/sites/lever/index.js';

class ContentController {
    constructor() {
        this.currentSite = null;
        this.currentMatcher = null;
        this.currentParser = null;
        this.pageType = null;
    }

    init() {
        this.detectSite();
        this.setupMessageListeners();
        this.setupURLChangeDetection();
    }

    detectSite() {
        const url = window.location.href;
        console.log('FITB AI: Checking URL:', url);

        // Map of supported sites
        const SUPPORTED_SITES = {
            [Lever.domain]: Lever
        };

        // Find matching site handler
        for (const [domain, handler] of Object.entries(SUPPORTED_SITES)) {
            if (url.includes(domain)) {
                console.log('FITB AI: Detected site:', handler.name);
                const instance = handler.create();
                this.currentMatcher = instance.matcher;
                this.currentParser = instance.parser;
                this.handlePage();
                break;
            }
        }
    }

    handlePage() {
        const url = window.location.href;
        this.pageType = this.currentMatcher.getPageType(url);
        console.log('FITB AI: Page type:', this.pageType);

        switch (this.pageType) {
            case PAGE_TYPES.JOB_VIEW:
                this.handleJobView();
                break;
            case PAGE_TYPES.APPLY_FORM:
                this.handleApplyForm();
                break;
            case PAGE_TYPES.POST_APPLY:
                this.handlePostApply();
                break;
        }
    }

    handleJobView() {
        const jobInfo = this.currentParser.parseJobInfo();
        console.log('FITB AI: Job info:', jobInfo);
        
        if (jobInfo) {
            chrome.storage.local.set({ currentJob: jobInfo }, () => {
                console.log('FITB AI: Job info saved to storage');
            });
        }
    }

    handleApplyForm() {
        this.handleJobView();
        const fields = this.currentParser.parseFormFields();
        console.log('FITB AI: Form fields:', fields);
    }

    handlePostApply() {
        // For future application tracking
        this.handleJobView();
        console.log('FITB AI: Application submitted');
    }

    setupMessageListeners() {
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            console.log('FITB AI: Received message:', request.action);

            switch (request.action) {
                case 'urlChanged':
                    // Re-run detection and parsing for new URL
                    this.detectSite();
                    sendResponse({ status: 'handled' });
                    break;
                case 'getJobInfo':
                    sendResponse(this.currentParser?.parseJobInfo() || null);
                    break;
                case 'getFormFields':
                    sendResponse(this.currentParser?.parseFormFields() || null);
                    break;
                case 'autofill':
                    if (this.pageType === PAGE_TYPES.APPLY_FORM) {
                        this.currentParser.fillForm(request.data);
                        sendResponse({ status: 'started' });
                    } else {
                        sendResponse({ status: 'error', message: 'Not on application form' });
                    }
                    break;
            }
            return true;
        });
    }

    setupURLChangeDetection() {
        let lastUrl = window.location.href;
        new MutationObserver(() => {
            const url = window.location.href;
            if (url !== lastUrl) {
                console.log('FITB AI: URL changed');
                lastUrl = url;
                this.handlePage();
            }
        }).observe(document, {subtree: true, childList: true});
    }
}

export function init() {
    console.log('FITB AI: Content main loaded');
    new ContentController().init();
} 