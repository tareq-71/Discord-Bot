import time
import random

# Math Game function STARTS HERE #
async def run_mathgame(ctx, bot):

    await ctx.send("Welcome to the Math Problem Solver Game!")
    await ctx.send("You have 60 seconds to solve as many math problems as you can.")
    await ctx.send("Type your answer as a number round your answer to two decimal places when required.")
    await ctx.send("Division worth: 3 points, Multiplication worth: 2 points, Addition/Subtraction worth: 1 points and -1 for incorrect answer.")
    await ctx.send("DO NOT CHEAT OR USE CALCULATOR")

    score = 0
    start_time = time.time()
    end_time = start_time + 60

    while time.time() < end_time:
        problem, correct_answer, points = generate_problem()
        await ctx.send(f"Problem: {problem}")

        try:
            msg = await bot.wait_for(
                "message", check=lambda message: message.author == ctx.author
            )
            player_answer = float(msg.content)
            if round(player_answer, 2) == round(correct_answer, 2):
                score += points
                await ctx.send(f"Correct! You earned {points} point(s).\n")
            else:
                await ctx.send("Incorrect. You lose 1 point.\n")
                score = score - 1
        except ValueError:
            await ctx.send("Invalid input. You lose 1 point.\n")
            score = score - 1

    await ctx.send("Time's up!")
    await ctx.send(f"Your final score: {score}")
    return score

def generate_problem():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    operator = random.choice(["+", "-", "*", "/"])
    problem = f"{num1} {operator} {num2}"
    correct_answer = eval(problem)
    
    if operator == "/":
        return problem, correct_answer, 3
    elif operator == "*":
        return problem, correct_answer, 2
    else:
        return problem, correct_answer, 1
    
# Math Game function ENDS HERE #

# Num Game function STARTS HERE #
async def run_numgame(ctx, bot):
    botGuess = random.randint(1, 100)
    winner = False
    award = 0

    for i in range(4):
        await ctx.send("Enter your guess(number 1 - 100): ")
        message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        guess = int(message.content)

        if guess == botGuess:
            winner = True
            break
        elif guess > botGuess:
            await ctx.send("Your guess is too high")
        elif guess < botGuess:
            await ctx.send("Your guess is too low")
    
    if winner:
        award = 10
        await ctx.send("Correct you win 10 SIUBucks!")
    else:
        award = 2
        await ctx.send(f"You Lose! Correct answer was {botGuess}")
        await ctx.send("You get 2 SIUBucks for playing")
    
    return award

# Num Game function ENDS HERE #

# Black Jack function STARTS HERE #

card_ranks = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
    "Ace",
]
card_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

def card_value(rank, current_score):
    if rank in ["Jack", "Queen", "King"]:
        return 10
    elif rank == "Ace":
        # Treat Ace as 11, but adjust to 1 if it would bust the hand
        return 11 if current_score + 11 <= 21 else 1
    else:
        return int(rank)

async def run_blackjack(ctx, bot):
    await ctx.send("Dealing cards...")
    deck = [{"rank": rank, "suit": suit} for suit in card_suits for rank in card_ranks]
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    dealer_up_card = dealer_hand[0]
    await ctx.send(f"Dealer's face-up card: {dealer_up_card['rank']} of {dealer_up_card['suit']}")

    while True:
        # Calculate player's score considering Aces
        player_score = sum(card_value(card["rank"], sum(card_value(card["rank"], 0) for card in player_hand)) for card in player_hand)

        # Show player their hand and score
        player_hand_str = ", ".join([f"{card['rank']} of {card['suit']}" for card in player_hand])
        await ctx.send(f"Your hand: {player_hand_str}\nYour score: {player_score}")

        # Check if player busts immediately
        if player_score > 21:
            await ctx.send(f"Busted! Your score is {player_score}. Dealer wins.")
            return 1  # Dealer wins

        # Ask player for decision
        await ctx.send("Would you like to [Hit or Stand]?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        response = await bot.wait_for("message", timeout=60.0, check=check)
        choice = response.content.lower()

        if choice == "hit":
            new_card = deck.pop()
            player_hand.append(new_card)
            player_score += card_value(new_card["rank"], player_score)

            # Show updated hand and check for bust
            player_hand_str = ", ".join([f"{card['rank']} of {card['suit']}" for card in player_hand])
            #await ctx.send(f"New card: {new_card['rank']} of {new_card['suit']}\nYour hand: {player_hand_str}\nYour score: {player_score}")

            if player_score > 21:
                await ctx.send(f"Busted! Your score is {player_score}. Dealer wins.")
                return 1  # Dealer wins

        elif choice == "stand":
            # Dealer logic after player stands
            dealer_score = sum(card_value(card["rank"], sum(card_value(card["rank"], 0) for card in dealer_hand)) for card in dealer_hand)

            while dealer_score < 17:
                new_card = deck.pop()
                dealer_hand.append(new_card)
                dealer_score += card_value(new_card["rank"], dealer_score)

                dealer_hand_str = ", ".join([f"{card['rank']} of {card['suit']}" for card in dealer_hand])
                await ctx.send(f"Dealer's hand: {dealer_hand_str}\nDealer's score: {dealer_score}")

                if dealer_score > 21:
                    await ctx.send(f"Dealer busted! Their score is {dealer_score}. Player wins.")
                    return 2  # Player wins

            # Final comparison
            if player_score > dealer_score:
                await ctx.send(f"Player wins! Your score: {player_score}, Dealer's score: {dealer_score}")
                return 2  # Player wins
            elif dealer_score > player_score:
                await ctx.send(f"Dealer wins! Your score: {player_score}, Dealer's score: {dealer_score}")
                return 1  # Dealer wins
            else:
                await ctx.send(f"It's a tie! Both scores: {player_score}")
                return 3  # Tie

        else:
            await ctx.send("Invalid choice. Please type 'Hit' or 'Stand'.")
            
# Black Jack function ENDS HERE #
