'use strict'


function generateRandomName(){
    var randomName = new Array();
    for(var i = 0; i < 10; i++) {
        randomName.push(String.fromCharCode(Math.floor(Math.random() * 122)));
    }
    return randomName.join("");

}

class SingleCell{

    constructor(){
        this.name = generateRandomName();
        this.parent =  null;
        this.children = new Array();
    }

    divide(){
        var child = new SingleCell();
        child.parent = this;
        this.children.push(child);
        return child;
    }

}

module.exports = { SingleCell };