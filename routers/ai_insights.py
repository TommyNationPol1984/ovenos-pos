# routers/ai_insights.py — NEXUS AI Insights Router for OvenOS FastAPI backend
# Endpoints: /api/ai/chat, /api/ai/query, /api/ai/insights/daily, /api/ai/health
import os, logging
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from supabase import create_client, Client
logger = logging.getLogger("ovenos.ai_insights")
router = APIRouter(prefix="/api/ai", tags=["AI Insights"])
# ── Config ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o")
MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "600"))
NEXUS_SYSTEM_PROMPT = """You are NEXUS, the AI Chief of Staff for OvenOS restaurant POS.
You have direct access to live restaurant data and analytics.
Be concise, data-driven, and hospitality-aware. Max 200 words.
Always format currency as $X.XX. Use bullet points for lists."""
# ── Supabase client ──────────────────────────────────────────────────────────
def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise HTTPException(status_code=500, detail="Supabase env vars not configured.")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
# ── OpenAI client ────────────────────────────────────────────────────────────
def get_openai() -> AsyncOpenAI:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured.")
    return AsyncOpenAI(api_key=OPENAI_API_KEY)
# ── Pydantic models ──────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: Dict[str, Any] = Field(default_factory=dict)
    history: List[ChatMessage] = Field(default_factory=list)
class ChatResponse(BaseModel):
    reply: str
    model: str
    usage: Dict[str, int]
    timestamp: str
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
# ── Helper: build context string ─────────────────────────────────────────────
def _fmt_context(ctx: Dict[str, Any]) -> str:
    if not ctx:
        return ""
    lines = ["\n\nLIVE RESTAURANT DATA:"]
    ds = ctx.get("dailySummary", {})
    if ds:
        lines.append(
            f"TODAY: Revenue ${ds.get('revenue', 0):.2f} | "
            f"Covers: {ds.get('covers', 0)} | "
            f"Avg ticket: ${ds.get('avgTicket', 0):.2f} | "
            f"Open tabs: {ds.get('openTabs', 0)}"
        )
    fs = ctx.get("floorStatus", {})
    if fs:
        lines.append(
            f"FLOOR: {fs.get('occupied', 0)} occupied | "
            f"{fs.get('available', 0)} available | "
            f"{fs.get('occupancyPct', 0)}% occupancy"
        )
    low = [i for i in ctx.get("inventory", []) if i.get("currentStock", 0) <= i.get("parLevel", 0)]
    if low:
        names = ", ".join(f"{i['name']} ({i['currentStock']}{i.get('unit','')})" for i in low[:5])
        lines.append(f"LOW STOCK ({len(low)}): {names}")
    return "\n".join(lines)
# ── POST /api/ai/chat ─────────────────────────────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, ai: AsyncOpenAI = Depends(get_openai)):
    system_content = NEXUS_SYSTEM_PROMPT + _fmt_context(req.context)
    messages = [{"role": "system", "content": system_content}]
    messages += [m.dict() for m in req.history[-10:]]
    messages.append({"role": "user", "content": req.message})
    try:
        resp = await ai.chat.completions.create(
            model=AI_MODEL, messages=messages,
            temperature=0.4, max_tokens=MAX_TOKENS
        )
        return ChatResponse(
            reply=resp.choices[0].message.content.strip(),
            model=resp.model,
            usage={
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
                "total_tokens": resp.usage.total_tokens
            },
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        logger.error(f"OpenAI chat error: {e}")
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")
