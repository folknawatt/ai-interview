# app.py
import os
import av
import subprocess
import streamlit as st
from dotenv import load_dotenv
from core.ai_evaluator import evaluate_candidate
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from core.audio_processor import extract_audio, transcribe_audio

# โหลด API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Interviewer", layout="wide")

st.title("🤖 AI Interview Screening System")
st.markdown("ระบบคัดกรองสัมภาษณ์งานอัตโนมัติด้วย AI")

# --- ส่วนตั้งค่า (Sidebar) ---
with st.sidebar:
    st.header("Settings")
    question_input = st.text_input(
        "ระบุคำถามสัมภาษณ์", value="ช่วยแนะนำตัวและบอกจุดแข็งของคุณหน่อยครับ")
    # ถ้าไม่ได้ใส่ใน .env ก็มาใส่ตรงนี้ได้
    if not API_KEY:
        API_KEY = st.text_input("Google API Key", type="password")

if "video_path" not in st.session_state:
    st.session_state["video_path"] = None

# --- ส่วนอัพโหลด / อัดวิดีโอ ---
tab1, tab2 = st.tabs(["📁 Upload Video", "📹 Record Video"])

with tab1:
    uploaded_file = st.file_uploader(
        "อัพโหลดวิดีโอสัมภาษณ์ (MP4)", type=["mp4", "mov"])
    if uploaded_file:
        st.video(uploaded_file)
        if st.button("ใช้ไฟล์นี้", key="btn_upload"):
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state["video_path"] = "temp_video.mp4"
            st.success("อัพโหลดวิดีโอสำเร็จ! ไปที่ขั้นตอนวิเคราะห์ได้เลย")


# --- Logic การบันทึกวิดีโอ ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    # ตรงนี้คุณสามารถใส่ Image Processing ได้ (เช่น Face Detection)
    # ...

    return av.VideoFrame.from_ndarray(img, format="bgr24")


with tab2:
    st.info("ฟีเจอร์อัดวิดีโอ (WebRTC) กำลังพัฒนา...")
    # ในขั้นตอนนี้เราจะใช้ streamlit-webrtc
    # แต่การ save video file จาก webrtc ต้องใช้ MediaRecorder ฝั่ง client หรือ av ฝั่ง server
    # เพื่อความรวดเร็วและ stable ผมจะใช้ท่า upload ไปก่อนใน tab 1
    # หรือถ้า user ต้องการจริงๆ ผมจะลง code webrtc ให้

    webrtc_ctx = webrtc_streamer(
        key="interview-recording",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={"video": True, "audio": True},
        video_frame_callback=video_frame_callback,
        async_processing=True,
    )

    st.warning("หมายเหตุ: การบันทึกไฟล์วิดีโอจาก WebRTC บน Streamlit Cloud/Local อาจต้องใช้เทคนิคเพิ่มเติม (MediaRecorder). ในเวอร์ชันนี้แนะนำให้ใช้การ Upload ไฟล์ที่อัดจากเครื่องไปก่อน")


if st.session_state["video_path"]:
    st.write(f"Source: {st.session_state['video_path']}")

    if st.button("🚀 เริ่มวิเคราะห์ (Start Analysis)", key="btn_analyze"):

        # Grid Layout
        col1, col2 = st.columns(2)

        # --- Step 1: ถอดความ (Speech-to-Text) ---
        with col1:
            st.info("กำลังถอดเสียงจากวิดีโอ...")
            audio_path = extract_audio("temp_video.mp4")
            transcript = transcribe_audio(audio_path)
            st.success("ถอดความสำเร็จ!")
            st.text_area("Transcript:", transcript, height=200)

        # --- Step 2: วิเคราะห์ (AI Evaluation) ---
        with col2:
            st.info("AI กำลังตรวจคำตอบ...")
            result = evaluate_candidate(API_KEY, question_input, transcript)

            if "error" in result:
                st.error(f"เกิดข้อผิดพลาด: {result['error']}")
            else:
                st.success("วิเคราะห์เสร็จสิ้น!")

                # แสดงคะแนนเป็น Metric สวยๆ
                metric_scores = result.scores
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Communication", f"{metric_scores.communication}/10")
                m2.metric("Relevance", f"{metric_scores.relevance}/10")
                m3.metric("Quality", f"{metric_scores.quality}/10")
                m4.metric("Total Score", f"{metric_scores.total}/30")

                # แสดง Feedback
                st.subheader("📝 Analysis")
                feedback = result.feedback
                st.write(f"**จุดแข็ง:** {feedback.strengths}")
                st.write(f"**จุดอ่อน:** {feedback.weaknesses}")
                st.info(f"**สรุปผล:** {feedback.summary}")

                # ผลลัพธ์ Pass/Fail
                passed = result.pass_prediction
                if passed:
                    st.balloons()
                    st.success("✅ แนะนำให้: ผ่าน (PASS)")
                else:
                    st.warning("❌ แนะนำให้: ไม่ผ่าน (FAIL)")

elif not API_KEY:
    st.warning("กรุณาใส่ Google API Key ก่อนเริ่มใช้งาน")
