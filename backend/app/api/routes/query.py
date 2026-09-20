import logging

from fastapi import APIRouter, Request, HTTPException

from app.schemas.query import QueryRequest, QueryResponse


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post(
    "/query",
    response_model=QueryResponse
)
def query(request: Request, query_request: QueryRequest):

    try:

        retrieval_service = request.app.state.retrieval_service
        generation_service = request.app.state.generation_service

        chunks = retrieval_service.retrieve(
            query_request.question,
            top_k=5
        )

        # ============================================================
        # DEBUG: PRINT RETRIEVED CHUNKS
        # ============================================================

        print("\n================ RETRIEVED CHUNKS ================\n")

        for i, chunk in enumerate(chunks, start=1):
            print(f"[Source {i}]")
            print(f"Document: {chunk['document']}")
            print(f"Page: {chunk['page']}")
            print(chunk["text"])
            print("\n--------------------------------------------------\n")

        # ============================================================
        # GENERATE ANSWER
        # ============================================================

        answer = generation_service.generate(
            query_request.question,
            chunks
        )

        sources = [
            f"{chunk['document']} p.{chunk['page']}"
            for chunk in chunks
        ]

        return QueryResponse(
            answer=answer,
            sources=sources
        )

    except Exception as e:

        logger.exception(
            "Error while processing query: %s",
            query_request.question
        )

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the query."
        )