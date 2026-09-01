const { execSync } = require('child_process');
const fs = require('fs');

// Get previous book_data.js
const oldContent = execSync('git show HEAD^:book_data.js').toString();
const oldMatch = oldContent.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const oldPages = eval('(' + oldMatch[2] + ')').pages;

// Get current book_data.js
const newContent = fs.readFileSync('book_data.js', 'utf8');
const newMatch = newContent.match(/^([\s\S]*?const bookData = )(\{[\s\S]*?\});/);
const newPages = eval('(' + newMatch[2] + ')').pages;

const oldTitles = oldPages.map(p => p.title).filter(Boolean);
const newTitles = newPages.map(p => p.title).filter(Boolean);

const deleted = oldTitles.filter(t => !newTitles.includes(t));
console.log("=== DELETED TITLES ===");
deleted.forEach(t => console.log("- " + t));
