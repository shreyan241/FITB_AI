// Page Types
export const PAGE_TYPES = {
    JOB_VIEW: 'JOB_VIEW',
    APPLY_FORM: 'APPLY_FORM',
    POST_APPLY: 'POST_APPLY',
    UNKNOWN: 'UNKNOWN'
};

// Base class for site URL matching
export class SiteMatcher {
    // Check if URL belongs to this job site
    isMatch(url) {
        throw new Error('isMatch must be implemented');
    }

    // Get the type of page (job view, apply form, etc)
    getPageType(url) {
        throw new Error('getPageType must be implemented');
    }

    // Extract company and job ID from URL
    parseURL(url) {
        throw new Error('parseURL must be implemented');
    }

    // Get base domain for the job site
    getBaseDomain() {
        throw new Error('getBaseDomain must be implemented');
    }
}

// Base class for site parsing
export class SiteParser {
    constructor() {
        // Cache for parsed job info
        this._jobInfo = null;
        // Cache for form fields
        this._formFields = null;
    }

    // Parse job information (with caching)
    parseJobInfo() {
        if (!this._jobInfo) {
            try {
                this._jobInfo = this._parseJobInfoFromPage();
            } catch (error) {
                console.error('Error parsing job info:', error);
                return null;
            }
        }
        return this._jobInfo;
    }

    // Parse form fields (with caching)
    parseFormFields() {
        if (!this._formFields) {
            try {
                this._formFields = this._getFormFields();
            } catch (error) {
                console.error('Error parsing form fields:', error);
                return null;
            }
        }
        return this._formFields;
    }

    // Fill form with provided data
    fillForm(data) {
        throw new Error('fillForm must be implemented');
    }

    // Methods that must be implemented by child classes
    getJobTitle() {
        throw new Error('getJobTitle must be implemented');
    }

    getCompanyName() {
        throw new Error('getCompanyName must be implemented');
    }

    getJobDescription() {
        throw new Error('getJobDescription must be implemented');
    }

    getLocation() {
        throw new Error('getLocation must be implemented');
    }

    _getFormFields() {
        throw new Error('_getFormFields must be implemented');
    }

    findLabel(field) {
        // Try for explicit label
        const labelElement = document.querySelector(`label[for="${field.id}"]`);
        if (labelElement) return labelElement.textContent.trim();

        // Try parent label
        const parentLabel = field.closest('label');
        if (parentLabel) return parentLabel.textContent.trim();

        return null;
    }

    // Clear caches
    clearCache() {
        this._jobInfo = null;
        this._formFields = null;
    }

    _parseJobInfoFromPage() {
        throw new Error('Not implemented');
    }
}