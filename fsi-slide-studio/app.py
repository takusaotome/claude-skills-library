"""FSI Slide Studio - Professional Presentation Generator.

A Streamlit chat application that generates FUJISOFT America-branded
presentations using the Claude Agent SDK and domain expert skills.
"""

import logging

import streamlit as st
from pathlib import Path

from config.settings import APP_TITLE, APP_ICON, SUPPORTED_LANGUAGES, OUTPUT_DIR, setup_logging
from agent.client import PresentationAgent
from agent.async_bridge import AsyncBridge

# Initialize logging once at module load
setup_logging()
logger = logging.getLogger(__name__)

# --- Page Config ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- IME Composition Fix ---
# Prevent Enter during IME composition (Japanese/Chinese input) from
# submitting the chat message.  Only suppress Enter while composing;
# normal Enter (no IME) still sends as usual.
_IME_FIX_JS = """
<script>
(function() {
    var doc = window.parent.document;
    function fix() {
        var els = doc.querySelectorAll('textarea');
        for (var i = 0; i < els.length; i++) {
            var el = els[i];
            if (el.dataset.imeFix) continue;
            if (!el.closest('[data-testid="stChatInput"]')) continue;
            el.dataset.imeFix = '1';
            var composing = false;
            el.addEventListener('compositionstart', function() { composing = true; });
            el.addEventListener('compositionend', function() { composing = false; });
            el.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey && (composing || e.isComposing)) {
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                }
            }, true);
        }
    }
    new MutationObserver(fix).observe(doc.body, {childList: true, subtree: true});
    fix();
})();
</script>
"""
st.components.v1.html(_IME_FIX_JS, height=0)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "current_pdf_path" not in st.session_state:
    st.session_state.current_pdf_path = None
if "current_html_path" not in st.session_state:
    st.session_state.current_html_path = None
if "language" not in st.session_state:
    st.session_state.language = "EN"
if "bridge" not in st.session_state:
    st.session_state.bridge = AsyncBridge()


# --- Sidebar ---
with st.sidebar:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown("---")

    # Language selection
    language = st.selectbox(
        "Language / 言語",
        SUPPORTED_LANGUAGES,
        index=SUPPORTED_LANGUAGES.index(st.session_state.language),
        format_func=lambda x: "English" if x == "EN" else "日本語",
    )
    if language != st.session_state.language:
        logger.info("Language changed: %s -> %s", st.session_state.language, language)
        st.session_state.language = language
        # Reset agent to apply new language
        if st.session_state.agent:
            try:
                st.session_state.bridge.run(st.session_state.agent.disconnect())
            except Exception:
                pass
            st.session_state.agent = None
        st.session_state.bridge.shutdown()
        st.session_state.bridge = AsyncBridge()

    st.markdown("---")

    # New conversation button
    label_new = "New Conversation" if language == "EN" else "新しい会話"
    if st.button(label_new, use_container_width=True):
        logger.info("New conversation requested")
        if st.session_state.agent:
            try:
                st.session_state.bridge.run(st.session_state.agent.disconnect())
            except Exception:
                pass
        st.session_state.agent = None
        st.session_state.bridge.shutdown()
        st.session_state.bridge = AsyncBridge()
        st.session_state.messages = []
        st.session_state.current_pdf_path = None
        st.session_state.current_html_path = None
        st.rerun()

    st.markdown("---")

    # Download section
    if st.session_state.current_pdf_path:
        pdf_path = Path(st.session_state.current_pdf_path)
        if pdf_path.exists():
            label_dl = "Download PDF" if language == "EN" else "PDF ダウンロード"
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=label_dl,
                    data=f.read(),
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    use_container_width=True,
                )

    # Info
    st.markdown("---")
    st.caption(
        "Powered by Claude Agent SDK\n\n"
        "FUJISOFT America, Inc."
    )


# --- Tool Label Mapping ---
_TOOL_LABELS = {
    "list_skills": ("Loading skills", "スキル一覧を取得中"),
    "load_skill": ("Loading domain knowledge", "専門知識を読み込み中"),
    "review_structure": ("Reviewing structure", "構成をレビュー中"),
    "review_design": ("Reviewing design", "デザインをレビュー中"),
    "convert_to_pdf": ("Generating PDF", "PDFを生成中"),
    "convert_to_html": ("Generating preview", "プレビューを生成中"),
}


# --- Helper Functions ---
async def _stream_agent_response(agent, user_input, on_tool, on_text):
    """Consume streaming response and invoke callbacks for live progress.

    Handles both token-level deltas (text_delta) from StreamEvent and
    block-level text from AssistantMessage as fallback.
    """
    accumulated = []
    has_deltas = False
    async for chunk in agent.send_message_streaming(user_input):
        ctype = chunk["type"]
        if ctype == "text_delta":
            has_deltas = True
            accumulated.append(chunk["content"])
            on_text("".join(accumulated))
        elif ctype == "text":
            if not has_deltas:
                # Fallback: no StreamEvent deltas, use block-level text
                accumulated.append(chunk["content"])
                on_text("".join(accumulated))
                logger.debug("Fallback to block-level text")
        elif ctype == "tool_use":
            on_tool(chunk["content"])
        elif ctype == "error":
            accumulated.append(f"\n\n⚠️ {chunk['content']}")
            on_text("".join(accumulated))
    return "".join(accumulated) if accumulated else "(No response)"


def _check_for_generated_files():
    """Scan output directory for newly generated PDF/HTML files."""
    pdf_files = sorted(
        OUTPUT_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if pdf_files:
        st.session_state.current_pdf_path = str(pdf_files[0])

    html_files = sorted(
        OUTPUT_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if html_files:
        st.session_state.current_html_path = str(html_files[0])


# --- Main Chat Area ---
header_text = (
    "Create professional FUJISOFT America presentations through conversation."
    if st.session_state.language == "EN"
    else "チャットでプロフェッショナルなプレゼンテーションを作成できます。"
)
st.markdown(f"### {header_text}")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
placeholder = (
    "Describe the presentation you want to create..."
    if st.session_state.language == "EN"
    else "作りたいプレゼンテーションを説明してください..."
)

if user_input := st.chat_input(placeholder):
    logger.info("User message received (%d chars)", len(user_input))
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Initialize agent if needed
    if st.session_state.agent is None:
        st.session_state.agent = PresentationAgent(
            language=st.session_state.language,
        )

    # Get agent response
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        response_placeholder = st.empty()

        status_text = (
            "Thinking..." if st.session_state.language == "EN" else "考え中..."
        )
        status_placeholder.status(status_text, state="running")

        full_response = ""
        try:
            if not st.session_state.bridge.is_alive:
                st.session_state.bridge = AsyncBridge()

            lang = st.session_state.language

            def _on_tool(name):
                short = name.split("__")[-1] if "__" in name else name
                pair = _TOOL_LABELS.get(short, (short, short))
                label = pair[0] if lang == "EN" else pair[1]
                status_placeholder.status(f"🔧 {label}...", state="running")

            def _on_text(text):
                response_placeholder.markdown(text + " ▌")

            logger.info("Streaming response for user input (%d chars)", len(user_input))
            full_response = st.session_state.bridge.run(
                _stream_agent_response(
                    st.session_state.agent,
                    user_input,
                    _on_tool,
                    _on_text,
                )
            )
        except Exception as e:
            logger.error("Response failed: %s", e, exc_info=True)
            full_response = f"Error: {str(e)}"

        status_placeholder.empty()
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Check if a PDF/HTML was generated and rerun to update sidebar
    old_pdf = st.session_state.current_pdf_path
    old_html = st.session_state.current_html_path
    _check_for_generated_files()
    if (st.session_state.current_pdf_path != old_pdf
            or st.session_state.current_html_path != old_html):
        st.rerun()

# --- Slide Preview ---
if st.session_state.current_html_path:
    html_path = Path(st.session_state.current_html_path)
    if html_path.exists():
        st.markdown("---")
        preview_label = (
            "Slide Preview" if st.session_state.language == "EN" else "スライドプレビュー"
        )
        with st.expander(preview_label, expanded=False):
            html_content = html_path.read_text()
            st.components.v1.html(html_content, height=600, scrolling=True)
