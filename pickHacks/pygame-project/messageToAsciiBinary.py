def main():
    message = "Pickhacks"

    for char in message:
        print(f"0{numToBin(ord(char))} - {ord(char)} - {char}")

def numToBin(number):
    numStr = ""

    cont = True
    while cont:
        numStr = str(int(number%2)) + numStr
        number -= number % 2
        number /= 2
        if number == 0:
            cont = False

    return numStr

if __name__ == "__main__":
    main()
