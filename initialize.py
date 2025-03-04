from logic import monte_carlo_simulation
from logic import determine_winner
from player_class import Card
from player_class import Deck
from player_class import Player





# === 初始化 ===
deck = Deck()
players = [Player(f"玩家{i+1}") for i in range(2)]  # 4 人桌

# === 手动设置底牌 ===
P11=Card('A', '♦')
P12=Card('A', '♥')
P21=Card('A', '♣')
P22=Card('K', '♣')
players[0].set_hand([P11, P12])
players[1].set_hand([P21, P22])
deck.pick(P11,P12,P21,P22)
# === 手动设置公共牌（如果不想手动输入，注释掉这一段即可）===

#===比赛开始===
print("\n--- 玩家手牌 ---")
for player in players:
    print(player)

# === 计算胜率 ===
win_rates_blind = monte_carlo_simulation(players, [], deck, simulations=50000)
print("\n--- 预测胜率 ---")
for player, rate in win_rates_blind.items():
    print(f"{player}: {rate:.0f}%")



# ===flop====
f1=Card('J', '♠')
f2=Card('4', '♠')
f3=Card('10', '♣')
flop = [f1,f2,f3]
deck.pick(f1,f2,f3)
print("\n--- 公共牌 (已知) ---")
print(flop)

# === 计算胜率 ===
win_rates_flop = monte_carlo_simulation(players, flop, deck, simulations=50000)
print("\n--- 预测flop胜率 ---")
for player, rate in win_rates_flop.items():
    print(f"{player}: {rate:.0f}%")


# ===turn====
turn_card=Card('10', '♠')
turn = [turn_card]
deck.pick(turn_card)
print("\n--- 公共牌 (已知) ---")
print(flop+turn)

# === 计算胜率 ===
win_rates_turn = monte_carlo_simulation(players, flop+turn, deck, simulations=50000)

print("\n--- 预测turn胜率 ---")
for player, rate in win_rates_turn.items():
    print(f"{player}: {rate:.0f}%")

# ===river====
river_card= Card('Q', '♠')
river = [river_card]
deck.pick(turn_card)
public_cards = flop + turn + river
print("\n--- 公共牌 (已知) ---")
print(public_cards)
# === 计算胜率 ===
win_rates_river = monte_carlo_simulation(players, public_cards, deck, simulations=100)
print("\n--- 预测final胜率 ---")
for player, rate in win_rates_river.items():
    print(f"{player}: {rate:.0f}%")

# # === 自动发底牌 ===
# # === 初始化 ===
# deck = Deck()
# players = [Player(f"玩家{i+1}") for i in range(2)]  # 4 人桌
# for player in players:
#     player.receive_cards(deck.draw(2))
#
# # === 发公共牌 ===
# flop = deck.draw(3)  # 翻牌
# turn = deck.draw(1)  # 转牌
# river = deck.draw(1)  # 河牌
# public_cards = flop + turn + river  # 公共牌

# === 判断赢家 ===
print("\n--- 结果 ---")
print(determine_winner(players, public_cards))
