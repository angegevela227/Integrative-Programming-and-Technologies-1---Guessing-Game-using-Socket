import socket



host = "localhost"
port = 56604 #port of my pc


s = socket.socket()
s.connect((host, port))

# received the banner
data = s.recv(1024)
# print banner
print(data.decode().strip())

while True:
    username = input("Enter your username: ").strip()
    s.sendall(username.encode())


    while True:
        difficulty = input( "Choose Difficulty you want to play: \n(easy/medium/hard)").strip().lower()
        if difficulty in ['easy', 'medium', 'hard']:
            s.sendall(difficulty.encode())
            break
        else:
            print("Invalid difficulty. Please choose again (easy/medium/hard).")


    while True:
        try:
            user_input = input("Enter your guess: ").strip()#input the number guess
            s.sendall(user_input.encode())

            #Receive server response and handle based on game outcome
            reply = s.recv(1024).decode().strip()
            if "You guessed the right number!" in reply:
                print(reply)
                break
            else:
                print(reply)#continue the too low or too high
                continue

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Prompt to retry or end the game
    game_retry = input("Do you want to retry the game?(end/retry): ").strip().lower() 
    s.sendall(game_retry.encode())
    if game_retry == 'end':#end game
        s.sendall('end'.encode())
        print("Exiting game.")
        break
    else:
        #Reset the game state or if user wants to play again
        s.sendall('retry'.encode())
        print("Restarting game...")

s.close()
