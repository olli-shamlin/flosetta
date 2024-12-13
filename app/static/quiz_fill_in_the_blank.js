
class FillInTheBlankQuestion extends Question {
    constructor(payload) {
        super();
        this.left_column = [];
        this.right_column = [];
        this.choices = payload;
    }

    show() {
        document.getElementById('prompt-word').innerText = this.choices[0].key;
    }
}

class FillInTheBlankQuiz extends Quiz {
    constructor() {
        super();

        this.items = [];
        for (let i=0; i < this.payload.questions.length; i++)
            this.items.push(new FillInTheBlankQuestion(this.payload.questions[i]))

        this.items[this.current_item].show();
    }
}