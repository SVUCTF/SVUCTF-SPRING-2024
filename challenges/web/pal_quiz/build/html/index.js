const questionMap = {
    "q1": -6565984,
    "q2": -7942262,
    "q3": -6238514,
    "q4": -7025504,
    "q5": -6960247,
    "q6": -3421540,
    "q7": -7483761,
    "q8": -929000826,
    "q9": -1600549426,
    "q10": -862872640,
};


function checkAnswers() {
    const resultAlert = document.getElementById("resultAlert");
    resultAlert.hidden = false;

    let totalScore = 0;
    let answers = [];

    document.querySelectorAll("input").forEach(input => {
        const answer = input.value.trim();
        answers.push(answer);
        if (check(answer, input.id)) {
            totalScore += 10;
        }
    });

    if (totalScore == 100) {
        resultAlert.className = 'alert alert-success';
        resultAlert.innerHTML = `恭喜你，本次测验总得分为 ${totalScore}。<br>flag{pal_pal_pal_${getFlag(answers)}}`;
    } else {
        resultAlert.className = 'alert alert-secondary';
        resultAlert.innerHTML = `本次测验总得分为 ${totalScore}。<br>没有全部答对，不能给你 flag 哦。`;
    }

    return false;
}

function check(answer, questionId) {
    return questionMap[questionId] == ~parseInt(answer, 2);
}

function getFlag(answers) {
    return answers.map(answer => {
        return answer.match(/.{1,8}/g).map(b => {
            return String.fromCharCode(parseInt(b, 2));
        }).join("");
    }).join("");
}
