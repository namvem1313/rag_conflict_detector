# app/retrieval.py

import logging
from app import store,qa_model

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def answer_question(question):
    results = store.search(question, k=5)

    # Generate answers from each retrieved chunk
    qa_answers = []
    for r in results:
        try:
            result = qa_model(question=question, context=r["text"])
            qa_answers.append({
                "doc_id": r["doc_id"],
                "text": r["text"],
                "answer": result["answer"],
                "score": result["score"]
            })
        except Exception as e:
            logger.warning(f"QA generation failed for {r['doc_id']}: {e}")

    # Check for conflicting final answers (not just context)
    final_answers = set([a["answer"] for a in qa_answers if a.get("answer")])
    conflict_detected = len(final_answers) > 1

    return {
        "question": question,
        "answers": qa_answers,
        "conflict_detected": conflict_detected,
        "reason": "Conflicting answers generated for the same query" if conflict_detected else None
    }
