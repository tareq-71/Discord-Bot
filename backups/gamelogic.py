import time
import random
import asyncio

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
                "message", check=lambda message: message.author == ctx.author, timeout=30
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
        message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
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

        response = await bot.wait_for("message", timeout=30.0, check=check)
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

# Code for guess game STARTS HERE #
async def run_guessgame(ctx, bot):

    user_id = ctx.author.id

    question1 = "Is your person bad at soccer for there age?"
    question2 = "Is your person an OSU student?"
    question3 = "Is your person Stupid?"
    question4 = "Is your person in highschool/middleschool?"
    question5 = "Did your person go on the japan trip?"
    question6 = "Does your person have a little brother?"
    question7 = "Is your person a TRUE Anime fan?"
    question8 = "Can your person bench a 225+?"
    question9 = "Is your person fat or have previously been fat?"
    question10 = "Is your person bad at SKILLED video games?"
    question11 = "Is your person short?"
    question12 = "Is your person from Palestine?"
    question13 = "Is your person bad at basketball?"
    question14 = "Is your person Black?"
    question15 = "Is your person STEM?"

    question_map = {
        question1: {
            "yes": {"Niz", "Jamal", "Kerem", "Yazen"},
            "no": {
                "Tareq",
                "Amar",
                "Aymen",
                "Sami",
                "Shareef",
                "Abdulla",
                "Laith",
                "Abdi",
            },
        },
        question2: {
            "yes": {
                "Aymen",
                "Tareq",
                "Niz",
                "Shareef",
                "Amar",
                "Sami",
                "Kerem",
                "Abdulla",
            },
            "no": {"Jamal", "Yazen", "Abdi", "Laith"},
        },
        question3: {
            "yes": {
                "Sami",
                "Niz",
                "Shareef",
                "Aymen",
                "Jamal",
                "Abdi",
                "Kerem",
                "Yazen"
            },
            "no": {"Tareq", "Amar", "Laith", "Abdulla"},
        },
        question4: {
            "yes": {"Laith", "Niz", "Yazen"},
            "no": {
                "Tareq",
                "Aymen",
                "Amar",
                "Shareef",
                "Sami",
                "Jamal",
                "Abdulla",
                "Abdi",
                "Kerem",
            },
        },
        question5: {
            "yes": {"Tareq", "Sami", "Kerem", "Amar", "Aymen"},
            "no": {
                "Abdi",
                "Yazen"
                "Jamal",
                "Abdulla",
                "Niz",
                "Shareef",
                "Laith",
            },
        },
        question6: {
            "yes": {"Amar", "Abdi", "Jamal", "Shareef", "Sami"},
            "no": {"Tareq", "Aymen", "Abdulla", "Kerem", "Yazen", "Laith", "Niz"},
        },
        question7: {
            "yes": {"Tareq", "Abdulla"},
            "no": {
                "Amar",
                "Aymen",
                "Shareef",
                "Sami",
                "Abdi",
                "Laith",
                "Kerem",
                "Niz",
                "Jamal",
                "Yazen",
            },
        },
        question8: {
            "yes": {"Amar", "Aymen", "Abdulla"},
            "no": {
                "Kerem",
                "Sami",
                "Abdi",
                "Jamal",
                "Niz",
                "Laith",
                "Shareef",
                "Tareq",
                "Yazen",
            },
        },
        question9: {
            "yes": {"Jamal", "Shareef", "Abdulla"},
            "no": {
                "Tareq",
                "Sami",
                "Aymen",
                "Laith",
                "Amar",
                "Niz",
                "Kerem",
                "Abdi",
                "Yazen",
            },
        },
        question10: {
            "yes": {"Shareef", "Sami", "Abdi", "Kerem", "Abdulla", "Yazen"},
            "no": {"Tareq", "Aymen", "Jamal", "Amar", "Laith", "Niz"},
        },
        question11: {
            "yes": {
                "Aymen",
                "Abdi",
                "Laith",
                "Kerem",
                "Niz",
                "Abdulla",
                "Yazen",
            },
            "no": {"Tareq", "Sami", "Amar", "Jamal", "Shareef"},
        },
        question12: {
            "yes": {
                "Tareq",
                "Amar",
                "Jamal",
                "Yazen",
                "Sami",
                "Laith",
                "Abdulla",
            },
            "no": {"Kerem", "Shareef", "Niz", "Aymen", "Abdi"},
        },
        question13: {
            "yes": {"Sami", "Aymen", "Laith", "Niz", "Abdi", "Kerem", "Yazen"},
            "no": {"Abdulla", "Tareq", "Jamal", "Amar", "Shareef"},
        },
        question14: {
            "yes": {"Abdi"},
            "no": {
                "Tareq",
                "Sami",
                "Aymen",
                "Laith",
                "Amar",
                "Niz",
                "Kerem",
                "Jamal",
                "Yazen",
                "Shareef",
                "Abdulla",
            },
        },
        question15: {
            "yes": {"Abdi", "Tareq", "Amar", "Jamal", "Niz", "Shareef", "Abdulla"},
            "no": {
                "Sami",
                "Aymen",
                "Laith",
                "Kerem",
                "Yazen",
            }
        }
    }

    players = [
        "Tareq",
        "Amar",
        "Aymen",
        "Sami",
        "Shareef",
        "Niz",
        "Abdulla",
        "Jamal",
        "Kerem",
        "Laith",
        "Abdi",
        "Yazen",
    ]

    questions = [
        question1,
        question2,
        question3,
        question4,
        question5,
        question6,
        question7,
        question8,
        question9,
        question10,
        question11,
        question12,
        question13,
        question14,
        question15
    ]

    player_scores = {player: 0 for player in players}

    await ctx.send(
        "Welcome to SIU guessing game, I will ask you questions and try to guess who you are thinking of."
    )

    while len(players) > 1 and len(questions) > 1:
        random_question = random.choice(questions)
        answer = await ask_question(ctx, random_question, bot)
        if random_question in question_map:
            if answer == "yes":
                affected_players = question_map[random_question]["no"]
            else:
                affected_players = question_map[random_question]["yes"]
        for player in affected_players:
            if player in players:
                players.remove(player)
        questions.remove(random_question)

    if len(players) == 1:
        await ctx.send("I have guessed your person! It's " + players[0] + "!")
    else:
        await ctx.send("I couldn't guess your person.")

async def ask_question(ctx, question, bot):
    await ctx.send(question)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    response = await bot.wait_for(
        "message", check=check, timeout=30
    )  # Wait for 30 seconds for a response
    userInput = response.content.lower()
    while userInput not in ["yes", "no"]:
        await ctx.send("Invalid response, enter 'yes' or 'no'.")
        response = await bot.wait_for("message", check=check, timeout=30)
        userInput = response.content.lower()
        await ctx.send("You took too long to respond. The game has ended.")

    return userInput

# guess game ENDS HERE #

# Fish game STARTS HERE #

