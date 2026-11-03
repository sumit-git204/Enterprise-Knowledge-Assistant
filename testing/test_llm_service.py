from app.services.llm_service import LLMService


llm = LLMService()

context = """
[Source 1]
Source: pdf
Title: test
Page: 1
Content:
The bank must investigate unauthorized debit complaints.
Customers should report suspicious transactions immediately.

[Source 2]
Source: pdf
Title: test
Page: 1
Content:
Eligible customers may receive compensation under bank policy.
"""

question = "What does the bank do when an unauthorized debit is reported?"

answer = llm.generate_answer(
    question=question,
    context=context,
)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)