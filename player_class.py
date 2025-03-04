import itertools

class Player:
    """ 代表一个玩家 """
    def __init__(self, name):
        self.name = name
        self.hand = []  # 2 张底牌

    def receive_cards(self, cards):
        self.hand = cards

    def __repr__(self):
        return f"{self.name}: {self.hand}"

    def set_hand(self, cards):
        """ 手动设置底牌 """
        if len(cards) != 2:
            raise ValueError("每个玩家必须有 2 张底牌")
        self.hand = cards

import random

# 定义点数大小（A 可以是 14 也可以是 1）
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
               'J': 11, 'Q': 12, 'K': 13, 'A': 14}


class Card:
    """ 代表一张扑克牌 """

    def __init__(self, rank, suit):
        self.rank = rank  # 点数 (2, 3, ..., Q, K, A)
        self.suit = suit  # 花色 (♠, ♥, ♦, ♣)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def value(self):
        return RANK_VALUES[self.rank]


class Deck:
    """ 生成、洗牌、抽牌 """
    suits = ['♠', '♥', '♦', '♣']
    ranks = list(RANK_VALUES.keys())

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)  # 洗牌

    def draw(self, num=1):
        """ 抽取 num 张牌 """
        return [self.cards.pop() for _ in range(num)] if len(self.cards) >= num else []

    def pick(self, *cards):
        picked_cards = []
        for card in cards:
            for c in self.cards:
                if c.rank == card.rank and c.suit == card.suit:
                    self.cards.remove(c)
                    picked_cards.append(c)
                    break  # 找到该牌就停止，防止重复移除
        return picked_cards
class PokerHand:
    """ 解析一手扑克牌并判断牌型 """

    def __init__(self, cards):
        self.cards = cards
        self.ranks = sorted([card.value() for card in cards], reverse=True)
        self.suits = [card.suit for card in cards]
        self.rank_count = {r: self.ranks.count(r) for r in set(self.ranks)}

    def is_flush(self):
        return len(set(self.suits)) == 1

    def is_straight(self):
        return len(self.rank_count) == 5 and (max(self.ranks) - min(self.ranks) == 4) or set(self.ranks) == {14, 2, 3,
                                                                                                             4, 5}

    def get_hand_rank(self):
        """ 计算牌型分级 """
        if self.is_flush() and self.is_straight():
            return (8, max(self.ranks))  # 同花顺
        elif 4 in self.rank_count.values():
            return (7, max(k for k, v in self.rank_count.items() if v == 4))  # 四条
        elif sorted(self.rank_count.values()) == [2, 3]:
            return (6, max(k for k, v in self.rank_count.items() if v == 3))  # 葫芦
        elif self.is_flush():
            return (5, self.ranks)  # 同花
        elif self.is_straight():
            return (4, max(self.ranks))  # 顺子
        elif 3 in self.rank_count.values():
            return (3, max(k for k, v in self.rank_count.items() if v == 3))  # 三条
        elif list(self.rank_count.values()).count(2) == 2:
            return (2, sorted([k for k, v in self.rank_count.items() if v == 2], reverse=True))  # 两对
        elif 2 in self.rank_count.values():
            return (1, max(k for k, v in self.rank_count.items() if v == 2))  # 一对
        else:
            return (0, self.ranks)  # 高牌


def compare_hands(hand1, hand2):
    """ 比较两手牌大小 """
    rank1 = hand1.get_hand_rank()
    rank2 = hand2.get_hand_rank()

    if rank1 > rank2:
        return f"{hand1.cards} 胜出"
    elif rank1 < rank2:
        return f"{hand2.cards} 胜出"
    else:
        return f"{hand1.cards} 和 {hand2.cards} 平手"



def get_best_hand(cards):
    """ 从7张牌中选择最强的5张牌 """
    # 生成所有5张牌的组合
    combinations = itertools.combinations(cards, 5)

    best_hand = None
    best_rank = (-1, [])  # 用于存储最强的牌型（rank，牌）

    for combo in combinations:
        hand = PokerHand(combo)
        rank = hand.get_hand_rank()

        # 比较牌型，选出最强的
        if rank > best_rank:
            best_rank = rank
            best_hand = hand

    return best_hand.cards  # 返回最佳的5张牌

