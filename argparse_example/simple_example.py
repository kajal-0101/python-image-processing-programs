'''
We instantiate the ArgumentParser  object as ap.

We must specify both shorthand (-n) and longhand versions (--name)  where either flag could be used in the command line. This is a required argument as is noted by required=True.

The help  string will give additional information in the terminal if you need it.

call vars  on the object to turn the parsed command line arguments into a Python dictionary where the key to the dictionary is the name of the command line argument and the value is value of the dictionary supplied for the command line argument.

check print(args)
'''

#import the neccessary package

import argparse

#construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help = "name of the user")
args = vars(ap.parse_args())

#display a friendly message to the user

print("Hi there {}, it's nice to meet you!". format(args["name"]))

print(args)
