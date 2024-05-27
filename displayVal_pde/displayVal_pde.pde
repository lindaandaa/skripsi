

public class DisplayVal{

  public void display(int xPos, int yPos,int w,int h,String name,String val) {//
  
    fill(255);
    stroke(0);
    rect(xPos-50,yPos-50,w,h);
    fill(0, 70, 0);
    stroke(0, 70, 0);
    //rect(xPos,yPos,w,h);
  
    textSize(17);
    fill(150,50,50);
    text("The "+name+" is\n       "+val, xPos,yPos);               

  
       
    }
  }
