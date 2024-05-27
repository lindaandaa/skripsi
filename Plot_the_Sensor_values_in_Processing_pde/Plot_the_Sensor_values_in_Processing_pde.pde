import processing.serial.*;

Serial myPort;        // The serial port
float inByte;         // Incoming serial data
float voltage;
boolean newData = false;
int xPos = 100;    // horizontal position of the graph 
Chart chart1;
DisplayVal display1;
DisplayVal display2;
//Variables to draw a continuous line.
int lastxPos=100;
int lastheight=200;


PImage img1;
PImage img2;
void setup () {
  // set the window size:
 size(1200, 900);  
  
    // Images must be in the "data" directory to load correctly
  img1 = loadImage("EMG_GUI_backgound1.PNG");
  img2 = loadImage("EMG_GUI_backgound2.PNG");
   

  myPort = new Serial(this, "COM4", 9600);  

  // A serialEvent() is generated when a newline character is received :
  myPort.bufferUntil('\n');
  background(0);      // set inital background:
}
void draw () {
   image(img1, 0, 0, width, height/10);
   image(img2, 0, 750, width, height/5);
    chart1 = new Chart();
    chart1.display();
    display1=new DisplayVal();
    display2=new DisplayVal();
    display1.display(width-300,height-700,300,100,"time",Float.toString(millis()));
    display2.display(width-300,height-400,300,100,"voltage",Float.toString(voltage));
  
  if (newData) {
    //Drawing a line from Last inByte to the new one.
    stroke(127,34,255);     //stroke color
    strokeWeight(4);        //stroke wider
    //line(lastxPos, lastheight, xPos, height - inByte); 
    line(lastxPos, lastheight, xPos, height - voltage);
    lastxPos= xPos;
    //lastheight= int(height-inByte);
    lastheight= int(height-voltage);

    // at the edge of the window, go back to the beginning:
    if (xPos >= 100+chart1.w_Xaxis) {
      xPos = 100;
      lastxPos= 100;
      background(0);  //Clear the screen.
    } 
    else {
      // increment the horizontal position:
      xPos++;
    }
   newData =false;
 }
}

void serialEvent (Serial myPort) {
  // get the ASCII string:
  String inString = myPort.readStringUntil('\n');
  if (inString != null) {
    inString = trim(inString);                // trim off whitespaces.
    inByte = float(inString);           // convert to a number.
    voltage = inByte * (5.0 / 1023.0);//convert to voltage
    println(voltage);
    //inByte = map(inByte, 0, 1023, 200, height); //map to the screen height.
    voltage = map(voltage, 0, 5, 200, height-100); //map to the screen height.
    newData = true; 
  }
}
