var a=document.getElementById("a");
var b=document.getElementById("b");
a.onclick=function(){

document.getElementById("music").play();
}
b.onclick=function(){

document.getElementById("music").pause();
document.getElementById("music").currentTime = 0.0;
}
