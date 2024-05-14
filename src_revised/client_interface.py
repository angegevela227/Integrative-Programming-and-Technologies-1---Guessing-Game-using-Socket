import socket


host = "localhost"
port = 56604#port of my pc


s = socket.socket()
s.connect((host, port))

data = s.recv(1024)
print(data.decode().strip())

username = input("Enter Your desired Username: ")
s.send(username.encode())


difficulty = input("Choose Difficulty you want to play: \n easy \n medium \hard")
s.send(difficulty.encode())

if difficulty == 'end':
    print("You exit the game..")
    s.close()
else:
    print('The game is restarting')
    

while True:
    response = s.recv(1024).decode()
    print(response)
    if "You Guessed the Right Number!" in response:
        break
    guess = input("Enter Your Guess in Mind: ")
    s.send(guess.encode())
    if guess == 'end':
        break

s.close()