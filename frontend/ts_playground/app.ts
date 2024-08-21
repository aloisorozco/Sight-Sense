class Petuh{

    private name: string;
    private phrases: string[];
    

    constructor(n: string, arr: string[]){
        this.name = n
        this.phrases = arr
    }

    speak() : string{
        let index = Math.random() * this.phrases.length
        return this.phrases[index]
    }

    learn(str:string) : void{
        this.phrases.push(str)
    }

    anounce() : string{
        return `My name is ${this.name}`
    }
}

interface PuppyInTheWindow{
    readonly colors: string[]
    readonly furries: number
    readonly owner: string | undefined
}

class Puppy implements PuppyInTheWindow{
    colors: string[];
    furries: number;
    owner: string | undefined;

    constructor(colors: string[], furries: number){
        this.colors = colors
        this.furries = furries
        this.owner = undefined
    }

    adopt(owner: string) : void{
        this.owner = owner
    }
    
}

const dog = new Puppy(["blue", "yello"], 1)
dog.adopt("Mr Fresh")
console.log(dog)
dog.furries = 7
console.log(dog)