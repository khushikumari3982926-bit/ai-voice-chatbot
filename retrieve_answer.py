
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from prepare_data import DATA_FILE, prepare_dataset


class KnowledgeRetriever:
    def __init__(self, dataset_path, threshold=0.20):
        # Load and clean the dataset.
        self.data = prepare_dataset(dataset_path)

        # Get all stored questions.
        self.questions = self.data["question"].tolist()

        # Convert questions into numerical text features.
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )

        # Build the searchable question representations.
        self.question_vectors = self.vectorizer.fit_transform(
            self.questions
        )

        # Minimum similarity required to return an answer.
        self.threshold = threshold

    def search(self, user_question):
        user_question = user_question.strip()

        if not user_question:
            return {
                "found": False,
                "answer": "Please enter a question.",
                "matched_question": None,
                "score": 0.0
            }

        # Convert the user's question using the same vectorizer.
        user_vector = self.vectorizer.transform([user_question])

        # Compare it with all stored questions.
        scores = cosine_similarity(
            user_vector,
            self.question_vectors
        ).flatten()

        # Find the most similar stored question.
        best_index = scores.argmax()
        best_score = float(scores[best_index])

        # Reject weak matches instead of guessing.
        if best_score < self.threshold:
            return {
                "found": False,
                "answer": (
                    "I could not find a sufficiently relevant "
                    "answer in my knowledge dataset."
                ),
                "matched_question": None,
                "score": round(best_score, 3)
            }

        return {
            "found": True,
            "answer": self.data.iloc[best_index]["answer"],
            "matched_question": self.questions[best_index],
            "score": round(best_score, 3)
        }


if __name__ == "__main__":
    retriever = KnowledgeRetriever(DATA_FILE)

    print("Knowledge system is ready!")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ")

        if question.strip().lower() == "exit":
            print("Goodbye!")
            break

        result = retriever.search(question)

        print(f"\nMatched question: {result['matched_question']}")
        print(f"Similarity score: {result['score']}")
        print(f"Answer: {result['answer']}\n")
