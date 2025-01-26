import { SiteMatcher, PAGE_TYPES } from '../base.js';

export class LeverMatcher extends SiteMatcher {
    static PATTERNS = {
        JOB_VIEW: /^https:\/\/jobs\.lever\.co\/([^\/]+)\/([^\/]+)\/?$/,
        APPLY_FORM: /^https:\/\/jobs\.lever\.co\/([^\/]+)\/([^\/]+)\/apply\/?$/,
        POST_APPLY: /^https:\/\/jobs\.lever\.co\/([^\/]+)\/([^\/]+)\/thanks\/?$/
    };

    isMatch(url) {
        return Object.values(LeverMatcher.PATTERNS)
            .some(pattern => pattern.test(url));
    }

    getPageType(url) {
        if (LeverMatcher.PATTERNS.APPLY_FORM.test(url)) return PAGE_TYPES.APPLY_FORM;
        if (LeverMatcher.PATTERNS.JOB_VIEW.test(url)) return PAGE_TYPES.JOB_VIEW;
        if (LeverMatcher.PATTERNS.POST_APPLY.test(url)) return PAGE_TYPES.POST_APPLY;
        return PAGE_TYPES.UNKNOWN;
    }

    parseUrl(url) {
        const match = url.match(/^https:\/\/jobs\.lever\.co\/([^\/]+)\/([^\/]+)/);
        if (!match) return null;
        
        return {
            company: match[1],
            jobId: match[2]
        };
    }

    getBaseDomain() {
        return 'jobs.lever.co';
    }
} 