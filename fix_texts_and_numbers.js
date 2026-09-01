const fs = require('fs');
let content = fs.readFileSync('book_data.js', 'utf8');

// 1. Fix the titles of the misplaced diary chapters in Part 1
// They are:
// "1장. 내가 생각하는 디자인 1: 존중과 순응"
// "2장. 내가 생각하는 디자인 2: 포용과 사이 공간"
// "3장. 시지프스의 언덕과 인간다움의 회복"
// Let's remove "1장. ", "2장. ", "3장. " from them so they don't look like chapters of Part 1.
content = content.replace(/"title": "1장. 내가 생각하는 디자인/g, '"title": "[디자인 철학] 내가 생각하는 디자인');
content = content.replace(/"title": "2장. 내가 생각하는 디자인/g, '"title": "[디자인 철학] 내가 생각하는 디자인');
content = content.replace(/"title": "3장. 시지프스의 언덕과/g, '"title": "[디자인 철학] 시지프스의 언덕과');

// And remove them in the markdown/text bodies as well:
content = content.replace(/## 1장. 내가 생각하는 디자인/g, '## [디자인 철학] 내가 생각하는 디자인');
content = content.replace(/## 2장. 내가 생각하는 디자인/g, '## [디자인 철학] 내가 생각하는 디자인');
content = content.replace(/## 3장. 시지프스의 언덕/g, '## [디자인 철학] 시지프스의 언덕');

// 2. Fix the "제N장." in Part 2
// "제3장. 건축의 철학 - 50년 쟁이의 원칙"
// "제4장. 완벽한 시스템이 놓친 것들 (Y구역 현장 기록)"
// "제5장. 26년 현장의 기록: 삭제할 수 없는 85개의 조각들"
content = content.replace(/"title": "제3장. 건축의 철학/g, '"title": "[건축의 철학]');
content = content.replace(/## 제3장. 건축의 철학/g, '## [건축의 철학]');

content = content.replace(/"title": "제4장. 완벽한 시스템이 놓친 것들/g, '"title": "[현장 기록] 완벽한 시스템이 놓친 것들');
content = content.replace(/## 제4장. 완벽한 시스템이 놓친 것들/g, '## [현장 기록] 완벽한 시스템이 놓친 것들');

content = content.replace(/"title": "제5장. 26년 현장의 기록/g, '"title": "[일기장] 26년 현장의 기록');
content = content.replace(/## 제5장. 26년 현장의 기록/g, '## [일기장] 26년 현장의 기록');

// 3. Search and replace any hardcoded "2부" or "3부" in the intro texts.
// If there's any text like "이 1부에서는" inside the PropTech section, we should change it to "이 3부에서는"
content = content.replace(/이 1부에서는/g, '이 장에서는');
content = content.replace(/본 1부에서는/g, '이 파트에서는');
content = content.replace(/1부의 목적은/g, '이 장의 목적은');

fs.writeFileSync('book_data.js', content, 'utf8');
console.log("Replaced text!");
