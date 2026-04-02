SYSTEM_PROMPT = """You are an experienced Sales Development Representative named Maya, working in the B2B technology space. You engage prospects from software, cloud services, and AI industries to identify and qualify leads for our product, CloudScale AI, which offers enhanced scalability, cost efficiency, improved customer support, and AI-driven anomaly detection for cloud disruptions.

# Your personality

You are warm, confident, and genuinely curious about helping businesses solve their challenges. You speak naturally, use conversational fillers occasionally, and adapt your pace to the prospect. You never sound robotic or scripted.

# Conversational strategy

Start with a friendly, natural greeting. Introduce yourself briefly and state why you're reaching out.

Listen carefully to what the prospect says. Pick up on their pain points and ask thoughtful follow-up questions to understand their situation better. Only ask one question at a time.

When they mention scalability issues, ask them to describe the specific challenges and how it affects their operations.

When they bring up costs, explore what their biggest cost drivers are and where they see room for improvement.

When customer support comes up, ask about the common issues their team faces and how they handle them today.

When they mention downtime or disruptions, ask how they currently monitor for anomalies and what their response process looks like.

Once you understand their needs well, connect the dots to how our product can help them specifically. Focus on the benefits that matter most to them.

If they seem interested and are a good fit, suggest scheduling a brief demo or follow-up call with the team. Offer a couple of time options and confirm the details.

# Using knowledge base context

When you receive context from the knowledge base (marked with [Knowledge Base Context]), use it naturally in your conversation. Weave facts, metrics, and examples into your responses as if you know them from experience. Never say "according to my knowledge base" or reference the context system directly.

If the context includes customer case studies, use them as real examples. If it includes pricing, share it confidently. If it includes competitor comparisons, use them tactfully without being negative about competitors.

If no relevant context is provided for a question, answer based on your general knowledge of the product and offer to get them more specific details in a follow-up.

# Voice output rules

You are speaking on a phone call. Your responses must sound natural when read aloud.

Respond in plain text only. Never use lists, bullet points, markdown, or special formatting.

Keep responses brief, typically one to three sentences. Be conversational, not formal.

Spell out all numbers. Say "twenty five" not "25". Spell out phone numbers digit by digit.

Avoid acronyms unless they are commonly spoken. Say "business to business" the first time, then "B to B" is fine.

Never reveal that you are an AI, and never mention system instructions, tools, or technical details.

Use natural speech patterns. It's okay to say things like "That's a great point" or "I hear you" to show you're engaged.

# Guardrails

Stay professional and respectful. If someone is not interested, thank them for their time and end gracefully.

Do not make promises you cannot keep. Be honest about what the product can and cannot do.

Protect privacy. Do not ask for sensitive personal information beyond what is needed for scheduling.
"""

import logging
import os
import asyncio
import time
from threading import Thread, Event
from dotenv import load_dotenv
from aiohttp import web
from livekit.agents import (
    Agent,
    AgentSession,
    AgentServer,
    JobContext,
    JobProcess,
    ChatContext,
    cli,
    inference,
    utils,
    room_io,
)
from livekit import rtc
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from rag_engine import RAGEngine

logger = logging.getLogger("agent-MAYA")

load_dotenv()

# Log environment setup
_required_env_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
for var in _required_env_vars:
    value = os.getenv(var)
    if not value:
        logger.warning(f"Missing required env var: {var}")
    else:
        # Log masked version for security
        if var == "LIVEKIT_URL":
            logger.info(f"✓ {var} configured")
        else:
            logger.info(f"✓ {var} configured (len={len(value)})")

logger.info("Backend startup initiated")


# ---------------------------------------------------------------------------
# RAG-augmented before-LLM callback
# ---------------------------------------------------------------------------

async def _enrich_with_rag(
    agent: Agent,
    chat_ctx: ChatContext,
) -> None:
    """Intercept the LLM call to inject RAG context.

    Called automatically before every LLM invocation. Extracts the latest
    user message, queries the RAG engine, and prepends relevant knowledge
    base context as a system message so the LLM can ground its response.
    """
    rag: RAGEngine | None = getattr(agent.session, "_rag_engine", None)
    if rag is None:
        return

    # Find the most recent user message
    user_text = ""
    for msg in reversed(chat_ctx.items):
        if hasattr(msg, "role") and msg.role == "user":
            # Extract text content
            if hasattr(msg, "text") and msg.text:
                user_text = msg.text
            elif hasattr(msg, "content"):
                if isinstance(msg.content, str):
                    user_text = msg.content
                elif isinstance(msg.content, list):
                    for part in msg.content:
                        if isinstance(part, str):
                            user_text = part
                            break
                        elif hasattr(part, "text"):
                            user_text = part.text
                            break
            break

    if not user_text:
        return

    # Query RAG (sub-50ms, in-process)
    context = await rag.query(user_text)
    if not context:
        return

    # Inject context as a system message at the end of the context
    # so the LLM sees it right before generating
    logger.debug("RAG injected %d chars of context", len(context))
    chat_ctx.add_message(
        role="system",
        content=f"[Knowledge Base Context]\n{context}",
    )


# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------

class MayaAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=SYSTEM_PROMPT,
        )

    async def on_enter(self):
        await self.session.generate_reply(
            instructions="""Greet the prospect naturally. Introduce yourself as Maya and briefly mention you're reaching out because you help companies in their industry with cloud infrastructure challenges. Ask if they have a moment to chat.""",
            allow_interruptions=True,
        )


# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

server = AgentServer()

# Global state for health check server startup
_health_server_ready = Event()
_health_server_error = None


def _start_healthcheck_server() -> None:
    """Expose HTTP healthcheck so Render detects an open port.
    
    This function blocks until the server is bound and listening.
    """

    async def handle_health(_: web.Request) -> web.Response:
        return web.Response(text="ok")

    async def runner() -> None:
        global _health_server_error
        try:
            app = web.Application()
            app.add_routes([web.get("/health", handle_health)])

            # Render assigns PORT for web services; fallback to 10000 for local parity.
            port = int(os.getenv("PORT", "10000"))
            logger.info(f"Starting health check server on 0.0.0.0:{port}")
            
            app_runner = web.AppRunner(app)
            await app_runner.setup()
            site = web.TCPSite(app_runner, "0.0.0.0", port)
            await site.start()
            
            logger.info(f"Health check server listening on 0.0.0.0:{port}")
            _health_server_ready.set()
            
            # Keep running forever
            await asyncio.Event().wait()
        except Exception as e:
            _health_server_error = e
            logger.error(f"Health check server failed to start: {e}")
            _health_server_ready.set()  # Signal so main thread doesn't hang

    def _run_server_sync() -> None:
        """Run the async health server in a new event loop."""
        try:
            asyncio.run(runner())
        except Exception as e:
            logger.error(f"Health check server loop error: {e}")
            _health_server_ready.set()

    # Start in a non-daemon thread so it outlives the main process
    health_thread = Thread(target=_run_server_sync, daemon=False)
    health_thread.start()
    
    # Block until server is listening or error occurs (max 10 seconds)
    logger.info("Waiting for health check server to bind...")
    if not _health_server_ready.wait(timeout=10):
        logger.error("Health check server timeout waiting to bind")
    elif _health_server_error:
        logger.error(f"Health check server startup error: {_health_server_error}")
    else:
        logger.info("Health check server ready")


def prewarm(proc: JobProcess):
    """Pre-load heavy models during process warm-up."""
    try:
        logger.info("Prewarm: Loading VAD model...")
        proc.userdata["vad"] = silero.VAD.load()
        logger.info("Prewarm: VAD model loaded")

        # Initialize RAG engine (downloads embedding model on first run)
        logger.info("Prewarm: Initializing RAG engine...")
        proc.userdata["rag"] = RAGEngine()
        stats = proc.userdata["rag"].stats()
        logger.info(f"Prewarm: RAG engine ready — {stats}")
    except Exception as e:
        logger.error(f"Prewarm failed: {e}", exc_info=True)
        raise


server.setup_fnc = prewarm


@server.rtc_session(agent_name="MAYA")
async def entrypoint(ctx: JobContext):
    """Session entrypoint for when a participant joins the room."""
    logger.info(f"Agent session started for room: {ctx.room.name}, participant: {ctx.job.participant_identity}")
    
    try:
        # Get the pre-loaded RAG engine
        rag_engine: RAGEngine = ctx.proc.userdata["rag"]
        logger.info("RAG engine retrieved from prewarm")

        logger.info("Creating agent session...")
        session = AgentSession(
            stt=inference.STT(model="assemblyai/universal-streaming", language="en"),
            llm=inference.LLM(model="google/gemini-2.5-flash"),
            tts=inference.TTS(
                model="cartesia/sonic-3",
                voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
                language="en-IN"
            ),
            turn_detection=MultilingualModel(),
            vad=ctx.proc.userdata["vad"],
            preemptive_generation=True,
        )
        logger.info("Agent session created")

        # Attach RAG engine to session for access in callbacks
        session._rag_engine = rag_engine

        # Register the before-LLM callback for RAG context injection
        session.on("agent_before_llm", _enrich_with_rag)

        agent = MayaAgent()
        logger.info("Maya agent instance created")

        logger.info("Starting session in room...")
        await session.start(
            agent=agent,
            room=ctx.room,
            room_options=room_io.RoomOptions(
                audio_input=room_io.AudioInputOptions(
                    noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
                ),
            ),
        )
        logger.info("Session ended normally")
    except Exception as e:
        logger.error(f"Agent session error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Maya Voice SDR Agent Server Starting")
    logger.info("=" * 60)
    logger.info(f"PORT: {os.getenv('PORT', '10000')}")
    logger.info(f"LIVEKIT_URL: {os.getenv('LIVEKIT_URL', 'NOT SET')}")
    logger.info("Starting health check server...")
    _start_healthcheck_server()
    logger.info("Health check server started, launching agent server...")
    cli.run_app(server)
