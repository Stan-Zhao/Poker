from player_class import PokerHand
from itertools import combinations
import random

def best_five_card_hand(player, public_cards):
    """ 从 7 张牌中选出最佳 5 张 """
    best_hand = max(combinations(player.hand + public_cards, 5), key=lambda hand: PokerHand(hand).get_hand_rank())
    return PokerHand(best_hand)


def determine_winner(players, public_cards):
    """ 计算所有玩家的最佳5张牌，并判断谁赢了 """
    best_hands = {player: best_five_card_hand(player, public_cards) for player in players}

    # 找出最高牌型
    winning_hand = max(best_hands.values(), key=lambda hand: hand.get_hand_rank())
    winners = [player for player, hand in best_hands.items() if hand.get_hand_rank() == winning_hand.get_hand_rank()]

    if len(winners) == 1:
        return f"赢家: {winners[0].name} - {winning_hand.cards}"
    else:
        return f"平局: {' 和 '.join(player.name for player in winners)} - {winning_hand.cards}"



def monte_carlo_simulation(players, known_public_cards, deck, simulations=10000):
    """ 进行蒙特卡洛模拟，计算玩家的胜率 """
    win_counts = {player: 0 for player in players}
    # 初始化归一化胜率字典
    normalized_win_rates = {}

    for _ in range(simulations):
        # 剩余的牌池
        remaining_deck = deck.cards[:]
        random.shuffle(remaining_deck)

        # 随机补充未翻开的公共牌
        missing_cards = 5 - len(known_public_cards)
        simulated_public_cards = known_public_cards + random.sample(remaining_deck, missing_cards)

        # 计算胜者
        winners = determine_winner(players, simulated_public_cards)
        for player in players:
            if player.name in winners:
                win_counts[player] += 1

    # 计算原始胜率
    raw_win_rates = {player.name: (win_counts[player] / simulations) * 100 for player in players}

    # 计算总和（可能不是 100%）
    total = sum(raw_win_rates.values())

    for player,rate in raw_win_rates.items():
        predic=(rate / total) * 100
        if  0 < predic < 1 :
            predic = 1
        # 更新或设置该玩家的胜率
        normalized_win_rates[player] = predic
    # 归一化，使得总胜率严格等于 100%
    # normalized_win_rates = {player: (rate / total) * 100 for player, rate in raw_win_rates.items()}
    # 确保所有玩家的胜率总和为 100%
    win_rate_total = sum(normalized_win_rates.values())
    if win_rate_total != 100:
        difference = 100 - win_rate_total
        normalized_win_rates[players[0].name] += difference  # 将剩余差值添加到第一个玩家

    return normalized_win_rates


