import socket
import random 
import os
import pandas as pd
from openpyxl import workbook


host = "localhost"
port = 56604 #one of the port in my pc
banner = """
== Guessing Game v2.0 ==
Welcome! Shall we start?"""


#define the 3 choices of difficulty
def get_random_choice(difficulty):
    if difficulty == 'easy':
        return random.randint(1, 50)
    elif difficulty == 'medium':
        return random.randint(1, 100)
    elif difficulty == 'hard':
        return random.randint(1, 500)
    pass

class LeaderBoard:
    def __init__(self):
        self.data = {'Username': [], 'Difficulty': [], 'Attempt': [], 'Score': []} #sequence of data that will input into the file.

    def add_entry(self, username, difficulty, attempt, score): #evey entry will add to file whenever the server send an data to the client
        self.data['Username'].append(username)
        self.data['Difficulty'].append(difficulty)
        self.data['Attempt'].append(attempt)
        self.data['Score'].append(score)
    


def new_filelead(leaderboard): #this define will update and save into the file
    df = pd.DataFrame(leaderboard.data)
    writer = pd.ExcelWriter('leaderboard.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    writer._save()

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")

try:
    while True:
        print("Waiting for incoming connections...")
        conn, addr = s.accept()#this part will receive any client that will enter this game.
        print(f"New client connected: {addr[0]}")

        conn.sendall(banner.encode())#this will send the introduction banner where the game start.

        username = conn.recv(1024).decode().strip()#receive data from client
        difficulty = conn.recv(1024).decode().strip()

        #this part will process all the client or data 
        leaderboard = LeaderBoard()
        while True:
            guessme = get_random_choice(difficulty)
            attempts = 0 
            max_attempts = 10 #the attempts user have is limit into 10 
            score = 0

            while True:
                try:
                    user_input = int(conn.recv(1024).decode().strip())
                    attempts += 1
                    guess = int(user_input)

                    if user_input == guessme:#this conditional will serve as the commentator whenever user input was too low, too high, or the number is guessed the right
                        conn.sendall("You guessed the right number!".encode())
                        score = 100 - (attempts - 1) * 10
                        leaderboard.add_entry(username, difficulty,attempts,score)
                        new_filelead(leaderboard)
                        break
                    elif user_input < guessme:
                        conn.sendall("Guess Higher!\n".encode())
                        continue
                    elif user_input > guessme:
                        conn.sendall("Guess Lower!\n".encode())
                        continue
                    if attempts >= max_attempts:
                        conn.sendall(f"Maximum attempts reached. The number was {guessme}.\n".encode())
                        score = 100 - (attempts - 1) * 10#the attempts will subtracted into score
                        leaderboard.add_entry(username, difficulty, attempts, score)
                        new_filelead(leaderboard)#this part is added when attempt and score come into the end
                        break

                    #Handle commands sent by the client
                    command = conn.recv(1024).decode().strip()
                    if command == 'retry':
                        conn.sendall("the game is restarting ".encode())
                        guessme 
                        continue
                    elif command == 'end':
                        conn.sendall("end".encode())
                        print(f"Client {addr[0]} has ended the game.")
                        break

                except ValueError:#handle the other side of try
                    conn.sendall("Invalid input. Please enter a valid number.\n".encode())

finally:
    s.close()