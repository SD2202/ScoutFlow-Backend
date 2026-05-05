import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://Sparsh:SSD@cluster1.wu5egox.mongodb.net/?appName=Cluster1")
DATABASE_NAME = "ai_recruiter"

candidates = [
    {
        "name": "Rohan Sharma",
        "role": "Senior Full Stack Engineer",
        "skills": ["React", "Node.js", "Python", "AWS", "Docker", "PostgreSQL"],
        "experience": "8 years",
        "projects": ["Cloud-native E-commerce platform", "Real-time collaboration tool"],
        "summary": "Expert in building scalable web applications and cloud architecture.",
        "location": "Bangalore, KA",
        "expected_salary": "₹19,50,000 per annum",
        "current_ctc": "₹17,50,000 per annum",
        "notice_period": "4 weeks"
    },
    {
        "name": "Priya Iyer",
        "role": "Product Manager",
        "skills": ["Agile", "Scrum", "Product Strategy", "User Research", "Jira"],
        "experience": "6 years",
        "projects": ["Mobile banking app redesign", "B2B SaaS marketplace"],
        "summary": "Data-driven product leader with a focus on user experience and business outcomes.",
        "location": "Mumbai, MH",
        "expected_salary": "₹18,00,000 per annum",
        "current_ctc": "₹16,00,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Arjun Malhotra",
        "role": "Data Scientist",
        "skills": ["Python", "TensorFlow", "SQL", "Scikit-learn", "NLP", "Pandas"],
        "experience": "5 years",
        "projects": ["Customer churn prediction model", "Recommendation engine for streaming"],
        "summary": "Passionate about leveraging machine learning to solve complex business problems.",
        "location": "Remote (India)",
        "expected_salary": "₹16,50,000 per annum",
        "current_ctc": "₹14,50,000 per annum",
        "notice_period": "Immidiate"
    },
    {
        "name": "Ananya Reddy",
        "role": "UX/UI Designer",
        "skills": ["Figma", "Adobe XD", "User Testing", "Prototyping", "Design Systems"],
        "experience": "4 years",
        "projects": ["Eco-friendly travel app", "Fintech dashboard"],
        "summary": "Creative designer focused on building intuitive and aesthetically pleasing interfaces.",
        "location": "Pune, MH",
        "expected_salary": "₹14,00,000 per annum",
        "current_ctc": "₹12,00,000 per annum",
        "notice_period": "3 weeks"
    },
    {
        "name": "Vikram Singh",
        "role": "DevOps Engineer",
        "skills": ["Kubernetes", "Terraform", "CI/CD", "Jenkins", "Go", "Azure"],
        "experience": "7 years",
        "projects": ["Auto-scaling infrastructure for gaming", "Security hardening for banking"],
        "summary": "Infrastructure enthusiast with expertise in automation and system reliability.",
        "location": "Hyderabad, TS",
        "expected_salary": "₹19,00,000 per annum",
        "current_ctc": "₹17,00,000 per annum",
        "notice_period": "4 weeks"
    },
    {
        "name": "Ishita Desai",
        "role": "Digital Marketing Manager",
        "skills": ["SEO", "SEM", "Content Strategy", "Google Analytics", "Social Media"],
        "experience": "5 years",
        "projects": ["D2C brand launch", "Organic traffic growth campaign (300% increase)"],
        "summary": "Strategic marketer specializing in multi-channel growth and brand positioning.",
        "location": "Gurugram, HR",
        "expected_salary": "₹15,50,000 per annum",
        "current_ctc": "₹13,50,000 per annum",
        "notice_period": "1 month"
    },
    {
        "name": "Karan Kapoor",
        "role": "HR Generalist",
        "skills": ["Recruitment", "Employee Relations", "Payroll", "Conflict Resolution"],
        "experience": "6 years",
        "projects": ["Company culture overhaul", "Automated onboarding system"],
        "summary": "Personable HR professional dedicated to building high-performing teams.",
        "location": "Chennai, TN",
        "expected_salary": "₹12,00,000 per annum",
        "current_ctc": "₹10,50,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Siddharth Verma",
        "role": "Frontend Developer",
        "skills": ["React/Next.js", "Tailwind CSS", "TypeScript", "Three.js", "Redux"],
        "experience": "3 years",
        "projects": ["Interactive 3D portfolio", "E-learning platform UI"],
        "summary": "Frontend specialist who loves creating pixel-perfect, interactive web experiences.",
        "location": "Bangalore, KA",
        "expected_salary": "₹11,00,000 per annum",
        "current_ctc": "₹9,50,000 per annum",
        "notice_period": "1 month"
    },
    {
        "name": "Meera Joshi",
        "role": "Backend Developer",
        "skills": ["Python", "Django", "FastAPI", "MongoDB", "Redis", "Elasticsearch"],
        "experience": "5 years",
        "projects": ["Microservices architecture for logistics", "Real-time chat API"],
        "summary": "Efficient backend coder with a focus on performance and clean architecture.",
        "location": "Kochi, KL",
        "expected_salary": "₹16,00,000 per annum",
        "current_ctc": "₹14,00,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Aditya Bannerjee",
        "role": "Sales Executive",
        "skills": ["CRM", "Negotiation", "B2B Sales", "Lead Generation", "Public Speaking"],
        "experience": "4 years",
        "projects": ["New market entry in SE Asia", "Enterprise software sales closer"],
        "summary": "Results-oriented sales professional with a track record of exceeding quotas.",
        "location": "Noida, UP",
        "expected_salary": "₹10,50,000 per annum",
        "current_ctc": "₹9,00,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Tanvi Gupta",
        "role": "Customer Success Manager",
        "skills": ["Relationship Management", "Training", "Zendesk", "Upselling"],
        "experience": "5 years",
        "projects": ["Client retention program (95% rate)", "User documentation revamp"],
        "summary": "Empathetic problem-solver dedicated to ensuring client value and long-term success.",
        "location": "Ahmadabad, GJ",
        "expected_salary": "₹11,50,000 per annum",
        "current_ctc": "₹10,00,000 per annum",
        "notice_period": "1 month"
    },
    {
        "name": "Sanjay Nair",
        "role": "Cybersecurity Analyst",
        "skills": ["Penetration Testing", "SIEM", "Incident Response", "Network Security"],
        "experience": "6 years",
        "projects": ["GDPR compliance audit", "Internal phishing awareness program"],
        "summary": "Security expert focused on proactive threat detection and risk mitigation.",
        "location": "Bangalore, KA",
        "expected_salary": "₹18,50,000 per annum",
        "current_ctc": "₹16,50,000 per annum",
        "notice_period": "3 weeks"
    },
    {
        "name": "Divya Choudhary",
        "role": "QA Engineer",
        "skills": ["Selenium", "Playwright", "Manual Testing", "API Testing", "LoadRunner"],
        "experience": "4 years",
        "projects": ["Automated test suite for mobile apps", "E-commerce checkout stress testing"],
        "summary": "Meticulous tester who ensures zero-defect software releases.",
        "location": "Pune, MH",
        "expected_salary": "₹10,00,000 per annum",
        "current_ctc": "₹8,50,000 per annum",
        "notice_period": "1 month"
    },
    {
        "name": "Kabir Das",
        "role": "Cloud Architect",
        "skills": ["AWS", "GCP", "Serverless", "BigQuery", "Identity Management"],
        "experience": "9 years",
        "projects": ["Serverless backend for global news app", "Hybrid cloud migration"],
        "summary": "Strategic architect designing resilient and cost-effective cloud solutions.",
        "location": "Remote",
        "expected_salary": "₹20,00,000 per annum",
        "current_ctc": "₹18,00,000 per annum",
        "notice_period": "4 weeks"
    },
    {
        "name": "Riya Saxena",
        "role": "Content Strategist",
        "skills": ["Copywriting", "SEO", "Brand Voice", "CMS", "Email Marketing"],
        "experience": "5 years",
        "projects": ["Viral blog series", "Corporate re-branding"],
        "summary": "Storyteller who connects brands with people through meaningful content.",
        "location": "Mumbai, MH",
        "expected_salary": "₹13,50,000 per annum",
        "current_ctc": "₹11,50,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Varun Maheshwari",
        "role": "Mobile Developer (iOS/Swift)",
        "skills": ["Swift", "SwiftUI", "Core Data", "XCode", "TestFlight"],
        "experience": "4 years",
        "projects": ["Award-winning health tracker app", "Social media photo editor"],
        "summary": "Dedicated iOS developer with a passion for sleek, performant mobile apps.",
        "location": "Indore, MP",
        "expected_salary": "₹15,00,000 per annum",
        "current_ctc": "₹13,00,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Nisha Sharma",
        "role": "AI/ML Engineer",
        "skills": ["PyTorch", "OpenCV", "Deep Learning", "Stable Diffusion", "CUDA"],
        "experience": "4 years",
        "projects": ["Real-time gesture recognition", "Generative AI for fashion design"],
        "summary": "AI researcher pushing the boundaries of computer vision and GANs.",
        "location": "Bangalore, KA",
        "expected_salary": "₹19,00,000 per annum",
        "current_ctc": "₹17,00,000 per annum",
        "notice_period": "2 months"
    },
    {
        "name": "Rahul Chatterjee",
        "role": "Financial Analyst",
        "skills": ["Excel (VBA)", "Financial Modeling", "Power BI", "Forecasting"],
        "experience": "6 years",
        "projects": ["Annual budget planning ($50M)", "Cost optimization study"],
        "summary": "Detail-oriented analyst providing actionable insights for business growth.",
        "location": "Kolkata, WB",
        "expected_salary": "₹12,50,000 per annum",
        "current_ctc": "₹11,00,000 per annum",
        "notice_period": "2 weeks"
    },
    {
        "name": "Aavriti Bhatia",
        "role": "Project Manager",
        "skills": ["Waterfall", "Agile", "Risk Management", "Stakeholder Comm."],
        "experience": "7 years",
        "projects": ["ERP implementation", "Cross-departmental efficiency project"],
        "summary": "Organized manager who delivers complex projects on time and within budget.",
        "location": "Hyderabad, TS",
        "expected_salary": "₹17,00,000 per annum",
        "current_ctc": "₹15,00,000 per annum",
        "notice_period": "4 weeks"
    },
    {
        "name": "Sameer Joshi",
        "role": "Legal Consultant",
        "skills": ["Corporate Law", "Contract Negotiation", "Compliance", "Intellectual Property"],
        "experience": "8 years",
        "projects": ["International expansion legal framework", "Tech startup M&A advisory"],
        "summary": "Experienced consultant ensuring legal integrity and strategic protection.",
        "location": "Surat, GJ",
        "expected_salary": "₹20,00,000 per annum",
        "current_ctc": "₹18,00,000 per annum",
        "notice_period": "4 weeks"
    },
    {
        "name": "Aarav Patel",
        "profile": {
            "name": "Aarav Patel",
            "role": "Software Engineer",
            "location": "Ahmedabad, GJ",
            "experience": "4 years",
            "skills": ["Python", "Django", "PostgreSQL", "Docker"],
            "current_company": "Patel Tech Solutions",
            "current_ctc": "₹14,00,000"
        }
    },
    {
        "name": "Ananya Iyer",
        "profile": {
            "name": "Ananya Iyer",
            "role": "Product Designer",
            "location": "Chennai, TN",
            "experience": "5 years",
            "skills": ["Figma", "Adobe XD", "User Research", "Prototyping"],
            "current_company": "Creative Minds Studio",
            "current_ctc": "₹12,50,000"
        }
    },
    {
        "name": "Ishaan Sharma",
        "profile": {
            "name": "Ishaan Sharma",
            "role": "Data Analyst",
            "location": "Gurugram, HR",
            "experience": "3 years",
            "skills": ["SQL", "Tableau", "Excel", "Python"],
            "current_company": "Insights Corp",
            "current_ctc": "₹9,00,000"
        }
    },
    {
        "name": "Kavya Reddy",
        "profile": {
            "name": "Kavya Reddy",
            "role": "Frontend Developer",
            "location": "Hyderabad, TS",
            "experience": "2 years",
            "skills": ["React", "CSS", "TypeScript", "Tailwind"],
            "current_company": "Reddy Digital",
            "current_ctc": "₹8,50,000"
        }
    },
    {
        "name": "Advait Gupta",
        "profile": {
            "name": "Advait Gupta",
            "role": "DevOps Engineer",
            "location": "Noida, UP",
            "experience": "6 years",
            "skills": ["Kubernetes", "AWS", "Terraform", "CI/CD"],
            "current_company": "CloudSecure Ltd",
            "current_ctc": "₹22,00,000"
        }
    },
    {
        "name": "Sana Khan",
        "profile": {
            "name": "Sana Khan",
            "role": "QA Lead",
            "location": "Mumbai, MH",
            "experience": "8 years",
            "skills": ["Selenium", "Appium", "Jira", "Test Automation"],
            "current_company": "QualityFirst Systems",
            "current_ctc": "₹18,00,000"
        }
    },
    {
        "name": "Vivaan Malhotra",
        "profile": {
            "name": "Vivaan Malhotra",
            "role": "Backend Developer",
            "location": "Chandigarh, CH",
            "experience": "4 years",
            "skills": ["Node.js", "MongoDB", "Express", "Redis"],
            "current_company": "Malhotra Tech",
            "current_ctc": "₹13,50,000"
        }
    },
    {
        "name": "Diya Nair",
        "profile": {
            "name": "Diya Nair",
            "role": "UX Researcher",
            "location": "Kochi, KL",
            "experience": "3 years",
            "skills": ["User Interviews", "Usability Testing", "Miro", "Hotjar"],
            "current_company": "UX Bridge",
            "current_ctc": "₹10,00,000"
        }
    },
    {
        "name": "Arjun Mehra",
        "profile": {
            "name": "Arjun Mehra",
            "role": "Full Stack Developer",
            "location": "Jaipur, RJ",
            "experience": "5 years",
            "skills": ["MERN Stack", "Next.js", "GraphQL", "AWS"],
            "current_company": "PinkCity Tech",
            "current_ctc": "₹16,00,000"
        }
    },
    {
        "name": "Myra Kapoor",
        "profile": {
            "name": "Myra Kapoor",
            "role": "AI Researcher",
            "location": "Bhubaneswar, OR",
            "experience": "4 years",
            "skills": ["PyTorch", "NLP", "Computer Vision", "TensorFlow"],
            "current_company": "AI Frontier",
            "current_ctc": "₹20,00,000"
        }
    },
    {
        "name": "Kabir Singh",
        "profile": {
            "name": "Kabir Singh",
            "role": "Mobile App Developer",
            "location": "Lucknow, UP",
            "experience": "3 years",
            "skills": ["Flutter", "Dart", "Firebase", "State Management"],
            "current_company": "Singh Apps",
            "current_ctc": "₹11,00,000"
        }
    },
    {
        "name": "Zara Ahmed",
        "profile": {
            "name": "Zara Ahmed",
            "role": "Cloud Architect",
            "location": "Kolkata, WB",
            "experience": "10 years",
            "skills": ["Azure", "Google Cloud", "Microservices", "Security"],
            "current_company": "Global Cloud Connect",
            "current_ctc": "₹35,00,000"
        }
    },
    {
        "name": "Reyansh Verma",
        "profile": {
            "name": "Reyansh Verma",
            "role": "Cybersecurity Analyst",
            "location": "Indore, MP",
            "experience": "4 years",
            "skills": ["Ethical Hacking", "SIEM", "Firewalls", "Compliance"],
            "current_company": "CyberShield MP",
            "current_ctc": "₹15,00,000"
        }
    },
    {
        "name": "Kiara Joshi",
        "profile": {
            "name": "Kiara Joshi",
            "role": "Data Scientist",
            "location": "Nagpur, MH",
            "experience": "5 years",
            "skills": ["R", "Statistics", "Machine Learning", "SAS"],
            "current_company": "DataPoint Solutions",
            "current_ctc": "₹17,50,000"
        }
    },
    {
        "name": "Ayaan Das",
        "profile": {
            "name": "Ayaan Das",
            "role": "Systems Engineer",
            "location": "Guwahati, AS",
            "experience": "6 years",
            "skills": ["Linux", "Bash", "Networking", "Virtualization"],
            "current_company": "NorthEast Tech",
            "current_ctc": "₹13,00,000"
        }
    },
    {
        "name": "Navya Rao",
        "profile": {
            "name": "Navya Rao",
            "role": "UI Designer",
            "location": "Visakhapatnam, AP",
            "experience": "3 years",
            "skills": ["Typography", "Color Theory", "Sketch", "Interaction Design"],
            "current_company": "Pixel Perfect",
            "current_ctc": "₹9,50,000"
        }
    },
    {
        "name": "Vedant Bhat",
        "profile": {
            "name": "Vedant Bhat",
            "role": "Java Developer",
            "location": "Pune, MH",
            "experience": "4 years",
            "skills": ["Spring Boot", "Microservices", "Hibernate", "Maven"],
            "current_company": "Pune Core Systems",
            "current_ctc": "₹14,50,000"
        }
    },
    {
        "name": "Anvi Saxena",
        "profile": {
            "name": "Anvi Saxena",
            "role": "Machine Learning Engineer",
            "location": "Bhopal, MP",
            "experience": "3 years",
            "skills": ["Scikit-learn", "Keras", "Deep Learning", "Pandas"],
            "current_company": "ML Vision",
            "current_ctc": "₹11,50,000"
        }
    },
    {
        "name": "Atharv Kulkarni",
        "profile": {
            "name": "Atharv Kulkarni",
            "role": "Python Developer",
            "location": "Thane, MH",
            "experience": "2 years",
            "skills": ["FastAPI", "Web Scraping", "PyTest", "NumPy"],
            "current_company": "Kulkarni Tech",
            "current_ctc": "₹8,00,000"
        }
    },
    {
        "name": "Saanvi Chawla",
        "profile": {
            "name": "Saanvi Chawla",
            "role": "Digital Marketer",
            "location": "Ludhiana, PB",
            "experience": "5 years",
            "skills": ["SEO", "SEM", "Content Strategy", "Google Ads"],
            "current_company": "GrowFast Digital",
            "current_ctc": "₹10,50,000"
        }
    }
]

async def seed_data():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db.candidates
    
    
    await collection.delete_many({})
    
    
    result = await collection.insert_many(candidates)
    print(f"Secussefully seeded {len(result.inserted_ids)} candidates!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
