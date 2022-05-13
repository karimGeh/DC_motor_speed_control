#include <Arduino.h>
#include <math.h>

#define ENA 9
#define ENB 10

#define IN1 7
#define IN2 6
#define IN3 5
#define IN4 4

#define CHA 2
#define CHB 3

#define TIME_INTERVAL 50.0
#define TICKS_TURN 100.0
#define MAX_MOTOR_SPEED 4650.0
#define ALPHA 0.0219
#define X0 30
float REF_SPEED = 300.0;

#define K 16.28
#define Ti 36.3

unsigned long ticksCounter = 0;
unsigned long prevTicksValue = 0;
float numberOfTurns = 0;
float motorSpeed = 0;

float command = 0;
float error = 0;

float intervalMin = TIME_INTERVAL / 60000;

float rpm_to_pwm(float speed_rpm)
{
  float cmd = X0 - log(1 - (speed_rpm / MAX_MOTOR_SPEED)) * (1 / ALPHA);
  return constrain(cmd, 0, 255);
}

void controlDriver(int SpeedA, int SpeedB, int pinIN1, int pinIN2, int pinIN3, int pinIN4)
{
  analogWrite(ENA, SpeedA);
  analogWrite(ENB, SpeedB);
  digitalWrite(IN1, pinIN1);
  digitalWrite(IN2, pinIN2);
  digitalWrite(IN3, pinIN3);
  digitalWrite(IN4, pinIN4);
}

// motor control - start
void turnLeft(int MOTORS_SPEED)
{
  controlDriver(MOTORS_SPEED, MOTORS_SPEED, LOW, HIGH, LOW, HIGH);
}
void turnRight(int MOTORS_SPEED)
{
  controlDriver(MOTORS_SPEED, MOTORS_SPEED, HIGH, LOW, HIGH, LOW);
}
void stopMotors()
{
  controlDriver(0, 0, LOW, LOW, LOW, LOW);
}
// motor control - end

// speed control - start
float getSpeedWithInterval()
{
  numberOfTurns = ticksCounter / TICKS_TURN;
  ticksCounter = 0;
  return numberOfTurns * (60000 / TIME_INTERVAL);
}

void countTick()
{
  ticksCounter++;
}
// speed control - end

void setup()
{
  Serial.begin(9600);

  // initialize pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  pinMode(CHA, INPUT);
  attachInterrupt(digitalPinToInterrupt(CHA), countTick, FALLING);

  // Stop Motors
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void loop()
{
  delay(TIME_INTERVAL);

  motorSpeed = getSpeedWithInterval();
  float ct = millis();
  if (ct < 20000 && ct > 10000)
  {
    REF_SPEED = 2000.0;
  }

  float currentErr = REF_SPEED - motorSpeed;
  error = currentErr * 0.9986 - error;
  command += error;

  turnLeft(rpm_to_pwm(command));

  Serial.print(ct);
  Serial.print(",");
  Serial.print(REF_SPEED);
  Serial.print(",");
  Serial.println(motorSpeed);
}
