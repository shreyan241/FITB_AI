import { PAGE_TYPES } from '../autofill/sites/base.js';

export class PopupController {
    constructor() {
        this.elements = {
            status: document.getElementById('status'),
            jobInfo: document.getElementById('jobInfo'),
            company: document.getElementById('company'),
            title: document.getElementById('title'),
            location: document.getElementById('location'),
            autofillBtn: document.getElementById('autofillBtn')
        };
    }

    async init() {
        console.log('FITB AI: Initializing popup');
        await this.setupEventListeners();
        await this.checkCurrentTab();
    }

    setupEventListeners() {
        console.log('FITB AI: Setting up event listeners');
        // Autofill button click
        this.elements.autofillBtn.addEventListener('click', async () => {
            const tab = await this.getCurrentTab();
            try {
                await chrome.tabs.sendMessage(tab.id, { 
                    action: 'autofill',
                    data: {} // TODO: Add user data
                });
                this.elements.status.textContent = 'Filling form...';
            } catch (error) {
                console.error('FITB AI: Error:', error);
                this.elements.status.textContent = 'Error connecting to page';
            }
        });
    }

    async getCurrentTab() {
        const [tab] = await chrome.tabs.query({ 
            active: true, 
            currentWindow: true 
        });
        return tab;
    }

    async checkCurrentTab() {
        console.log('FITB AI: Checking current tab');
        const tab = await this.getCurrentTab();
        
        try {
            console.log('FITB AI: Sending getJobInfo message');
            const response = await chrome.tabs.sendMessage(tab.id, { 
                action: 'getJobInfo' 
            });
            console.log('FITB AI: Received response:', response);
            this.updateJobInfo(response);
        } catch (error) {
            console.error('FITB AI: Error:', error);
            this.elements.status.textContent = 'Please refresh the page and try again';
            this.elements.jobInfo.style.display = 'none';
            this.elements.autofillBtn.disabled = true;
        }
    }

    updateJobInfo(jobInfo) {
        console.log('FITB AI: Updating job info:', jobInfo);
        if (!jobInfo) {
            this.elements.status.textContent = 'No job information found. Make sure you are on a supported job site.';
            this.elements.jobInfo.style.display = 'none';
            this.elements.autofillBtn.disabled = true;
            return;
        }

        // Update UI with job info
        this.elements.company.textContent = jobInfo.company ? `Company: ${jobInfo.company}` : 'Company: Not specified';
        this.elements.title.textContent = jobInfo.title ? `Position: ${jobInfo.title}` : 'Position: Not specified';
        this.elements.location.textContent = jobInfo.location ? `Location: ${jobInfo.location}` : 'Location: Not specified';
        
        this.elements.jobInfo.style.display = 'block';
        this.elements.status.textContent = 'Job found!';
        this.elements.autofillBtn.disabled = false;
    }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('FITB AI: Popup DOM loaded');
    new PopupController().init();
}); 