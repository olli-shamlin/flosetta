
class MultipleChoiceQuestion extends Question {
    constructor(payload) {
        super();
        this.left_column = [];
        this.right_column = [];
        this.choices = payload;
    }

    show() {
        document.getElementById('prompt-word').innerText = this.choices[0].key;
        for (let i=0; i < this.choices.length; i++)
            document.getElementById(`choice-text-${i+1}`).innerText = this.choices[i].key;
    }
}

class MultipleChoiceQuiz extends Quiz {
    constructor() {
        super();

        this.items = [];
        for (let i=0; i < this.payload.questions.length; i++)
            this.items.push(new MultipleChoiceQuestion(this.payload.questions[i]))

        this.items[this.current_item].show();
    }
}