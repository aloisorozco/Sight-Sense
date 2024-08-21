"use strict";
class Petuh {
    constructor(n, arr) {
        this.name = n;
        this.phrases = arr;
    }
    speak() {
        let index = Math.random() * this.phrases.length;
        return this.phrases[index];
    }
    learn(str) {
        this.phrases.push(str);
    }
    anounce() {
        return `My name is ${this.name}`;
    }
}
class Puppy {
    constructor(colors, furries) {
        this.colors = colors;
        this.furries = furries;
        this.owner = undefined;
    }
    adopt(owner) {
        this.owner = owner;
    }
}
const dog = new Puppy(["blue", "yello"], 1);
dog.adopt("Mr Fresh");
console.log(dog);
dog.furries = 7;
console.log(dog);
