from django.core.management.base import BaseCommand
from django.db import transaction
from profiles.models import Skill
from profiles.utils.logger.logging_config import logger

class Command(BaseCommand):
    help = 'Create common skills for various tech and business roles'

    def handle(self, *args, **options):
        # Define skills by category
        skills_by_category = {
            "Programming Languages": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go",
                "Rust", "Swift", "Kotlin", "R", "PHP", "Ruby", "Scala", "MATLAB",
                "Solidity", "Assembly", "Perl", "Shell", "SQL", "Dart"
            ],
            
            "Web Development": [
                "React", "Angular", "Vue.js", "Next.js", "Node.js", "Django",
                "Flask", "FastAPI", "Spring Boot", "Express.js", "HTML5", "CSS3",
                "Sass", "Webpack", "GraphQL", "REST APIs", "WebSockets", "Redux",
                "Svelte", "Tailwind CSS", "Bootstrap", "Material UI", "jQuery",
                "Web3.js", "Ethereum", "Smart Contracts", "Solana", "WebGL"
            ],
            
            "Data Science & ML": [
                "Machine Learning", "Deep Learning", "Natural Language Processing",
                "Computer Vision", "TensorFlow", "PyTorch", "Scikit-learn",
                "Pandas", "NumPy", "SciPy", "Keras", "NLTK", "spaCy",
                "Data Visualization", "Statistical Analysis", "A/B Testing",
                "Feature Engineering", "Model Deployment", "MLOps", "Reinforcement Learning",
                "Time Series Analysis", "Recommendation Systems", "Neural Networks",
                "Transfer Learning", "GANs", "Transformers", "BERT", "GPT",
                "Object Detection", "Image Segmentation", "Speech Recognition"
            ],
            
            "Big Data": [
                "Apache Spark", "Hadoop", "Kafka", "Airflow", "Databricks",
                "Big Query", "Snowflake", "Data Warehousing", "ETL", "Data Pipelines",
                "Data Modeling", "Data Architecture", "Hive", "Presto", "Redshift",
                "Delta Lake", "dbt", "Apache Beam", "Apache Flink", "Stream Processing",
                "Data Lake", "Data Mesh", "Data Quality", "Data Governance"
            ],
            
            "Cloud & DevOps": [
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
                "GitLab CI", "GitHub Actions", "Terraform", "Ansible", "Linux",
                "Shell Scripting", "Infrastructure as Code", "Microservices",
                "Service Mesh", "Cloud Architecture", "Prometheus", "Grafana",
                "ELK Stack", "Site Reliability Engineering", "DevSecOps",
                "Cloud Security", "Serverless", "Lambda", "Azure Functions",
                "Cloud Functions", "Istio", "Kong", "CI/CD"
            ],
            
            "Database": [
                "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
                "Cassandra", "DynamoDB", "SQL", "NoSQL", "Database Design",
                "Database Optimization", "Database Administration", "Neo4j",
                "Graph Databases", "Time Series Databases", "InfluxDB", "CockroachDB",
                "Database Sharding", "Database Replication", "Database Migration",
                "Database Security", "Database Monitoring"
            ],
            
            "Data Analytics": [
                "SQL", "Power BI", "Tableau", "Looker", "Excel", "Data Analysis",
                "Business Intelligence", "Data Visualization", "Reporting",
                "Dashboard Design", "Metrics & KPIs", "Google Analytics",
                "Data Studio", "Predictive Analytics", "Prescriptive Analytics",
                "Customer Analytics", "Marketing Analytics", "Sales Analytics",
                "Financial Analytics", "People Analytics", "Product Analytics",
                "Web Analytics", "Mobile Analytics", "Attribution Modeling"
            ],
            
            "Product Management": [
                "Product Strategy", "Product Roadmap", "User Stories", "Agile",
                "Scrum", "JIRA", "Product Analytics", "UX/UI Design", "Wireframing",
                "Competitive Analysis", "Market Research", "Customer Development",
                "Product Marketing", "Stakeholder Management", "Product Discovery",
                "Product Launch", "Growth Strategy", "Pricing Strategy",
                "Go-to-Market Strategy", "Product Operations", "OKRs",
                "Product Metrics", "User Research", "Customer Journey Mapping"
            ],
            
            "Finance & Quant": [
                "Quantitative Analysis", "Financial Modeling", "Risk Management",
                "Algorithmic Trading", "Time Series Analysis", "Options Trading",
                "Portfolio Management", "Bloomberg Terminal", "Financial Markets",
                "Derivatives", "Fixed Income", "Equity Research", "Python for Finance",
                "R for Finance", "Risk Analytics", "Market Microstructure",
                "Statistical Arbitrage", "High Frequency Trading", "Factor Investing",
                "Asset Allocation", "Backtesting", "Market Making", "Systematic Trading",
                "Quantitative Portfolio Management", "Financial Engineering"
            ],
            
            "Soft Skills": [
                "Communication", "Leadership", "Problem Solving", "Team Management",
                "Project Management", "Critical Thinking", "Presentation Skills",
                "Collaboration", "Time Management", "Mentoring", "Cross-functional Leadership",
                "Strategic Thinking", "Negotiation", "Conflict Resolution",
                "Decision Making", "Emotional Intelligence", "Adaptability",
                "Cultural Awareness", "Public Speaking", "Written Communication",
                "Team Building", "Change Management", "Stakeholder Communication"
            ],
            
            "Tools & Platforms": [
                "Git", "GitHub", "VS Code", "PyCharm", "Jupyter", "Postman",
                "Slack", "Confluence", "Linear", "Notion", "Figma", "Adobe XD",
                "Microsoft Office", "Google Workspace", "IntelliJ IDEA", "Eclipse",
                "Android Studio", "Xcode", "Docker Desktop", "Kubernetes Dashboard",
                "AWS Console", "Azure Portal", "GCP Console", "Terminal",
                "PowerShell", "Bash", "Vim", "Sublime Text"
            ],
            
            "Mobile Development": [
                "iOS Development", "Android Development", "React Native",
                "Flutter", "Swift", "Kotlin", "SwiftUI", "Jetpack Compose",
                "Mobile UI Design", "App Store Optimization", "Mobile Security",
                "Push Notifications", "Mobile Analytics", "Mobile Testing",
                "Mobile CI/CD", "Mobile Architecture", "Cross-Platform Development"
            ],
            
            "Security": [
                "Cybersecurity", "Network Security", "Application Security",
                "Cloud Security", "Security Architecture", "Penetration Testing",
                "Vulnerability Assessment", "Security Auditing", "Incident Response",
                "Threat Modeling", "Security Operations", "Identity Management",
                "Access Control", "Encryption", "Security Compliance"
            ],

            # New non-tech categories
            "Marketing & Communications": [
                "Digital Marketing", "Content Marketing", "Social Media Marketing",
                "Email Marketing", "SEO", "SEM", "Google Ads", "Facebook Ads",
                "Marketing Automation", "Brand Management", "Public Relations",
                "Copywriting", "Content Strategy", "Marketing Analytics",
                "Marketing Operations", "Campaign Management", "CRM",
                "Marketing Research", "Influencer Marketing", "Event Marketing",
                "Account Based Marketing", "Marketing Attribution", "Brand Strategy",
                "Community Management", "Crisis Communication"
            ],

            "Sales": [
                "B2B Sales", "B2C Sales", "Sales Strategy", "Account Management",
                "Business Development", "Sales Operations", "Sales Analytics",
                "CRM Management", "Lead Generation", "Pipeline Management",
                "Contract Negotiation", "Sales Forecasting", "Territory Management",
                "Solution Selling", "Enterprise Sales", "Channel Sales",
                "Inside Sales", "Outside Sales", "Sales Enablement",
                "Customer Success", "Relationship Building", "Cold Calling",
                "Sales Presentations", "Value Proposition Development"
            ],

            "Human Resources": [
                "Talent Acquisition", "Recruitment", "Employee Relations",
                "Performance Management", "Compensation & Benefits",
                "HR Analytics", "HRIS", "Employee Engagement", "Training & Development",
                "Organizational Development", "HR Compliance", "Succession Planning",
                "Workforce Planning", "Employee Onboarding", "HR Operations",
                "Benefits Administration", "Labor Relations", "HR Strategy",
                "Diversity & Inclusion", "Employee Experience", "HR Technology",
                "Talent Management", "Change Management", "Culture Development"
            ],

            "Operations": [
                "Operations Management", "Supply Chain Management", "Logistics",
                "Inventory Management", "Process Improvement", "Quality Management",
                "Six Sigma", "Lean Management", "Vendor Management",
                "Contract Management", "Facilities Management", "Risk Management",
                "Business Continuity", "Operations Strategy", "Cost Optimization",
                "Performance Optimization", "Resource Planning", "Procurement",
                "Warehouse Management", "Distribution Management"
            ],

            "Healthcare": [
                "Clinical Research", "Healthcare Administration", "Patient Care",
                "Healthcare Compliance", "Medical Coding", "Healthcare Analytics",
                "Electronic Health Records", "HIPAA Compliance", "Clinical Trials",
                "Healthcare Operations", "Population Health", "Medical Devices",
                "Healthcare Technology", "Telemedicine", "Healthcare Policy",
                "Public Health", "Health Informatics", "Patient Experience",
                "Healthcare Quality", "Medical Writing"
            ],

            "Legal": [
                "Contract Law", "Corporate Law", "Intellectual Property",
                "Legal Research", "Legal Writing", "Regulatory Compliance",
                "Legal Operations", "eDiscovery", "Legal Technology",
                "Privacy Law", "Employment Law", "Securities Law",
                "Mergers & Acquisitions", "Legal Analytics", "Legal Project Management",
                "Risk Assessment", "Legal Strategy", "Litigation Support"
            ],

            "Consulting": [
                "Management Consulting", "Strategy Consulting", "Technology Consulting",
                "Business Process Consulting", "Change Management Consulting",
                "Financial Advisory", "HR Consulting", "IT Consulting",
                "Operations Consulting", "Risk Consulting", "Digital Transformation",
                "Business Analysis", "Process Mapping", "Requirements Gathering",
                "Solution Architecture", "Vendor Selection", "Implementation Planning"
            ],

            "Design": [
                "UX Design", "UI Design", "Graphic Design", "Web Design",
                "Product Design", "Industrial Design", "Design Thinking",
                "User Research", "Prototyping", "Visual Design", "Interaction Design",
                "Design Systems", "Brand Design", "Motion Design", "Design Strategy",
                "Information Architecture", "Service Design", "Design Operations",
                "Accessibility Design", "Mobile Design"
            ],

            "Research": [
                "Market Research", "User Research", "Scientific Research",
                "Research Design", "Qualitative Research", "Quantitative Research",
                "Research Analysis", "Literature Review", "Research Methodology",
                "Data Collection", "Research Operations", "Research Strategy",
                "Experimental Design", "Survey Design", "Focus Groups",
                "Research Ethics", "Research Publication", "Grant Writing"
            ],

            "Education": [
                "Curriculum Development", "Instructional Design", "E-Learning",
                "Educational Technology", "Learning Management Systems",
                "Course Development", "Training Development", "Assessment Design",
                "Educational Research", "Student Engagement", "Online Teaching",
                "Educational Leadership", "Special Education", "Adult Learning",
                "Educational Psychology", "Learning Analytics", "Education Policy"
            ]
        }
        
        try:
            with transaction.atomic():
                skills_created = 0
                skills_existed = 0
                
                for category, skills in skills_by_category.items():
                    self.stdout.write(f"\nProcessing {category}:")
                    
                    for skill_name in skills:
                        skill, created = Skill.objects.get_or_create(name=skill_name)
                        
                        if created:
                            skills_created += 1
                            self.stdout.write(self.style.SUCCESS(f"Created: {skill_name}"))
                        else:
                            skills_existed += 1
                            self.stdout.write(self.style.WARNING(f"Already exists: {skill_name}"))
                
                self.stdout.write("\nSummary:")
                self.stdout.write(self.style.SUCCESS(f"Created {skills_created} new skills"))
                self.stdout.write(self.style.WARNING(f"Found {skills_existed} existing skills"))
                
        except Exception as e:
            logger.error(f"Error creating skills: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to create skills: {str(e)}"))
