#include "433Utils/rc-switch/RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
 
int main(int argc, char *argv[]) {
    int PIN = 0; // siehe wiring Pi Belegung
    // DOSE 3
    int codeSocketDon = 13982732;
    int codeSocketDoff = 13982721;
    
    // DOSE 1
    // int codeSocketDon = 14013444;
    // int codeSocketDoff = 14013443;
 
 
    if (wiringPiSetup() == -1) return 1;
 
    RCSwitch mySwitch = RCSwitch();
    mySwitch.enableTransmit(PIN);
 
    if (atoi(argv[1]) == 1) { // hier kannst du deine eigenen Bedingungen setzen
        mySwitch.send(codeSocketDon, 24);
    } else {
        mySwitch.send(codeSocketDoff, 24);
    }
    return 0;
}
