# FITB AI - Automated Job Application System

## Project Overview
FITB AI is a comprehensive system consisting of a Chrome extension for automated job application form filling and a Django backend for managing user profiles and data. The system aims to streamline the job application process by automatically filling out application forms using user-provided information.

## System Architecture

### Backend (Django + Ninja API)
The backend is built using Django with the Ninja API framework, providing RESTful endpoints for managing user data.

#### Endpoints Structure:
```
/profiles/api/endpoints/
├── profile.py         # Core user profile management
├── education.py       # Educational background
├── work_experience.py # Work history
├── skill.py          # Skills management
├── resume.py         # Resume handling
└── social_link.py    # Social media links
```

#### Key Features:
- Asynchronous API endpoints
- Comprehensive user profile management
- File handling for resumes
- Authentication and authorization
- Detailed logging system

### Chrome Extension
The extension is built using vanilla JavaScript with a modular architecture.

#### Directory Structure:
```
chrome-extension/
├── manifest.json    # Extension configuration
├── background/      # Background service worker
├── content/        # Content scripts for job sites
├── popup/          # Extension UI
└── autofill/      # Autofill logic and site handlers
    └── sites/     # Site-specific implementations
        └── lever/ # Lever.co specific logic
```

## Current Implementation Status

### Completed Features

#### Backend
- ✅ User profile management
- ✅ Education history
- ✅ Work experience
- ✅ Skills management
- ✅ Resume upload and management
- ✅ Social links
- ✅ Authentication system

#### Chrome Extension
- ✅ Basic extension setup
- ✅ Background script for URL monitoring
- ✅ Content script for Lever job site detection
- ✅ Popup UI for displaying job info
- ✅ Site matcher and parser for Lever
- ✅ Module system for site handlers

### Pending Implementation

#### Backend Integration
- [ ] API client implementation in extension
- [ ] Authentication flow
- [ ] Data synchronization
- [ ] Error handling and retry mechanisms

#### Form Filling Logic
- [ ] Complete form field detection
- [ ] Field mapping system
- [ ] Data validation
- [ ] Error recovery

#### User Interface
- [ ] Login/Authentication UI
- [ ] Profile data display
- [ ] Form field preview
- [ ] Settings panel
- [ ] Error notifications

## Technical Details

### Data Flow
1. User Authentication
   - Login through extension
   - Token storage and management
   - API authentication

2. Profile Data Management
   ```javascript
   // Data structure
   {
     profile: {
       first_name: string,
       last_name: string,
       email: string,
       phone: string
     },
     education: [{
       institution: string,
       degree: string,
       field_of_study: string,
       start_date: date,
       end_date: date
     }],
     work_experience: [{
       company: string,
       title: string,
       description: string,
       start_date: date,
       end_date: date
     }],
     skills: [string],
     social_links: [{
       platform: string,
       url: string
     }]
   }
   ```

3. Form Detection and Filling
   - URL monitoring
   - Form field detection
   - Data mapping
   - Validation
   - Error handling

### API Integration Points

```javascript
class APIClient {
    // Profile management
    async getProfile()
    async updateProfile(data)
    
    // Education management
    async getEducation()
    async addEducation(data)
    async updateEducation(id, data)
    
    // Work experience
    async getWorkExperience()
    async addWorkExperience(data)
    async updateWorkExperience(id, data)
    
    // Skills management
    async getSkills()
    async updateSkills(skillIds)
    
    // Resume management
    async getResumes()
    async uploadResume(file, title)
    async setDefaultResume(id)
}
```

## Next Steps

### Immediate Priorities
1. Complete the authentication system integration
2. Implement API client in the extension
3. Add form field detection for Lever
4. Create basic form filling logic

### Medium-term Goals
1. Add support for more job sites
2. Implement data caching and sync
3. Add user settings and preferences
4. Improve error handling and recovery

### Long-term Goals
1. Add AI-powered form field detection
2. Implement smart data mapping
3. Add support for document parsing
4. Create analytics dashboard

## Development Setup

### Backend Setup
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable Developer Mode
3. Click "Load unpacked" and select the `chrome-extension` directory
4. The extension should now be visible in your toolbar

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
