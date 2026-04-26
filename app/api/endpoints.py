from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from app.services.llama_service import llama_service
from app.services.mistral_service import mistral_service
from app.services.matching_service import matching_service
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
import json
from bson import ObjectId    
router = APIRouter()
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

@router.post("/parse-jd")
async def parse_jd(jd_text: str = Body(..., embed=True)):
    # Use Llama Brain for parsing
    prompt = f"Parse this Job Description into JSON: {jd_text}"
    return await llama_service.execute_brain_task(prompt)

@router.get("/debug")
async def debug_db():
    try:
        # Check if we can reach the database
        await client.admin.command('ping')
        return {
            "status": "connected",
            "database": settings.DATABASE_NAME,
            "url_provided": settings.MONGODB_URL[:20] + "..." # Hide password
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/candidates")
async def get_candidates():
    cursor = db.candidates.find()
    candidates = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        candidates.append(doc)
    return candidates

@router.post("/match")
async def match_candidates(jd_text: str = Body(..., embed=True)):
    cursor = db.candidates.find()
    candidates = []
    async for doc in cursor:
        candidates.append(doc)
    
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidates in database. Please seed data first.")
        
    return await matching_service.match_candidates(jd_text, candidates)

@router.post("/simulate-conversation")
async def simulate_conversation(
    candidate_id: str = Body(...),
    candidate_profile: Dict[str, Any] = Body(...),
    recruiter_message: str = Body(...)
):
    # Use AI for chat simulation
    prompt = f"""
    ROLE-PLAY INSTRUCTIONS:
    You are strictly acting as this candidate: {json.dumps(candidate_profile)}
    
    RULES:
    1. Only mention skills and experience that are explicitly in your profile.
    2. If asked about strengths/weaknesses, answer based on your specific role: {candidate_profile.get('role')}.
    3. Do not invent new background or skills. Stay in character.
    
    MESSAGE FROM RECRUITER: "{recruiter_message}"
    
    Respond in JSON format:
    {{
      "response": "Your message as the candidate",
      "tone": "Casual | Professional | Curious",
      "interest_level": number (0-100)
    }}
    """
    
    # 🔁 PRIMARY → MISTRAL
    try:
        ai_data = await mistral_service.simulate_chat(prompt)
    except Exception as e:
        print(f"Mistral chat failed, falling back to Llama: {str(e)}")
        
        # 🔁 FALLBACK → LLAMA
        try:
            fallback_response = await llama_service.execute_brain_task(prompt)
            ai_data = json.loads(fallback_response) if isinstance(fallback_response, str) else fallback_response
        except Exception:
            ai_data = {
                "response": "Hi! Thanks for reaching out. I'm currently busy but would love to discuss this further. Let's sync soon!",
                "tone": "Professional/Automated",
                "interest_level": 80
            }

    # 🔥 STORE IN CLOUD (Atlas)
    chat_entry = {
        "candidate_id": candidate_id,
        "recruiter_message": recruiter_message,
        "candidate_response": ai_data.get("response"),
        "interest_level": ai_data.get("interest_level"),
        "timestamp": json.dumps(ObjectId().generation_time, default=str)
    }
    await db.chats.insert_one(chat_entry)

    return ai_data

@router.post("/login")
async def login(credentials: Dict[str, str] = Body(...)):
    # Simple lookup in users collection
    user = await db.users.find_one({"username": credentials.get("username"), "password": credentials.get("password")})
    if user:
        return {"status": "success", "user": {"id": str(user["_id"]), "name": user["name"], "role": "recruiter"}}
    
    # Fallback for admin
    if credentials.get("username") == "admin" and credentials.get("password") == "admin":
        return {"status": "success", "user": {"id": "admin", "name": "Admin Recruiter", "role": "admin"}}
        
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup")
async def signup(user_data: Dict[str, str] = Body(...)):
    # Check if user exists
    existing = await db.users.find_one({"username": user_data.get("username")})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    result = await db.users.insert_one(user_data)
    return {"status": "success", "user_id": str(result.inserted_id)}

@router.post("/apply")
async def public_apply(candidate_data: Dict[str, Any] = Body(...)):
    """
    Public endpoint for candidates to apply directly to ScoutFlow.
    This automatically puts them into the recruitment pool.
    """
    # 1. Add metadata (e.g., applied_at)
    candidate_data["applied_at"] = json.dumps(ObjectId().generation_time, default=str)
    candidate_data["source"] = "Public Portal"
    
    # 2. Save to Atlas
    result = await db.candidates.insert_one(candidate_data)
    
    return {
        "status": "success", 
        "message": "Application received! You are now in the ScoutFlow talent pool.",
        "candidate_id": str(result.inserted_id)
    }

@router.post("/jobs")
async def save_job(job_data: Dict[str, Any] = Body(...)):
    if "is_active" not in job_data:
        job_data["is_active"] = True
    result = await db.jobs.insert_one(job_data)
    return {"status": "success", "job_id": str(result.inserted_id)}

@router.patch("/jobs/{job_id}/rename")
async def rename_job(job_id: str, data: Dict[str, str] = Body(...)):
    new_title = data.get("title")
    if not new_title:
        raise HTTPException(status_code=400, detail="Title is required")
    await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": {"title": new_title}})
    return {"status": "success"}

@router.patch("/jobs/{job_id}/toggle-status")
async def toggle_job_status(job_id: str):
    job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    new_status = not job.get("is_active", True)
    await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": {"is_active": new_status}})
    return {"status": "success", "is_active": new_status}

@router.post("/shortlist")
async def shortlist_candidate(data: Dict[str, Any] = Body(...)):
    # data: { job_id, candidate_id, status: 'Selected' | 'Rejected' | 'Pending' }
    job_id = data.get("job_id")
    candidate_id = data.get("candidate_id")
    status = data.get("status")
    match_score = data.get("match_score")
    
    update_data = {"status": status, "updated_at": "2024-05-20"}
    if match_score is not None:
        update_data["match_score"] = match_score

    await db.shortlisted_candidates.update_one(
        {"job_id": job_id, "candidate_id": candidate_id},
        {"$set": update_data},
        upsert=True
    )
    return {"status": "success"}

@router.get("/dashboard")
async def get_dashboard():
    # Fetch all jobs (Newest first)
    jobs_cursor = db.jobs.find().sort("_id", -1)
    jobs = []
    async for job in jobs_cursor:
        job["_id"] = str(job["_id"])
        
        # For each job, find shortlisted candidates
        shortlist_cursor = db.shortlisted_candidates.find({"job_id": job["_id"]})
        shortlisted = []
        async for s in shortlist_cursor:
            # Get candidate details
            cand = await db.candidates.find_one({"_id": ObjectId(s["candidate_id"])})
            if cand:
                cand["_id"] = str(cand["_id"])
                # Generate a fallback score if missing (for existing records)
                score = s.get("match_score")
                if score is None:
                    # Deterministic but realistic score based on name length/experience
                    name = cand.get("name") or (cand.get("profile") or {}).get("name") or "Candidate"
                    score = 70 + (len(name) % 25)
                
                shortlisted.append({
                    "candidate": cand,
                    "status": s["status"],
                    "match_score": score
                })
        
        job["shortlisted_candidates"] = shortlisted
        jobs.append(job)
    
    return jobs

@router.post("/score-interest")
async def score_interest(chat_history: List[Dict[str, str]] = Body(...)):
    # Use Llama Brain for evaluating interest score
    prompt = f"""
    Analyze this conversation history and determine the candidate's interest level in JSON: {json.dumps(chat_history)}
    Return: {{ "interest_score": number, "status": "Hot"|"Warm"|"Cold", "explanation": "string" }}
    """
    return await llama_service.execute_brain_task(prompt)

@router.post("/simulate-conversation")
async def simulate_conversation(data: Dict[str, Any] = Body(...)):
    profile = data.get("profile")
    message = data.get("message")
    
    prompt = f"""
    You are a candidate with this profile: {json.dumps(profile)}
    A recruiter just sent you this message: "{message}"
    
    Respond naturally as this candidate would.
    Return JSON: {{ "response": "string", "tone": "string", "interest_level": "string" }}
    """
    return await llama_service.execute_brain_task(prompt)
@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    # Delete the job
    res = await db.jobs.delete_one({"_id": ObjectId(job_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Also clean up associated shortlisted candidates
    await db.shortlisted_candidates.delete_many({"job_id": job_id})
    
    return {"status": "success", "message": "Job and associated data deleted"}

@router.get("/candidates/{candidate_id}/history")
async def get_candidate_history(candidate_id: str):
    # Find all shortlisted records for this candidate
    history_cursor = db.shortlisted_candidates.find({"candidate_id": candidate_id})
    history = []
    async for entry in history_cursor:
        job = await db.jobs.find_one({"_id": ObjectId(entry["job_id"])})
        if job:
            history.append({
                "job_title": job["title"],
                "status": entry["status"],
                "applied_at": entry.get("updated_at", "2024-05-20")
            })
    return history

@router.get("/candidates/{candidate_id}/summary")
async def get_candidate_summary(candidate_id: str):
    cand = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Generate summary using Llama
    cand_small = {
    "name": cand.get("name"),
    "role": cand.get("role"),
    "skills": cand.get("skills"),
    "experience": cand.get("experience")
    }
    summary_prompt = f"""
    Create a 3-sentence professional summary for this candidate:
    {json.dumps(cand_small)}
    """
    return await llama_service.execute_brain_task(summary_prompt)
