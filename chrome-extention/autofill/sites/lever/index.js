import { LeverMatcher } from './matcher.js';
import { LeverParser } from './parser.js';

// Export everything needed for Lever site handling
export const Lever = {
    name: 'Lever',
    domain: 'jobs.lever.co',
    matcher: LeverMatcher,
    parser: LeverParser,
    
    // Factory method to create instances
    create() {
        return {
            matcher: new LeverMatcher(),
            parser: new LeverParser()
        };
    }
};

// Export individual classes if needed
export { LeverMatcher, LeverParser }; 