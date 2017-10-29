// Controlling a servo position using a potentiometer (variable resistor)
// by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>
// create servo object to control a servo
Servo myservo0;
Servo myservo1;
Servo myservo2;
Servo myservo3;
// analog pin used to connect the potentiometer
int input_pin = A0;
// Pin to control the servo
const int servo_pin0 = D3;
const int servo_pin1 = D4;
// const int servo_pin2 = D5;
const int hue_button = D5;
const int servo_pin3 = D2;
const int rPin = D0;
const int gPin = D1;
const int bPin = A1;
// variable to read the value from the analog pin
int val;

int r_val = 0;
int g_val = 0;
int b_val = 0;

int color_pointer = 0;

int start_time = millis();
int current_time = millis();

void setup(){
// attaches the servo on pin 9 to the servo object
  myservo0.attach(servo_pin0);
  myservo1.attach(servo_pin1);
//   myservo2.attach(servo_pin2);
  myservo3.attach(servo_pin3);

  //Prep LED for output
  pinMode(rPin, OUTPUT);
  pinMode(gPin, OUTPUT);
  pinMode(bPin, OUTPUT);

  pinMode(hue_button, INPUT)
}

void loop()
{
  // reads the value of the potentiometer (value between 0 and 1023)
  val = analogRead(input_pin);
  //current_time = millis();
  // scale it to use it with the servo (value between 0 and 180)
  val = map(val, 0, 4095, 0, 179);
  // sets the servo position according to the scaled value
  myservo0.write(val);
  myservo1.write(val);
  myservo2.write(val);
  myservo3.write(val);
  // waits for the servo to get there

  //delay(15);
  delay(1000);

  cycleColor();
  color_pointer = (color_pointer+1)%7;
  r_val = (r_val+50)%255;
  g_val = (g_val+50)%255;
  b_val = (b_val+50)%255;

//   if(start_time-current_time %1000 < 150){
//     color_pointer = (color_pointer+1)%7;
//     r_val = (r_val+50)%255;
//     g_val = (g_val+50)%255;
//     b_val = (b_val+50)%255;
//   }
//   cycleColor();

}

void setColor(int red, int green, int blue){
  analogWrite(rPin, red);
  analogWrite(gPin, green);
  analogWrite(bPin, blue);
}

void cycleColor(){
  if(color_pointer==0){
    setColor(255,0,0);
  }
  else if(color_pointer==1){
    setColor(0,255,0);
  }
  else if(color_pointer==2){
    setColor(0,0,255);
  }
  else if(color_pointer==3){
    setColor(255,0,0);
  }
  else if(color_pointer==4){
    setColor(0,255,0);
  }
  else if(color_pointer==5){
    setColor(0,0,255);
  }
  else if(color_pointer==6){
    setColor(r_val,g_val,b_val);
  }
}
