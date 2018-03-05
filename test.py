import  os, killchain # Including module

# Create new device
dev = killchain.NetworkInterface()

# Loop for testing
mode = None
while mode is not "exit":

    # Prints device mode
    print("Current mode: " + dev.mode())
    input()

    mode = input("What mode to change to? ")

    if mode == "exit":
        break

    # Tests for unsupported mode
    elif not dev.is_mode_supported(mode) == "Inconclusive" and not dev.is_mode_supported(mode):
        print(mode + " is not a supported mode!")

    else:
        # Sets device mode
        dev.set_mode(mode)
    input()

    # Prints device mode
    print("New mode: " + dev.mode())

os.system("airodump-ng " + dev.name)
