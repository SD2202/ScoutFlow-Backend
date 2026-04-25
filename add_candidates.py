import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = "mongodb+srv://Sparsh:SSD@cluster1.wu5egox.mongodb.net/?appName=Cluster1"
DATABASE_NAME = "ai_recruiter"

candidates_to_add = [
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

async def add_candidates():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    result = await db.candidates.insert_many(candidates_to_add)
    print(f"Successfully added {len(result.inserted_ids)} candidates.")
    client.close()

if __name__ == "__main__":
    asyncio.run(add_candidates())
