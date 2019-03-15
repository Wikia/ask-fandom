$(function() {

    function say(text) {
        if (window.speechSynthesis) {
            // https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en';

            speechSynthesis.speak(utterance);
        }
        else {
            console.error('speechSynthesis is not available');
        }
    }

    var form = $('form').eq(0),
        answer_wrapper = $('#answer-wrapper'),
        answer_node = $('#answer'),
        body = $(document.body);

    form.on('submit', function(ev) {
        ev.preventDefault();

        var question = $('#question').val();
        console.log('Asking the "' + question + '" question');

        // make the question "linkable"
        document.location.hash = question.replace(/ /g, '_');

        answer_wrapper.hide();

        // https://api.jquery.com/jquery.getjson/
        $.getJSON('/ask', {'q': question}).
            done(function(resp) {
                console.log('Got a response', resp);

                answer_wrapper.show();
                answer_node.hide().fadeIn().text(resp.answer);

                say(resp.answer);
            }).
            fail(function(resp) {
                console.log('Got an error', resp.responseJSON);

                answer_wrapper.show();
                answer_node.hide().fadeIn().text(resp.responseJSON.error);
            });
    });

    // pre-fill the question box
    function ask(question) {
        $('#question').val(question);
        form.submit();
    }

    function onHashChange() {
        var hash_question = decodeURIComponent(document.location.hash).replace(/^#/, '').replace(/_/g, ' ');

        ask(hash_question);
    }

    if (document.location.hash) {
        onHashChange();
    }

    // $(window).bind( 'hashchange', onHashChange);

    // examples
    $('#examples a').on('click', function(ev) {
        ev.preventDefault();

        ask($(this).text());
    });

    /**
     * Speech recognition
     *
     * https://davidwalsh.name/speech-recognition
     */
    $('#say').on('click', function(ev) {
        ev.preventDefault();

        var button =$(this);
        button.css('opacity', '1');

        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 5;
        recognition.start();

        console.log('Please tell us your question');

        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            console.log('You said: ', text);
            button.css('opacity', '.5');

            ask(text);
        };
    });
});
