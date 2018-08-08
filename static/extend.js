$.extend({
    popUp: function (text, type, second = 2) {
        var types = {
            'info': {'background': 'rgba(50, 182, 67, .9)', 'border-color': '#32b643'},
            'warning': {'background': 'rgba(232, 86, 0, .9)', 'border-color': '#ffb700'},
            'error': {'background': 'rgba(50, 182, 67, .9)', 'border-color': '#e85600'},
        }
        var perfix = {
            'info': 'Info',
            'warning': 'Warning',
            'error': 'Error'
        }
        type = type in types ? type : 'info'
        $p = $('<p class="popup"></p>').text('{0}：{1}'.format(perfix[type], text)).css({
            'color': 'white',
            'width': '400px',
            'z-index': '5',
            'height': '50px',
            'line-height': '50px',
            'text-align': 'center',
            'position': 'fixed',
            'top': '0',
            'left': '50%',
            'margin': '3px',
            'margin-left': '-200px',
            'border-radius': '5px'
        }).css(types[type]);
        $('body').append($p);
        setTimeout(() => $('p.popup').remove(), parseInt(second) * 1000)
    },
});

String.prototype.format = function (args) {
    var result = this;
    if (arguments.length > 0) {
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if (args[key] != undefined) {
                    // noinspection Annotator
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    // noinspection Annotator
                    var reg = new RegExp("({[" + i + "]})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}

$(document).ajaxSuccess(function () {
    $.popUp('Success！', 'info', 1)
});

$(document).ajaxError(function () {
    $.popUp('Failure！', 'error', 1)
})