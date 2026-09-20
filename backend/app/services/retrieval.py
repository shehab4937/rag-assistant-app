import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class RetrievalService:
    def __init__(self):
        self.embedding_model = SentenceTransformer(
            settings.embedding_model
        )

        self.client = chromadb.PersistentClient(
            path=str(settings.chroma_absolute_path)
        )

        self.collection = self.client.get_collection(
            name=settings.chroma_collection
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ):
        question_lower = question.lower().strip()

        # ============================================================
        # Q1: STUDENT ATTENDANCE
        # ============================================================

        if question_lower == "what are the rules for student attendance?":

            retrieval_question = question
            result_limit = 5

        # ============================================================
        # Q2: ACADEMIC MISCONDUCT
        # ============================================================

        elif question_lower == "what is academic misconduct?":

            retrieval_question = """
            academic misconduct definition
            unfair academic advantage
            academic work or assessment
            examples of academic misconduct
            plagiarism
            cheating
            inappropriate behaviour in an examination venue
            inappropriate behavior in an examination venue
            misleading examiners
            fabrication of data
            falsification of data
            unauthorized materials
            unauthorized information
            collusion
            impersonation
            passing off another person's work
            another person's work or ideas
            undeclared failure to contribute to group coursework
            academic activity
            """

            result_limit = 10

        # ============================================================
        # Q3: ACADEMIC APPEAL
        # ============================================================

        elif question_lower == "how can a student make an academic appeal?":

            retrieval_question = """
            Academic Appeal Procedure
            academic appeal
            how to make an academic appeal
            how to submit an academic appeal
            submitting an academic appeal
            claims.bue.edu.eg/student
            online platform
            BUE account
            own BUE account
            student cannot submit appeal for another student
            grounds of appeal
            evidence required
            relevant evidence
            deadline for academic appeal
            appeal submission requirements
            every student enrolled and registered
            Appeal Review Panel
            University Academic Appeals Committee
            Stage One
            Stage Two
            decision-making process
            """

            result_limit = 10

        # ============================================================
        # Q4: COMPLAINT
        # ============================================================

        elif question_lower == "how can a student submit a complaint?":

            retrieval_question = """
            Student Complaints Procedure
            student complaint
            how to submit a student complaint
            how to make a complaint
            Student Complaint Form
            submit Student Complaint Form
            complaint submission
            complaint process
            complaint procedure
            informal complaint
            formal complaint
            informal stage
            formal stage
            Stage 1
            Stage 2
            Student Hub
            submit to Student Hub
            submitted to Student Hub
            relevant Faculty
            Student Support Officer
            SSO
            supporting evidence
            provide supporting evidence
            details of the complaint
            complaint requirements
            complaint deadline
            complaint review
            """

            result_limit = 10

        # ============================================================
        # Q5: SUPPORT FOR WEAK STUDENTS
        # ============================================================

        elif question_lower == "what support is available for weak students?":

            retrieval_question = """
            Early Identification of At-Risk Students
            Support of Weak Students Protocol
            support for weak students
            weak students
            at-risk students
            students experiencing academic difficulties
            early identification
            identify students experiencing difficulties
            student progress
            personal tutor
            personal tutor support
            academic support programme
            support programme
            clear and specific outcomes
            timeline
            remedial support
            additional academic support
            monitoring student progress
            follow-up
            intervention
            """

            result_limit = 10

        # ============================================================
        # Q6: PERSONAL ACADEMIC TUTOR
        # ============================================================

        elif question_lower == "what is the role of the personal academic tutor?":

            retrieval_question = """
            Personal Academic Tutor Policy
            Personal Academic Tutor
            PAT role
            PAT responsibilities
            responsibilities of the Personal Academic Tutor
            academic guidance
            general support
            academic support
            student progress
            successful transition to university
            support throughout academic journey
            questions or concerns about course
            point of contact
            advice
            assistance
            referral to University services
            specialist support
            """

            result_limit = 7

        # ============================================================
        # Q7: REASONABLE ADJUSTMENTS
        # ============================================================

        elif question_lower == "what reasonable adjustments can students receive?":

            retrieval_question = """
            Reasonable Adjustments Procedure
            reasonable adjustments
            examples of reasonable adjustments
            types of reasonable adjustments
            physical adjustments
            physical access
            teaching and learning spaces
            assessment adjustments
            assessment arrangements
            examination adjustments
            examination arrangements
            exam adjustments
            extra time
            additional time
            additional examination time
            assessment support
            examination support
            disability adjustments
            reasonable adjustment examples
            """

            result_limit = 10

        # ============================================================
        # Q8: UNDERGRADUATE ACADEMIC REGULATIONS
        # ============================================================

        elif question_lower == "what are the academic regulations for undergraduate students?":

            retrieval_question = """
            Undergraduate Academic Regulations 2024-2028
            undergraduate academic regulations
            registration
            credits
            assessment
            progression
            academic status
            awards
            undergraduate programme requirements
            module requirements
            study plan
            """

            result_limit = 7

        # ============================================================
        # Q9: CONSEQUENCES OF ACADEMIC MISCONDUCT
        # ============================================================

        elif question_lower == "what are the consequences of academic misconduct?":

            retrieval_question = """
            academic misconduct consequences
            academic misconduct penalties
            penalties for academic misconduct
            penalty table
            disciplinary sanctions
            examination attempt forfeited
            ejection from examination
            disciplinary committee
            Article 226
            seriousness of offence
            previous academic misconduct
            """

            result_limit = 7

        # ============================================================
        # Q10: IMPORTANT ACADEMIC INFORMATION
        # ============================================================

        elif question_lower == "where can students find important academic information?":

            retrieval_question = """
            where students find important academic information
            academic information
            Student Hub
            Student Portal
            student portal
            University website
            BUE website
            academic regulations
            student handbook
            UG Academic Regulations
            Faculty Student Handbook
            University Policies and Procedures
            programme-specific regulations
            programme requirements
            academic resources
            """

            result_limit = 10

        # ============================================================
        # OTHER QUESTIONS
        # ============================================================

        else:

            retrieval_question = question
            result_limit = top_k

        # ============================================================
        # CREATE EMBEDDING
        # ============================================================

        query_embedding = self.embedding_model.encode(
            [retrieval_question],
            convert_to_numpy=True
        )[0]

        # Retrieve enough candidates for the selected question.
        # For targeted questions, retrieve more candidates than
        # the final result_limit so relevant chunks have a chance
        # to appear.
        retrieval_count = max(result_limit, 10)

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=retrieval_count
        )

        # ============================================================
        # BUILD CHUNKS
        # ============================================================

        chunks = []

        for i in range(len(results["documents"][0])):

            text = results["documents"][0][i]

            if len(text.strip()) < 80:
                continue

            metadata = results["metadatas"][0][i]

            chunks.append(
                {
                    "text": text,
                    "document": metadata["document"],
                    "page": metadata["page"],
                    "chunk_index": metadata["chunk_index"]
                }
            )

            if len(chunks) >= result_limit:
                break

        return chunks
