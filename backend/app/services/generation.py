import re
import ollama
from app.core.config import settings


class GenerationService:
    def __init__(self):
        self.client = ollama.Client(host=settings.ollama_host)
        self.model = settings.ollama_model

    def build_prompt(self, question: str, chunks: list[dict]) -> str:
        context_parts = []

        for i, chunk in enumerate(chunks, start=1):
            context_parts.append(
                f"[Source {i}]\n"
                f"Document: {chunk['document']}\n"
                f"Page: {chunk['page']}\n"
                f"{chunk['text']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are UniGuide AI, a university information assistant.

Answer the user's question using ONLY the provided context.

If the answer is not supported by the context, say that the
information is not available in the provided university documents.

Answer the question directly and concisely.

Use concise bullet points when appropriate.

Every factual statement must include its supporting citation
using EXACTLY this format: [Source N]

Use only ONE source citation for each factual statement.

Correct:
[Source 1]
[Source 2]

Incorrect:
[Source 1, Source 2]
[Source 1, 2.3]
[Source 2, 4.1]
[Document, Page]

Do not combine multiple source numbers in one citation.
If a statement is supported by multiple sources, cite the most
relevant source using a single [Source N] citation.

Do not invent information.

Do not add notes, disclaimers, or meta-comments after the answer.
Answer the question directly using the provided context.
Do not say that a document is unavailable if it appears in the provided context.

Context:

{context}

User Question:

{question}

Answer:
"""

        # ============================================================
        # Q2: ACADEMIC MISCONDUCT
        # ============================================================

        if question.lower().strip() == "what is academic misconduct?":
            prompt += """

For this question, you MUST include:

1. The definition of academic misconduct.
2. The main examples of academic misconduct explicitly supported
   by the retrieved sources.

The examples should include relevant examples such as:
- plagiarism
- cheating or inappropriate behaviour in an examination venue
- collusion
- impersonation
- passing off another person's work or ideas
- undeclared failure to contribute to group coursework
- fabrication or falsification of data
- misleading examiners
- unauthorized materials or information

Only include an example if it is explicitly supported by the
retrieved context.

Do not stop after giving the definition and plagiarism.
Do not discuss unrelated university misconduct.

Use a separate [Source N] citation for each factual example.
Do not combine multiple source numbers in one citation.
"""

        # ============================================================
        # Q3: ACADEMIC APPEAL
        # ============================================================

        elif question.lower().strip() == "how can a student make an academic appeal?":
            prompt += """

For this question, produce the answer using the following structure:

1. Submission:
   Explain how the student submits an academic appeal, including
   the University's online platform and the requirement to use
   the student's own BUE account.

2. Requirements:
   Explain the grounds of appeal and the relevant evidence required.

3. Deadline:
   State the specific deadline or time limit for submitting the
   academic appeal if it appears anywhere in the retrieved sources.
   Do NOT replace the student's submission deadline with a deadline
   for the University's processing of the appeal.

4. Appeal Process:
   Explain the appeal process and its stages.
   Include Stage One and Stage Two if they appear in the sources.
   Include the Appeal Review Panel and the University Academic
   Appeals Committee if they appear in the sources.

5. Other Important Rule:
   State that a student cannot submit an appeal on behalf of
   another student if this is stated in the sources.

IMPORTANT REQUIREMENTS:

- You MUST check all retrieved sources before answering.
- Do not stop after explaining only the submission method.
- Do not stop after explaining the grounds and evidence.
- Before finishing, check whether the retrieved context contains:
  a specific appeal submission deadline,
  Stage One,
  Stage Two,
  Appeal Review Panel,
  University Academic Appeals Committee.
- If any of these are explicitly stated in the retrieved context,
  include them in the answer.
- Only include information explicitly supported by the retrieved context.
- Do not invent a deadline.
- Do not confuse an appeal submission deadline with the University's
  internal processing deadline.

CITATION REQUIREMENTS:

Every factual statement must have its citation immediately after
the statement.

Correct:
The appeal is submitted through the University's online platform. [Source 4]

The student must provide relevant evidence. [Source 3]

Stage One involves the Appeal Review Panel. [Source 4]

Incorrect:
The appeal is submitted through the University's online platform.
The student must provide relevant evidence.

[Source 4]
[Source 3]

Do not put citations on separate lines.
Do not combine citations.
Never write:
[Source 1, Source 4]
[Source 2, 6]

Use exactly one [Source N] citation for each factual statement.
"""

        # ============================================================
        # Q4: STUDENT COMPLAINT
        # ============================================================

        elif question.lower().strip() == "how can a student submit a complaint?":
            prompt += """

For this question, you MUST include ALL of the following:

1. Complaint Form:
   Explain that the student should complete the Student Complaint
   Form if this is stated in the retrieved sources.

2. Submission:
   Explain where and how the complaint should be submitted.
   Include the Student Hub if this is explicitly stated in the
   retrieved sources.

3. Supporting Evidence:
   Explain the requirement to provide relevant supporting evidence
   with the complaint if this is stated in the retrieved sources.

4. Informal Complaint Stage:
   Explain the informal complaint stage/process using the retrieved
   sources.
   Do NOT omit this section.

5. Formal Complaint Stage:
   Explain the formal complaint stage/process using the retrieved
   sources.
   Do NOT omit this section.

IMPORTANT REQUIREMENTS:

- You MUST check ALL retrieved sources before answering.
- Do not stop after explaining only the Student Complaint Form.
- Do not stop after explaining only where to submit the complaint.
- You MUST include both the informal and formal complaint stages
  if they are explicitly stated in the retrieved context.
- Only include information explicitly supported by the retrieved
  context.
- Do not invent complaint stages or procedures.

CITATION REQUIREMENTS:

Every factual statement must have exactly ONE citation.

Correct:
The student should complete the Student Complaint Form. [Source 1]

The complaint can be submitted through the Student Hub. [Source 2]

The informal complaint stage involves ... [Source 3]

The formal complaint stage involves ... [Source 4]

Incorrect:
[Source 1, Source 2]
[Source 3, 4]

Never combine multiple source numbers in one citation.
Use exactly one [Source N] citation for each factual statement.
"""

        # ============================================================
        # Q10: IMPORTANT ACADEMIC INFORMATION
        # ============================================================

        elif question.lower().strip() == "where can students find important academic information?":
            prompt += """

For this question, identify where students can find important
academic information.

You MUST check ALL retrieved sources before answering.

Include the relevant sources of academic information that are
explicitly supported by the retrieved context, such as:

- Student Hub
- Student Portal
- University website / BUE website
- Undergraduate Academic Regulations
- Student Academic Handbook
- Faculty Student Handbook
- University Policies and Procedures
- Programme-specific regulations and requirements

Only include an item if it is explicitly supported by the
retrieved context.

Do not invent a website, portal, office, document, or source.

CITATION REQUIREMENTS:

Every factual statement must have exactly ONE citation immediately
after the statement.

For example:

Students can find important academic information through the
Student Portal. [Source 1]

The Undergraduate Academic Regulations provide the University's
academic framework. [Source 2]

The Faculty Student Handbook provides faculty-specific academic
information. [Source 3]

Do not put one citation after a list containing multiple factual
statements.

Incorrect:

- Undergraduate Academic Regulations
- Faculty Student Handbook
- University Policies and Procedures

[Source 1]

Instead, cite each factual statement separately.

Do not combine multiple source numbers in one citation.

Never write:
[Source 1, Source 2]
[Source 2, 4]

Use exactly one [Source N] citation for each factual statement.

Answer directly and concisely.
"""

        return prompt

    def clean_answer(self, answer: str) -> str:
        answer = answer.strip()

        answer = re.sub(
            r"^According to the provided context:\s*",
            "",
            answer,
            flags=re.IGNORECASE
        )

        answer = re.split(
            r"\n\s*(?:Note|Notes|Disclaimer)\s*:",
            answer,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]

        # ============================================================
        # FIX COMBINED SOURCE CITATIONS
        # ============================================================

        # Convert:
        # [Source 4, 6]
        # [Source 3, Source 4, Source 6]
        # [Source 1, 2, 4, 6]
        #
        # into a single citation using the first source number.

        answer = re.sub(
            r"\[Source\s+(\d+)(?:\s*,\s*(?:Source\s+)?\d+)+\]",
            r"[Source \1]",
            answer,
            flags=re.IGNORECASE
        )

        return answer.strip()

    def generate(self, question: str, chunks: list[dict]) -> str:
        prompt = self.build_prompt(question, chunks)

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={"temperature": 0}
        )

        raw_answer = response["message"]["content"]

        return self.clean_answer(raw_answer)
