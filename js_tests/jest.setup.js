const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const templatePath = path.resolve(__dirname, '../templates/base.html');
const templateContents = fs.readFileSync(templatePath, 'utf8');

// Configure jsdom with the template contents
const { window } = new JSDOM(templateContents, { url: 'http://localhost' });
global.window = window;
global.document = window.document;

