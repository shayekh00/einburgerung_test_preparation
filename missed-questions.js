const MISSED_QUESTIONS_STORAGE_KEY = 'missedQuestions';

function loadMissedQuestions() {
    try {
        return JSON.parse(localStorage.getItem(MISSED_QUESTIONS_STORAGE_KEY)) || {};
    } catch (error) {
        return {};
    }
}

function saveMissedQuestions(missedQuestions) {
    localStorage.setItem(MISSED_QUESTIONS_STORAGE_KEY, JSON.stringify(missedQuestions));
}

function recordAnswer(questionId, wasAnsweredCorrectly) {
    const missedQuestions = loadMissedQuestions();

    if (wasAnsweredCorrectly) {
        delete missedQuestions[questionId];
    } else {
        const existingRecord = missedQuestions[questionId] || { timesWrong: 0 };
        missedQuestions[questionId] = {
            timesWrong: existingRecord.timesWrong + 1,
            lastWrongAt: new Date().toISOString()
        };
    }

    saveMissedQuestions(missedQuestions);
}

function getMissedQuestionIds() {
    return Object.keys(loadMissedQuestions()).map(Number);
}

function getMissedQuestionCount() {
    return getMissedQuestionIds().length;
}

const missedQuestionTracker = { recordAnswer, getMissedQuestionIds, getMissedQuestionCount };

if (typeof window !== 'undefined') {
    window.MissedQuestions = missedQuestionTracker;
}

if (typeof module !== 'undefined') {
    module.exports = missedQuestionTracker;
}
