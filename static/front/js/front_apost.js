$(function () {
    // var ue = UE.getEditor("editor", {
    //     'serverUrl': '/ueditor'
    // });

    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board_id']");
        var contentInput = $("textarea[name='content']");

        var title = titleInput.val();
        // var content = ue.getContent();
        var content = contentInput.val();
        var board_id = boardSelect.val();

        zlajax.post({
            'url': '/aposts/',
            'data': {
                'title': title,
                'content': content,
                'board_id': board_id
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location = '/'
                    // zlalert.alertConfirm({
                    //     'msg': '帖子发表成功',
                    //     'confirmText': '再发一篇',
                    //     'cancelText': '回到首页',
                    //     'cancelCallback': function () {
                    //         window.location = '/'
                    //     },
                    //     'confirmCallback': function () {
                    //
                    //     }
                    // });
                } else {
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});