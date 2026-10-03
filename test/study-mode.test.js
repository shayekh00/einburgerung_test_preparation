const test = require('node:test');
const assert = require('node:assert/strict');

const { applyStudyMode } = require('../study-mode.js');

function createOption(optionIndex) {
    const classes = new Set();

    return {
        dataset: { optionIndex: String(optionIndex) },
        classList: {
            add: (className) => classes.add(className),
            contains: (className) => classes.has(className),
            remove: (className) => classes.delete(className)
        }
    };
}

test('applyStudyMode marks only the correct answer when study mode is enabled', () => {
    const options = [createOption(0), createOption(1), createOption(2), createOption(3)];

    applyStudyMode(options, 3, true);

    assert.equal(options[0].classList.contains('study-answer'), false);
    assert.equal(options[1].classList.contains('study-answer'), false);
    assert.equal(options[2].classList.contains('study-answer'), true);
    assert.equal(options[3].classList.contains('study-answer'), false);
});

test('applyStudyMode removes only its own highlights when study mode is disabled', () => {
    const options = [createOption(0), createOption(1), createOption(2), createOption(3)];

    applyStudyMode(options, 3, true);
    applyStudyMode(options, 3, false);

    assert.equal(options[2].classList.contains('study-answer'), false);
});
