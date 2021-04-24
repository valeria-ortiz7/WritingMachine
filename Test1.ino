


#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>


//Variables iniciales 

String instruccion = "";
String valorString = "";
String valorS = "";
float valor = 0;

// Array of desired stepper positions

long positions[2]; 

//Pines de dirección y pasos para cada motor

//Pines del motor X
#define STEPPER1_DIR_PIN 5
#define STEPPER1_STEP_PIN 2

//Pines del motor Y
#define STEPPER2_DIR_PIN 6
#define STEPPER2_STEP_PIN 3

// Se definen los motores a pasos y los pines a utilizar
AccelStepper stepper1(AccelStepper::DRIVER, STEPPER1_STEP_PIN, STEPPER1_DIR_PIN);
AccelStepper stepper2(AccelStepper::DRIVER, STEPPER2_STEP_PIN, STEPPER2_DIR_PIN);


//Grupo de motores a utilizar
MultiStepper steppers;
//Servo a utilizar
Servo myservo; 

//Variable de posicion para cada motor
float posicionX=0;
float posicionY=0;

void setup() {

  Serial.begin(9600);

  // Maxima velocidad de cada motor
  stepper1.setMaxSpeed(75);
  stepper2.setMaxSpeed(75);

  

  // Se define "steppers" para controlar ambos motores de manera simultanea
  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);

  myservo.attach(11);
  myservo.write(180);
  
}

//Loop para llevar a cabo la ejecución de cada función de acuerdo al comportamiento deseado

void loop(){
      //Se definen parámetros relacionados a la conexión con Pyserial
      while(Serial.available()==0);
      if (Serial.available()){
      valorString = Serial.readStringUntil('\n');
      Serial.setTimeout(0.01);
      delay(100);
      instruccion=valorString.substring(0,valorString.indexOf(' '));
      valorS= valorString.substring(valorString.indexOf(' '),valorString.indexOf('\n'));
      valorS= valorS.substring(1,valorS.length());
      Serial.println("Instruccion enviada:" +instruccion+ ", valor:" +valorS);
      valor=valorS.toFloat();
    
  //Serial.print(stepper1.currentPosition());   
  //Serial.print(stepper2.currentPosition()); 


  //Condicional para realizar un movimiento en y positivo
  if (instruccion.equals("ContinueUp") || instruccion.equals("ontinueUp")) {

    //Serial.println("ContinueUp");
    //Serial.println(stepper1.currentPosition());   
    //Serial.println(stepper2.currentPosition());
    positions[0] = -valor + stepper1.currentPosition();
    positions[1] = valor + stepper2.currentPosition();
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();

    Serial.println("ContinueUp");
    //Serial.println(stepper1.currentPosition());   
    //Serial.println(stepper2.currentPosition());    
    
    //instruccion = "Up";
        
    //valor = 500;      
  }
  //Condicional para realizar un movimiento en y negativo
  else if (instruccion.equals ("ContinueDown")||instruccion.equals ("ontinueDown")) {
    
    Serial.println("ContinueDown");
    //Serial.println(stepper1.currentPosition());   
    //Serial.println(stepper2.currentPosition());
    positions[0] = valor + stepper1.currentPosition();
    positions[1] = -valor + stepper2.currentPosition();
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
    
    //instruccion = "ContinueLeft";
        
    //valor = 200;  
      
  }
  //Condicional para realizar un movimiento en x positivo
  else if (instruccion.equals("ContinueRight")||instruccion.equals("ontinueRight")) {

    //Serial.println("ContinueRight");
    
    positions[0] = -valor + stepper1.currentPosition();
    positions[1] = -valor + stepper2.currentPosition();
    
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();

    //instruccion = "ContinueDown";
      
  }
  //Condicional para realizar un movimiento en x negativo
  else if (instruccion.equals("ContinueLeft")||instruccion.equals("ontinueLeft")) {

    //Serial.println("ContinueLeft");

    positions[0] = valor + stepper1.currentPosition();
    positions[1] = valor + stepper2.currentPosition();
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
   
   //instruccion = "PosX";
      
  }
  //Condicional para volver al punto de inicio
  else if (instruccion.equals("begin")||instruccion.equals("egin")) {


    Serial.println("begin");

    positions[0] = 0;
    positions[1] = 0;
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();

    //instruccion = "PosY";
        
    //valor = 90;      
      
  }
  //Condicional para mover el lapiz a una posición en x dada  
  else if (instruccion.equals("PosX")||instruccion.equals("osX")) {

    positions[0] = 0;
    positions[1] = 0;
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();

    positions[0] = -valor + stepper1.currentPosition();
    positions[1] = -valor + stepper2.currentPosition();
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
    //instruccion = "PosY";
        
    //valor = 90;      
      
  }
  //Condicional para mover el lapiz a una posición en y dada
  else if (instruccion.equals("PosY")||instruccion.equals("osY")) {
   positions[0] = 0;
    positions[1] = 0;
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();

    positions[0] = -valor + stepper1.currentPosition();
    positions[1] = valor + stepper2.currentPosition();
    
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
      
  }
  //Condicional para modificar la velocidad inicial
  else if (instruccion.equals("Speed")|| instruccion.equals("peed")) {
    stepper1.setMaxSpeed(valor);
    stepper2.setMaxSpeed(valor);
    
  }
  //Condicional para levantar el lapiz 
  else if (instruccion.equals("Up")|| instruccion.equals("p")) {
    myservo.write(180);
    delay(100);
      
  }
  //Condicional para bajar el lapiz   
  else if (instruccion.equals("Down")||instruccion.equals("own")) {
    myservo.write(90);
    delay(100);
  }
  
  
   
  
  
  
  delay(100);
}
  delay(100);
} 