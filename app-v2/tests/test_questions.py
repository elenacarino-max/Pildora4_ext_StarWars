import unittest

from core.code_validator import validate_question_answer
from core.questions import QUESTIONS, TOPICS, choose_session_question_ids, questions_from_ids


class QuestionBankTests(unittest.TestCase):
    def test_bank_has_fifty_valid_questions(self):
        self.assertEqual(len(QUESTIONS), 50)
        self.assertEqual(len({item["id"] for item in QUESTIONS}), 50)
        for question in QUESTIONS:
            result = validate_question_answer(question, question["solution"])
            self.assertTrue(result.valid, f"{question['id']}: {result.message}")

    def test_session_selection_covers_every_topic(self):
        selected = questions_from_ids(choose_session_question_ids())
        self.assertEqual(len(selected), 6)
        self.assertEqual({item["topic"] for item in selected}, set(TOPICS))


if __name__ == "__main__":
    unittest.main()
