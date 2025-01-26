import { SiteParser } from '../base.js';

export class LeverParser extends SiteParser {
    _parseJobInfoFromPage() {
        try {
            return {
                title: this.getJobTitle(),
                company: this.getCompanyName(),
                description: this.getJobDescription(),
                location: this.getLocation(),
                url: window.location.href
            };
        } catch (error) {
            console.error('Error parsing job info:', error);
            return null;
        }
    }

    getJobTitle() {
        // Try the main heading first
        const titleElement = document.querySelector('.posting-headline h2');
        if (titleElement) {
            return titleElement.textContent.trim();
        }

        // Fallback to title tag
        const pageTitle = document.title;
        if (pageTitle) {
            // Handle formats like "Company - Job Title" or "Company Name - Job Title (W)"
            const titleMatch = pageTitle.match(/[^-]+-(.+)$/);
            if (titleMatch) {
                // Clean up the title (remove any trailing (W) or similar)
                return titleMatch[1].replace(/\([^)]*\)$/, '').trim();
            }
        }

        return null;
    }

    getCompanyName() {
        // Try logo alt text first
        const logoImg = document.querySelector('.main-header-logo img');
        if (logoImg?.alt) {
            return logoImg.alt.replace(' logo', '').trim();
        }
        
        // Try title tag next
        const pageTitle = document.title;
        if (pageTitle) {
            // Extract company name from formats like "Company - Job Title"
            const companyMatch = pageTitle.match(/^([^-]+)-/);
            if (companyMatch) {
                return companyMatch[1].trim();
            }
        }
        
        // Fallback to URL
        const match = window.location.href.match(/jobs\.lever\.co\/([^\/]+)/);
        return match ? match[1] : null;
    }

    getJobDescription() {
        const sections = {};
        
        // Get all section divs in order
        const sectionDivs = document.querySelectorAll('.section.page-centered');
        
        // Process sections in order of appearance
        sectionDivs.forEach(section => {
            const qaType = section.getAttribute('data-qa');
            
            if (qaType === 'job-description') {
                sections.introduction = section.textContent.trim();
            }
            else if (qaType === 'closing-description') {
                sections.closing = section.textContent.trim();
            }
            // Check for requirements sections by looking for h3 headers
            else if (section.querySelector('h3')) {
                const header = section.querySelector('h3').textContent.trim();
                const content = section.querySelector('.posting-requirements')?.textContent.trim();
                if (content) {
                    const key = this._normalizeHeader(header);
                    sections[key] = content;
                }
            }
            // If no specific identifier, try to determine by content
            else {
                const firstHeader = section.querySelector('b, strong')?.textContent.trim();
                if (firstHeader) {
                    const key = this._normalizeHeader(firstHeader);
                    sections[key] = section.textContent.trim();
                }
            }
        });

        return sections;
    }

    _normalizeHeader(header) {
        // Convert header to a consistent format
        return header.toLowerCase()
            .replace(/[^a-z0-9\s]/g, '')  // Remove special characters
            .replace(/\s+/g, '_')         // Replace spaces with underscores
            .trim();
    }

    getLocation() {
        let location = null;

        // Try getting from page content first
        const locationElement = document.querySelector('.posting-categories .location');
        if (locationElement) {
            location = locationElement.textContent.trim();
        }

        // Fallback to twitter meta tag
        if (!location) {
            const metaLocation = document.querySelector('meta[name="twitter:data1"]')?.getAttribute('value');
            if (metaLocation) {
                location = metaLocation.trim();
            }
        }

        // Remove zip code if location was found
        if (location) {
            return location.replace(/\s+\d{5}(?:-\d{4})?$/, '').trim();
        }

        return null;
    }

    
    parseFormFields() {
        return {};
    }

    fillForm(data) {
        return {};
    }
} 