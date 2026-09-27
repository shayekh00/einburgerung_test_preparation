function applyStudyMode(options, correctAnswer, isStudyModeEnabled) {
    const correctOptionIndex = correctAnswer - 1;

    options.forEach((option) => {
        const isCorrectOption = Number(option.dataset.optionIndex) === correctOptionIndex;

        if (isStudyModeEnabled && isCorrectOption) {
            option.classList.add('study-answer');
        } else {
            option.classList.remove('study-answer');
        }
    });
}

const studyMode = { applyStudyMode };

if (typeof window !== 'undefined') {
    window.StudyMode = studyMode;
}

if (typeof module !== 'undefined') {
    module.exports = studyMode;
}
