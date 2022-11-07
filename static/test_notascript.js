var sc = require("./notascript");

function testSingleCell() {
    mycell = new sc.SingleCell();
    console.log("Origin", mycell.name);
    mychild = mycell.divide();
    console.log(mycell.children[0].name == mychild.parent.name);
}

testSingleCell();