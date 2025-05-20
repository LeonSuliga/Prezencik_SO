def should_take_card(state):
    card = state["current_card"]
    tokens_on_card = state["tokens_on_card"]
    my_tokens = state["my_tokens"]
    my_cards = set(state["my_cards"])
    opponent_cards = [set(oc) for oc in state["opponent_cards"]]
    opponent_tokens = state["opponent_tokens"]

    # Nowe: ocena punktów
    my_score = state.get("my_score", None)
    opponent_scores = state.get("opponent_scores", [])
    worst_opponent = min(opponent_scores) if opponent_scores else None

    if my_tokens == 0:
        return 0.0, "Nie mam żetonów, więc muszę wziąć kartę"

    ratio = tokens_on_card / max(card, 1)

    if card - 1 in my_cards or card + 1 in my_cards:
        return 1.0, "Karta pasuje do mojego ciągu — darmowe punkty"

    if tokens_on_card >= card + 1:
        return 1.0, f"Biorę kartę — liczba żetonów ({tokens_on_card}) > wartość karty ({card})"

    if ratio >= 0.5:
        if my_tokens < 10:
            return 0.95, f"Na karcie aż {tokens_on_card} żetonów (≥50%) — okazja"
        else:
            return 0.75, f"Dużo żetonów na karcie, ale mam sporo własnych — umiarkowanie opłacalne"

    for opp, t in zip(opponent_cards, opponent_tokens):
        if t == 0 and any(abs(card - c) == 1 for c in opp):
            return 0.9, "Przeciwnik bez żetonów i karta mu pasuje — lepiej ją wziąć"

    if my_tokens < 5 and ratio >= 0.4:
        return 0.75, "Mało żetonów, ale karta oferuje coś w zamian"
    if my_tokens >= 18 and ratio >= 0.6:
        return 0.9, "Mam dużo żetonów — mogę sobie pozwolić na tę kartę"

    if my_score is not None and worst_opponent is not None:
        if my_score < worst_opponent - 15 and ratio >= 0.3:
            return 0.9, "Jestem w tyle — opłaca się ryzykować"
        if my_score > worst_opponent + 20 and ratio < 0.4:
            return 0.2, "Mam przewagę — nie warto ryzykować z tą kartą"


    if ratio < 0.2:
        return 0.1, f"Bardzo mało żetonów ({int(ratio * 100)}%) — PASS"

    if ratio >= 0.3:
        score = 0.6 + (ratio - 0.3) * (0.4 / 0.7)  # skala 0.6–1.0
        return round(score, 2), f"Żetony to {int(ratio * 100)}% wartości karty"
    else:
        score = 0.3 + ratio * (0.3 / 0.3)  # skala 0.3–0.6
        return round(score, 2), f"Mało żetonów: {int(ratio * 100)}% wartości"
def pretty_print_state(state):
    print(f"Karta: {state['current_card']}, Żetony na karcie: {state['tokens_on_card']}")
    print(f"Moje żetony: {state['my_tokens']}, Moje karty: {state['my_cards']}")
    print(f"Żetony przeciwników: {state['opponent_tokens']}")
    for i, oc in enumerate(state['opponent_cards']):
        print(f"Przeciwnik {i+1} karty: {oc}")
