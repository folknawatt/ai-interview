from app.services.interview.resume_service import ResumeService


if __name__ == "__main__":
    resume_service = ResumeService()
    resume_service.generate_questions_from_pdf(
        r"D:\ai-interview\backend\app\services\interview\resume.pdf")
