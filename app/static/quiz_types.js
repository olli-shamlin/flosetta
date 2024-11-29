      function my_func() { return 'Hello World'; }

      let i = 1;
      const ElementForm = Object.freeze({
        ENGLISH:  i++,
        ROMAJI:   i++,
        KANA:     i++,
        KANJI:    i++,
        HIRAGANA: i++,
        KATAKANA: i++,
      });

      class CorpusElement {
        constructor(key, values, prompt_form, choice_form, valid_element_forms) {

          for (let [k, v] of values) {
            if (! valid_element_forms.includes(k)) {
              throw new Error(`Invalid ${k}: ${k} is not a valid Form for ${this.constructor.name}`);
            }
          }

          this.key = key
          this.values = values
          this.prompt_form = prompt_form
          this.choice_form = choice_form
        }

        form_of(element_form) { return this.values.get(element_form); }
        prompt() { return this.form_of(this.prompt) }
        choice() { return this.form_of(this.choice_form) }
      }

      class CharacterElement extends CorpusElement{
        constructor(key, values, prompt_form, choice_form) {
          const valid_forms =
                  Object.freeze([ElementForm.ROMAJI, ElementForm.HIRAGANA, ElementForm.KATAKANA]);
          super(key, values, prompt_form, choice_form, valid_forms);
        }

        echo() { return `Romaji: ${this.values.get(ElementForm.ROMAJI)} ` +
                        `Hiragana: ${this.values.get(ElementForm.HIRAGANA)} ` +
                        `Katakana: ${this.values.get(ElementForm.KATAKANA)}`; }
      }

      class WordElement extends CorpusElement{
        constructor(key, values, prompt_form, choice_form) {
          const valid_forms =
                  Object.freeze([ElementForm.ENGLISH, ElementForm.ROMAJI, ElementForm.KANA, ElementForm.KANJI]);
          super(key, values, prompt_form, choice_form, valid_forms);
        }

        echo() { return `English: ${this.values.get(ElementForm.ENGLISH)} ` +
                        `Romaji: ${this.values.get(ElementForm.ROMAJI)} ` +
                        `Kana: ${this.values.get(ElementForm.KANA)} ` +
                        `Kanji: ${this.values.get(ElementForm.KANJI)}`; }
      }
