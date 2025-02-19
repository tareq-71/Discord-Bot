# Good Fish
fresh_water = ["Bass", "Trout", "Catfish", "Pike", "Carp", "Perch", "Bluegill", "Salmon", "Walleye", "Crappie", "Tilapia", "Sturgeon", "Piranha", "Eel", "Suckerfish", "Goldfish"]  # size 16
salt_water = ["Tuna", "Swordfish", "Flounder", "Clownfish", "Angelfish", "Herring", "Halibut", "Cod", "Sardine", "Snapper", "Sea Bass", "Flying fish", "Puffer fish", "Lobster", "Crab"] # size 15
cooler_salt_water = ["Shark", "Whale", "Dolphin", "Manta Ray", "King Crab", "Giant Squid", "Giant Squid", "Anglerfish", "Orca", "Lionfish"] # size 10
SIU_fish = ["iizam fish", "SlimSim fish", "Aboody fish", "KingLightning fish", "DragonFlame fish", "Taco fish", "papisah fish", "Bigjim fish"] # size 8
anime_fish = ["Devil Fruit", "Dragon Ball", "Death Note", "The Nine tailed fox", "Za Warudo", "Sukuna's Finger", "Zanpakuto", "Hunting License", "Grimoire", "Nichirin Sword"] # size 10
video_game_fish = ["Slurp fish", "Enchanted Book", "Legend fish", "Duke Fishron", "The Imposter", "Titanium White Octane", "Ray Gun"] # size 7
spongebob_fish = ["Spongebob", "Patrick Star", "Mr.Krabs" , "Squidward", "Sandy", "Plankton", "Gary", "Mrs.Puff", "Larry the Lobster", "King Neptune", "Mermaid Man", "The Flying Dutchman", "Pearl Krabs", "Karen Plankton", "Barnacle Boy", "Man Ray"] # size 16
soccer_fish = ["Man United fish", "Bayern fish", "Man City fish", "Liverpool fish", "Chelsea fish", "Arsenal fish", "Real Madrid fish", "Barca fish", "PSG fish", "SIU FC fish", "Juventus fish"] # size 11
special_fish = ["Ronaldo fish", "THE ONE PIECE"] # Size 2
special_events = ["Somali Pirates", "Kraken", "Lunchly"]



async def run_fish(ctx, bot):
    outcome = random.randint(1, 1000000)  # Adjust the range for 0.1% probability
    reward = 0
    lost_points = 0
    extra_bait = 0

    if outcome <= 35000:  # fresh water
        fish_name = random.choice(fresh_water)
        reward =  1
        await ctx.send("Casting...")
        wait_time = random.randint(1, 3)
        await asyncio.sleep(wait_time)

    elif outcome <= 65000:  # salt water
        fish_name = random.choice(salt_water)
        reward = 3
        await ctx.send("Casting...")
        await asyncio.sleep(1)  # Wait for 1 seconds
        await ctx.send("You've caught something nice!")
        await asyncio.sleep(3)

    elif outcome <= 80000:  # cooler salt water fish
        fish_name = random.choice(cooler_salt_water)
        reward = 10
        await ctx.send("Casting...")
        await asyncio.sleep(2)
        await ctx.send(f"{ctx.author.mention}, you've caught something BIG!")
        await asyncio.sleep(5)

    elif outcome <= 81000:  # Spongebob fish
        fish_name = random.choice(spongebob_fish)
        reward = 25
        await ctx.send("Casting...")
        await asyncio.sleep(4)
        match fish_name:
            case "Spongebob":
                await ctx.send("Who lives in a pineapple under the sea?")
            case "Gary":
                await ctx.send("Meow")
            case "Patrick":
                await ctx.send("Once there was an ugly barnacle")
                await asyncio.sleep(2)
                await ctx.send("He was so ugly that everyone died.")
                await ctx.send("The end.")
            case "Mr.Krabs":
                await ctx.send("Whats a five-letter word for happiness?")
                await asyncio.sleep(2)
                await ctx.send("MONEY!")
            case "Plankton":
                await ctx.send("No, I'm Not On My Way To The Grand Opening Ceremony.")
                await asyncio.sleep(2)
                await ctx.send("I'm Busy Planning To Rule The World!")
            case "Squidward":
                await ctx.send("What could be better than serving up smiles?")
                await asyncio.sleep(2)
                await ctx.send("Being dead. Or anything else.")
            case _:
                x = random.randint(1, 4)
                match x:
                    case 1:
                        await ctx.send("A few moments later")
                        await asyncio.sleep(1)
                        await ctx.send("Many months later")
                        await asyncio.sleep(2)
                        await ctx.send("5 years later")
                        await asyncio.sleep(3)
                        await ctx.send("Thousands of years later")
                        await asyncio.sleep(4)
                        await ctx.send("Much, Much, Much Later")
                        await asyncio.sleep(5)
                        await ctx.send("One Eternity Later")
                        await asyncio.sleep(10)
                    case 2 | 3 | 4:
                        await ctx.send("Ahh, another peaceful evening in Bikini Bottom.")
                        await asyncio.sleep(1)
                        await ctx.send("Listen to the tropical tranquility.")

    elif outcome <= 81500:  # Anime fish
        fish_name = random.choice(anime_fish)
        reward = 50
        await ctx.send("Casting...")
        await asyncio.sleep(2)

        match fish_name:
            case "Devil Fruit":
                await ctx.send("OMG A DEVIL FRUIT")
                await asyncio.sleep(1)
                await ctx.send("(You eat it)")
                await asyncio.sleep(1)
                await ctx.send("It was a smile devil fruit.")
            case "Dragon Ball":
                await ctx.send("KAMEEEEE")
                await asyncio.sleep(1)
                await ctx.send("HAMEEEE")
                await asyncio.sleep(1)
                await ctx.send("HAAAAAAAA")
            case "Death Note":
                await ctx.send("I'll Take A Potato Chip... And Eat It!")
            case "The Nine Tailed fox":
                await ctx.send("This Discord server shall know pain.")
            case "Za Warudo":
                await ctx.send("STAR PLATINUM")
                await asyncio.sleep(1)
                await ctx.send("ZAAA WAAAAARDUOOOOO")
            case "Sukuna's Finger":
                await ctx.send(f"Are you the strongest because your {ctx.author}?")
                await asyncio.sleep(1)
                await ctx.send(f"Or are you {ctx.author} because your the strongest?")
            case "Zanpakuto":
                await ctx.send("Yokoso")
                await asyncio.sleep(1)
                await ctx.send("watashi no")
                await ctx.send("SIU Discord server")
            case "Grimoire":
                await ctx.send("Disney Clover")
            case "Hunting License":
                await ctx.send("HxH fans waiting for a new chapter to drop.")
                await asyncio.sleep(1)
                await ctx.send("(You are going to be here for a while)")
                await asyncio.sleep(10)
            case  "Nichirin Sword":
                await ctx.send("Set your heart Ablaze")

    elif outcome <= 81600:  # SIU fish
        fish_name = random.choice(SIU_fish)
        reward = 100
        await ctx.send("Casting...")
        await asyncio.sleep(2)
        match fish_name:
            case "iizam fish":
                await ctx.send("This fish is really sexy")
            case "Slimsim fish":
                await ctx.send("This fish looks stupid")
            case "Aboody fish":
                await ctx.send("My mom made food")
            case "KingLightning fish":
                await ctx.send("Instead of using normal bait, this time im gonna use rage bait")
            case "DragonFlame fish":
                await ctx.send("ITS TIME TO MOG")
            case "papisah fish":
                await ctx.send("I love osman")
            case "Bigjim fish":
                await ctx.send("THIS FISH IS OZZZING AURA")
            case "Taco fish":
                await ctx.send("Soccer is for kids")
        
        await asyncio.sleep(3)
        
    
    elif outcome <= 81600:  # Soccer fish
        fish_name = random.choice(soccer_fish)
        reward = 100
        await ctx.send("Casting...")
        await asyncio.sleep(2)
        x = random.randint(1,4)
        match x:
            case 1:
                await ctx.send("From me, Martin Tyler, and alongside me, Alan Smith, let's get ready for a night of thrilling football!")
            case 2:
                await ctx.send("")
        


    elif outcome <= 92900:  # 15.5% chance for catching nothing
        await ctx.send("You cast your line... but caught nothing this time.")
        
    elif outcome <= 99989:  # 7.099% chance for line break
        fish_name = "Doakes Fish"
        lost_points = 10
        await ctx.send("Suprise MotherFucker")
        await ctx.send("Doakes stole 100 SIU Bucks from you!")
    
    elif outcome <= 81500:  # 0.5% chance for legendary fish
        fish_name = random.choice(["Enchanted Book", "Zephyr Fish", "Legend"])
        reward = 50
        await ctx.send("Casting...")
        follow_up_message = "What a beautiful day it is."
        await asyncio.sleep(2)
        await ctx.send(follow_up_message)
        follow_up_message1 = "Days like this are what I live for."
        await asyncio.sleep(4)
        await ctx.send(follow_up_message1)
        follow_up_message2 = f"OMG {ctx.author.mention}, YOUR GONNA BE RICH!!!!!!"
        await asyncio.sleep(4)
        await ctx.send(follow_up_message2)
        await asyncio.sleep(4)

        
    elif outcome <= 99999:  # 0.01% chance for super rare fish
        fish_name = "THE ONE PIECE"
        points_earned = 2000  # Adjust the points for the super rare fish

        await ctx.send("Casting...")
        follow_up_message = "Yo-hohoho, Yo-hoho-ho"
        await asyncio.sleep(2)
        await ctx.send(follow_up_message)
        follow_up_message1 = "Yo-hohoho, Yo-hoho-ho,"
        await asyncio.sleep(3)
        await ctx.send(follow_up_message1)
        follow_up_message2 = "Yo-hohoho, Yo-hoho-ho,"
        await asyncio.sleep(5)
        await ctx.send(follow_up_message2)
        follow_up_message3 = "Yo-hohoho, Yo-hoho-ho,"
        await asyncio.sleep(3)
        await ctx.send(follow_up_message3)
        await ctx.send("Gather up all of the crew!")
        await asyncio.sleep(1)
        await ctx.send("It's time to ship out Bink's brew!")
        await asyncio.sleep(1)
        await ctx.send("Sea wind blows. To where?")
        await asyncio.sleep(1)
        await ctx.send("Who knows?")
        await asyncio.sleep(1)
        await ctx.send("The waves will be our guide!")
        await asyncio.sleep(1)
        await ctx.send("O'er across the ocean's tide,")
        await asyncio.sleep(1)
        await ctx.send("Rays of sunshine far and wide,")
        await asyncio.sleep(1)
        await ctx.send("Birds they sing of cheerful things, in circles passing by!")
        await asyncio.sleep(1)
        await ctx.send("Bid farewell to weaver's town!")
        await asyncio.sleep(1)
        await ctx.send("Say so long to port renowned!")
        await asyncio.sleep(1)
        await ctx.send("Sing a song, it won't be long, before we're casting off!")
        await asyncio.sleep(1)
        await ctx.send("Cross the gold and silver seas")
        await asyncio.sleep(1)
        await ctx.send("The salty spray puts us at ease!")
        await asyncio.sleep(1)
        await ctx.send("Day and night to our delight,")
        await asyncio.sleep(1)
        await ctx.send("The voyage never ends!")
        await asyncio.sleep(1)
        await ctx.send("Gather up all of the crew!")
        await asyncio.sleep(1)
        await ctx.send("It's time to ship out Bink's brew!")
        await asyncio.sleep(1)
        await ctx.send("Pirates we, eternally are challenging the sea!")
        await asyncio.sleep(1)
        await ctx.send("With the waves to rest our heads,")
        await asyncio.sleep(1)
        await ctx.send("ship beneath us as our beds!")
        await asyncio.sleep(1)
        await ctx.send("Hoisted high upon the mast our Jolly Roger flies!")
        await asyncio.sleep(1)
        await ctx.send("Somewhere in the endless sky,")
        await asyncio.sleep(1)
        await ctx.send("Stormy winds are blowin' by!")
        await asyncio.sleep(1)
        await ctx.send("Waves are dancing, evening comes,")
        await asyncio.sleep(1)
        await ctx.send("It's time to sound the drums!")
        await asyncio.sleep(1)
        await ctx.send("But steady men may never fear!")
        await asyncio.sleep(1)
        await ctx.send("Tomorrow's skies are always clear!")
        await asyncio.sleep(1)
        await ctx.send("So pound your feet and clap your hands till sunny days return!")

        await asyncio.sleep(3)

        await ctx.send(f"Congratulations! {ctx.author.mention} You caught {fish_name}! You earned {points_earned} SIUbucks.")

        await asyncio.sleep(5)
        await ctx.send("Game is now shut down until further notice.")
        return
        
    elif outcome == 100000:  # 0.001% chance for super rare fish
        fish_name = "THE LEGENDARY MYTHICAL EXOTIC SUPREME KING FISH"
        points_earned = 5000  # Adjust the points for the super rare fish

        await ctx.send("Casting...")
        follow_up_message = "????????"
        await asyncio.sleep(2)
        await ctx.send(follow_up_message)
        follow_up_message1 = "?????????????"
        await asyncio.sleep(3)
        await ctx.send(follow_up_message1)
        follow_up_message2 = "NOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        await asyncio.sleep(5)
        await ctx.send(follow_up_message2)
        follow_up_message3 = "THIS WAS NEVER INTENDED TO ACUTALLY HAPPEN!!!!!"
        await asyncio.sleep(3)
        await ctx.send(follow_up_message3)
        user7 = ctx.guild.get_member(700122491754119299)
        follow_up_message4 = f"{user7.mention} ITS HAPPENING ITS ACUTALLY HAPPENING!"
        await asyncio.sleep(3)
        await ctx.send(follow_up_message4)

        await asyncio.sleep(3)

        await ctx.send(f"Congratulations! You caught a {fish_name}! You earned {points_earned} SIUbucks.")

        await asyncio.sleep(5)
        await ctx.send("Game is now shut down until further notice.")
        return
    
    await ctx.send(f"You caught a {fish_name}! You earned {points_earned} SIUbucks.")
    return reward, lost_points
