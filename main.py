import json
from difflib import get_close_matches

#load the knowledge base
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

#save the knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

#find the best match for a user's question in a list of questions
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

#get the answer for a specific question from the knowledge base
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    

    while True:
        user_input: str = input('You: ')

        # Check if the user wants to quit the chat
        if user_input.lower() == 'quit':
            break

        # Find the best match for the user's question in the knowledge base
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        # If a match is found, provide the answer and ask if the user wants to change it
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
            
            change_answer = input("Do you want to change this answer? (yes/no): ").lower()

            if change_answer == 'yes':
                # Ask for the new answer
                new_answer: str = input('Type the updated answer: ')

                # Update the answer in the knowledge base
                for q in knowledge_base["questions"]:
                    if q["question"] == best_match:
                        q["answer"] = new_answer
                        save_knowledge_base('knowledge_base.json', knowledge_base)
                        print('Bot: Answer updated!')

        # If no match is found, ask the user to teach the bot and add the new response to the knowledge base
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type answer or type "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()