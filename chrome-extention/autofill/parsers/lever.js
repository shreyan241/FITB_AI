// autofill/parsers/lever.js
class LeverParser {
    static getAllInfo() {
        try {
            return {
                company: this.getCompanyName(),
                jobTitle: this.getJobTitle(),
                jobDescription: this.getJobDescription(),
                location: this.getLocation()
            };
        } catch (error) {
            console.error('Error parsing job info:', error);
            return null;
        }
    }

    static getCompanyName() {
        // Try to get company name from logo alt text
        const logoImg = document.querySelector('.main-header-logo img');
        if (logoImg?.alt) {
            return logoImg.alt.replace(' logo', '').trim();
        }
        
        // Fallback: Get from URL
        const match = window.location.href.match(/jobs\.lever\.co\/([^\/]+)/);
        return match ? match[1] : null;
    }

    static getJobTitle() {
        const titleElement = document.querySelector('.posting-headline h2');
        return titleElement ? titleElement.textContent.trim() : null;
    }

    static getJobDescription() {
        const descElement = document.querySelector('.posting-description');
        return descElement ? descElement.textContent.trim() : null;
    }

    static getLocation() {
        const locationElement = document.querySelector('.posting-categories .location');
        return locationElement ? locationElement.textContent.trim() : null;
    }
}

// Set the parser in SITE_CONFIGS after LeverParser is defined
SITE_CONFIGS.LEVER.parser = LeverParser;