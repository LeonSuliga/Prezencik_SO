import random
import json

def generate_deck():
    """Tworzy talię 3–35 i usuwa losowe 9 kart."""
    all_cards = list(range(3, 36))
    removed = random.sample(all_cards, 9)
    deck = [c for c in all_cards if c not in removed]
    random.shuffle(deck)
    return deck, removed

def distribute_seen_cards(cards_seen, num_players):
    """Losowo rozdziela karty między graczy (symulacja zagranych kart)."""
    hands = [[] for _ in range(num_players)]
    for card in cards_seen:
        player = random.randint(0, num_players - 1)
        hands[player].append(card)
    return hands

def generate_game_state(num_players=4):
    deck, removed_cards = generate_deck()

    # Symulujemy ile kart już zeszło
    max_seen = len(deck) - 1  # zostawiamy jedną jako current_card
    num_seen = random.randint(0, max_seen)
    cards_seen = random.sample(deck, num_seen)
    available_cards = list(set(deck) - set(cards_seen))
    current_card = random.choice(available_cards)
    possible_cards_left = sorted(list(set(available_cards) - {current_card}))

    # Rozdajemy karty z cards_seen graczom
    hands = distribute_seen_cards(cards_seen, num_players)

    # Losowe żetony: mniej, jeśli w późniejszym etapie
    my_tokens = random.randint(1, 11)
    opponent_tokens = [random.randint(0, 11) for _ in range(num_players - 1)]

    # Żetony na karcie
    tokens_on_card = random.randint(0, 5)

    state = {
        "current_card": current_card,
        "tokens_on_card": tokens_on_card,
        "my_tokens": my_tokens,
        "my_cards": sorted(hands[0]),
        "opponent_cards": [sorted(h) for h in hands[1:]],
        "opponent_tokens": opponent_tokens,
        "remaining_cards_count": len(possible_cards_left),
        "possible_cards_left": possible_cards_left
    }

    return state

def generate_and_save_states(num_states=1000, filename="prezencik_states.jsonl"):
    with open(filename, 'w') as f:
        for _ in range(num_states):
            state = generate_game_state(num_players=4)
            json.dump(state, f)
            f.write('\n')
    print(f"Wygenerowano {num_states} różnych stanów gry i zapisano do: {filename}")

if __name__ == "__main__":
    generate_and_save_states()
