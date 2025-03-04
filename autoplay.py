from logic import monte_carlo_simulation
from logic import determine_winner
from player_class import Card
from player_class import Deck
from player_class import Player


# === 自动发底牌 ===
# === 初始化 ===
deck = Deck()
players = [Player(f"玩家{i+1}") for i in range(2)]  # 4 人桌

for player in players:
    player.receive_cards(deck.draw(2))
print("\n--- 玩家手牌 ---")
for player in players:
    print(player)

# === 计算胜率 ===
win_rates_blind = monte_carlo_simulation(players, [], deck, simulations=10000)
print("\n--- 预测blind胜率 ---")
for player, rate in win_rates_blind.items():
    print(f"{player}: {rate:.0f}%")


# === 发公共牌 ===
flop = deck.draw(3)  # 翻牌
print("\n--- 公共牌 (已知) ---")
print(flop)

# === 计算胜率 ===
win_rates_flop = monte_carlo_simulation(players, flop, deck, simulations=50000)
print("\n--- 预测flop胜率 ---")
for player, rate in win_rates_flop.items():
    print(f"{player}: {rate:.0f}%")


turn = deck.draw(1)  # 转牌
print("\n--- 公共牌 (已知) ---")
print(flop+turn)
# === 计算胜率 ===
win_rates_turn = monte_carlo_simulation(players, flop+turn, deck, simulations=50000)

print("\n--- 预测turn胜率 ---")
for player, rate in win_rates_turn.items():
    print(f"{player}: {rate:.0f}%")


river = deck.draw(1)  # 河牌
public_cards = flop + turn + river  # 公共牌
print("\n--- 公共牌 (已知) ---")
print(public_cards)
# === 计算胜率 ===
win_rates_river = monte_carlo_simulation(players, public_cards, deck, simulations=100)
print("\n--- 预测final胜率 ---")
for player, rate in win_rates_river.items():
    print(f"{player}: {rate:.0f}%")




# === 判断赢家 ===
print("\n--- 结果 ---")
print(determine_winner(players, public_cards))