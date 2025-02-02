# FITB AI - Automated Job Application System

FITB AI streamlines the job application process by automatically filling out application forms. It consists of a Chrome extension for form filling and a Django backend for managing user data.

## What's Done

### Backend
- Async API with token authentication
- Complete profile management (personal info, education, work experience)
- Skills and social links management
- Resume upload/management
- Equal employment data handling
- Proper permissions and validation

### Chrome Extension
- Basic extension setup
- URL monitoring
- Lever job site detection
- Basic popup UI

## What's Next

### Priority 1: NextJS Frontend
- User authentication with token management
- Profile dashboard with sections:
  - Personal info management
  - Education/Work experience forms
  - Skills and social links
  - Resume upload/management
- Real-time form validation
- Mobile-responsive design
- Integration with Django backend

### Priority 2: Chrome Extension + Integration
- Connect extension with frontend auth
- Load user data from backend
- Build form field detection
- Implement autofill logic
- Add error handling

### Priority 3: AI Content Generation
- RAG pipeline using deepseek-r1
- Cover letter generation using resume + job description
- Answer generation for subjective questions
- Company research integration
- Response quality optimization
