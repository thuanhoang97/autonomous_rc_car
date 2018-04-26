
#define MAX_SPEED 255
#define MIN_SPEED 0

#define STOP 0
#define UP 1
#define DOWN 2
#define LEFT 3
#define RIGHT 4 

struct Motor{
    byte d;
    byte pwd;
};

Motor m_left = {4,5};
Motor m_right = {7,6};
int car_speed = 200;

void setup() {
  Serial.begin(9600);
  pinMode(m_left.d, OUTPUT);
  pinMode(m_left.pwd, OUTPUT);
  pinMode(m_right.d, OUTPUT);
  pinMode(m_right.pwd, OUTPUT);
}

void stop_left_motor(){
  digitalWrite(m_left.d, LOW);
  digitalWrite(m_left.pwd, LOW);  
}

void stop_right_motor(){
  digitalWrite(m_right.d, LOW);
  digitalWrite(m_right.pwd, LOW);
}

void stop_motor(){
  stop_left_motor();
  stop_right_motor();
}

void forward_left(int speed){
  digitalWrite(m_left.d, LOW);
  analogWrite(m_left.pwd, speed+10);
}

void forward_right(int speed){
  digitalWrite(m_right.d, HIGH);
  analogWrite(m_right.pwd, MAX_SPEED-speed);
}

void forward(int speed){
  forward_left(speed);
  forward_right(speed);
}

void backward_left(int speed){
  digitalWrite(m_left.d, HIGH);
  analogWrite(m_left.pwd, MAX_SPEED-speed);
}

void backward_right(int speed){
  digitalWrite(m_right.d, LOW);
  analogWrite(m_right.pwd, speed);
}
void backward(int speed){
  backward_left(speed);
  backward_right(speed);
}

void turn_left(int speed){
  stop_left_motor();
  forward_right(speed-20);
}

void turn_right(int speed){
  stop_right_motor();
  forward_left(speed-20);
}

void action(int command){
    switch(command){
      case STOP:
        stop_motor();
        break;
      case UP:
        forward(car_speed);
        break;
      case DOWN:
        backward(car_speed);
        break;
      case LEFT:
        turn_left(car_speed);
        break;
      case RIGHT:
        turn_right(car_speed);
        break;
    }
}

void loop() {
  if(Serial.available()){
      int command = Serial.read()-48;
      //Serial.println(command);
      action(command);
  }

}
