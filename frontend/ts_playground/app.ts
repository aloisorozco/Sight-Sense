// Write your createCipher function here! ✨
// You'll need to export it so the tests can run it.

type Cypher = (txt: string) => string
type Stronk = (input: string) => string

type StronkNew = (input: string) => string | undefined
type Guess = (text: string, attempt: number) => string
type ValidateGuess = (text: string) => boolean

const vowels: string[] = ["a", "e", "i", "o", "u"] 
const consonant: string[] = [  "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"] 


function createCipher(cipher: Cypher): Stronk{

    return (txt) =>{
        let final_str: string = ""

        for(const i of txt){
            final_str = final_str.concat(cipher(i))
        }

        return final_str
    }
}

function createAdvancedCipher(onVowel: Stronk, onConsonant: Stronk, onPunctuation: Stronk): Stronk{

    return (txt) =>{
        let final_str: string = ""

        for(const i of txt){
            if(vowels.includes(i)){
                final_str = final_str.concat(onVowel(i))
            }
            if(consonant.includes(i)){
                final_str = final_str.concat(onConsonant(i))
            }
            else{
                final_str = final_str.concat(onPunctuation(i))
            }
        }

        return final_str
    }
}

function createCodeCracker(attempts: number, makeGuess: Guess, validateGuess: ValidateGuess ): StronkNew{

    return (txt) =>{
        let good_guess : string | undefined = undefined;

        for(let i = 1; i < attempts; i++){
            good_guess = makeGuess(txt, i)
            if (validateGuess(good_guess)){
                return good_guess
            }
        }
        return good_guess
    }
}



