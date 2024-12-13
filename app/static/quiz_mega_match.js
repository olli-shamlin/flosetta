
class MegaMatchQuestion extends Question {
    constructor(payload) {
        super();
        this.word = payload;
    }

    show() {}
}

class MegaMatchQuiz extends Quiz {
    constructor() {
        super();

        if (this.payload.questions.length !== 1) fatalError('KanaTableQuiz.constructor(): only one question expected');

        this.progress_bar.max = this.payload.questions[0].length;

        this.items = [];
        for (let i=0; i < this.payload.questions[0].length; i++)
            this.items.push(new MegaMatchQuestion(this.payload.questions[0][i]));

//        <tr>
//            <td class="col-1"><button id="r1c1" type="button" class="btn btn-outline-secondary">?</button></td>
//            <td class="col-1"><button id="r1c2" type="button" class="btn btn-outline-secondary">?</button></td>
//            <td class="col-1"><button id="r1c3" type="button" class="btn btn-outline-secondary">?</button></td>
//            <td class="col-1"><button id="r1c4" type="button" class="btn btn-outline-secondary">?</button></td>
//        </tr>

        let table_el = document.getElementById('response-table');
        let row_el, col_el, button_el;
        for (let i=0; i < this.payload.parameters.size; i++) {
            row_el = document.createElement('tr');

            for (let j=0; j < this.payload.parameters.size; j++) {
                button_el = document.createElement('button');
                button_el.setAttribute('id', `r${i+1}c${j+1}`);
                button_el.setAttribute('type', 'button');
                button_el.setAttribute('class', 'btn btn-outline-secondary')
                button_el.innerText = '?';

                col_el = document.createElement('td');
                col_el.setAttribute('class', 'col-1');

                col_el.appendChild(button_el);
                row_el.appendChild(col_el);
            }
            table_el.appendChild(row_el);
        }
    }
}