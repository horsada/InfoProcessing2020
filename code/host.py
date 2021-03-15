import subprocess

def send_on_jtag(cmd):
    # this setup will only send chars, if you want to change this, 
    # you need to modify the code running on the NIOS II to have 
    # the variable prompt accept multiple chars.
    assert len(cmd)==1, "Please make the cmd a single character"

    inputCmd = "nios2-terminal <<< {}".format(cmd);

    # subprocess allows python to run a bash command
    output = subprocess.run(inputCmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)

    vals = output.stdout
    vals = vals.decode("utf-8")
    vals = vals.split('<-->')

    return vals[1].strip()

def main():
    # put your code here ...
    res = send_on_jtag('t') # example of how to use send_on_jtag function
    print(x, res)
    
if __name__ == '__main__':
    main()
