$(document).ready(function () {
    var raw_keys = []
    var raw_args = []
    $.popUp("Only db0 is supported！", "warning")

    $('#login').on('click', function () {
        raw_args = $('#ip').val().split(':')
        var ip = raw_args[0]
        var port = raw_args[1]
        var password = raw_args.length > 2 ? raw_args[2] : ''
        $.ajax({
            url: "get",
            data: {'ip': ip, 'port': port, 'password': password, 'key': '*'},
            type: "get",
            dataType: 'text',
            success: function (data) {
                resize()
                var keys = JSON.parse(data)
                show_keys(keys)
                raw_keys = keys
            }
        });
    })

    $('#search').on('click', function () {
        var keywords = $('#keywords').val().toLowerCase()
        var filtered = []
        if (keywords.trim() == '') {
            filtered = raw_keys
        }
        else {
            for (var key of raw_keys) {
                if (key.toLowerCase().indexOf(keywords) >= 0) {
                    filtered.push(key)
                }
            }
        }
        show_keys(filtered)
    })

    $('#keys').on('click', 'li', function () {
        var ip = raw_args[0]
        var port = raw_args[1]
        var password = raw_args.length > 2 ? raw_args[2] : ''
        var key = $(this).text()
        $.ajax({
            url: "get",
            data: {'ip': ip, 'port': port, 'password': password, 'key': key},
            type: "get",
            dataType: 'text',
            success: function (data) {
                var result = JSON.parse(data)
                $('#info').text('Key: {0}, Type: {1}, Length: {2}, Size: {3}'.format(result['key'], result['type'], data.length, result['size']))
                $('#text').text('Text:\n' + result['value'])
                $('#json').text('Json:\n' + JSON.stringify(JSON.parse(result['value']), null, 4))
            }
        });
    })

    function show_keys(keys) {
        $('ol li').remove()
        var lis = ''
        for (var key of keys) {
            lis = lis + '<li>{0}</li>'.format(key)
        }
        $('#keys').append(lis)
    }

    $(window).resize(function () {
        resize()
    })

    function resize() {
        $('ol').height($('body').height() - 120)
    }
})