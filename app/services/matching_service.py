import json
import asyncio
import traceback
from typing import List, Dict, Any
from bson import ObjectId
from sklearn.metrics.pairwise import cosine_similarity

from app.services.llama_service import llama_service
from app.services.mistral_service import mistral_service
from app.services.embedding_service import embedding_service


class MatchingService:

    # 🔥 GLOBAL SERIALIZER
    def serialize_data(self, obj):
        if isinstance(obj, list):
            return [self.serialize_data(item) for item in obj]

        if isinstance(obj, dict):
            return {
                key: self.serialize_data(value)
                for key, value in obj.items()
            }

        if isinstance(obj, ObjectId):
            return str(obj)

        return obj


    async def _evaluate_single_candidate(self, cand: Dict[str, Any], jd_text: str, similarity: float) -> Dict[str, Any]:
        try:
            profile = cand.get("profile", cand) if isinstance(cand.get("profile"), dict) else cand

            # 🔥 SMALL SAFE PAYLOAD
            cand_small = {
                "name": profile.get("name", "Unknown"),
                "role": profile.get("role", ""),
                "skills": profile.get("skills", []),
                "experience": profile.get("experience", "N/A")
            }

            eval_prompt = f"""
You are a Senior Technical Recruiter. Your task is to perform a STRICT technical audit.
Prioritize Hard Skills (Programming Languages, Frameworks, Cloud Tools) above all else.

Candidate Profile:
{json.dumps(cand_small)}

Target Job Description:
{jd_text}

Evaluation Rules:
1. TECHNICAL PRIORITY: If a core "Must-Have" technology from the JD is missing, the score MUST be below 60.
2. HARD SKILLS: Match specific tools (e.g., React, Go, Docker) against the candidate's skills list.
3. SENIORITY: Does their years of experience actually align with the JD's requirement?
4. MISMATCH PENALTY: Heavily penalize generalists applying for specialist roles.

Return STRICT JSON:
{{
  "match_score": number (0-100),
  "technical_alignment": number (0-100),
  "seniority_match": "Yes | No | Partial",
  "strengths": ["Specific tool match", "Domain expertise"],
  "weaknesses": ["Missing critical tool X", "Seniority gap"],
  "explanation": "Brief technical justification focusing on SKILL match",
  "recommendation_status": "Highly Recommended | Good Fit | Needs Improvement"
}}
Highly Recommended is reserved ONLY for >90% technical skill alignment.
"""

            # 🔁 PRIMARY → LLAMA
            try:
                evaluation_raw = await llama_service.execute_brain_task(eval_prompt)
            except Exception as e:
                print("Llama failed, switching to Mistral:", str(e))
                evaluation_raw = None

            # 🔁 FALLBACK → MISTRAL
            if not evaluation_raw:
                try:
                    fallback_text = await mistral_service.generate(eval_prompt)
                    evaluation = {
                        "match_score": 50,
                        "strengths": [],
                        "weaknesses": [],
                        "explanation": fallback_text,
                        "recommendation_status": "Fallback"
                    }
                except:
                    evaluation = {
                        "match_score": 50,
                        "strengths": [],
                        "weaknesses": [],
                        "explanation": "Both models failed",
                        "recommendation_status": "Fallback"
                    }
            else:
                # 🔥 SAFE JSON PARSE
                try:
                    evaluation = json.loads(evaluation_raw) if isinstance(evaluation_raw, str) else evaluation_raw
                except:
                    evaluation = {
                        "match_score": 50,
                        "strengths": [],
                        "weaknesses": [],
                        "explanation": "Parsing failed",
                        "recommendation_status": "Unknown"
                    }

            llm_score = evaluation.get("match_score", 50)

            # 🔥 FINAL SCORE (Strict Weighting: 20% Vector Search / 80% AI Analysis)
            final_score = (similarity * 100 * 0.2) + (llm_score * 0.8)

            clean_profile = {
                "_id": str(cand.get("_id")),
                "name": cand_small["name"],
                "role": cand_small["role"],
                "skills": cand_small["skills"],
                "experience": cand_small["experience"]
            }

            return {
                "candidate_id": str(cand.get("_id", "")),
                "name": cand_small["name"],
                "final_score": round(final_score, 1),
                "semantic_similarity": round(float(similarity) * 100, 1),
                "llm_score": llm_score,
                "evaluation": evaluation,
                "profile": clean_profile
            }

        except Exception as e:
            print(f"Error evaluating candidate: {str(e)}")

            return {
                "candidate_id": str(cand.get("_id", "")),
                "name": cand.get("name", "Unknown"),
                "final_score": similarity * 100,
                "semantic_similarity": round(float(similarity) * 100, 1),
                "llm_score": 0,
                "evaluation": {"error": "Processing failed"},
                "profile": {
                    "_id": str(cand.get("_id")),
                    "name": cand.get("name")
                }
            }


    async def match_candidates(self, jd_text: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            # 🔥 JD EMBEDDING
            jd_embedding = await embedding_service.get_text_embedding(jd_text)

            scored_candidates = []

            for cand in candidates:

                # 🔁 ALWAYS REGENERATE EMBEDDINGS (avoid mismatch)
                role = cand.get('role') or (cand.get('profile') or {}).get('role') or 'Candidate'
                skills_list = cand.get('skills') or (cand.get('profile') or {}).get('skills') or []
                skills = ', '.join(skills_list) if skills_list else 'General Skills'
                summary = cand.get('summary') or (cand.get('profile') or {}).get('summary') or ''
                experience = cand.get('experience') or (cand.get('profile') or {}).get('experience') or 'N/A'
                
                # Richer text for better semantic matching
                cand_text = f"{role} with {experience} experience. Skills: {skills}. {summary}".strip()
                cand_embedding = await embedding_service.get_text_embedding(cand_text)

                # 🔥 SAFE SIMILARITY
                try:
                    if len(jd_embedding) != len(cand_embedding):
                        print("⚠️ Dimension mismatch → skipping similarity")
                        similarity = 0
                    else:
                        similarity = cosine_similarity([jd_embedding], [cand_embedding])[0][0]
                except Exception as e:
                    print("Similarity error:", str(e))
                    similarity = 0

                scored_candidates.append((cand, similarity))

            # 🔥 TOP 15 ONLY (WIDE NET)
            scored_candidates.sort(key=lambda x: x[1], reverse=True)
            top_candidates = scored_candidates[:15]

            # 🔥 PARALLEL EXECUTION
            tasks = [
                self._evaluate_single_candidate(cand, jd_text, sim)
                for cand, sim in top_candidates
            ]

            results = await asyncio.gather(*tasks)

            # 🔥 SORT FINAL
            results.sort(key=lambda x: x["final_score"], reverse=True)

            return self.serialize_data(results)

        except Exception as e:
            print("CRITICAL ERROR IN MATCHING:")
            print(traceback.format_exc())
            raise e


matching_service = MatchingService()
