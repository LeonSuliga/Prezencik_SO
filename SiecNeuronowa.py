import json
import random
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

from Ekspert import should_take_card, pretty_print_state

def extract_features(state):
    card = state["current_card"]
    tokens_on_card = state["tokens_on_card"]
    my_tokens = state["my_tokens"]
    my_cards = set(state["my_cards"])

    opponent_cards = [set(oc) for oc in state["opponent_cards"]]
    opponent_tokens = state["opponent_tokens"]

    features = []
    features.append(card / 35)
    features.append(tokens_on_card / 15)
    features.append(my_tokens / 20)
    features.append(len(my_cards) / 10)
    features.append(1 if any(abs(card - c) == 1 for c in my_cards) else 0)
    features.append(1 if any(abs(card - c) == 1 for opp in opponent_cards for c in opp) else 0)
    features.append(1 if any(t == 0 for t in opponent_tokens) else 0)
    features.append(max(opponent_tokens) / 20)
    return features

def load_data(filename):
    X = []
    y = []
    states = []

    with open(filename, 'r') as f:
        for line in f:
            state = json.loads(line)
            score, _ = should_take_card(state)
            features = extract_features(state)

            X.append(features)
            y.append(score)
            states.append(state)

    return X, y, states

def main():
    X, y, raw_states = load_data("prezencik_states.jsonl")

    X_train, X_test, y_train, y_test, states_train, states_test = train_test_split(
        X, y, raw_states, test_size=0.2, random_state=42
    )

    model = MLPRegressor(hidden_layer_sizes=(32, 32), max_iter=500, random_state=42)
    print("Trenuję model...")
    model.fit(X_train, y_train)
    print("Trening zakończony.")

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    y_tesy_binary = (np.array(y_test) >= 0.5).astype(int)
    predictions_binary = (np.array(predictions) >= 0.5).astype(int)

    correct_predictions = np.sum(predictions_binary == y_tesy_binary)

    print('\n')
    print(f'Correct predictions: {correct_predictions} out of {len(y_test)} ({correct_predictions/len(y_test)*100}%)')
    print(f"Mean Squared Error: {mse:.4f}\n")

    print("Przykładowe decyzje testowe:")
    for i in range(min(5, len(states_test))):
        state = states_test[i]
        pred = predictions[i]
        decision = "TAKE" if pred >= 0.5 else "PASS"
        pretty_print_state(state)
        print(f"Model ocena: {pred:.2f} → {decision}")
        print("-" * 40)

    # Tryb interaktywny
    while True:
        print("\nWprowadź nową sytuację do oceny przez model (lub wpisz 'q' by zakończyć):")
        try:
            if input("Czy chcesz kontynuować? (tak/q): ").strip().lower() == "q":
                break

            card = int(input("Aktualna karta (np. 25): "))
            tokens_on_card = int(input("Żetony na karcie (np. 3): "))
            my_tokens = int(input("Twoje żetony (np. 7): "))
            my_cards = list(map(int, input("Twoje karty (np. 22 23): ").split()))
            my_score = int(input("Twój aktualny wynik (np. 35): "))

            opp_count = int(input("Liczba przeciwników (np. 2): "))
            opponent_cards = []
            opponent_tokens = []
            opponent_scores = []

            for i in range(opp_count):
                cards = list(map(int, input(f"Karty przeciwnika {i+1} (np. 10 11): ").split()))
                tokens = int(input(f"Żetony przeciwnika {i+1} (np. 6): "))
                score = int(input(f"Wynik przeciwnika {i+1} (np. 40): "))
                opponent_cards.append(cards)
                opponent_tokens.append(tokens)
                opponent_scores.append(score)

            new_state = {
                "current_card": card,
                "tokens_on_card": tokens_on_card,
                "my_tokens": my_tokens,
                "my_cards": my_cards,
                "opponent_cards": opponent_cards,
                "opponent_tokens": opponent_tokens,
                "my_score": my_score,
                "opponent_scores": opponent_scores
            }

            features = extract_features(new_state)
            prediction = model.predict([features])[0]
            decision = "TAKE" if prediction >= 0.5 else "PASS"
            print("\nOcena modelu:")
            pretty_print_state(new_state)
            print(f"Model ocenia skłonność do wzięcia na: {prediction:.2f} → {decision}")

            expert_score, expert_comment = should_take_card(new_state)
            print(f"Ekspert ocenia: {expert_score:.2f} → {'TAKE' if expert_score >= 0.5 else 'PASS'}")
            print(f"Komentarz eksperta: {expert_comment}")

        except Exception as e:
            print(f"Błąd danych wejściowych: {e}")

if __name__ == "__main__":
    main()
