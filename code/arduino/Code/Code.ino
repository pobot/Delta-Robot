/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int step_pin_0 = 3;
int dir_pin_0 = 2;
int step_pin_1 = 5;
int dir_pin_1 = 4;
int step_pin_2 = 7;
int dir_pin_2 = 6;

//int step_pin_1 = 7;
//int dir_pin_1 = 6;
//int step_pin_2 = 5;
//int dir_pin_2 = 4;


int limit_0 = 13;
int limit_1 = 12;
int limit_2 = 11;
//int limit_1 = 11;
//int limit_2 = 12;

int ms_0 = 10;
int ms_1 = 9;
int ms_2 = 8;

int count = 0;
char inByte = 's';
boolean dir_0 = HIGH;
boolean dir_1 = HIGH;
boolean dir_2 = HIGH;

boolean run = false;

// the setup routine runs once when you press reset:
void setup() {                
    // initialize the digital pin as an output.
    pinMode(step_pin_0, OUTPUT);
    pinMode(dir_pin_0, OUTPUT);
    pinMode(step_pin_1, OUTPUT);
    pinMode(dir_pin_1, OUTPUT);
    pinMode(step_pin_2, OUTPUT);
    pinMode(dir_pin_2, OUTPUT);
    pinMode(ms_0, OUTPUT);
    pinMode(ms_1, OUTPUT);
    pinMode(ms_2, OUTPUT);

    pinMode(limit_0, INPUT);
    pinMode(limit_1, INPUT);
    pinMode(limit_2, INPUT);

    digitalWrite(ms_0,HIGH);
    digitalWrite(ms_1,HIGH);
    digitalWrite(ms_2,HIGH);
    
    Serial.begin(115200);
    Serial.setTimeout(10);
}



boolean readData(unsigned char* z0, unsigned char* z1, unsigned char* z2, unsigned char* microstep){
    //Frame format
    //
    //  byte 0 - z0
    //      0 = no step
    //      1 = forward step
    //      2 = backward step
    //
    //  byte 1 - z1
    //      0 = no step
    //      1 = forward step
    //      2 = backward step
    //
    //  byte 2 - z2
    //      0 = no step
    //      1 = forward step
    //      2 = backward step
    //    
    //  byte 3 - Microstep
    //      0 = x1
    //      1 = x2
    //      2 = x4
    //      3 = x8
    //      4 = x16
    //
    
    
    char buffer[10];
    if (Serial.readBytesUntil('\n',buffer,10)){
        *z0 = buffer[0];
        *z1 = buffer[1];
        *z2 = buffer[2];
        *microstep = buffer[3];
        return true;
    }
    else{
        *z0 = 0;
        *z1 = 0;
        *z2 = 0;
        return false;
    }
}

void setMicrostep(unsigned char microstep){
    digitalWrite(ms_0,microstep & 0x01 );
    digitalWrite(ms_1,(microstep & 0x02) <<1);
    digitalWrite(ms_2,(microstep & 0x04) <<2);
}

void stepMotors(unsigned char z0, unsigned char z1, unsigned char z2){
        
    if (z0 == 1){
        digitalWrite(dir_pin_0,LOW);
        digitalWrite(step_pin_0,LOW);
    }
    if (z0 == 2){
        digitalWrite(dir_pin_0,HIGH);
        digitalWrite(step_pin_0,LOW);
    }
    if (z1 == 1){
        digitalWrite(dir_pin_1,HIGH);
        digitalWrite(step_pin_1,LOW);
    }
    if (z1 == 2){
        digitalWrite(dir_pin_1,LOW);
        digitalWrite(step_pin_1,LOW);
    }
    if (z2 == 1){
//        digitalWrite(dir_pin_2,HIGH);
        digitalWrite(dir_pin_2,LOW);
        digitalWrite(step_pin_2,LOW);
    }
    if (z2 == 2){
//        digitalWrite(dir_pin_2,LOW);
        digitalWrite(dir_pin_2,HIGH);
        digitalWrite(step_pin_2,LOW);
    }

    delayMicroseconds(100);

    boolean enable_up_0 = !digitalRead(limit_0);
    boolean enable_up_1 = !digitalRead(limit_1);
    boolean enable_up_2 = !digitalRead(limit_2);
    
    //Check up movement
    if(z0 == 2 && enable_up_0)digitalWrite(step_pin_0,HIGH);
    if(z1 == 2 && enable_up_1)digitalWrite(step_pin_1,HIGH);
    if(z2 == 2 && enable_up_2)digitalWrite(step_pin_2,HIGH);
    
    
    //Check down movement
    if(z0 == 1 )digitalWrite(step_pin_0,HIGH);
    if(z1 == 1 )digitalWrite(step_pin_1,HIGH);
    if(z2 == 1 )digitalWrite(step_pin_2,HIGH);
    
    
}

// the loop routine runs over and over again forever:
void loop() {
    unsigned char z0 = 0;
    unsigned char z1 = 0;
    unsigned char z2 = 0;
    unsigned char microstep = 0;
    
    if (readData(&z0, &z1, &z2, &microstep)){
        setMicrostep(microstep);
        stepMotors(z0,z1,z2);
    }
}
