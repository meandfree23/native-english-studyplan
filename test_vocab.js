const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf-8');
const dictMatch = html.match(/<script src="master\/data\/dictionary.js"><\/script>/);
console.log("Dictionary script linked?", !!dictMatch);

const dataContent = fs.readFileSync('master/data/month1.js', 'utf-8');
eval(dataContent.replace('window.dayData = Object.assign(window.dayData || {},', 'let dayData =').replace(/\)$/, ''));

const dictContent = fs.readFileSync('master/data/dictionary.js', 'utf-8');
eval(dictContent.replace('window.globalDictionary =', 'let globalDictionary ='));

const data = dayData["1"]; // Day 1
let dayText = data.sentences.map(s => s.txt).join(' ').toLowerCase();
dayText = dayText.replace(/[.,?!;:()'"]/g, '');
let words = dayText.split(/\s+/);
let uniqueWords = [...new Set(words)];

console.log("Extracted words:", uniqueWords);

let foundVocab = [];
if (globalDictionary) {
    uniqueWords.forEach(w => {
        if (globalDictionary[w]) {
            foundVocab.push({ word: w, meaning: globalDictionary[w] });
        }
    });
}
console.log("Found vocab:", foundVocab);
