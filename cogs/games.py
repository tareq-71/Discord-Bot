import discord
import random
import time
import asyncio
from discord.ext import commands

# Game lock system to prevent users from playing multiple games at once
game_locks = {}

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def award_SIUBucks(self, user, amount):
        """Helper function to award SIUBucks using the SIUBucks cog."""
        siubucks_cog = self.bot.get_cog("SIUBucks")
        if siubucks_cog:
            siubucks_cog.award_SIUBucks(user, amount)
        else:
            print("SIUBucks cog not found.")

    async def remove_SIUBucks(self, user, amount):
        """Helper function to remove SIUBucks using the SIUBucks cog."""
        siubucks_cog = self.bot.get_cog("SIUBucks")
        if siubucks_cog:
            siubucks_cog.remove_SIUBucks(user, amount)
        else:
            print("SIUBucks cog not found.")

    async def run_mathgame(self, ctx):
        """Math Game: Solve math problems for SIUBucks."""
        await ctx.send("Welcome to the Math Problem Solver Game!")
        await ctx.send("You have 60 seconds to solve as many math problems as you can.")
        await ctx.send("Type your answer as a number, rounding to two decimal places if necessary.")
        await ctx.send("Division: 3 points, Multiplication: 2 points, Addition/Subtraction: 1 point, -1 for incorrect answers.")

        score = 0
        start_time = time.time()
        end_time = start_time + 60

        while time.time() < end_time:
            problem, correct_answer, points = self.generate_problem()
            await ctx.send(f"Problem: {problem}")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            def isfloat(num):
                try:
                    float(num)
                    return True
                except ValueError:
                    return False

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=30)

                # ✅ Keep asking for a valid number, but don't let it get stuck forever
                while not isfloat(msg.content):
                    await ctx.send("❌ Invalid input! Please enter a number.")
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send("⏳ You took too long! Moving to the next problem.")
                        break  # ✅ Break out of the loop instead of getting stuck

                # ✅ Ensure we have a valid number before processing
                if isfloat(msg.content):
                    player_answer = float(msg.content)
                    if round(player_answer, 2) == round(correct_answer, 2):
                        score += points
                        await ctx.send(f"✅ Correct! You earned {points} point(s).")
                    else:
                        score -= 1
                        await ctx.send("❌ Incorrect. You lose 1 point.")
            except asyncio.TimeoutError:
                await ctx.send("⏳ Too slow! No points awarded.")
                break  # ✅ Ensure the game doesn't continue waiting endlessly

        await ctx.send(f"Time's up! Your final score: {score}")
        return score

    def generate_problem(self):
        """Generate a math problem and return the problem, answer, and point value."""
        num1, num2 = random.randint(1, 100), random.randint(1, 100)
        operator = random.choice(["+", "-", "*", "/"])
        problem = f"{num1} {operator} {num2}"
        correct_answer = eval(problem)

        if operator == "/":
            return problem, correct_answer, 3
        elif operator == "*":
            return problem, correct_answer, 2
        else:
            return problem, correct_answer, 1

    @commands.command()
    async def mathgame(self, ctx):
        """Starts a math game where users earn SIUBucks."""
        user_id = ctx.author.id
        if game_locks.get(user_id, False):
            await ctx.send("Please Finish the current game your playing before starting a new one.")
            return

        game_locks[user_id] = True
        try:
            award_amount = await self.run_mathgame(ctx)
            await self.award_SIUBucks(ctx.author, award_amount)
            await ctx.send(f"You gained {award_amount} SIUBucks.")
        except Exception as e:
            await ctx.send("An error occurred. Please try again.")
            print(f"Error: {e}")
        finally:
            game_locks[user_id] = False

    @commands.command()
    async def numgame(self, ctx):
        """Number Guessing Game"""
        user_id = ctx.author.id
        if game_locks.get(user_id, False):
            await ctx.send("Please Finish the current game your playing before starting a new one.")
            return

        game_locks[user_id] = True
        try:
            bot_guess = random.randint(1, 100)
            attempts = 4

            while attempts > 0:
                await ctx.send(f"Enter your guess (1-100). Attempts left: {attempts}")
                def check(m): return m.author == ctx.author and m.channel == ctx.channel
                response = await self.bot.wait_for("message", check=check, timeout=30)

                while not response.content.isdigit():
                    await ctx.send("❌ Invalid input! Please enter a number.")
                    await ctx.send(f"Enter your guess (1-100). Attempts left: {attempts}")
                    def check(m): return m.author == ctx.author and m.channel == ctx.channel
                    response = await self.bot.wait_for("message", check=check, timeout=30)

                guess = int(response.content)

                if guess == bot_guess:
                    await ctx.send("Correct! You win 10 SIUBucks!")
                    await self.award_SIUBucks(ctx.author, 10)
                    return
                elif guess > bot_guess:
                    await ctx.send("Too high!")
                else:
                    await ctx.send("Too low!")

                attempts -= 1

            await ctx.send(f"You lost! The correct number was {bot_guess}. You get 2 SIUBucks for playing.")
            await self.award_SIUBucks(ctx.author, 2)
        except asyncio.TimeoutError:
            await ctx.send("You took too long! No SIUBucks awarded.")
        finally:
            game_locks[user_id] = False

    def create_deck(self):
        """Creates and shuffles a deck of 52 cards."""
        card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        deck = [(card, category) for category in card_categories for card in cards_list]
        random.shuffle(deck)
        return deck

    def card_value(self, card, current_score):
        """Returns the Blackjack value of a given card."""
        if card in ['Jack', 'Queen', 'King']:
            return 10
        elif card == 'Ace':
            return 11 if current_score + 11 <= 21 else 1
        else:
            return int(card)

    async def run_blackjack(self, ctx):
        """Main game loop for Blackjack."""
        '''
        Returns:
        - 1: Player wins (2x winnings)
        - 2: Player gets Blackjack (1.5x winnings)
        - 3: Player loses (bet lost)
        - 4: Tie (bet refunded)
        '''
        deck = self.create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        player_score = sum(self.card_value(card[0], 0) for card in player_hand)
        dealer_score = sum(self.card_value(card[0], 0) for card in dealer_hand)
        print("heloooooooooooooo")


        # ✅ Check for Blackjack
        if player_score == 21:
            await ctx.send("You got Blackjack! You win 1.5x your bet.")
            return 2

        await ctx.send(f"Your hand: {', '.join(f'{card[0]} of {card[1]}' for card in player_hand)}\nYour score: {player_score}")
        await ctx.send(f"Dealer's face-up card: {dealer_hand[0][0]} of {dealer_hand[0][1]}")

        # ✅ Player's turn
        while player_score < 21:
            await ctx.send("Would you like to Hit or Stand?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["hit", "stand"]

            try:
                response = await self.bot.wait_for("message", timeout=45, check=check)
                choice = response.content.lower()
            except:
                await ctx.send("You took too long! You automatically stand.")
                choice = "stand"

            if choice == "hit":
                new_card = deck.pop()
                player_hand.append(new_card)
                player_score += self.card_value(new_card[0], player_score)
                await ctx.send(f"You drew: {new_card[0]} of {new_card[1]}\nYour score: {player_score}")

                if player_score > 21:
                    await ctx.send("You busted! Dealer wins.")
                    return 3
            elif choice == "stand":
                break

        # ✅ Dealer's turn
        await ctx.send(f"Dealer's full hand: {', '.join(f'{card[0]} of {card[1]}' for card in dealer_hand)}\nDealer's score: {dealer_score}")

        while dealer_score < 17:
            new_card = deck.pop()
            dealer_hand.append(new_card)
            dealer_score += self.card_value(new_card[0], dealer_score)
            await ctx.send(f"Dealer drew: {new_card[0]} of {new_card[1]}\nDealer's score: {dealer_score}")

            if dealer_score > 21:
                await ctx.send("Dealer busted! You win!")
                return 1

        # ✅ Determine winner
        if player_score > dealer_score:
            await ctx.send(f"You win! Your score: {player_score}, Dealer's score: {dealer_score}")
            return 1
        elif dealer_score > player_score:
            await ctx.send(f"Dealer wins! Your score: {player_score}, Dealer's score: {dealer_score}")
            return 3
        else:
            await ctx.send(f"It's a tie! Both scores: {player_score}")
            return 4

    @commands.command()
    async def blackjack(self, ctx):
        """Starts a Blackjack game with a bet."""
        user_id = ctx.author.id
        if game_locks.get(user_id, False):
            await ctx.send("Please Finish the current game your playing before starting a new one.")
            return
        
        game_locks[user_id] = True
        try:
            # Get SIUBucks system
            siubucks_cog = self.bot.get_cog("SIUBucks")
            if not siubucks_cog:
                await ctx.send("Error: SIUBucks system unavailable.")
                return

            balance = siubucks_cog.members_SIUBucks.get(str(user_id))
            if balance == 0 or balance is None:
                await self.award_SIUBucks(ctx.author, 1)
                balance = siubucks_cog.members_SIUBucks.get(str(user_id))

            # ✅ Keep asking for a valid bet amount
            while True:
                await ctx.send(f"How much would you like to bet? Your balance is {balance} SIUBucks.")

                try:
                    response = await self.bot.wait_for(
                        "message", 
                        timeout=30, 
                        check=lambda m: m.author == ctx.author and m.channel == ctx.channel
                    )

                    if not response.content.isdigit():  # ✅ Corrected method name
                        await ctx.send("❌ Invalid bet! Please enter a **number**.")
                        continue  # Ask again

                    bet_amount = int(response.content)  # ✅ Convert to int before checking

                    if 1 <= bet_amount <= balance:
                        break  # ✅ Valid bet, exit loop
                    else:
                        await ctx.send("❌ Invalid bet amount! Please enter a number within your balance.")

                except:
                    await ctx.send("⏳ You took too long to respond or your bet was not a valid number. Please try again later.")
                    return  # ✅ Exit game if no response

            # ✅ Deduct bet immediately
            siubucks_cog.remove_SIUBucks(ctx.author, bet_amount)
            await ctx.send(f"Bet placed: {bet_amount} SIUBucks. Dealing cards...")

            # ✅ Run game
            result = await self.run_blackjack(ctx)
            game_locks[user_id] = False

            # ✅ Handle winnings
            if result == 1:
                winnings = bet_amount * 2
                siubucks_cog.award_SIUBucks(ctx.author, winnings)
                await ctx.send(f"You won {winnings} SIUBucks!")
            elif result == 2:
                winnings = int(bet_amount * 1.5)
                siubucks_cog.award_SIUBucks(ctx.author, winnings)
                await ctx.send(f"Blackjack! You win {winnings} SIUBucks!")
            elif result == 3:
                await ctx.send(f"You lost {bet_amount} SIUBucks.")
            elif result == 4:
                siubucks_cog.award_SIUBucks(ctx.author, bet_amount)
                await ctx.send("It's a tie. Your bet has been refunded.")
        
        except Exception as e:
            await ctx.send("An error occurred. Please try again.")
            print(f"Error: {e}")
        finally:
            game_locks[user_id] = False




    @commands.command()
    async def guessgame(self, ctx):
        """Play the SIU guessing game."""
        user_id = ctx.author.id
        if game_locks.get(user_id, False):
            await ctx.send("Please Finish the current game your playing before starting a new one.")
            return
        
        game_locks[user_id] = True
        try:
            await self.run_guessgame(ctx)
            await self.award_SIUBucks(ctx.author, 2)
            await ctx.send("You earned 2 SIUBucks!")
        except Exception as e:
            await ctx.send("An error occurred. Please try again.")
            print(f"Error: {e}")
        finally:
            game_locks[user_id] = False

    async def run_guessgame(self, ctx):
        """SIU Guessing Game Logic."""
        players = [
            "Tareq", "Amar", "Aymen", "Sami", "Shareef", "Niz", "Abdulla",
            "Jamal", "Kerem", "Laith", "Abdi", "Yazen"
        ]

        questions = [
            "Is your person bad at soccer?",
            "Is your person an OSU student?",
            "Is your person bad at basketball?",
            "Did your person go on the Japan trip?",
            "Does your person have a little brother?",
            "Is your person a true anime fan?",
            "Can your person bench 225+?",
            "Is your person short?",
            "Is your person from Palestine?",
            "Is your person STEM?",
        ]

        question_map = {
            "Is your person bad at soccer?": {"yes": {"Niz", "Jamal", "Kerem", "Yazen"}, "no": {"Tareq", "Amar", "Aymen", "Sami", "Shareef", "Abdulla", "Laith", "Abdi"}},
            "Is your person an OSU student?": {"yes": {"Aymen", "Tareq", "Niz", "Shareef", "Amar", "Sami", "Kerem", "Abdulla"}, "no": {"Jamal", "Yazen", "Abdi", "Laith"}},
            "Is your person bad at basketball?": {"yes": {"Sami", "Aymen", "Laith", "Niz", "Abdi", "Kerem", "Yazen"}, "no": {"Abdulla", "Tareq", "Jamal", "Amar", "Shareef"}},
            "Did your person go on the Japan trip?": {"yes": {"Tareq", "Sami", "Kerem", "Amar", "Aymen"}, "no": {"Abdi", "Yazen", "Jamal", "Abdulla", "Niz", "Shareef", "Laith"}},
            "Does your person have a little brother?": {"yes": {"Amar", "Abdi", "Jamal", "Shareef", "Sami"}, "no": {"Tareq", "Aymen", "Abdulla", "Kerem", "Yazen", "Laith", "Niz"}},
            "Is your person a true anime fan?": {"yes": {"Tareq", "Abdulla"}, "no": {"Amar", "Aymen", "Shareef", "Sami", "Abdi", "Laith", "Kerem", "Niz", "Jamal", "Yazen"}},
            "Can your person bench 225+?": {"yes": {"Amar", "Aymen", "Abdulla"}, "no": {"Kerem", "Sami", "Abdi", "Jamal", "Niz", "Laith", "Shareef", "Tareq", "Yazen"}},
            "Is your person short?": {"yes": {"Aymen", "Abdi", "Laith", "Kerem", "Niz", "Abdulla", "Yazen"}, "no": {"Tareq", "Sami", "Amar", "Jamal", "Shareef"}},
            "Is your person from Palestine?": {"yes": {"Tareq", "Amar", "Jamal", "Yazen", "Sami", "Laith", "Abdulla"}, "no": {"Kerem", "Shareef", "Niz", "Aymen", "Abdi"}},
            "Is your person STEM?": {"yes": {"Abdi", "Tareq", "Amar", "Jamal", "Niz", "Shareef", "Abdulla"}, "no": {"Sami", "Aymen", "Laith", "Kerem", "Yazen"}}
        }

        await ctx.send("Welcome to SIU Guessing Game! Answer 'yes' or 'no'.")

        while len(players) > 1 and questions:
            random_question = random.choice(questions)
            answer = await self.ask_question(ctx, random_question)
            
            if random_question in question_map:
                if answer == "yes":
                    players = [p for p in players if p in question_map[random_question]["yes"]]
                else:
                    players = [p for p in players if p in question_map[random_question]["no"]]

            questions.remove(random_question)

        if len(players) == 1:
            await ctx.send(f"I have guessed your person! It's **{players[0]}**!")
        else:
            await ctx.send("I couldn't guess your person.")

    async def ask_question(self, ctx, question):
        """Helper function to ask a question and get a 'yes' or 'no' response."""
        await ctx.send(question)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no"]

        try:
            response = await self.bot.wait_for("message", check=check, timeout=30)
            return response.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. The game has ended.")
            raise asyncio.CancelledError

async def setup(bot):
    await bot.add_cog(Games(bot))