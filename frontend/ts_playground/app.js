"use strict";
// Write your createCipher function here! ✨
// You'll need to export it so the tests can run it.
const vowels = ["a", "e", "i", "o", "u"];
const consonant = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"];
function createCipher(cipher) {
    return (txt) => {
        let final_str = "";
        for (const i of txt) {
            final_str = final_str.concat(cipher(i));
        }
        return final_str;
    };
}
function createAdvancedCipher(onVowel, onConsonant, onPunctuation) {
    return (txt) => {
        let final_str = "";
        for (const i of txt) {
            if (vowels.includes(i)) {
                final_str = final_str.concat(onVowel(i));
            }
            if (consonant.includes(i)) {
                final_str = final_str.concat(onConsonant(i));
            }
            else {
                final_str = final_str.concat(onPunctuation(i));
            }
        }
        return final_str;
    };
}
function createCodeCracker(attempts, makeGuess, validateGuess) {
    return (txt) => {
        let good_guess = undefined;
        for (let i = 1; i < attempts; i++) {
            good_guess = makeGuess(txt, i);
            if (validateGuess(good_guess)) {
                return good_guess;
            }
        }
        return good_guess;
    };
}
//# sourceMappingURL=app.js.map