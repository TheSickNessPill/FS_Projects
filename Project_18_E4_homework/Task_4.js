// Реализовать следующее консольное приложение подобно примеру,
// который разбирался в видео. Реализуйте его на прототипах.

// Определить иерархию электроприборов. Включить некоторые в розетку.
// Посчитать потребляемую мощность. 

// Таких приборов должно быть, как минимум, два 
// (например, настольная лампа и компьютер). 
// Выбрав прибор, подумайте, какими свойствами он обладает.


const ElectricalAppliance = {
  isActive: false,
  I: 0,
  V: 0,
  
  on: function(){
    this.is_active = true;
  },
  off: function(){
    this.is_active = false;
  },
  calculateP: function(){
    return this.I * this.V;
  }
}


const DeskLamp = Object.create(ElectricalAppliance);
DeskLamp.brightness = 0;
DeskLamp.color = "white";
DeskLamp.setBrightness = function(percent){
  this.brightness = percent;
}

DeskLamp.setColor = function(new_color){
  this.color = new_color;
}


const Computer = Object.create(ElectricalAppliance);
Computer.OS = "";
Computer.installOS = function(new_os){
  if (this.OS){
    console.log(`Deleted ${this.OS}`);
  }
  this.OS = new_os;
  console.log(`Installed ${new_os}`);
}


const DeskLamp1 = DeskLamp;
DeskLamp1.I = 2;
DeskLamp1.V = 10;
DeskLamp1.setBrightness(20);
DeskLamp1.setColor("green");
console.log(DeskLamp1.calculateP());


const Computer1 = Computer;
Computer1.I = 5;
Computer1.V = 12;
Computer1.installOS("WIN_14");
console.log(Computer1.calculateP());
