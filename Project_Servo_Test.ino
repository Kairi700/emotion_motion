// Controlling a servo position using a potentiometer (variable resistor)
// by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>
// create servo object to control a servo
Servo myservo0;
Servo myservo1;
Servo myservo2;
Servo myservo3;
// analog pin used to connect the potentiometer
int heightPin = A0;
// Pin to control the servo
const int servo_pin0 = D3;
const int servo_pin1 = D4;
// const int servo_pin2 = D5;
const int huePin = D5;
const int brightnessPin = A2;
const int servo_pin3 = D2;
const int rPin = D0;
const int gPin = D1;
const int bPin = A1;
// variable to read the value from the analog pin
int val;
int bright_val;

int r_val = 0;
int g_val = 0;
int b_val = 0;

int color_pointer = 0;

// State of the button
byte current_button = LOW;
// Previous state of the button
byte old_button = LOW;

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

  pinMode(huePin, INPUT);
  pinMode(brightnessPin, INPUT);

  Serial.begin(9600);
}

void loop()
{
  current_button = read_button(huePin,old_button);

    //When start button is unpressed
    if ((old_button == HIGH) && (current_button == LOW)){
      Serial.println("Button pressed!");
      //Turn light green as start button feedback
      color_pointer = (color_pointer+1)%7;
    }

  // reads the value of the potentiometer (value between 0 and 1023)
  val = analogRead(heightPin);
  bright_val = analogRead(brightnessPin);
  //current_time = millis();
  // scale it to use it with the servo (value between 0 and 180)
  val = map(val, 0, 4095, 0, 179);
  bright_val = map(bright_val, 0, 4095, 0, 255);
  // sets the servo position according to the scaled value
  myservo0.write(val);
  myservo1.write(val);
  myservo2.write(val);
  myservo3.write(val);
  // waits for the servo to get there

  r_val = bright_val;
  g_val = bright_val;
  b_val = bright_val;

  delay(15);
  //delay(1000);

  cycleColor();
  // color_pointer = (color_pointer+1)%7;
  // r_val = (r_val+50)%255;
  // g_val = (g_val+50)%255;
  // b_val = (b_val+50)%255;

  old_button = current_button;

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
    setColor(r_val,0,0);
  }
  else if(color_pointer==1){
    setColor(r_val,g_val,0);
  }
  else if(color_pointer==2){
    setColor(0,g_val,0);
  }
  else if(color_pointer==3){
    setColor(0,g_val,b_val);
  }
  else if(color_pointer==4){
    setColor(0,0,b_val);
  }
  else if(color_pointer==5){
    setColor(r_val,0,b_val);
  }
  else if(color_pointer==6){
    setColor(r_val,g_val,b_val);
  }
}

//Function below taken from class
byte read_button(byte pin, byte ref_value){
  // observed the state of the button
  byte current_button = digitalRead(pin);
  // There is a LOW -> HIGH transition
  // or a HIGH -> LOW transition
  if (((ref_value == LOW) && (current_button == HIGH))
   || ((ref_value == HIGH) && (current_button == LOW))){
    // wait for a while (5ms)
    delay(5);
    // update the state of the button
    current_button = digitalRead(pin);
  }
  return(current_button);
}
