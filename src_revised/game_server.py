import socket
import pandas as pd
import os 
import random



host = "0.0.0.0"
port = 56604 #port of my pc
banner = """
    == Guessing Game v2.0 ==
    Welcome to the Game!"""

#define the 3 choices of difficulty
def easy():
    return  random.randint(1, 50)
def medium():
    return random.randint(1, 100)

def hard():
    return random.randint(1, 500)

def get_random_num(difficulty):
    if difficulty == 'easy':
        return easy()
    elif difficulty == 'medium':
        return medium()
    elif difficulty == 'hard':
         return hard()
    return None



# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print(f"server is listening in port {port}")


while True:      
        print("Waiting for incoming connections...")
        conn, addr = s.accept()
        print(f"New client connected: {addr[0]}") 

        conn.send(b"Enter Username: ")#Enter Username the User or client Desired
        Username = conn.recv(1024).decode().strip().lower()

        conn.send(b"Choose Difficulty you want to play: \n easy \n medium \n hard\n").encode()#user input of difficulty
        difficulty_choice = conn.recv(1024).decode().strip().lower
        

        random_num = get_random_num(difficulty_choice)#if user input none of the choices
        if random_num is None:
             conn.send(b'Invalid difficulty choice. Pick Again')
             continue
                    


        while True: 
                usr_guess = conn.recv(1024).decode().strip()#receive the client send

                if difficulty_choice not in ['a','b','c','end']:# loop where choices were made
                     conn.send("Please Enter 'a','b','c', or 'end' ")
                     conn.close()
                     continue
                if usr_guess == 'end':
                     conn.send("You exit the game..")
                     conn.close()
                     break
                elif usr_guess == 'retry':
                     conn.send("The game is restarting")
                     get_random_num
                     continue
                
                
                
                attempts = 0 #defined starting attempt starting at 0
                while True:
                    if usr_guess == 'end': # if the user input end the game itself is ending
                     conn.send("You exit the game..")
                     conn.close()
                     break
                
                    if usr_guess.isdigit():
                        num = (usr_guess)# user number input where guessing is expecting be in too low, too high, or correct number guessed
                
                        if num == random_num:
                            print("You Guessed the Right Number! You guessed the number in {attempts} attempts.")
                            break
                        elif num <  random_num:
                            conn.send("Too low. Guess again")
                        elif num > random_num:
                            conn.send("Too High.Guess again")
                        else:
                            conn.send("Invalid input, please enter 'a', 'b', or 'c'.")
                
        score = max(10 - attempts, 0)#score and attempt 

        data = {'Username':[Username], 'Difficulty':[difficulty_choice], 'Score': [score]}
        df = pd.DataFrame(data)#data saving into excel

        if os.path.exists('LeaderBoard.xlsx'):
            old_file = pd.read_excel('LeaderBoard.xlsx')
            df = pd.concat([old_file,df], ignore_index=True)

        df.to_excel('LeaderBoard.xlsx', index=False)
        conn.close()