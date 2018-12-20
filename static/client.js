$(document).ready(function () {
    /*login keys and search result keys*/
    var RAW_KEYS = []
    /*hash keys*/
    var RAW_KEYS_BACKUP = []
    /*login keys, search result keys, hash keys info*/
    var RAW_INFO = {}
    /*show as json and text*/
    var RAW_VALUE = []

    /*hash key(first level) 2018-12-20*/
    var HASH_KEY = ''

    init();

    function init() {
        RAW_KEYS = []
        RAW_KEYS_BACKUP = []
        RAW_INFO = {}
        RAW_VALUE = []
        HASH_KEY = ''
        resize()
        $('aside.more,#back').hide()
        $('#keywords,ol,#info,#json').text('')
    }

    $('#more').on('click', function () {
        $('aside.more').toggle()
        if ($('aside.more').is(':hidden')) {
            $('#keys').height($('body').height() - 164)
        }
        else {
            $('#keys').height($('body').height() - 203)
        }
    })

    $('#login').on('click', function () {
        init()
        var data = get_data('*')
        try {
            resize()
            RAW_KEYS = JSON.parse(data)
            show_keys(RAW_KEYS, 'ALL')
        }
        catch (error) {
            alert(data)
            $('#host').focusin()
        }
    })

    $('#search').on('click', function () {
        var keywords = $('#keywords').val().toLowerCase()
        var filtered = [], type = 'SEARCH'
        if (keywords.trim() == '') {
            filtered = RAW_KEYS
            type = 'ALL'
        }
        else {
            for (var key of RAW_KEYS) {
                if (key.toLowerCase().indexOf(keywords) >= 0) {
                    filtered.push(key)
                }
            }
        }
        show_keys(filtered, type)
    })

    $('#keys').on('click', 'li', function () {
        $('#keys li').eq(RAW_VALUE[0]).removeClass('active')
        $(this).addClass('active')

        /*Hash Type*/
        if (HASH_KEY) {
            var key = HASH_KEY
            var hash_key = $(this).text()
            var data = get_data(key, hash_key)
            var result = JSON.parse(data)
            RAW_VALUE = [$(this).index(), result['value']]
            $('#info').text('Key: {0}, HashKey: {1}, Type: {2}'.format(result['key'], result['hash_key'], result['type']))
            $('ul li').eq(0).trigger('click')
        }
        else {
            var key = $(this).text()
            var data = get_data(key)
            var result = JSON.parse(data)
            if (result['type'] == 'hash') {
                HASH_KEY = key
                RAW_VALUE = [0, result['value']]
                RAW_KEYS_BACKUP = RAW_KEYS
                RAW_KEYS = JSON.parse(RAW_VALUE[1])
                show_keys(RAW_KEYS, key)
                $('#back').show()
                $('#keys').height($('body').height() - 203)
            }
            else {
                RAW_VALUE = [$(this).index(), result['value']]
                $('#info').text('Key: {0}, Type: {1}'.format(result['key'], result['type']))
                $('ul li').eq(0).trigger('click')
            }
        }
    })

    $('ul li').on('click', function () {
        $(this).addClass('active').siblings().removeClass('active')
        if ($(this).attr('value') == 'Text') {
            $('#json').text(RAW_VALUE[1])
        }
        else {
            var _data = JSON.parse(RAW_VALUE[1]);
            var data = '';
            if (typeof(_data) == 'string') {
                data = _data
            }
            else {
                data = RAW_VALUE[1]
            }
            var json = JSON.stringify(JSON.parse(data), null, 4)
            $('#json').text(json)
        }
    })

    $('#back').on('click', function () {
        $(this).hide()
        $('#keys').height($('body').height() - 164)
        RAW_KEYS = RAW_KEYS_BACKUP
        RAW_KEYS_BACKUP = []
        show_keys(RAW_KEYS, 'ALL')
        $('#search').trigger('click')
        HASH_KEY = ''
    })

    function get_data(key, hash_key = '') {
        if ($('#host').val().search(/(\d+\.){3}\d+[:：]\d+/) != 0) {
            $.popUp('Input format error, please check!', 'error')
            return
        }
        var args = '{0}:{1}:{2}:{3}'.format($('input:checked').val(), $('#host').val().replace('：', ':'), $('#db').val(), $('#password').val())
        var data = $.ajax({
            url: "get",
            data: {'args': args, 'key': key, 'hash_key': hash_key},
            type: "get",
            dataType: 'text',
            async: false
        }).responseText;
        return data
    }

    function show_keys(keys, type) {
        keys = keys.sort()
        var lis = '<li>{0}</li>'.format(keys.join('</li><li>'))
        $('#keys').html(lis)
        RAW_INFO = {'KEYS': keys.length.toString(), 'TYPE': type}
        $('#info').text(JSON.stringify(RAW_INFO))
    }

    $(window).resize(function () {
        resize()
    })

    function resize() {
        $('#keys').height($('body').height() - 164)
        $('#json').height($('body').height() - 104)
        $('article').height($('body').height() - 24)
    }
})