import  os, killchain

dev = killchain.NetworkInterface()
mode = None
while mode is not "exit":
    print("Current mode: " + dev.mode())
    input()
    mode = input("What mode to change to? ")
    if mode == "exit":
        break
    elif dev.is_mode_supported(mode) == "Inconclusive":
        print("Check for support for " + mode + " mode returned inconclusive, attempting to set mode")
        dev.set_mode(mode)
    elif dev.is_mode_supported(mode):
        print(mode + " is a supported mode!")
        dev.set_mode(mode)
    else:
        print(mode + " mode is not supported")
    input()
    print("New mode: " + dev.mode())

os.system("airodump-ng " + dev.name)
