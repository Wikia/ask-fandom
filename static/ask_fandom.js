$(function() {

    var form = $('form').eq(0),
        answer_wrapper = $('#answer-wrapper'),
        answer_node = $('#answer'),
        body = $(document.body);

    form.on('submit', function(ev) {
        ev.preventDefault();

        var question = $('#question').val();
        console.log('Asking the "' + question + '" question');

        // https://api.jquery.com/jquery.getjson/
        $.getJSON('/ask', {'q': question}).
            done(function(resp) {
                console.log('Got a response', resp);

                answer_wrapper.show();
                answer_node.hide().fadeIn().text(resp.answer);
            }).
            fail(function(resp) {
                console.log('Got an error', resp.responseJSON);

                answer_wrapper.show();
                answer_node.hide().fadeIn().text(resp.responseJSON.error);
            });
    });
});