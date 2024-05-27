import javax.swing.*;

public class Chart{
  
  int x_Yaxis,y_Yaxis,x_Xaxis,y_Xaxis,h_Yaxis,w_Yaxis,h_Xaxis,w_Xaxis;
  
  public Chart (){
    
    x_Yaxis = 100;
    y_Yaxis = 200;
    
    h_Yaxis = 400;
    w_Yaxis = 2;
    
    x_Xaxis = 100;
    y_Xaxis = 600;
    
    h_Xaxis = 2;
    w_Xaxis = 500;
   
  } 
  
  public  void display(){
    
    //Y axis
    fill(150,50,50);
    rect(x_Yaxis, y_Yaxis,w_Yaxis, h_Yaxis);
    
    //X axis
    fill(150,50,50);
    rect(x_Xaxis, y_Xaxis,w_Xaxis,h_Xaxis);
    
    
      
    // volt values
      textSize(17);
      fill(150,50,50);
      text("Voltage (mV)",10,170); 
      
      for(int i=0; i<11; i++){
          fill(150,50,50);
          rect(x_Yaxis-10,600-40*i,20,2);
          
      }
      for (int i=0; i<11; i++){
      float t = 0.5*i; 
      String T = Float.toString(t);
      textSize(17);
      fill(150,50,50);
      text(T, 65 ,610 - 40*i); 
      }
     //Time values
     
      textSize(17);
      fill(150,50,50);
      text("Time(s)",550,650);
      
       for(int i=0; i<11; i++){
          fill(150,50,50);
          rect(100+50*i,y_Xaxis-10,2,20);
      }
      for (int i=0; i<11; i++){
      int t = i; 
      String T = Integer.toString(t);
      textSize(17);
      fill(150,50,50);
      text(T, 95 + 50*i,630); 
      }
   
  }
}
