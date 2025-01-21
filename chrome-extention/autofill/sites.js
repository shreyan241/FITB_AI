const SITE_CONFIGS = {
    LEVER: {
        pattern: /^https:\/\/jobs\.lever\.co\/([^\/]+)\/([^\/]+)/,
        parser: null  // Will be set by lever.js
    }
    // Add more sites here later
};

function isJobSite(url) {
    return Object.values(SITE_CONFIGS).some(site => site.pattern.test(url));
}

function getParser(url) {
    const site = Object.values(SITE_CONFIGS).find(site => site.pattern.test(url));
    return site ? site.parser : null;
}

function parseJobInfo(url) {
    const parser = getParser(url);
    return parser ? parser.getAllInfo() : null;
}