// Controlling a servo position using a potentiometer (variable resistor)
// by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>
// create servo object to control a servo
Servo myservo;
// analog pin used to connect the potentiometer
int input_pin = A0;
// Pin to control the servo
const int servo_pin = D0;
// variable to read the value from the analog pin

const int ledRedPin = D1;
const int ledYellowPin = D2;

int val;
void setup()
{
  // attaches the servo on pin 9 to the servo object
  myservo.attach(servo_pin);
  pinMode(ledRedPin, OUTPUT);
  pinMode(ledYellowPin, OUTPUT);

  Serial.begin(9600);
}
void loop()
{
  // reads the value of the potentiometer (value between 0 and 1023)
  val = analogRead(input_pin);
  // scale it to use it with the servo (value between 0 and 180)
  val = map(val, 0, 1023, 0, 179);
  // sets the servo position according to the scaled value
  myservo.write(val);
  // waits for the servo to get there
  delay(15);

  digitalWrite(ledRedPin, HIGH);
  digitalWrite(ledYellowPin, LOW);
  delay(1000);
  digitalWrite(ledYellowPin, HIGH);
  digitalWrite(ledRedPin, LOW);
  delay(1000);
}
