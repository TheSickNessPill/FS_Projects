// Переписать консольное приложение из предыдущего юнита на классы.

class ElectricalAppliance{
  constructor(I=0, V=0){
    this.isActive = false;
    this.I = I;
    this.V = V;
  }
  on(){
    this.is_active = true;
  }
  off(){
    this.is_active = false;
  }
  calculateP(){
    return this.I * this.V;
  }
}

class DeskLamp extends ElectricalAppliance{
  constructor(I, V, brightness=0, color="white"){
    super(I, V);
    this.brightness = brightness;
    this.color = color;
  }
  
  setBrightness(percent){
    this.brightness = percent;
  }
  setColor(new_color){
    this.color = new_color;
  }
}


class Computer extends ElectricalAppliance{
  constructor(I, V){
    super(I, V);
    this.OS = "";
  }
  
  installOS(new_os){
    if (this.OS){
      console.log(`Deleted ${this.OS}`);
    }
    this.OS = new_os;
    console.log(`Installed ${new_os}`);
  }
}


const DL = new DeskLamp(3, 2, 0, "black");
console.log(DL.calculateP());
DL.setBrightness(22);
DL.setColor("purple")
console.log(DL.brightness);
console.log(DL.color);


const C = new Computer(11, 7);
C.installOS("WIN14");
console.log(C.OS);
C.installOS("WIN16");


