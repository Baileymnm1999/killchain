# REQUIRED TOOLS
# /sys/class/net
# iwconfig
# iw
# ifconfig
#
#
#

import os, time, subprocess

# Check for privileges
uid = os.geteuid()
if uid == 0:
    pass
else:
    print("KillChain requires elevated privileges. Please run as root")
    exit()

# Returns wlan interfaces for distros with /sys/class/net
def get_interfaces():
    return os.listdir('/sys/class/net/')

# Wifi card object definition
class NetworkInterface():

    # Wifi card initialization
    def __init__(self):
        self.name = self.set_name()

    # Prompts the user to select a card based off of availible interfaces
    def set_name(self):
        interfaces = get_interfaces()
        choice = None
        print("Which device would you like to use? (Program will fail if device does not support monitor mode)")

        # Runs through list of interfaces
        while isinstance(choice, str) or choice == None or choice > count or choice < 1:
            count = 0
            offset = 0
            print()
            for interface in interfaces:
                if interface == "lo":
                    index = interfaces.index("lo")
                    offset += 1
                    count += 1
                else:
                    count += 1
                    print("[" + str(count - offset) + "] " + interface)
            print()

            # User makes selection
            choice = input("Select device: ")

            # Input validation
            if choice.isdigit():

                # Accout for offset caused by ommiting 'lo'
                if int(choice) > index:
                    choice = int(choice) + offset
                else:
                    choice = int(choice)

                if choice > count or choice < 1:
                    print("Pick a valid card")
                    
        return interfaces[choice - 1]



    # Attribute returns current mode of interface
    def mode(self):

        # Find config data for current mode
        p = subprocess.Popen("iwconfig " + self.name + " | grep 'Mode'", stdout=subprocess.PIPE, shell=True)
        output = p.communicate()

        # Split data and look for mode and mode definition
        output = str(output).split()
        for entry in output:
            if "Mode" in entry:
                if "Monitor" in entry:
                    return "Monitor"
                elif "Managed" in entry:
                    return "Managed"
                elif "Master" in entry:
                    return "Master"
                else:
                    return None
            else:
                pass

    # Attribute to determine of given mode is supoorted
    def is_mode_supported(self, mode):

        # Sets mode to propper case
        mode = mode.lower()

        # Start with finding the phy# so that we can run 'iw phy# info' and parse for supported modes
        p = subprocess.Popen("iw " + self.name + " info | grep 'wiphy'", stdout=subprocess.PIPE, shell=True)
        output = p.communicate()
        output = str(output).split()

        # Running 'iw phy# info like I said'
        p = subprocess.Popen("iw phy" + output[1] + " info", stdout=subprocess.PIPE, shell=True)
        print("ERROR")
        output = p.communicate()

        # Parsing magic
        output = str(output).split("\t")
        output = str(output).split("\\t")

        #
        if "Supported interface modes:\\\\n\\" not in output or "Band 1:\\\\n\\" not in output:
            return "Inconclusive"
        else:
            index_start = output.index("Supported interface modes:\\\\n\\")
            index_end = output.index("Band 1:\\\\n\\")
            supported_modes = output[index_start + 1 : index_end - 1]
            supported_modes = tr(supported_modes).split('\n')
            supported_modes = tr(supported_modes).split('\\')

        # Look for mode in "PARSED" data
        for x in supported_modes:
            if mode in x:
                return True;
        return False



    # Set mode on the interface
    def set_mode(self, mode):

        # Sets mode to propper case
        mode = mode.lower()

        # Check for one of three modes we want to allow
        if mode == "monitor" or mode == "managed" or mode == "master":

            # Bring down the interface for changes
            status = os.system("ifconfig " + self.name + " down")
            print("Bringing down " + self.name)

            # Make sure device is down
            if status == 0:
                print(self.name + " brought down")
            else:
                # If bringing down failed then abort
                print("FAILED to bring " + self.name + " down. ABORTING")
                return -1

            # Attempt to change to mode requested
            status = os.system("iwconfig " + self.name + " mode " + mode)
            print("Attempting to enable " + mode + " mode for " + self.name)

            # Check status on the requested changes
            if status == 0:
                print(mode.upper() + " mode for " + self.name + ": ENABLED")
                fail = False
            else:
                print(mode.upper() + " mode for " + self.name + ": FAILED")
                fail = True

            # Either result we still bring back up interface
            status = os.system("ifconfig " + self.name + " up")
            print("Bringing up " + self.name)

            # Make sure device is brought back up and advises if otherwise
            if status == 0:
                print(self.name + " back up")
            else:
                print("FAILED to bring " + self.name + " back up. Manual reset may be needed")

            # Return -1 for fail
            if fail:
                return -1
            else:
                return 0

        else:

            # Notify user of invalid mode
            print(mode + " is an unallowed mode for the device. Aborting")
