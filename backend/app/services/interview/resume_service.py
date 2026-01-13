from app.config.prompts import GEN_QUESTION_PROMPT
from app.adapters.ai.gemini_client import GeminiClient
from app.adapters.pdf.pdf_extraction import extract_text_from_pdf


class RequestMock:
    """Helper to match the prompt format expectation {request.field}"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ResumeService:
    def __init__(self):
        self.ai_client = GeminiClient()

    def generate_questions_from_pdf(self, pdf_bytes: bytes, num_questions: int = 3) -> str:
        """
        Extracts text from a PDF resume and generates interview questions.

        Args:
            pdf_bytes: PDF file content as bytes.
            num_questions: Number of questions to generate.

        Returns:
            JSON string of generated questions.
        """
        # 1. Extract Text
        resume_text = extract_text_from_pdf(pdf_bytes)

        # 2. Prepare Prompt
        # The prompt template uses {request.num_questions} and {request.resume_text}
        mock_request = RequestMock(
            num_questions=num_questions,
            resume_text=resume_text
        )
        formatted_prompt = GEN_QUESTION_PROMPT.format(request=mock_request)

        # 3. Generate Content
        generated_json = self.ai_client.generate_content(formatted_prompt)

        return generated_json
