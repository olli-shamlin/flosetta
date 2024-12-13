
class MatchQuestion extends Question {
    constructor(payload) {
        super();
        this.choices = payload;
    }

    show() {
        for(let i=0; i < this.choices.length; i++) {
            document.getElementById(`LCT${i+1}`).innerText = this.choices[i].key;
            document.getElementById(`RCT${i+1}`).innerText = this.choices[4-i].key;
        }
    }
}

class MatchQuiz extends Quiz {
    constructor() {
        super();

        this.items = [];
        for (let i=0; i < this.payload.questions.length; i++)
            this.items.push(new MatchQuestion(this.payload.questions[i]))

        this.items[this.current_item].show();
    }
}